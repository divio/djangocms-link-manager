{% load i18n cms_tags %}

===========================================================
{% trans "Broken Link Report" %}
===========================================================

{% blocktrans with timestamp=timestamp %}Report generated {{timestamp}}{% endblocktrans %}
verify-exists: {% if options.verify_exists %}enabled {% else %}{% trans "disabled" %}{% endif %}
{% blocktrans with scheme=options.scheme %}Default scheme: {{ scheme }}{% endblocktrans %}
{% blocktrans with netloc=options.netloc %}Default host/port: {{ netloc }}{% endblocktrans %}

-----------------------------------------------------------
{% trans "Broken Links" %}
-----------------------------------------------------------

{% blocktrans with num=bad_links|length total=count_all_links %}The following {{ num }}/{{ total }} plugins appear broken.{% endblocktrans %}
{% for link in bad_links %}
    - {{ link.cls }} ({{ link.pk }}) in placeholder "{{ link.slot }}" on page "{{ link.page }}"{% if link.page_url %} ({{ link.page_url }}){% endif %} has a broken link labeled: "{{ link.label }}" <{{ link.url }}>
{% empty %}
    {% trans "No bad links found." %}
{% endfor %}

{% if unknown_plugin_classes %}
-----------------------------------------------------------
{% trans "Un-managed link plugins" %}
-----------------------------------------------------------

{% trans "The following plugin types do not have a registered link manager." %}
{% for cls in unknown_plugin_classes %}
    - {{ cls }}
{% endfor %}
{% endif %}
{% trans "End of report" %}
