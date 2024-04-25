import requests

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': settings.TELEGRAM_GROUP_ID,
        'text': message
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
