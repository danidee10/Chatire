"""Notification channels for django-notifs."""

from json import dumps

import pika

from notifications.channels import BaseNotificationChannel


class BroadCastWebSocketChannel(BaseNotificationChannel):
    """Fanout notification for RabbitMQ."""

    def _connect(self):
        """Connect to the RabbitMQ server."""
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()

        return connection, channel

    def construct_message(self):
        """Construct the message to be sent."""
        extra_data = self.notification_kwargs['extra_data']

        return dumps(extra_data['message'])

    def notify(self, message):
        """put the message of the RabbitMQ queue."""
        connection, channel = self._connect()

        uri = self.notification_kwargs['extra_data']['uri']

        channel.exchange_declare(exchange=uri, exchange_type='fanout')
        channel.basic_publish(exchange=uri, routing_key='', body=message)

        connection.close()
