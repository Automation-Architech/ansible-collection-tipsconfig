#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Sacha Boudjema <sachaboudjema@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
author: Sacha Boudjema (@sachaboudjema)
httpapi: sachaboudjema.aruba.clearpass
short_description: HttpApi Plugin for Aruba Clearpass SOAP Configuration API.
description:
  - Implements the httpapi connection type for Aruba Clearpass Configuration API.
version_added: "2.9"
'''

from ansible.module_utils._text import to_text, to_native
from ansible.errors import AnsibleConnectionFailure
from ansible.plugins.httpapi import HttpApiBase
from http.client import HTTPException

CHARSET = 'UTF-8'
HEADERS = {
    'Accept': '*/*',
    'Content-Type': 'application/xml'
}


class HttpApi(HttpApiBase):

    def send_request(self, path, method='POST', params=dict(), data=None):
        try:
            response, response_data = self.connection.send(
                path, data, method=method, headers=HEADERS
            )
        except HTTPException as exc:
            raise AnsibleConnectionFailure(f'HTTP exception: {to_native(exc)}')
        return self.handle_response(response, response_data)

    def handle_response(self, response, response_data):
        response_body = response_data.read().decode(CHARSET)
        return response_body

    def handle_httperror(self, exc):
        # Always raise http errors
        return False
