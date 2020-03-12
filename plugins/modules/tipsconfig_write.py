#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Sacha Boudjema <sachaboudjema@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
author: Sacha Boudjema (@sachaboudjema)
module: sachaboudjema.aruba.clearpass_request
version_added: 2.9
short_description: Gets a list of Entity objects to save. The operation either adds a new object or updates an existing one.
description:
  - Either raw xml or a Jinja2 template can be provided as arguments.
  - If a template is provided, it is rendered localy using the playbook context.
  - If both template and xml are specified, template takes precedence.
options:

  entity:
    description:
      - Element type to be retrieved.
    type: str
    required: yes
    choices: See API documentation.

  template:
    description:
      - Template name to be rendered.
      - The search path is the same as for the standard ansible template module.
      - The standard Jinja2 lib is used for rendering (custom ansible jinja filters or not supported).
    type: str
    required: no

  xml:
    description:
      - Raw XML to be sent to the server.
      - The content must comply to the expected format, i.e. XML declaration and default namespace (see API docmentation).
    type: str
    required: no
'''

EXAMPLES = r'''
- name: Add role definitions (from template)
  tipsconfig_write:
    entity: GuestUser
    template: guest_user.j2

- name: Add role definitions (from raw xml)
  tipsconfig_write:
    entity: GuestUser
    xml: >-\n
      <?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
      <TipsApiRequest xmlns="http://www.avendasys.com/tipsapiDefs/1.0">\n
      <TipsHeader version="3.0" source="Guest"/>\n
      <GuestUsers>\n
          <GuestUser enabled="true" expiryTime="2010-12-30 12:24:37" startTime="2010-09-30 12:26:08"sponsorName="admin" guestType="USER" password="avenda123" name="mike">\n
          <GuestUserDetails sendSms="false" sendEmail="false" description="Test"/>\n
          <GuestUserTags tagName="First Name" tagValue="Michael"/>\n
          <GuestUserTags tagName="Email Address" tagValue="mike@sample.net"/>\n
          <GuestUserTags tagName="Phone" tagValue="4888888888"/>\n
          </GuestUser>\n
      </GuestUsers>\n
      </TipsApiRequest>\n
'''

RETURNS = r'''
tips_path:
  type: str
  returned: check mode
  description:
    - Destination URI of the API call, relative to the API root path.

tips_request:
  type: str
  returned: always
  description:
    - XML content sent to the server
  sample: |-\n
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
    <TipsApiRequest xmlns="http://www.avendasys.com/tipsapiDefs/1.0">\n
      <TipsHeader version="3.0" source="Guest"/>\n
      <GuestUsers>\n
        <GuestUser enabled="true" expiryTime="2010-12-30 12:24:37" startTime="2010-09-30 12:26:08"sponsorName="admin" guestType="USER" password="avenda123" name="mike">\n
          <GuestUserDetails sendSms="false" sendEmail="false" description="Test"/>\n
          <GuestUserTags tagName="First Name" tagValue="Michael"/>\n
          <GuestUserTags tagName="Email Address" tagValue="mike@sample.net"/>\n
          <GuestUserTags tagName="Phone" tagValue="4888888888"/>\n
        </GuestUser>\n
      </GuestUsers>\n
    </TipsApiRequest>\n

tips_response:
  type: str
  returned: on success
  description:
    - XML content returned by the server
  sample: |-\n
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
    <TipsApiResponse xmlns="http://www.avendasys.com/tipsapiDefs/1.0">\n
      <TipsHeader exportTime="Thu Sep 30 10:51:27 IST 2010" version="3.0"/>\n
      <StatusCode>Success</StatusCode>\n
      <LogMessages>\n
        <Message>Added 1 guest user(s)</Message>\n
      </LogMessages>\n
    </TipsApiResponse>\n
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

from ansible_collections.sachaboudjema.tipsconfig.plugins.module_utils.argspec import TipsArgSpec
from ansible_collections.sachaboudjema.tipsconfig.plugins.module_utils.tipsapi import TipsApiRequest


def run_module():
    argspec = dict(
        entity=TipsArgSpec.entity,
        xml=dict(required=False, type='str', default=None),
        template=dict(required=False, type='str', default=None),
    )
    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )
    tips_request = TipsApiRequest.write(
        module.params.get('entity'),
        module.params.get('xml')
    )

    if module.check_mode:
        module.exit_json(
            changed=False,
            tips_path=tips_request.path,
            tips_request=tips_request.tostring()
        )

    tips_response = tips_request.get_response(module)

    module.exit_json(
        changed=True,
        tips_request=tips_request.tostring(),
        tips_response=tips_response.tostring(),
        msg=tips_response.message
    )


def main():
    run_module()


if __name__ == '__main__':
    main()
