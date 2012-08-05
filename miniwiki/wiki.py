
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

import re

import markdown2
from markdown2 import Markdown

def linkify(text):
    pattern = re.compile(r'\[\[(\w+)\]\]')
    tag = r'[\1](/\1)'

    return pattern.sub(tag, text)

def wikify(text):

    text = linkify(text)

    text = Markdown(safe_mode="escape").convert(text)

    return mark_safe(text)
