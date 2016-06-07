# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import NoReverseMatch

from ..link_manager import LinkManager, LinkReport


class CMSPluginLinkLinkManager(LinkManager):

    def check_link(self, instance, verify_exists=False):

        if instance.page_link:
            try:
                url = instance.page_link.get_absolute_url('en')
                return LinkReport(
                    valid=True,
                    text=instance.name,
                    url=url
                )
            except NoReverseMatch:
                return LinkReport(
                    valid=False,
                    text=instance.name,
                    url=None
                )
        else:
            return LinkReport(
                valid=self.validate_url(instance.url, verify_exists=verify_exists),
                text=instance.name,
                url=instance.url
            )
