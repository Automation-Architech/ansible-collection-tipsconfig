#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Sacha Boudjema <sachaboudjema@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class EntityStatusChoices:
    CHOICES = (
        'Enabled',
        'Disabled'
    )
    ENABLED = 'Enabled'
    DISABLED = 'Disabled'


class MatchChoices:
    CHOICES = (
        'equals',
        'notequals',
        'contains',
        'icontains',
        'belongsto',
    )
    EQUALS = 'equals'
    NOT_EQUALS = 'notequals'
    CONTAINS = 'contains'
    ICONTAINS = 'icontains'
    BELONGS_TO = 'belongsto'


class EntityChoices:
    CHOICES = (
        'Service',
        'AuthMethod',
        'AuthSource',
        'LocalUser',
        'Endpoint',
        'StaticHostList',
        'Role',
        'RoleMapping',
        'PostureInternal',
        'PostureExternal',
        'AuditPosture',
        'EnforcementPolicy',
        'EnforcementProfile',
        'NadClient',
        'NadGroup',
        'ProxyTarget',
        'Simulation',
        'AdminUser',
        'AdminPrivileges',
        'ServerConfig',
        'SnmpTrapConfig',
        'ExtSyslog',
        'DataFilter',
        'SyslogExportData',
        'ContextServer',
        'ContextServerAction',
        'RADIUS Dictionary',
        'PostureDictionary',
        'TacacsServiceDictionary',
        'TagDictionary',
        'TagDefinition',
        'GuestUser',
        'OnboardDevice',
    )
    SERVICE = 'Service'
    AUTH_METHOD = 'AuthMethod'
    AUTH_SOURCE = 'AuthSource'
    LOCAL_USER = 'LocalUser'
    ENDPOINT = 'Endpoint'
    STATIC_HOSTLIST = 'StaticHostList'
    ROLE = 'Role'
    ROLE_MAPPING = 'RoleMapping'
    POSTURE_INTERNAL = 'PostureInternal'
    POSTURE_EXTERNA = 'PostureExternal'
    AUDIT_POSTURE = 'AuditPosture'
    ENF_POLICY = 'EnforcementPolicy'
    ENF_PROFILE = 'EnforcementProfile'
    NAD_CLIENT = 'NadClient'
    NAD_GROUP = 'NadGroup'
    PROXY_TARGET = 'ProxyTarget'
    SIMULATION = 'Simulation'
    ADMIN_USER = 'AdminUser'
    ADMIN_PRIVILEGES = 'AdminPrivileges'
    SERVER_CONFIG = 'ServerConfig'
    SNMP_TRAP_CONFIG = 'SnmpTrapConfig'
    EXT_SYSLOG = 'ExtSyslog'
    DATA_FILTER = 'DataFilter'
    SYSLOG_EXPORT_DATA = 'SyslogExportData'
    CONTEXT_SERVER = 'ContextServer'
    CONTEXT_SERVER_ACTION = 'ContextServerAction'
    RADIUS_DICT = 'RADIUS Dictionary'
    POSTURE_DICT = 'PostureDictionary'
    TACACS_DICT = 'TacacsServiceDictionary'
    TAG_DICT = 'TagDictionary'
    TAG_DEF = 'TagDefinition'
    GUEST_USER = 'GuestUser'
    ONBOARD_DEVICE = 'OnboardDevice'
