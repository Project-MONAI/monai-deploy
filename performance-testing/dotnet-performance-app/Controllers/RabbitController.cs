using dotnet_performance_app.Data.WorkflowRequestEvents;
using dotnet_performance_app.Support;
using Microsoft.AspNetCore.Mvc;
using Monai.Deploy.Messaging.Events;
using Monai.Deploy.Messaging.Messages;

namespace dotnet_performance_app.Controllers
{
    [ApiController]
    [Route("rabbit")]
    public class RabbitController : ControllerBase
    {
        public RabbitController()
        {
            _rabbitPublisher = new RabbitPublisher("monaideploy", "md.workflow.request");
        }

        private RabbitPublisher _rabbitPublisher { get; set; }

        [Route("activeworkflow")]
        [HttpGet]
        public IActionResult PublishActiveWorkflowRequest()
        {
            try
            {
                var message = new JsonMessage<WorkflowRequestEvent>(
                    WorkflowRequestEventTestData.GetActiveWorkflowRequestEvent(),
                    "16988a78-87b5-4168-a5c3-2cfc2bab8e54",
                    Guid.NewGuid().ToString(),
                    string.Empty);

                _rabbitPublisher.PublishMessage(message.ToMessage());

                return Ok();
            }
            catch (Exception)
            {
                return BadRequest();
            }
        }

        [Route("inactiveworkflow")]
        [HttpGet]
        public IActionResult PublishInactiveWorkflowRequest()
        {
            try
            {
                var message = new JsonMessage<WorkflowRequestEvent>(
                    WorkflowRequestEventTestData.GetInactiveWorkflowRequestEvent(),
                    "16988a78-87b5-4168-a5c3-2cfc2bab8e54",
                    Guid.NewGuid().ToString(),
                    string.Empty);

                _rabbitPublisher.PublishMessage(message.ToMessage());

                return Ok();
            }
            catch (Exception)
            {
                return BadRequest();
            }
        }
    }
}