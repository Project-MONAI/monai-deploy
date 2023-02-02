using System.Diagnostics;
using FellowOakDicom;
using FellowOakDicom.Network;
using FellowOakDicom.Network.Client;

namespace dotnet_performance_app.Support
{
    public class DicomScu
    {
        private static readonly object SyncRoot = new object();
        internal int TotalTime { get; private set; } = 0;

        public async Task<DicomStatus> CStore(string host, int port, string callingAeTitle, string calledAeTitle, IList<DicomFile> dicomFiles, TimeSpan timeout)
        {
            var stopwatch = new Stopwatch();
            stopwatch.Start();
            var dicomClient = CreateClient(host, port, callingAeTitle, calledAeTitle);
            var countdownEvent = new CountdownEvent(dicomFiles.Count);
            var failureStatus = new List<DicomStatus>();
            var seriesUID = await Anonymize(dicomFiles[0].Dataset.GetString(DicomTag.SeriesInstanceUID).Trim());
            var studyUID = await Anonymize(dicomFiles[0].Dataset.GetString(DicomTag.StudyInstanceUID).Trim());

            foreach (var file in dicomFiles)
            {
                file.Dataset.AddOrUpdate<string>(DicomTag.SeriesInstanceUID, seriesUID);
                file.Dataset.AddOrUpdate<string>(DicomTag.StudyInstanceUID, studyUID);
                var cStoreRequest = new DicomCStoreRequest(file);
                cStoreRequest.OnResponseReceived += (DicomCStoreRequest request, DicomCStoreResponse response) =>
                {
                    if (response.Status != DicomStatus.Success) failureStatus.Add(response.Status);
                    countdownEvent.Signal();
                };
                await dicomClient.AddRequestAsync(cStoreRequest);
            }

            try
            {
                await dicomClient.SendAsync();
                countdownEvent.Wait(timeout);
                stopwatch.Stop();
                lock (SyncRoot)
                {
                    TotalTime += (int)stopwatch.Elapsed.TotalMilliseconds;
                }
            }
            catch (DicomAssociationRejectedException ex)
            {
                return DicomStatus.Cancel;
            }

            if (failureStatus.Count == 0) return DicomStatus.Success;

            return failureStatus.First();
        }

        private async Task<string> Anonymize(string uid)
        {
            uid = uid.Substring(0, uid.Length - 10);
            var r = new Random();
            var x = r.Next(0, 99999);
            var s = x.ToString("000000");
            return uid + s;
        }

        private IDicomClient CreateClient(string host, int port, string callingAeTitle, string calledAeTitle)
        {
            return DicomClientFactory.Create(host, port, false, callingAeTitle, calledAeTitle);
        }
    }
}
