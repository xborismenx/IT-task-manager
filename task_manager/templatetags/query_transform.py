from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    context = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            context[key] = value
        else:
            context.pop(key, None)
    return context.urlencode()
