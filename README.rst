=======================
django CMS Link Manager
=======================

.. image:: https://travis-ci.org/divio/djangocms-link-manager.svg?branch=master
    :target: https://travis-ci.org/divio/djangocms-link-manager

An extensible means of checking for broken links in virtually any
django CMS plugin.

--------
Overview
--------

There are numerous plugins that provide hyperlink capabilities in django CMS
each with their own fields for store a variety of types of hyperlinks. As a
result, it can become a challenge to find bad links across the whole project.
This project attempts to provide a solution in an extensible manner.

------------
Installation
------------

This package requires Python 2.7 or later and Django 1.8 or later.

First, install the package from PyPI: ::

    pip install djangocms-link-manager

Then add it to your ``INSTALLED_APPS``: ::

    # settings.py
    ...
    INSTALLED_APPS = [
        ...
        'djangocms_link_manager',
    ]

-----
Usage
-----

The simplest way to run this is: ::

    python manage.py check_links

However, this command accepts a number of optional arguments: ::

    --verify-exists     Check that each link's target exists (use caution,
                        makes HTTP HEAD requests).
    --scheme SCHEME     Default scheme to use for scheme-less URLs
                        (default: "http").
    --host NETLOC       Default [host:port] to use for relative URLs (defaults
                        to "localhost:8000").
    --template TEMPLATE Override the report rendering template.
    --mail-managers     Instead of printing report to the console, email it to
                        the addresses defined in the MANAGERS list in the
                        project's settings.py.


---------
Extending
---------

This package currently supports to plugins by their class names:
``Bootstrap3ButtonCMSPlugin`` and ``LinkPlugin`` which come from the packages:
``aldryn_bootstrap3`` and ``djangocms_link`` respectively. To add support for
a new CMSPlugin, one simply writes creates a class that subclasses
``djangocms_link_manager.link_manager.LinkManager`` and overrides the
``check_link()`` method according to the particulars of the CMSPlugin you wish
to support.

Once this is created, register the link manager into the link manager pool on
startup with: ::

    from djangocms_link_manager.link_manager import LinkManager, LinkReport
    from djangocms_link_manager.link_manager_pool import link_manager_pool

    class MyLinkPluginLinkManager(LinkManager):
        """MyLinkPlugin only contains the fields 'name' and 'url'."""

        def check_link(self, instance, verify_exists=False):
            """Override this method and adapt to MyLinkPlugin."""
            return LinkReport(
                valid=self.validate_url(instance.url, verify_exists=verify_exists),
                text=instance.name,
                url=instance.url
            )

    link_manager_pool.register('MyLinkPlugin', MyLinkPluginLinkManager)


Support for additional URL schemes
----------------------------------

This package already provides support for the following URL schemes: ``ftp``,
``ftps``, ``http``, ``https``, ``bitcoin``, ``mailto``, and ``tel``. If a project
requires validation of other schemes, they can be added to the link manager
(subclass of LinkManager) simply by including a method with the name
``validate_MYSCHEME`` with the signature: ::

    def validate_MYSCHEME(self, parts, verify_exists=False):
        # Do your thing here
        if valid:
            return True
        else:
            return False

Replace "MYSCHEME" with the lower-case scheme of your choice.

``verify_exists``, when set to True, is intended to check to see if the resource
is really available. For example, for ``http(s)``, ``ftp(s)`` validator will
actually attempt to fetch the URL (using an HTTP HEAD request) and will return
``False`` if the result is an HTTP 404 error. Use this responsibly.

``parts`` is a dict of the URLs parts as follows: ::

    parts = {
        'scheme': ...,
        'netloc': ...,
        'path': ...,
        'params': ...,
        'query': ...,
        'fragment': ...,
    }

For more information about these elements, please review the docs for
`urllib.parse <https://docs.python.org/3/library/urllib.html>`_.
