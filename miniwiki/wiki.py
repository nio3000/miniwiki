
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

import re

def linkify(text):
    text = conditional_escape(text)

    pattern = re.compile(r'\[\[(\w+)\]\]')
    tag = r'<a href="\1">\1</a>'

    return mark_safe(pattern.sub(tag, text))
