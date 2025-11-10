from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Allows you to access dictionary items in templates."""
    return dictionary.get(key)
