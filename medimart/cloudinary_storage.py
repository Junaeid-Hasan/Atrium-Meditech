"""
Custom Cloudinary storage backend for Django 5+ compatibility.
Replaces django-cloudinary-storage which is not maintained for Django 5+.
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.core.files.storage import Storage
from django.conf import settings
from django.utils.deconstruct import deconstructible


@deconstructible
class CloudinaryMediaStorage(Storage):
    """
    A Django Storage backend that uploads media files to Cloudinary.
    Works with Django 5.0+ STORAGES configuration.
    """

    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'),
            api_key=settings.CLOUDINARY_STORAGE.get('API_KEY'),
            api_secret=settings.CLOUDINARY_STORAGE.get('API_SECRET'),
            secure=True,
        )

    def _save(self, name, content):
        # Remove extension from name since Cloudinary manages it
        public_id = name.rsplit('.', 1)[0]
        response = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            overwrite=True,
            resource_type='auto',
        )
        return response['public_id'] + '.' + response['format']

    def _open(self, name, mode='rb'):
        raise NotImplementedError("CloudinaryMediaStorage does not support opening files.")

    def delete(self, name):
        public_id = name.rsplit('.', 1)[0]
        cloudinary.uploader.destroy(public_id)

    def exists(self, name):
        try:
            public_id = name.rsplit('.', 1)[0]
            cloudinary.api.resource(public_id)
            return True
        except cloudinary.exceptions.NotFound:
            return False

    def url(self, name):
        public_id = name.rsplit('.', 1)[0]
        return cloudinary.CloudinaryImage(public_id).build_url(secure=True)

    def size(self, name):
        public_id = name.rsplit('.', 1)[0]
        resource = cloudinary.api.resource(public_id)
        return resource.get('bytes', 0)
