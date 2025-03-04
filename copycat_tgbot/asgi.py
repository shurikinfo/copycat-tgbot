import logging

from copycat_tgbot.app import App

logger = logging.getLogger(__name__)

app = App()
app.init_app()
app.init_server()
