# -*- encoding: utf-8 -*-
"""
    django-thumbs by Antonio Melé
    http://antoniomele.es
    http://django.es

    extended by Daniel Vera Rodríguez
    https://github.com/daniel-vera-rguez
"""
# django
from django.core.management.base import LabelCommand, CommandError


class ThumbsCommand(LabelCommand):
    label = 'AppName[.ModelName[.FieldName]]'

    @staticmethod
    def _get_specific_sizes(raw_sizes):
        if raw_sizes is not None:
            raw_sizes = raw_sizes.split(',')
            sizes = []
            for size in raw_sizes:
                (w, h) = size.split('x')
                sizes.append((int(w), int(h)))
        else:
            sizes = None
        return sizes

    def add_arguments(self, parser):
        parser.add_argument(
            '-s', '--sizes', dest='sizes',
            help="Lets you specify the sizes you want to create. "
                 "i.e: --sizes=120x120,50x20. "
                 "If not provided django-thumbs will generate thumbnails "
                 "for the sizes you have specified "
                 "in each 'ImageWithTumbsField'.")

    def action(self, image_field, sizes):
        """
        Perform the command's action.
        """
        raise NotImplementedError(
            "Subclasses of ThumbsCommand must provide an action() method.")

    def process_field(self, model, field, sizes=None):
        from django_thumbs.fields import ImageWithThumbsField

        sizes = sizes if sizes else getattr(field, 'sizes', None)
        if sizes and isinstance(field, ImageWithThumbsField):
            for obj in model.objects.all():
                image_field = getattr(obj, field.attname)
                if image_field:
                    self.action(image_field, sizes=sizes)

    def parse_element_path(self, element):
        from django.apps import apps

        model_name = None
        field_name = None
        things = element.split('.')
        length = len(things)
        if length == 3:
            (app_label, model_name, field_name) = things
        elif length == 2:
            (app_label, model_name) = things
        elif length == 1:
            app_label = things[0]
        else:
            raise ValueError(
                "'{0}' hasn't format {1}".format(element, self.label))

        try:
            app = apps.get_app_config(app_label)
        except (LookupError, ImportError) as e:
            raise CommandError(
                "%s. Are you sure your INSTALLED_APPS setting is correct?" % e)

        return app, model_name, field_name

    def handle_label(self, element, **options):
        app, model_name, field_name = self.parse_element_path(element)
        sizes = self._get_specific_sizes(options.get('sizes', None))

        if model_name is None:
            # No model given, create all thumbs of the app
            for model in app.get_models():
                for field in model._meta.fields:
                    self.process_field(model, field, sizes)

        elif field_name is None:
            # No field given, create all thumbs of the model
            model = app.get_model(model_name)
            for field in model._meta.fields:
                self.process_field(model, field, sizes)

        else:
            # Create all thumbs of the field
            model = app.get_model(model_name)
            field = model._meta.get_field(field_name)
            self.process_field(model, field, sizes)

        print 'All thumbs for "%s" processed' % element
