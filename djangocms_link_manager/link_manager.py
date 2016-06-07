# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import namedtuple, OrderedDict

from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlparse, urlunparse

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

LinkReport = namedtuple('LinkReport', 'valid text url')


class HeadRequest(Request):
    def get_method(self):
        return "HEAD"


class LinkManager(object):
    """
    Defines an interface for the link manager.
    """
    scheme = 'http'
    netloc = 'localhost:8000'

    def __init__(self, scheme, netloc):
        self.scheme = scheme
        self.netloc = netloc

    def validate_url(self, url, verify_exists=False):
        """
        Utility for checking absolute, external URLs.
        :param url:
        :param verify_exists:
        :param scheme: default scheme to try if none exists
        :param netloc: default netloc (host:port) to try if none exists
        :return:
        """
        validator = URLValidator()
        parts = OrderedDict(zip(['scheme', 'netloc', 'path', 'params', 'query', 'fragment'], urlparse(url)))

        if not parts['scheme']:
            # Sometimes users enter urls without the scheme (intentionally or
            # otherwise). These are valid in browsers, but possibly not for our
            # validator, so we'll use 'http'
            parts['scheme'] = self.scheme
        if not parts['netloc']:
            # If there is no host/port, then this may be a link to a local
            # resource (media or static asset, etc.) Use localhost:8000.
            parts['netloc'] = self.netloc
        url = urlunparse(parts.values())

        try:
            validator(url)
        except ValidationError as exception:
            return False
        else:
            if verify_exists:
                try:
                    response = urlopen(HeadRequest(url))
                    # NOTE: urllib should have already resolved any 301/302s
                    return 200 <= response.code < 400
                except (HTTPError, URLError):
                    return False
            else:
                return True

    def check_link(self, instance, verify_exists=False):
        """
        Return True if the plugin instance's url form is valid.
        If `verify_exists` is True, also attempt to HEAD the link, return True
        only if exists.

        :param instance: Plugin instance
        :param verify_exists:
        :return: (Boolean, link_text, url)
        """
        raise NotImplementedError('Must be implemented in sub-class.')
