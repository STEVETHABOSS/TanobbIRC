#!/usr/bin/python3

import requests

url = "http://www.transltr.org/api/translate"


def translate(trans_to, trans_from, text):
    data = {"text": text, "to": trans_to, "from": trans_from}
    r = requests.get(url, params=data)
    return r.json()

