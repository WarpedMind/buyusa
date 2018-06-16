# -*- coding: UTF-8 -*-
from django import template
from django.template import Context
from django.template.loader import get_template

from math import floor
import re, urllib

from django.forms import BaseForm
from django.forms.forms import BoundField
from django.forms.widgets import TextInput, CheckboxInput, CheckboxSelectMultiple, RadioSelect,Textarea
from django.conf import settings
from django.utils.html import format_html_join
import random
import datetime

register = template.Library()

@register.filter
def add_class(field, cssclass=''):
    if cssclass:
        if field and field.field:
            if 'class' in field.field.widget.attrs:
                field.field.widget.attrs['class'] += ' %s' % (cssclass)
            else:
                field.field.widget.attrs['class'] = cssclass
    return field

@register.filter
def commaSplit(value, sep = ","):
    parts = value.split(sep)
    output = []
    i = 0
    for part in parts:
        i += 1
        output.append("<span>" + part.strip().capitalize() + "</span>")
        if i >= 6:
            break
    return "".join(output)