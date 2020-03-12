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
module: sachaboudjema.tipsconfig.tipsconfig_reorder
version_added: 2.9
short_description: Receives a list of names of objects of the Entity type and applies the new order to the list of objects.
description:
  - The XML request contains an EntityOrderList that should specify the entity-type and a list of names.
  - This list should contain the names of all elements of the entity-type.
  - The new order is returned in the XML response.
  - The Reorder method is available for the Services entity-type.
options:

  entity:
    description:
      - Element type to be retrieved.
    type: str
    required: yes
    choices: See API documentation.

  names:
    description:
      - Ordered list of entity names
    type: list
    required: yes
    elements: str
'''

EXAMPLES = r'''
- name: Reorder services
  tipsconfig_reorder:
    entity: Service
    names:
        - "[Guest Operator Logins]"
        - "test 802.1X Wireless"
        - "[Policy Manager Admin Network Login Service]"
        - "[AirGroup Authorization Service]"
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
      <EntityOrderList entity="Service"><Name>[Aruba Device Access Service]</Name>\n
        <Name>[Guest Operator Logins]</Name>\n
        <Name>test 802.1X Wireless</Name>\n
        <Name>[Policy Manager Admin Network Login Service]</Name>\n
        <Name>[AirGroup Authorization Service]</Name>\n
      </EntityOrderList>\n
    </TipsApiRequest>\n

tips_response:
  type: str
  returned: on success
  description:
    - XML content returned by the server
  sample: |-\n
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
    <TipsApiResponse xmlns="http://www.avendasys.com/tipsapiDefs/1.0">\n
      <TipsHeader exportTime="Wed May 28 15:45:24 IST 2014" version="6.3"/>\n
      <StatusCode>Success</StatusCode>\n
      <LogMessages><Message>Services have been reordered successfully</Message></LogMessages>\n
      <EntityOrderList entity="Service"><Name>[Aruba Device Access Service]</Name>\n
        <Name>[Guest Operator Logins]</Name>\n
        <Name>test 802.1X Wireless</Name>\n
        <Name>[Policy Manager Admin Network Login Service]</Name>\n
        <Name>[AirGroup Authorization Service]</Name>\n
      </EntityOrderList>\n
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
        names=dict(required=True, type='list', element='str')
    )

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    tips_request = TipsApiRequest.reorder(
        module.params.get('entity'),
        module.params.get('names')
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
