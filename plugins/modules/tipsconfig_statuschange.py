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
module: sachaboudjema.tipsconfig.tipsconfig_statuschange
version_added: 2.9
short_description: Gets the name-list of disabled and enabled entities of a specific type and changes the status of the entities appropriately.
description:
  - The XML request contains an EntityStatusList that includes the entity-type and a namelist.
  - You must specify the Enabled elements first and then the Disabled elements within the name-list.
  - The status list of the entity is returned in the XML response.
options:

  entity:
    description:
      - Element type to be retrieved.
    type: str
    required: yes
    choices: See API documentation.

  status_list:
    description:
      - List of entity names and status.
    type: list
    required: yes
    elements: dict
    options:
      name:
        description:
          - Entity name.
        type: str
        required: yes
      enabled:
        description:
          - Status of the entity.
        type: bool
        required: yes
'''

EXAMPLES = r'''
- name: Change services status
  tipsconfig_statuschange:
    entity: Service
    status_list:
      - name: "[Aruba Device Access Service]"
        enabled: true
      - name: "[Guest Operator Logins]"
        enabled: true
      - name: "test 802.1X Wireless"
        enaled: false
      - name: "[Policy Manager Admin Network Login Service]"
        enabled: false
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
      <TipsHeader version="6.3"/>\n
      <EntityStatusList entity="Service">\n
        <Enabled>[Aruba Device Access Service]</Enabled>\n
        <Enabled>[Guest Operator Logins]</Enabled>\n
        <Disabled>test 802.1X Wireless</Disabled>\n
        <Disabled>[Policy Manager Admin Network Login Service]</Disabled>\n
      </EntityStatusList>\n
    </TipsApiRequest>\n

tips_response:
  type: str
  returned: on success
  description:
    - XML content returned by the server
  sample: |-\n
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
    <TipsApiResponse xmlns="http://www.avendasys.com/tipsapiDefs/1.0">\n
      <TipsHeader exportTime="Wed May 28 16:08:13 IST 2014" version="6.3"/>\n
      <StatusCode>Success</StatusCode>\n
      <LogMessages><Message>Status successfully changed</Message></LogMessages>\n
      <EntityStatusList entity="Service">\n
        <Enabled>[AirGroup Authorization Service]</Enabled>\n
        <Enabled>[Aruba Device Access Service]</Enabled>\n
        <Enabled>[Guest Operator Logins]</Enabled>\n
        <Disabled>[Policy Manager Admin Network Login Service]</Disabled>\n
        <Disabled>test 802.1X Wireless</Disabled>\n
      </EntityStatusList>\n
    </TipsApiResponse>\n
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.six.moves.urllib.error import HTTPError

from ansible_collections.sachaboudjema.tipsconfig.plugins.module_utils.argspec import TipsArgSpec
from ansible_collections.sachaboudjema.tipsconfig.plugins.module_utils.tipsapi import TipsApiRequest


def run_module():
    argspec = dict(
        entity=TipsArgSpec.entity,
        status_list=dict(required=True, type='list', element='dict')
    )

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    tips_request = TipsApiRequest.statuschange(
        module.params.get('entity'),
        module.params.get('status_list')
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
