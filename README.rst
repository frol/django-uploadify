Works on Django >= 1.2 <= 1.6. Note that there is support of different Uploadify versions and UploadiFive.

django-uploadify
================

A "Django":http://www.djangoproject.com/ re-usable app to integrate "Uploadify and UploadiFive":http://www.uploadify.com/.

.. contents::

Installation
============

Installing django-uploadify
---------------------------

#) Install package ::

    pip install git+git://github.com/frol/django-uploadify.git

#) Add 'uploadify' to your INSTALLED_APPS in your project's settings.py file
#) There is support of Uploadify 2 (default), Uploadify 3 and UploadiFive v1.1.1. You can decide what version you would like to use by settings option UPLOADIFY_VERSION, available values are 2 (just int), 3 (just int) and 'uploadifive'.
#) Add a reference to uploadify in your urls.py... ::

    (r'^uploadify/', include('uploadify.urls')),


Installing Uploadify
--------------------

.. _Download uploadify: http://www.uploadify.com/
#) "`Download uploadify`_"
#) Copy all of the 'uploadify' folder from the Uploadify distribution into your media root.  Default is: MEDIA_URL\js\uploadify\
#) Rename the uploadify file from "jquery.uploadify.v2.1.0.min.js" (or whatever version it is) to simply "jquery.uploadify.js"
#) In uploadify/settings.py, make sure the setting UPLOADIFY_PATH is set to the correct value if the uploadify folder is installed to a location other than the default.  Note that the UPLOADIFY_PATH setting is relative to the MEDIA_URL value.

Requrements
-----------

* django >= 1.2
.. _django-misc: https://github.com/ilblackdragon/django-misc/
* django-misc_ - application with a lot of useful stuff

Using django-uploadify
======================

How It Works
------------

Django-uploadify works by providing a template tag, {% multi_file_upload <upload_complete_url> %}., which takes a single parameter.  The template tag will render the Uploadify jquery/flash multi-file upload interface on the page.  A user may operate Uploadify, selecting and uploading multiple files.  For each file that is uploaded a Django signal will be fired, containing the file data.  After all uploads have been completed, the template tag will use the value of 'upload_complete_url'.  It will fetch that page via AJAX, and replace the Uploadify GUI with the contents of the page (a jQuery $.load).

Code Examples
-------------

To insert the django-uploadify template tag... ::
    
    {% load uploadify_tags %}{% multi_file_upload '/your/url/upload/complete/' %}

To add custom parameters to uploadify... ::
    
    {% multi_file_upload '/your/url/upload/complete/' unique_id=someobj.id auto=1 %}

Creating a signal receiver... ::

    def upload_received_handler(sender, request, data, **kwargs):
        if data:
            # process the received file here
            try:
                related_obj = SomeObj.objects.get(id=request.GET.get('unique_id'), owner=request.user)
            except SomeObj.DoesNotExist:
                return {'status': 'failed', 'status_msg': 'SomeObj not found'}
            Media = Media.objects.create(image=data)
            return {'status': 'ok', 'url': photo.get_preview_url()}
        raise Http404

    upload_received.connect(upload_received_handler, dispatch_uid='yourapp.whatever.upload_received')


Reference
=========

Client Side Event:  allUploadsComplete
--------------------------------------
On the client side, a javascript event is provided to capture when all uploads have been completed.  It can be bound with the following jQuery code: ::

    $('#uploadify').bind('allUploadsComplete', function(e, data){
         // This code executes on AllUploadsComplete event...
    }

upload_complete_url Parameter
-----------------------------
When this page is fetched by the client-side javascript, the following Uploadify values are POST'ed to it:
* filesUploaded - The total number of files uploaded
* errors - The total number of errors while uploading
* allBytesLoaded - The total number of bytes uploaded
* speed - The average speed of all uploaded files
