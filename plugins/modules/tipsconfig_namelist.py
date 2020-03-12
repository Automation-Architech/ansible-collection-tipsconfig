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
module: sachaboudjema.tipsconfig.tipsconfig_namelist
version_added: 2.9
short_description: Returns the list of names for all objects created for an Entity type.
description:
  - The XML request contains an EntityNameList request passed in the entity-type.
  - In the XML response, EntityNameList is populated with the entity-names.
  - The list of names in the XML response is not displayed in a specific order.
  - However, for the entities that have a specific order (for example, Services), the names are populated in the order as specified in the EntityNameList.
options:

  entity:
    description:
      - Element type to be retrieved.
    type: str
    required: yes
    choices: See API documentation.
'''

EXAMPLES = r'''
- name: Get a list of services
  tipsconfig_namelist:
    entity: Service
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
      <TipsHeader version="3.0"/>\n
      <EntityNameList entity="Service"/>\n
    </TipsApiRequest>\n

tips_response:
  type: str
  returned: on success
  description:
    - XML content returned by the server
  sample: |-\n
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
    <TipsApiResponse xmlns="http://www.avendasys.com/tipsapiDefs/1.0">\n
    <TipsHeader exportTime="Wed May 28 15:39:01 IST 2014" version="6.3"/>\n
      <StatusCode>Success</StatusCode>\n
      <EntityNameList entity="Service">\n
        <Name>[Policy Manager Admin Network Login Service]</Name>\n
        <Name>[AirGroup Authorization Service]</Name>\n
        <Name>[Aruba Device Access Service]</Name>\n
        <Name>[Guest Operator Logins]</Name><Name>test 802.1X Wireless</Name>\n
      </EntityNameList>\n
    </TipsApiResponse>\n
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

from ansible_collections.sachaboudjema.tipsconfig.plugins.module_utils.argspec import TipsArgSpec
from ansible_collections.sachaboudjema.tipsconfig.plugins.module_utils.tipsapi import TipsApiRequest


def run_module():
    argspec = dict(
        entity=TipsArgSpec.entity,
        entity_type_list=dict(required=False, type='list', elements='str', default=list())
    )

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    tips_request = TipsApiRequest.namelist(
        module.params.get('entity'),
        module.params.get('entity_type_list')
    )

    if module.check_mode:
        module.exit_json(
            changed=False,
            tips_path=tips_request.path,
            tips_request=tips_request.tostring()
        )

    tips_response = tips_request.get_response(module)

    module.exit_json(
        changed=False,
        tips_request=tips_request.tostring(),
        tips_response=tips_response.tostring(),
        msg=tips_response.message
    )


def main():
    run_module()

if __name__ == '__main__':
    main()
