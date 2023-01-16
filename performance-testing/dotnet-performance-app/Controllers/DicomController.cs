using dotnet_performance_app.Support;
using FellowOakDicom;
using FellowOakDicom.Network;
using Microsoft.AspNetCore.Mvc;
using System.Reflection;

namespace dotnet_performance_app.Controllers
{
    [ApiController]
    [Route("dicom")]
    public class DicomController : ControllerBase
    {
        public DicomController(IConfiguration configuration)
        {
            Host = configuration.GetValue<string>("InformaticsGateway:Host");
            Port = configuration.GetValue<int>("InformaticsGateway:Port");
            _dicomScu = new DicomScu();
        }

        private string? Host { get; set; }
        private int Port { get; set; }
        private DicomScu _dicomScu { get; }

        [HttpGet]
        public async Task<IActionResult> DicomAssociation([FromQuery(Name = "modality")] string modality, [FromQuery(Name = "AET")] string AET)
        {
            try
            {
                var result = await _dicomScu.CStore(Host, Port, AET, AET, await GetDicoms(GetFolder(modality.ToUpper())), TimeSpan.FromSeconds(120));
                if (result.State.Equals(DicomState.Success))
                {
                    return Ok();
                }
                else
                {
                    return BadRequest(result.Description);
                }
            }
            catch (Exception e)
            {
                return BadRequest(e.InnerException);
            }
        }

        private DirectoryInfo GetFolder(string subfolder)
        {
            var rand = new Random();
            var pathname = Path.Combine(GetDirectory(), "Data", "DICOM", subfolder);
            var directory = new DirectoryInfo(pathname);
            var directories = directory.GetDirectories();
            return directories[rand.Next(directories.Length)];
        }

        private async Task<IList<DicomFile>> GetDicoms(DirectoryInfo filePath)
        {
            var dicoms = new List<DicomFile>();

            foreach (var file in filePath.GetFiles("*.dcm"))
            {
                var isDicom = DicomFile.HasValidHeader(file.FullName);
                if (isDicom)
                {
                    var dicom = await DicomFile.OpenAsync(file.FullName);
                    dicoms.Add(dicom);
                }
            }

            return dicoms;
        }

        private string GetDirectory()
        {
            return Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        }
    }
}
