# -*- encoding: utf-8 -*-
"""
    django-thumbs by Antonio Melé
    http://antoniomele.es
    http://django.es

    extended by Daniel Vera Rodríguez
    https://github.com/daniel-vera-rguez
"""
# project
from django_thumbs.management.utils import ThumbsCommand


class Command(ThumbsCommand):
    help = "Creates desired thumbnails for "
    "specified applications [AppName ...], models [AppName.ModelName ...] "
    "or specific fields [AppName.ModelName.FieldName ...]."

    def action(self, image_field, sizes):
        image_field.create_thumbs(sizes=sizes, method='regenerate')
