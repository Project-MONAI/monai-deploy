// SPDX-FileCopyrightText: © 2021-2022 MONAI Consortium
// SPDX-License-Identifier: Apache License 2.0

using Monai.Deploy.Messaging.Messages;
using RabbitMQ.Client;

namespace dotnet_performance_app.Support
{
    public class RabbitPublisher
    {
        public RabbitPublisher(string exchange, string routingKey)
        {
            var connectionFactory = new ConnectionFactory
            {
                HostName = "localhost",
                UserName = "admin",
                Password = "admin",
                VirtualHost = "monaideploy"
            };

            Exchange = exchange;
            RoutingKey = routingKey;
            var connection = connectionFactory.CreateConnection();
            Channel = connection.CreateModel();
            Channel.ExchangeDeclare(Exchange, ExchangeType.Topic, durable: true);
        }

        private string Exchange { get; set; }

        private string RoutingKey { get; set; }

        private IModel Channel { get; set; }

        public void PublishMessage(Message message)
        {
            var propertiesDictionary = new Dictionary<string, object>
            {
                { "CreationDateTime", message.CreationDateTime.ToString("o") }
            };

            var properties = Channel.CreateBasicProperties();
            properties.Persistent = true;
            properties.ContentType = message.ContentType;
            properties.MessageId = message.MessageId;
            properties.AppId = message.ApplicationId;
            properties.CorrelationId = message.CorrelationId;
            properties.DeliveryMode = 2;
            properties.Headers = propertiesDictionary;
            properties.Type = message.MessageDescription;

            Channel.BasicPublish(exchange: Exchange,
                routingKey: RoutingKey,
                basicProperties: properties,
                body: message.Body);
        }

        public void CloseConnection()
        {
            Channel.Close();
        }
    }
}
