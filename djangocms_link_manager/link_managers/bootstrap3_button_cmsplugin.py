# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import NoReverseMatch

from ..link_manager import LinkManager, LinkReport


class Bootstrap3ButtonCMSPluginLinkManager(LinkManager):

    def check_link(self, instance, verify_exists=False):
        if instance.link_phone:
            # TODO?
            return LinkReport(valid=True, text=instance.label, url=instance.link_phone)
        elif instance.link_mailto:
            # TODO?
            return LinkReport(valid=True, text=instance.label, url=instance.link_mailto)
        elif instance.link_url:
            return LinkReport(
                valid=self.validate_url(instance.link_url, verify_exists=verify_exists),
                text=instance.label,
                url=instance.link_url
            )
        elif instance.link_page:
            try:
                url = instance.link_page.get_absolute_url('en')
                return LinkReport(
                    valid=True,
                    text=instance.label,
                    url=url
                )
            except NoReverseMatch:
                return LinkReport(
                    valid=False,
                    text=instance.label,
                    url=None
                )
        elif instance.link_file:
            return LinkReport(
                valid=self.validate_url(instance.link_file.url, verify_exists=verify_exists),
                text=instance.label,
                url=instance.link_file.url
            )
        else:
            return LinkReport(valid=False, text=instance.label, url=None)
