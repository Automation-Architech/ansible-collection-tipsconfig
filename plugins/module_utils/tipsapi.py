#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Sacha Boudjema <sachaboudjema@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
author: Sacha Boudjema (@sachaboudjema)
short_description: Object representations of API messages.
version_added: "2.9"
'''

import re

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, QName
from ansible.errors import AnsibleError
from ansible_collections.sachaboudjema.tipsconfig.plugins.module_utils.choices import EntityChoices, EntityStatusChoices

VERSION = '6.7'
ROOT_PATH = '/tipsapi/config'
XMLNS = 'http://www.avendasys.com/tipsapiDefs/1.0'


def parse_filter_criteria(expression):
    m = re.match(r'^(?P<field>\w+) (?P<operator>\w+) (?P<value>.+)$', expression)
    if not m:
        raise AnsibleError(f'Unable to parse criteria expression: "{expression}"')
    return m.group('field'), m.group('operator'), m.group('value')


class TipsApiXML:
    def __init__(self, xml):
        self.xml = xml

    def tostring(self, remove_whitespaces=True):
        ElementTree.register_namespace('', XMLNS)
        xml_string = ElementTree.tostring(self.xml, encoding='utf8', method='xml').decode()
        if remove_whitespaces:
            xml_string = re.sub(r'\s+(?=<)', '', xml_string)
        return xml_string


class TipsApiRequest(TipsApiXML):
    def __init__(self, method, entity):
        self.path = f'{ROOT_PATH}/{method}/{entity}'
        self.entity = entity
        self.path = None
        self.xml = Element(QName(XMLNS, 'TipsApiRequest'))
        tips_header = SubElement(self.xml, QName(XMLNS, 'TipsHeader'), {'version': VERSION})
        if entity in (EntityChoices.GUEST_USER, EntityChoices.ONBOARD_DEVICE):
            tips_header.set('source', 'Guest')

    @staticmethod
    def delete(cls, entity, identifiers):
        instance = cls('delete', entity)
        instance.xml.append(instance.tips_delete(identifiers))
        return instance

    @staticmethod
    def deleteconfirm(cls, entity, filters=list()):
        instance = cls('deleteConfirm', entity)
        for f in filters:
            instance.xml.append(instance.tips_filter(f))
        if not filters:
            instance.xml.append(instance.tips_filter())
        return instance

    @classmethod
    def namelist(cls, entity, entity_type_list=list()):
        instance = cls('namelist', entity)
        for e in entity_type_list:
            instance.xml.append(instance.tips_namelist(e))
        if not entity_type_list:
            instance.xml.append(instance.tips_namelist(entity))
        return instance

    @classmethod
    def read(cls, entity, filters=list()):
        instance = cls('read', entity)
        for f in filters:
            instance.xml.append(instance.tips_filter(f))
        if not filters:
            instance.xml.append(instance.tips_filter())
        return instance

    @staticmethod
    def reorder(cls, entity, names):
        instance = cls('reorder', entity)
        instance.xml.append(instance.tips_orderlist(names))
        return instance

    @classmethod
    def statuschange(cls, entity, status_list):
        instance = cls('status', entity)
        instance.xml.append(instance.tips_statuslist(status_list))
        return instance

    @classmethod
    def write(cls, entity, xml):
        instance = cls('write', entity)
        instance.xml = ElementTree.fromstring(xml)
        return instance

    def get_response(self, ansible_module):
        from ansible.module_utils.connection import Connection
        try:
            response = Connection(ansible_module._socket_path).send_request(
                self.path,
                data=self.tostring()
            )
            tips_response = TipsApiResponse(response)
        except TipsApiError as exc:
            ansible_module.fail_json(
                changed=False,
                msg=f'{exc.errorcode}: {exc.message}',
                tips_request=self.tostring(),
                tips_response=response
            )
        return tips_response

    def tips_delete(self, identifiers):
        el = Element(QName(XMLNS, 'Delete'))
        for name in identifiers:
            subel = SubElement(el, QName(XMLNS, 'Element-Id'))
            subel.text = name
        return el

    def tips_filter(self, filtr=dict()):
        entity = filtr.get('entity', self.entity)
        criteria = filtr.get('criteria', list())
        el = Element(QName(XMLNS, 'Filter'), {'entity': entity})
        if criteria:
            field, operator, value = parse_filter_criteria(criteria[0])
            crit = SubElement(el, QName(XMLNS, 'Criteria'), {
                'fieldName': field,
                'filterString': value,
                'match': operator
            })
            for more in criteria[1:]:
                field, operator, value = parse_filter_criteria(more)
                SubElement(crit, QName(XMLNS, 'MoreFilterConditions'), {
                    'fieldName': field,
                    'fieldValue': value,
                    'match': operator
                })
        return el

    def tips_namelist(self, entity=None):
        if entity is None:
            entity = self.entity
        return Element(QName(XMLNS, 'EntityNameList'), {'entity': entity})

    def tips_orderlist(self, names):
        el = Element(QName(XMLNS, 'EntityOrderList'), {'entity': self.entity})
        for name in names:
            subel = SubElement(el, QName(XMLNS, 'Name'))
            subel.text = name
        return el

    def tips_statuslist(self, status_list):
        el = Element(QName(XMLNS, 'EntityStatusList'), {'entity': self.entity})
        for item in status_list:
            status = EntityStatusChoices.ENABLED if item['enabled'] else EntityStatusChoices.DISABLED
            subel = SubElement(el, QName(XMLNS, status))
            subel.text = item['name']
        return el


class TipsApiError(Exception):
    def __init__(self, xml):
        self.xml = xml

    @property
    def errorcode(self):
        tag = QName(XMLNS, 'ErrorCode').text
        return self.xml.find(tag).text

    @property
    def messages(self):
        tag = QName(XMLNS, 'Message').text
        return [m.text for m in self.xml.findall(tag)]

    @property
    def message(self):
        return '. '.join(self.messages)


class TipsApiResponse(TipsApiXML):
    def __init__(self, body):
        self.xml = ElementTree.fromstring(body)
        if self.statuscode == 'Failure':
            tag = QName(XMLNS, 'TipsApiError').text
            raise TipsApiError(self.xml.find(tag))

    @property
    def statuscode(self):
        tag = QName(XMLNS, 'StatusCode').text
        return self.xml.find(tag).text

    @property
    def messages(self):
        logmessages_tag = QName(XMLNS, 'LogMessages').text
        message_tag = QName(XMLNS, 'Message').text
        el = self.xml.find(logmessages_tag)
        if not el:
            return list()
        return list(m.text for m in el.findall(message_tag))

    @property
    def message(self):
        if not self.messages:
            return ''
        return '. '.join(self.messages)
