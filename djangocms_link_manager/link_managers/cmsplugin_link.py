# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import NoReverseMatch

from ..link_manager import LinkManager, LinkReport


class CMSPluginLinkLinkManager(LinkManager):

    def check_link(self, instance, verify_exists=False):
        internal_link = instance.internal_link
        valid = False

        if internal_link:
            try:
                url = internal_link.get_absolute_url(instance.language)
            except NoReverseMatch:
                url = None
            else:
                valid = True
        else:
            url = instance.external_link
            valid = self.validate_url(url, verify_exists=verify_exists)

        return LinkReport(
            valid=valid,
            text=instance.name,
            url=url,
        )
