# -*- coding: utf-8 -*-
import os
import json

from .packages.requests import Session


class MprofiAPIConnector(object):

    url_base = 'http://api.mprofi.pl'
    api_version = '1.0'
    send_endpoint = 'send'
    sendbulk_endpoint = 'sendbulk'

    def __init__(self, api_token=None, payload=None):
        self.token = api_token or os.environ.get('MPROFI_API_TOKEN', '')
        self.session = Session()
        self.session.headers.update({
            'Authorization': 'Token {0}'.format(self.token)
        })
        self.payload = payload or []

    def add_message(self, recipient, message):

        if not recipient:
            raise ValueError("`recipient` can't be empty.")
        if not message:
            raise ValueError("`message` can't be empty.")

        self.payload.append({
            'recipient': recipient,
            'message': message
        })

    def send(self, reference=None):

        if len(self.payload) == 1:
            used_endpoint = self.send_endpoint
            full_payload = self.payload[0]
            if reference is not None:
                full_payload.update({
                    'reference': reference
                })

        elif len(self.payload) > 1:
            used_endpoint = self.sendbulk_endpoint
            full_payload = {
                'messages': self.payload
            }
            if reference is not None:
                full_payload.update({
                    'reference': reference
                })

        else:
            raise ValueError("Empty payload. Please use `add_message` first.")

        full_url = '/'.join([
            self.url_base,
            self.api_version,
            used_endpoint, ""
        ])

        encoded_payload = json.dumps(full_payload)

        self.session.post(full_url, json=encoded_payload, verify=True)
