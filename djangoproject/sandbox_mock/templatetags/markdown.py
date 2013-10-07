from django import template
register = template.Library()


def markdown(text):
    return text


def strip_markdown(text):
    return text


register.filter('markdown', markdown)
register.filter('strip_markdown', strip_markdown)
