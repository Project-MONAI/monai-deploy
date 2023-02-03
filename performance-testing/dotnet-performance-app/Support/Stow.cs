using System.Net.Http.Headers;

namespace dotnet_performance_app.Support
{
    public class Stow
    {
        private readonly IHttpClientFactory _httpClientFactory;

        public Stow(IHttpClientFactory httpClientFactory)
        {
            _httpClientFactory = httpClientFactory;
        }

        public async Task<HttpResponseMessage> SendStowRequest(string directory, string url, string authenticationString)
        {
            var client = _httpClientFactory.CreateClient();
            var mimeType = "application/dicom";
            var multiContent = GetMultipartContent(mimeType);

            foreach (var path in Directory.EnumerateFiles(directory, "*.*", SearchOption.AllDirectories))
            {
                var sContent = new StreamContent(File.OpenRead(path));

                sContent.Headers.ContentType = new MediaTypeHeaderValue(mimeType);

                multiContent.Add(sContent);
            }

            if (multiContent.Count() > 0)
            {
                var request = new HttpRequestMessage(HttpMethod.Post, url);

                var base64EncodedAuthenticationString = Convert.ToBase64String(System.Text.ASCIIEncoding.UTF8.GetBytes(authenticationString));

                request.Headers.Add("Authorization", "Basic " + base64EncodedAuthenticationString);

                request.Content = multiContent;

                var response = await client.SendAsync(request);

                return response;
            }

            return null;
        }

        private static MultipartContent GetMultipartContent(string mimeType)
        {
            var multiContent = new MultipartContent("related", "DICOM DATA BOUNDARY");

            multiContent.Headers.ContentType.Parameters.Add(new System.Net.Http.Headers.NameValueHeaderValue("type", "\"" + mimeType + "\""));

            return multiContent;
        }
    }
}
