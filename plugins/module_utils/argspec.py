#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Sacha Boudjema <sachaboudjema@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.sachaboudjema.tipsconfig.plugins.module_utils.choices import EntityChoices, MatchChoices


class TipsArgSpec:
    entity = dict(
        required=True,
        type='str',
        choices=EntityChoices.CHOICES
    )

    _fieldname = dict(
        required=True,
        type='str'
    )
    _filterstring = dict(
        required=True,
        type='str'
    )
    _match = dict(
        required=True,
        type='str',
        choices=MatchChoices.CHOICES
    )
    _criteria = dict(
        required=False,
        type='list',
        element='dict',
        default=list(),
        options=dict(
            field_name=_fieldname,
            filter_string=_filterstring,
            match=_match,
        )
    )
    _entity = dict(
        required=False,
        type='str',
        choices=EntityChoices.CHOICES
    )
    filterlist = dict(
        required=False,
        type='list',
        element='dict',
        default=list(),
        options=dict(
            entity=_entity,
            criteria=_criteria
        )
    )