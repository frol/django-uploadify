from django.conf import settings as django_settings
from django.template import Node, resolve_variable
from django.template.loader import render_to_string
from django.utils import simplejson

if 'coffin' in django_settings.INSTALLED_APPS:
    from coffin.template import Library
    is_coffin = True
else:
    from django.template import Library
    is_coffin = False

from uploadify import settings

register = Library()

# -----------------------------------------------------------------------------
#   multi_file_upload
# -----------------------------------------------------------------------------
class MultiFileUpload(Node):
    def __init__(self, sender='"uploadify"', unique_id=None, data=None, **kwargs):
        self.sender = sender
        self.unique_id = unique_id
        self.data = data or {}
        self.options = kwargs

    def build_context(self, unique_id, data, options, auto):
        return {
            'uploadify_query': ("?unique_id=%s" % unique_id) if unique_id else "",
            'uploadify_data': simplejson.dumps(data)[1:-1],
            'uploadify_path': settings.UPLOADIFY_PATH,
            'uploadify_version': settings.UPLOADIFY_VERSION,
            'uploadify_options': ','.join(("'%s': %s" % (item[0], item[1])
                                            for item in options.items())),
            'uploadify_filename': options['fileDataName'],
            'uploadify_auto': auto,
        }

    def render(self, context):
        if self.unique_id is not None:
            unique_id = "?unique_id=%s" % str(resolve_variable(self.unique_id, context))

        options = {'fileDataName': 'Filedata'}
        for key, value in self.options.items():
            options[key] = resolve_variable(value, context)

        auto = options.get('auto', False)
        
        data = {
            'fileDataName': options['fileDataName'],
            'sender': str(resolve_variable(self.sender, context)),
        }
        for key, value in self.data.items():
            data[key] = resolve_variable(value, context)

        options['fileDataName'] = '"%s"' % options['fileDataName']
        context.update(self.build_context(unique_id, data, options, auto))

        return render_to_string('uploadify/multi_file_upload.html', context)


@register.tag
def multi_file_upload(parser, token):
    """
    Displays a Flash-based interface for uploading multiple files.
    For each POST request (after file upload) send GET query with `unique_id`.

    {% multi_file_upload sender='SomeThing' fileDataName='Filename' %}

    For all options see http://www.uploadify.com/documentation/

    """
    args = token.split_contents()
    tag_name = args[0]
    args = args[1:]

    options = {}
    for arg in args:
        name, val = arg.split("=")
        val = val.replace('\'', '').replace('"', '')
        options[name] = val

    return MultiFileUpload(**options)


if is_coffin:
    from coffin.template.loader import render_to_string as coffin_render_to_string
    from jinja2 import Markup

    @register.object
    def multi_file_upload(request, sender='uploadify', unique_id=None, data=None, **options):
        """
        Jinja2 tag.

        Displays a Flash-based interface for uploading multiple files.
        For each POST request (after file upload) send GET query with `unique_id`.

        {{ multi_file_upload(request, sender='SomeThing', fileDataName='Filename') }}

        For all options see http://www.uploadify.com/documentation/
        """
        if 'fileDataName' not in options:
            options['fileDataName'] = 'Filedata'

        auto = options.get('auto', False)
        
        _data = {
            'fileDataName': options['fileDataName'],
            'sender': sender,
        }
        if data:
            _data.update(data)

        options['fileDataName'] = '"%s"' % options['fileDataName']
        multi_file_upload = MultiFileUpload(sender, unique_id, data, **options)
        return Markup(coffin_render_to_string('uploadify/multi_file_upload.html',
            dict(multi_file_upload.build_context(unique_id, _data, options, auto), request=request)))
