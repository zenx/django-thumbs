# -*- encoding: utf-8 -*-
"""
    django-thumbs by Antonio Melé
    http://antoniomele.es
    http://django.es
"""
from django.core.management.base import LabelCommand
from optparse import make_option

class Command(LabelCommand):
    help = "Creates desired thumbnails for specified applications [appname ...], models [appname.modelname ...] or specific fields [appname.modelname.fieldname ...]."
    args = "[appname ...]"
    label = 'app name'
    
    option_list = LabelCommand.option_list + (
        make_option('--sizes', dest='sizes', help='Lets you specify the sizes you want to create. i.e: --sizes=120x120,50x20. If not provided django-thumbs will generate thumbnails for the sizes you have specified in each ImageWithTumbsField.'),
    )
    
    def process_field(self, model, field, sizes=None):
        if hasattr(field,"sizes") and type(field).__name__ == 'ImageWithThumbsField':
            for obj in model.objects.all():
                image_field = getattr(obj, field.attname)
                if image_field:
                    image_field.create_thumbs(sizes=sizes, method='regenerate')
    
    def handle_label(self, element, **options):
        from django.db.models import get_models, get_model, get_app
        
        raw_sizes = options.get('sizes', None)
        
        if raw_sizes != None:
            raw_sizes = raw_sizes.split(',')
        
            sizes = []
            for size in raw_sizes:
                (w,h) = size.split('x')
                sizes.append((w,h))
        else:
            sizes = None
            
        model_name = None
        field_name = None
        things = element.split('.')
        length = len(things)
        
        if length == 3:
            (app, model_name, field_name) = things
        elif length == 2:
            (app, model_name) = things
        elif length == 1:
            app = things[0]
        
        app = get_app(app)
        
        if model_name == None:
            # No model given, delete all thumbs of the app
            for model in get_models(app):
                for field in model._meta.fields:
                    self.process_field(model, field, sizes)
        
        elif field_name == None:
            # No field given, delete all thumbs of the model
            model = get_model(app, model_name)
            for field in model._meta.fields:    
                self.process_field(model, field, sizes)
                
        else:
            # Delete all thumbs of the field
            model = get_model(app, model_name)
            field = model._meta.get_field(field_name)
            self.process_field(model, field, sizes)
                
        print 'All thumbs for "%s" created' % element
                       