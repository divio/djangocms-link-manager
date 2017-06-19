# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.template.loader import get_template
from django.utils.lru_cache import lru_cache
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from django.core.mail import mail_managers

from cms.models import CMSPlugin, NoReverseMatch

from ...link_manager_pool import link_manager_pool


class Command(BaseCommand):
    help = """Generate link report."""

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--verify-exists', action='store_true', dest='verify_exists', default=False,
            help="Check that each link's target exists (use caution, makes HTTP HEAD requests)."
        )
        parser.add_argument(
            '--scheme', action='store', dest='scheme', default='http',
            help='Default scheme to use for scheme-less URLs (default: "http").'
        )
        parser.add_argument(
            '--host', action='store', dest='netloc', default='localhost:8000',
            help='Default [host:port] to use for relative URLs (defaults to "localhost:8000").'
        )
        parser.add_argument(
            '--template', action='store', dest='template', default='djangocms_link_manager/text_only.rst',
            help='Override the report rendering template.'
        )
        parser.add_argument(
            '--mail-managers', action='store_true', dest='mail_managers', default=False,
            help="Instead of printing report to the console, email it to the "
                 "addresses defined in MANAGERS in the project's settings.py."
        )

    @lru_cache(maxsize=100)
    def get_link_manager(self, plugin_type, scheme, netloc):
        return link_manager_pool.get_link_manager(plugin_type)(scheme=scheme, netloc=netloc)

    def handle(self, *args, **options):
        """
        We're only interested in link plugins that are either not on any page or
        are on a published page.

        NOTE: This could be a large set.
        """
        verify_exists = options['verify_exists']
        scheme = options['scheme']
        netloc = options['netloc']

        bad_links = []
        unknown_plugin_classes = []
        count_all_links = 0

        # Check only plugins contained in placeholders which are on a
        # published page or no page at all (PlaceholderFields).
        link_plugins = (
            CMSPlugin.objects
            .filter(plugin_type__in=link_manager_pool.get_link_plugin_types())
            .filter(
                Q(placeholder__page__isnull=True) |
                Q(placeholder__page__publisher_is_draft=False)
            )
        )
        self.stdout.write('Will check {} Plugins'.format(link_plugins.count()))
        count = 0
        for link_plugin in link_plugins.iterator():
            count += 1
            if not (count % 1000):
                self.stdout.write('  Checked {} plugins...'.format(count))
            plugin_inst, plugin_class = link_plugin.get_plugin_instance()
            link_manager = self.get_link_manager(plugin_inst.plugin_type, scheme=scheme, netloc=netloc)

            if link_manager:
                link_reports = link_manager.check_link(
                    plugin_inst,
                    verify_exists=verify_exists,
                )
                # Convert to a list if only a single item was returned.
                try:
                    iter(link_reports)
                except TypeError:
                    # Result is not a list
                    link_reports = [link_reports]

                for link_report in link_reports:
                    count_all_links += 1

                    if not link_report.valid:
                        slot = link_plugin.placeholder.slot
                        page = getattr(link_plugin.placeholder, 'page', None)
                        if page:
                            try:
                                page_url = 'https://{}{}'.format(
                                    page.site.domain,
                                    page.get_absolute_url(plugin_inst.language),
                                )
                            except NoReverseMatch:
                                page_url = ''
                        else:
                            page_url = ''

                        bad_link = {
                            'cls': plugin_inst.plugin_type,
                            'page': page,
                            'page_url': page_url,
                            'pk': plugin_inst.pk,
                            'slot': slot,
                            'label': link_report.text,
                            'url': link_report.url,
                            'instance': plugin_inst,
                        }
                        self.stdout.write(
                            'Broken link "{url}" on "{page_url}" plugin.id:{pk} placeholder:{slot}'.format(**bad_link)
                        )
                        bad_links.append(bad_link)
            else:
                if plugin_inst.plugin_type not in unknown_plugin_classes:
                    unknown_plugin_classes.append(plugin_inst.plugin_type)

        template = get_template(options['template'])
        report = template.render({
            'bad_links': bad_links,
            'count_all_links': count_all_links,
            'options': options,
            'timestamp': now(),
            'unknown_plugin_classes': unknown_plugin_classes,
        })

        if options['mail_managers']:
            try:
                mail_managers(
                    _('Broken link report: {0}').format(now()),
                    report,
                    fail_silently=False
                )
                self.stdout.write('Successfully sent broken link report via email')
            except Exception as exception:
                self.stderr.write('ERROR: Report could not be sent via mail: {0}'.format(exception))
        else:
            self.stdout.write(report)
