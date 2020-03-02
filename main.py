import datetime
import json
from consumers import AmqpConsumer, ReconnectingAmqpConsumer
import settings
import logging
from google_speech import recognize
from google.api_core.exceptions import GoogleAPIError


class GoogleAmqpConsumer(AmqpConsumer):
    EXCHANGE = settings.EXCHANGE
    QUEUE = settings.QUEUE_IN
    ROUTING_KEY = settings.ROUTING_KEY

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        try:
            request = json.loads(body)
        except json.JSONDecodeError:
            self.logger.error('Error decoding json message')
            self.acknowledge_message(basic_deliver.delivery_tag)
            return

        if properties.app_id and properties.app_id in settings.ALLOWED_APP_ID:
            try:
                result = recognize(request['url'],
                                   settings.CREDITIONALS_JSON,
                                   request['language_code'],
                                   int(request['sample_rate_hertz']))
            except KeyError as e:
                self.logger.error(f'Error in json object. There is no mandatory key: {e}')
                self.acknowledge_message(basic_deliver.delivery_tag)
                return

            except GoogleAPIError as e:
                self.logger.error(f'Google API error: {e}')
                self.acknowledge_message(basic_deliver.delivery_tag)
                return

            self.logger.info(result)
            if result:
                properties.app_id = 'subtitle.speechtotext'
                properties.timestamp = datetime.datetime.now()
                self._channel.basic_publish('', settings.QUEUE_OUT, result, properties)
            super().on_message(_unused_channel, basic_deliver, properties, body)
        else:
            self.logger.warning(f'App id {properties.app_id} is not allowed.')
            self.acknowledge_message(basic_deliver.delivery_tag)

    def on_channel_open(self, channel):
        super().on_channel_open(channel)
        channel.queue_declare(settings.QUEUE_OUT)


def main():
    logging.basicConfig(level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)
    consumer = ReconnectingAmqpConsumer(settings.BROKER, consumer=GoogleAmqpConsumer)
    consumer.run()


if __name__ == '__main__':
    main()
