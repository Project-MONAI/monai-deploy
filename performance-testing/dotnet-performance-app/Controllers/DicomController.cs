using dotnet_performance_app.Support;
using FellowOakDicom;
using Microsoft.AspNetCore.Mvc;
using System.Reflection;

namespace dotnet_performance_app.Controllers
{
    [ApiController]
    [Route("dicom")]
    public class DicomController : ControllerBase
    {
        public DicomController()
        {
            _dicomScu = new DicomScu();
        }

        private DicomScu _dicomScu { get; }

        [Route("ct")]
        [HttpGet]
        public async Task<IActionResult> PublishCt()
        {
            try
            {
                await _dicomScu.CStore("127.0.0.1", 4242, "TEST", "ORTHANC", await GetDicoms(GetFolder("CT")), TimeSpan.FromSeconds(100));
                return Ok();
            }
            catch (Exception)
            {
                return BadRequest();
            }
        }

        [Route("xray")]
        [HttpGet]
        public async Task<IActionResult> PublishXray()
        {
            try
            {
                await _dicomScu.CStore("127.0.0.1", 4242, "TEST", "ORTHANC", await GetDicoms(GetFolder("XRAY")), TimeSpan.FromSeconds(100));
                return Ok();
            }
            catch (Exception)
            {
                return BadRequest();
            }
        }

        [Route("mri")]
        [HttpGet]
        public async Task<IActionResult> PublishMri()
        {
            try
            {
                await _dicomScu.CStore("127.0.0.1", 4242, "TEST", "ORTHANC", await GetDicoms(GetFolder("MRI")), TimeSpan.FromSeconds(100));
                return Ok();
            }
            catch (Exception)
            {
                return BadRequest();
            }
        }

        [Route("ultrasound")]
        [HttpGet]
        public async Task<IActionResult> PublishUltrasound()
        {
            try
            {
                await _dicomScu.CStore("127.0.0.1", 4242, "TEST", "ORTHANC", await GetDicoms(GetFolder("ULTRASOUND")), TimeSpan.FromSeconds(100));
                return Ok();
            }
            catch (Exception)
            {
                return BadRequest();
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
