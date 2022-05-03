#!/usr/bin/env python

# Copyright 2022 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import os
import time
import uuid
import sys
from pathlib import Path
from signal import SIGINT, signal

import pika
from minio import Minio


class App():

    def __init__(self) -> None:
        self._logger = logging.getLogger("demo")
        self._load_config()
        self._init_messaging()
        self._init_storage()
        self._output_directories = {}

    def _init_storage(self) -> None:
        config = self._config['storage']
        self._storage_client = Minio(
            config['endpoint'],
            config['username'],
            config['password'],
            secure=False  # DEMO purposes only!!! Make sure to use a secure connection!!!
        )

        if not self._storage_client.bucket_exists(config['bucket']):
            raise f"Bucket '{config['bucket']}' does not exist"

    def _init_messaging(self) -> None:
        config = self._config['messaging']
        credentials = pika.credentials.PlainCredentials(
            config['username'], config['password'])

        self._logger.info(f"Connecting to message broker at {config['host']}")
        self._pika_connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=config['host'], credentials=credentials, virtual_host=config['virtual_host']))
        self._pika_channel = self._pika_connection.channel()
        self._pika_channel.exchange_declare(exchange=config['exchange'], exchange_type='topic', durable=True)
        result = self._pika_channel.queue_declare('', exclusive=True)
        self.messaging_queue_name = result.method.queue

        for topic in config['topics']:
            self._pika_channel.queue_bind(
                exchange=config['exchange'], queue=self.messaging_queue_name, routing_key=topic)
        self._pika_channel.basic_consume(
            queue=self.messaging_queue_name, on_message_callback=self._message_callback, auto_ack=False)

    def _load_config(self) -> None:
        with open('config.json', 'r') as f:
            self._config = json.load(f)

    def _handle_workflow_request(self, properties, method, request_message):
        correlation_id = properties.correlation_id
        
        if 'workflows' not in request_message or len(request_message['workflows']) == 0:
            self._logger.error(
                f"No applications defined in the message body, skipping.")
            # may want to reject here in real use
            self._send_acknowledgement(method.delivery_tag)
            return

        workflow_id =  str(uuid.uuid4())
        output_dir = f"/spleen-output/{workflow_id}"
        task_dispatch = {
            "workflow_id": workflow_id,
            "task_id": str(uuid.uuid4()),
            "execution_id": str(uuid.uuid4()),
            "correlation_id": correlation_id,
            "type": "argo",
            "task_plugin_arguments": {
                "baseUrl": self._config['argo']['baseUrl'],
                "workflowTemplateName": request_message['workflows'][0],
                "workflowTemplateEntrypoint": request_message['workflows'][1],
                "messagingEndpoint": f"{self._config['messaging']['host']}/{self._config['messaging']['virtual_host']}",
                "messagingUsername": self._config['messaging']['username'],
                "messagingPassword": self._config['messaging']['password'],
                "messagingExchange": self._config['messaging']['exchange'],
                "messagingTopic": "md.tasks.callback",
            },
            "inputs": [],
            "outputs": []            
        }
        
        task_dispatch['inputs'].append(
            {
                "name": "input-dicom",
                "endpoint": self._config['storage']['endpoint'],
                "bucket": self._config['storage']['bucket'],
                "secured_connection": False,
                "relative_root_path": f"{request_message['payload_id']}/"
            })
        task_dispatch['outputs'].append(
            {
                "name": "tempStorage",
                "endpoint": self._config['storage']['endpoint'],
                "bucket": self._config['storage']['bucket'],
                "secured_connection": False,
                "relative_root_path": "/rabbit"
            })
        task_dispatch['outputs'].append(
            {
                "name": "output",
                "endpoint": self._config['storage']['endpoint'],
                "bucket": self._config['storage']['bucket'],
                "secured_connection": False,
                "relative_root_path": output_dir
            })
        self._publish(task_dispatch, 'md.tasks.dispatch')
        self._output_directories[workflow_id] = output_dir
        self._send_acknowledgement(method.delivery_tag)

    def _handle_task_update(self, properties, method, message):
        
        if message['status'] == 'Succeeded':
            if message['workflow_id'] not in self._output_directories:
                self._logger.warn('Unable to send an export request due to missing workflow')
                return
            
            export_request = {
                "workflow_id": message['workflow_id'],
                "export_task_id": str(uuid.uuid4()),
                "destination": 'STORESCP',  
                "correlation_id": message['correlation_id'],
                "files": self._list_files(message['workflow_id'])
            }
            self._publish(export_request, 'md.export.request.monaiscu')
            self._logger.info("==> Export request sent.")
        elif message['status'] == 'Accepted':
            self._logger.info("==> Task accepted by Task Manager.")
        else:
            self._logger.warn("Task did not complete: Status={message['status']}, Failure={message['reason']}, Message={message['message']}")
            
        self._send_acknowledgement(method.delivery_tag)
        
    def _list_files(self, workflow_id):
        objects = self._storage_client.list_objects(
            self._config['storage']['bucket'], 
            prefix=f"/spleen-output/{workflow_id}",
            recursive=True)
        
        files = []
        for obj in objects:
            if obj.object_name.endswith('.dcm'):
                files.append(obj.object_name)

        return files

    def _handle_export_complete(self, properties, method, message):
        self._logger.info(f"==> Export task completed with status={message['status']}.")

    def _message_callback(self, ch, method, properties, body):
        self._logger.info(
            f"Message received from application={properties.app_id}. Correlation ID={properties.correlation_id}. Delivery tag={method.delivery_tag}. Topic={method.routing_key}")

        request_message = json.loads(body)

        self._logger.debug('===================')
        self._logger.debug(request_message)
        self._logger.debug('===================')
        
        if method.routing_key == 'md.workflow.request':
            self._handle_workflow_request(properties, method, request_message)
        elif method.routing_key == 'md.tasks.update':
            self._handle_task_update(properties, method, request_message)
        elif method.routing_key == 'md.export.complete':
            self._handle_export_complete(properties, method, request_message)
        else:
            self._logger.error("Unsupported message {method.routing_key}.")
            self._pika_channel.basic_reject(method.delivery_tag, False)
            
        self._logger.info(f"Waiting for events...")

    def _publish(self, message_body, event_type):
        props = pika.BasicProperties(
            message_id=str(uuid.uuid4()),
            content_type='application/json',
            content_encoding='utf-8',
            delivery_mode=2,
            correlation_id=message_body['correlation_id'],
            timestamp=int(time.time()),
            app_id='Demo Workflow Manager',
            type=event_type,
        )

        self._logger.debug(f"publishing message: {event_type}...")
        self._pika_channel.basic_publish(
            exchange=self._config['messaging']['exchange'], routing_key=event_type, body=json.dumps(message_body), properties=props)
        self._logger.info(f"Message published: {event_type}...")

    def _send_acknowledgement(self, delivery_tag):
        self._logger.debug(f"Sending acknowledgement...")
        self._pika_channel.basic_ack(delivery_tag)
        self._logger.info(f"Acknowledgement sent...")

    def run(self):
        self._logger.info('[*] Waiting for logs. To exit press CTRL+C')
        self._pika_channel.start_consuming()

def signal_handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    sys.exit(1)

if __name__ == "__main__":
    signal(SIGINT, signal_handler)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    app = App()
    app.run()
