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
module: sachaboudjema.tipsconfig.tipsconfig_deleteconfirm
version_added: 2.9
short_description: Gets one or more filters and returns a list of element identifiers to be deleted.
description:
  - Operates like a read request with filters.
  - The XML response contains a list of filtered elements with their identifier (element-id).
  - The response can be used to delete items by identifier with the tipsconfig_delete module.
options:

  entity:
    description:
      - Element type to be retrieved.
    type: str
    required: yes
    choices: See API documentation.

  filters:
    description:
      - List of filters do be applied to the query.
      - Multiple filters are combined by an OR operator.
      - Multiple criteria within filters are combined by an AND operator
    type: list
    elements: dict
    required: no
    default: []
    suboptions:
      entity:
        description:
          - Sub-entity type to be filtered
        required: no
        default: Entity specified in top level options.
      criteria:
        description:
          - List of filter expressions to be combined by an AND operator
        type: list
        elements: str
        required: yes
        suboptions:
          description:
            - Condition expression in the form "field operator value".
            - List of valid operators: equals, notequals, contains, icontains, belongsto.
          type: str
          required: yes
'''

EXAMPLES = r'''
- name: Get identifiers of Guest Users with a name containing 'kang'
  tipsconfig_deleteconfirm:
    entity: GuestUser
    filters:
      - criteria:
        - name contains kang
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
      <Filter entity="GuestUser">\n
        <Criteria fieldName="name" filterString="kang" match="contains"/>\n
      </Filter>\n
    </TipsApiRequest>\n

tips_response:
  type: str
  returned: on success
  description:
    - XML content returned by the server
    - Contains the list of <element-id> elements to be used in with the delete module
  sample: |-\n
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
    <TipsApiResponse xmlns="http://www.avendasys.com/tipsapiDefs/1.0">\n
      <TipsHeader exportTime="Thu Sep 30 10:47:26 IST 2010" version="3.0"/>\n
      <StatusCode>Success</StatusCode>\n
      <EntityMaxRecordCount>1</EntityMaxRecordCount>\n
        <GuestUsers>\n
          <GuestUser enabled="true" name="bob kang">\n
            <element-id>GuestUser_bkang_MCw</element-id>\n
          </GuestUser>\n
          <GuestUser enabled="true" name="alice kang">\n
            <element-id>GuestUser_akang_MCw</element-id>\n
          </GuestUser>\n
        </GuestUser>\n
      </GuestUsers>\n
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
        filters=TipsArgSpec.filterlist
    )

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    tips_request = TipsApiRequest.deleteconfirm(
        module.params.get('entity'),
        module.params.get('filters')
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
