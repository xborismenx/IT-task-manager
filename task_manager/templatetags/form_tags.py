from django import template

register = template.Library()


@register.filter(name='add_tags')
def add_tags(value, css_class):
    excited_class = value.field.widget.attrs.get("class", "")
    new_class = f"{excited_class} {css_class}".strip()
    return value.as_widget(attrs={"class": new_class})
