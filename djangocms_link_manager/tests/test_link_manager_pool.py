# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test.testcases import TestCase

from ..link_manager import LinkManager
from ..link_manager_pool import link_manager_pool


class LinkManagerPoolTests(TestCase):

    def test_link_manager_pool(self):
        class FakeManager(LinkManager):
            pass

        link_manager_pool.clear_pool()
        link_manager_pool.register('TestPlugin', FakeManager)

        self.assertTrue(len(link_manager_pool._managers) == 1)
        self.assertTrue('TestPlugin' in link_manager_pool.get_link_plugin_types())
        self.assertTrue(link_manager_pool.get_link_manager('TestPlugin') == FakeManager)
