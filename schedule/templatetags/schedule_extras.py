from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Allow dict lookup by variable key in templates.
    Usage: {{ my_dict|get_item:variable_key }}
    """
    return dictionary.get(key, [])
