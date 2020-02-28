"""All settings was here"""

# AMQP settings
BROKER = 'amqp://guest:guest@localhost:5672/%2F'
EXCHANGE = 'suptitle'
QUEUE_IN = 'STT.in'
QUEUE_OUT = 'STT.out'
ROUTING_KEY = 'suptitle.STT.in'
APP_ID = 'suptitle.sst'
ALLOWED_APP_ID = ['suptitle.videoresizer', 'suptitle.website']

# STT settings
CREDITIONALS_JSON = 'steady-cat-269313-8b90bcfb5b51.json'

# log settings
LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'
LOG_LEVEL = 'INFO'

