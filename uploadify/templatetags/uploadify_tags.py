from django import template
from django.template import resolve_variable
from django.utils import simplejson

from uploadify import settings

register = template.Library()

# -----------------------------------------------------------------------------
#   multi_file_upload
# -----------------------------------------------------------------------------
class MultiFileUpload(template.Node):
    def __init__(self, sender='"uploadify"', unique_id=None, data=None, **kwargs):
        self.sender = sender
        self.unique_id = unique_id
        self.data = data or {}
        self.options = kwargs
       
    def render(self, context):
        if self.unique_id is not None:
            unique_id = "?unique_id=%s" % str(resolve_variable(self.unique_id, context))
        else:
            unique_id = ""

        options = {'fileDataName': 'Filedata'}
        for key, value in self.options.items():
            options[key] = resolve_variable(value, context)
        js_options = ",".join(map(lambda item: "'%s': '%s'" % (item[0], item[1]),
                                  options.items()))

        auto = options.get('auto', False)
        
        data = {
            'fileDataName': options['fileDataName'],
            'sender': str(resolve_variable(self.sender, context)),
        }
        for key, value in self.data.items():
            data[key] = resolve_variable(value, context)

        context.update({
            'uploadify_query': unique_id,
            'uploadify_data': simplejson.dumps(data)[1:-1],
            'uploadify_path': settings.UPLOADIFY_PATH,
            'uploadify_version': settings.UPLOADIFY_VERSION,
            'uploadify_options': js_options,
            'uploadify_filename': options['fileDataName'],
            'uploadify_auto': auto,
        })

        t = template.loader.get_template('uploadify/multi_file_upload.html')
        return t.render(context)


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
