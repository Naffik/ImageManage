from django import template
import markdown2

register = template.Library()


@register.filter(name='markdown_to_html')
def markdown_to_html(markdown_text):
    return markdown2.markdown(markdown_text)
