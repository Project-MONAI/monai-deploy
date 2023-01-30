using dotnet_performance_app.Support;
using Microsoft.AspNetCore.Mvc;
using System.Net;
using System.Reflection;

namespace dotnet_performance_app.Controllers
{
    [ApiController]
    [Route("stow")]
    public class StowController : ControllerBase
    {
        public StowController(IConfiguration configuration, IHttpClientFactory httpClientFactory)
        {
            Host = configuration.GetValue<string>("InformaticsGateway:Host");
            Port = configuration.GetValue<int>("InformaticsGateway:Port");
            Stow = new Stow(httpClientFactory);
        }

        private string? Host { get; set; }
        private int Port { get; set; }
        private Stow Stow { get; set; }

        [HttpGet]
        public async Task<IActionResult> DicomAssociation(
            [FromQuery(Name = "modality")] string modality)
        {
            var result = Stow.SendStowRequest(GetFolder(modality.ToUpper()).ToString(), $"https://{Host}:{Port}").Result;

            if (result.StatusCode.Equals(HttpStatusCode.OK))
            {
                return Ok();
            } 
            else
            {
                return BadRequest(result.Content);
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

        private string GetDirectory()
        {
            return Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        }
    }
}
