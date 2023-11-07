"""Papertrail logger

Sends basic logging over to papertrailapp.com
"""
import logging
from logging.handlers import SysLogHandler
from datetime import datetime
# import requests
import json

PAPERTRAIL_HOST = 'logs6.papertrailapp.com'
PAPERTRAIL_PORT = 16831

now = datetime.now()
fdate = now.strftime("%y%m%d")

logger = logging.getLogger("sandwich_webapp")

log_file_apth = f"/Volumes/sandwich-post/assets/_automation/render_farm/nuke/_logs/render_farm_{fdate}.log"

# the handler determines where the logs go: stdOut / File
shell_handler = logging.StreamHandler()
# remote_handler = SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
file_handler = logging.FileHandler(log_file_apth)

# class WebhookHandler(logging.Handler):
#     def __init__(self, webhook_url):
#         super().__init__()
#         self.webhook_url = webhook_url

#     def emit(self, record):
#         log_entry = self.format(record)
#         payload = {
#             'title': 'Sandwich Webserver',
#             'token': 'aisvwgwdnduf2o1sj2bc2g8yc44qp7',
#             'user': 'u5bd4h9roggx68d2f9fa8obtw92hze',
#             'message': log_entry
#             }

#         try:
#             headers = {'Content-Type': 'application/json'}
#             response = requests.post(self.webhook_url, json=payload, headers=headers)
#             response.raise_for_status()
#         except requests.RequestException as e:
#             print(f"Failed to send log to webhook: {e}")

logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.INFO)
# remote_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# the formatter determines what the logs will look like
fmt_shell = '[%(levelname)s] %(message)s'
fmt_remote = (
    '%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
)

shell_formatter = logging.Formatter(fmt_shell)
# remote_formatter = logging.Formatter(fmt_remote)
file_formatter = logging.Formatter(fmt_remote)

shell_handler.setFormatter(shell_formatter)
# remote_handler.setFormatter(remote_formatter)
file_handler.setFormatter(file_formatter)

# webhook_handler = WebhookHandler(webhook_url="https://api.pushover.net/1/messages.json")
# webhook_formatter = logging.Formatter(fmt_remote)
# webhook_handler.setFormatter(webhook_formatter)
# webhook_handler.setLevel(logging.ERROR)
# logger.addHandler(webhook_handler)



logger.addHandler(shell_handler)
# logger.addHandler(remote_handler)
logger.addHandler(file_handler)
