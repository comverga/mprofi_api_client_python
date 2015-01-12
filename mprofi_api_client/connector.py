# -*- coding: utf-8 -*-
"""Module with connector managing communication with Mprofi API."""

import os
import json

from .packages.requests import Session


class MprofiAPIConnector(object):

    """Connector class that manages communication  with mprofi public API.

    :param api_token: Optional, explicit api token, as string. If api_token
        is not specified `MPROFI_API_TOKEN` env variable will be used.
    :param payload: Optional initial payload (list of dicts).

    """

    #: Base URL for public API
    url_base = 'http://api.mprofi.pl'

    #: Version of API stored as string (used to merge with url_base)
    api_version = '1.0'

    #: Name of send endpoint
    send_endpoint = 'send'

    #: Name of bulk send endpoint
    sendbulk_endpoint = 'sendbulk'

    #: Name of status endpoint
    status_endpoint = 'status'

    def __init__(self, api_token=None, payload=None):
        self.token = api_token or os.environ.get('MPROFI_API_TOKEN', '')
        self.session = Session()
        self.session.headers.update({
            'Authorization': 'Token {0}'.format(self.token)
        })
        self.payload = payload or []
        self.response = []

    def add_message(self, recipient, message):
        """Add one message to current payload.

        :param recipient: Message recipient as string. This should be telephone
            number like `123 123 123`.
        :param message: Message content as string.

        :raises: ValueError
        :returns: None

        """

        if not recipient:
            raise ValueError("`recipient` can't be empty.")
        if not message:
            raise ValueError("`message` can't be empty.")

        self.payload.append({
            'recipient': recipient,
            'message': message
        })

    def send(self, reference=None):
        """Send message or messages stored in payload.

        :param reference: Optional string that will be stored in mprofi to
            mark messages from this batch.

        This method will use different endpoints of api (send or sendbulk)
        depending on the size of payload. When sending only one message -
        `send` api endpoint will be used, when sending multiple messages -
        it will use `sendbulk` endpoint.

        :raises: ValueError
        :returns: JSON string with updated status data

        """

        if len(self.payload) == 1:
            used_endpoint = self.send_endpoint
            full_payload = self.payload[0]
            if reference is not None:
                full_payload.update({
                    'reference': reference
                })
            extract_from_response = lambda r: [{'id': r['id']}]

        elif len(self.payload) > 1:
            used_endpoint = self.sendbulk_endpoint
            full_payload = {
                'messages': self.payload
            }
            if reference is not None:
                full_payload.update({
                    'reference': reference
                })
            extract_from_response = lambda r: r['result']

        else:
            raise ValueError("Empty payload. Please use `add_message` first.")

        full_url = '/'.join([
            self.url_base,
            self.api_version,
            used_endpoint, ""
        ])

        encoded_payload = json.dumps(full_payload)

        response = self.session.post(
            full_url,
            json=encoded_payload,
            verify=True
        )

        response_json = response.json()
        self.response = self.payload
        self.payload = []

        for sent_message, response_message in zip(
                self.response,
                extract_from_response(response_json)
        ):
            sent_message.update(response_message)

        return response_json

    def get_status(self):
        """Check status of messages existing in payload.

        This method grabs message id from each message in payload and calls
        to API to check message status.

        :returns: JSON string with updated status data

        """
        status_full_url = '/'.join([
            self.url_base,
            self.api_version,
            self.status_endpoint, ""
        ])

        for sent_message in self.response:
            message_id = sent_message['id']

            response = self.session.get(
                status_full_url,
                params={'id': message_id},
                verify=True
            )

            sent_message.update(response.json())

        return self.response
