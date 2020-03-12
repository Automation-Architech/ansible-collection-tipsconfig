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
module: sachaboudjema.tipsconfig.tipsconfig_delete
version_added: 2.9
short_description: Removes a list of elements from the configuration.
descirption:
  - Deletes a set of configuration elements identified by element-id.
  - The XML response contains a log of deleted elements.
  - The list of identifiers for each object that needs to be deleted can be returned by the tipsconfig_deleteconfirm module.
options:

  entity:
    description:
      - Element type to be deleted.
    type: str
    required: yes
    choices: See API documentation.

  identifiers:
    description:
      - List of elements to be deleted.
    type: list
    elements: str
    required: yes
'''

EXAMPLES = r'''
- name: Delete Guest User
  tipsconfig_delete:
    entity: GuestUser
    identifiers:
      - GuestUser_kang_MCw
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
      <Delete>\n
        <Element-Id>GuestUser_kang_MCw</Element-Id>\n
      </Delete>\n
    </TipsApiRequest>\n

tips_response:
  type: str
  returned: on success
  description:
    - XML content returned by the server
  sample: |-\n
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
    <TipsApiResponse xmlns="http://www.avendasys.com/tipsapiDefs/1.0">\n
      <TipsHeader exportTime="Thu Sep 30 10:56:00 IST 2010" version="3.0"/>\n
      <StatusCode>Success</StatusCode>\n
      <LogMessages>\n
        <Message>Guest user deleted successfully</Message>\n
      </LogMessages>\n
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
        elementid_list=dict(required=True, type='list', element='str')
    )

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    tips_request = TipsApiRequest.delete(
        module.params.get('entity'),
        module.params.get('identifiers')
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
