#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Sacha Boudjema <sachaboudjema@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
author: Sacha Boudjema (@sachaboudjema)
short_description: Action to render templates used with the tipsconfig_write module.
version_added: "2.9"
'''

import os
import jinja2

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError, AnsibleFileNotFound, AnsibleAction, AnsibleActionFail
from ansible.module_utils._text import to_bytes, to_text, to_native


class ActionModule(ActionBase):

    def get_template_searchpath(self, task_vars, source):
        searchpath = task_vars.get('ansible_search_path', [])
        searchpath.extend([self._loader._basedir, os.path.dirname(source)])
        for i in range(len(searchpath)):
            searchpath.append(os.path.join(searchpath[i], 'templates'))
        return searchpath

    def run(self, tmp=None, task_vars=None):

        module_args = self._task.args

        # Do whatever the parent action should do.
        if task_vars is None:
            task_vars = dict()
        result = super(ActionModule, self).run(tmp, task_vars)

        # If a template file path is provided in the module arguments,
        # render it and replace the xml payload with rendered contents.
        if module_args.get('template', None):
            template_source = module_args['template']
            try:
                searchpath = self.get_template_searchpath(task_vars, template_source)
                env = jinja2.Environment(
                    loader=jinja2.FileSystemLoader(searchpath),
                    autoescape=jinja2.select_autoescape(['html', 'xml'])
                )
                template = env.get_template(template_source)
                module_args['template'] = None
                module_args['xml'] = to_text(template.render(**task_vars))
            except Exception as exc:
                raise AnsibleActionFail(f'Error trying to process template, {type(exc).__name__}: {to_text(exc)}')

        # Execute the module and return final result.
        result.update(self._execute_module(
            module_args=module_args,
            tmp=tmp,
            task_vars=task_vars
        ))
        return result
