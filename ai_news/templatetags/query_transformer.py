from django import template

register = template.Library()


@register.simple_tag
def query_transformer(request, **kwargs):
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value:
            updated[key] = value
        else:
            updated.pop(key, None)
    return updated.urlencode()
