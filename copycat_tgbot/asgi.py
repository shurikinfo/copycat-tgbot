import logging

import uvicorn

from copycat_tgbot.app import App
from copycat_tgbot.constants import UVICORN_LOG_CONFIG

logger = logging.getLogger(__name__)

app = App()
app.init_app()
app.init_server()

uvicorn.run(app.server.app, host="localhost", port=8000, log_config=UVICORN_LOG_CONFIG)
