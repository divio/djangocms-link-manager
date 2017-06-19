# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class LinkManagerPool(object):
    _managers = {}

    def clear_pool(self):
        self._managers = {}

    def register(self, plugin_class, link_manager):
        self._managers[plugin_class] = link_manager

    def get_link_manager(self, cls):
        return self._managers.get(cls, None)

    def get_link_plugin_types(self):
        return self._managers.keys()


link_manager_pool = LinkManagerPool()
