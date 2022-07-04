using Monai.Deploy.Messaging.Events;

namespace dotnet_performance_app.Data.WorkflowRequestEvents
{
    public static class WorkflowRequestEventTestData
    {
        public static WorkflowRequestEvent GetActiveWorkflowRequestEvent()
        {
            var workflowRequestEvent = new WorkflowRequestEvent()
            {
                Bucket = "bucket_1",
                PayloadId = Guid.NewGuid(),
                Workflows = new List<string>() { },
                CorrelationId = Guid.NewGuid().ToString(),
                Timestamp = DateTime.Now,
                CalledAeTitle = "Active_AE",
                CallingAeTitle = "MWM",
            };

            return workflowRequestEvent;
        }

        public static WorkflowRequestEvent GetInactiveWorkflowRequestEvent()
        {
            var workflowRequestEvent = new WorkflowRequestEvent()
            {
                Bucket = "bucket_1",
                PayloadId = Guid.NewGuid(),
                Workflows = new List<string>() { },
                CorrelationId = Guid.NewGuid().ToString(),
                Timestamp = DateTime.Now,
                CalledAeTitle = "Inactive_AE",
                CallingAeTitle = "MWM",
            };

            return workflowRequestEvent;
        }
    }
}
