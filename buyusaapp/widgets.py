# -*- coding: UTF-8 -*-
from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

from django.forms import FileInput
from django.template.loader import render_to_string
from django.db.models.fields.files import ImageFieldFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import File

import os,random,datetime,io,base64,json

try:
    from PIL import Image
except ImportError:
    import Image


from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import conditional_escape, format_html

def generate_tradeno():
    rand = random.SystemRandom()
    rand7 = ''.join(rand.choice('0123456789') for x in range(7))
    tm = datetime.datetime.now().strftime('%Y%m%d%H%I%S')
    return '%s%s' % (tm,rand7)

class ImagePreviewInput(FileInput):
    def value_from_datadict(self, data, files, name):
        imagedata = data.get(name + '-data',None)
        value = {}
        if imagedata and imagedata[:5] == 'data:':

            realdata = imagedata.split(';')[1][7:]
            ext='jpeg'
            image = Image.open(io.BytesIO(base64.b64decode(realdata)))
            if image.mode == 'RGBA':
                ext='png'
            content = io.BytesIO()
            image.save(content, ext.upper(), quality=70)
        
            file_name = u'{}.{}'.format(generate_tradeno(), ext)
            
            files = {name:InMemoryUploadedFile(content, None, file_name, 'image/' + ext, len(content.getvalue()), None)}
            if hasattr(content, 'seek') and callable(content.seek):
                content.seek(0)
        return super(ImagePreviewInput, self).value_from_datadict(data, files, name)
        
    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['accept'] = "image/*"
        base = super(ImagePreviewInput, self).render(name, value, attrs)
        valuedata=''
        photourl = u'%s%s' % ( settings.STATIC_URL, 'buyusa.png') # default
        if value and hasattr(value,'url'):
            photourl = value.url
            valuedata = photourl
        if value and type(value) == InMemoryUploadedFile:
            value.file.seek(0)
            valuedata = "data:%s;base64,%s" % (value.content_type,base64.b64encode(value.file.read()).decode('utf-8'))
            photourl = valuedata
        return mark_safe(base+u"""
        <div class="docs-preview clearfix">
            <img id="%(name)s-preview" src="%(photourl)s" style="width:150px"/>
            <input type="hidden" id="%(name)s-data" name="%(name)s-data" value="%(valuedata)s">
        </div>
        <script>
        $(function () {
        $("#id_%(name)s").change(function () {
          if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
              $("#%(name)s-preview").attr("src", e.target.result);
              $("#%(name)s-data").val(e.target.result);
            }
            reader.readAsDataURL(this.files[0]);
          }
        });
        });
        </script>
        """ % {'name':name,'photourl':photourl,'valuedata':valuedata})