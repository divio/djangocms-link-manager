# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import NoReverseMatch

from ..link_manager import LinkManager, LinkReport


class Bootstrap3ButtonCMSPluginLinkManager(LinkManager):

    def check_link(self, instance, verify_exists=False):
        valid = False

        if instance.link_phone:
            url = instance.link_phone
            valid = True  # TODO
        elif instance.link_mailto:
            url = instance.link_mailto
            valid = True  # TODO
        elif instance.link_url:
            url = instance.link_url
            valid = self.validate_url(url, verify_exists=verify_exists)
        elif instance.link_page:
            try:
                url = instance.link_page.get_absolute_url(instance.language)
            except NoReverseMatch:
                url = None
                valid = False
            else:
                valid = True

        elif instance.link_file:
            url = instance.link_file.url
            valid = self.validate_url(url, verify_exists=verify_exists),

        else:
            url = None

        return LinkReport(
            valid=valid,
            text=instance.label,
            url=url,
        )
