# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test.testcases import TestCase

from ..link_manager import LinkManager


class LinkManagerTests(TestCase):

    def setUp(self):
        super(LinkManagerTests, self).setUp()
        self.link_manager = LinkManager()

    def test_validate_url(self):
        # ftp
        self.assertTrue(self.link_manager.validate_url('ftp://user:password@host.com:1234/path'))

        # ftps
        self.assertTrue(self.link_manager.validate_url('ftps://user:password@host.com:1234/path'))

        # http
        self.assertTrue(self.link_manager.validate_url('http://www.google.com'))
        self.assertTrue(self.link_manager.validate_url('http://www.google.com/'))
        self.assertTrue(self.link_manager.validate_url('http://www.google.com/path/?q=query'))
        self.assertFalse(self.link_manager.validate_url('http://localhost/non-existent-obj/', verify_exists=True))  # noqa non-existent object
        self.assertFalse(self.link_manager.validate_url('/non-existent-obj/', verify_exists=True))  # noqa non-existent relative object
        self.assertFalse(self.link_manager.validate_url('http://192.168.0.256/', verify_exists=True))  # noqa Invalid IPv4 address
        self.assertFalse(self.link_manager.validate_url('http://2002::/', verify_exists=True))  # Invalid IPv6 address
        self.assertFalse(self.link_manager.validate_url('', verify_exists=True))  # No URL provided

        # https
        self.assertTrue(self.link_manager.validate_url('https://www.google.com'))
        self.assertTrue(self.link_manager.validate_url('https://www.google.com/'))
        self.assertTrue(self.link_manager.validate_url('https://www.google.com/path/?q=query'))

        # bitcoin
        self.assertTrue(self.link_manager.validate_url('bitcoin:1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i'))
        self.assertTrue(self.link_manager.validate_url('bitcoin:1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i?amount=1.0'))
        self.assertTrue(self.link_manager.validate_url('bitcoin:1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i?amount=1.0&label=label+for+tx&message=message+for+recipient'))  # noqa
        self.assertFalse(self.link_manager.validate_url('bitcoin:1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW6XX'))  # bad checksum

        # mailto
        self.assertTrue(self.link_manager.validate_url('mailto:user@host.com?subject=the+subject'))
        self.assertFalse(self.link_manager.validate_url('mailto:user@host'))  # bad host

        # tel
        self.assertTrue(self.link_manager.validate_url('tel:+41444801270'))
        self.assertTrue(self.link_manager.validate_url('tel:+12016934846'))
        self.assertTrue(self.link_manager.validate_url('tel:+120169DIVIO'))  # Text as numbers is OK
        self.assertFalse(self.link_manager.validate_url('tel:+1201693484'))  # Number too short
        self.assertTrue(self.link_manager.validate_url('tel:+12006934846', verify_exists=False))  # Looks ok, but...
        self.assertFalse(self.link_manager.validate_url('tel:+12006934846', verify_exists=True))  # Bad area code
        self.assertFalse(self.link_manager.validate_url('tel:+9992006934846', verify_exists=True))  # Bad country code

        # Invalid scheme
        self.assertFalse(self.link_manager.validate_url('gopher:192.168.0.1'))  # Unhandled scheme (for now)
