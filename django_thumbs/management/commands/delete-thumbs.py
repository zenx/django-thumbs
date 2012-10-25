# -*- encoding: utf-8 -*-
"""
    django-thumbs by Antonio Melé
    http://zenx.es
    http://django.es
"""
from django.core.management.base import LabelCommand
from optparse import make_option

class Command(LabelCommand):
    help = "Deletes desired thumbnails for specified applications [appname ...], models [appname.modelname ...] or specific fields [appname.modelname.fieldname ...]."
    args = "[appname ...]"
    label = 'app name'
    
    
    option_list = LabelCommand.option_list + (
        make_option('--sizes', dest='sizes', help='Lets you specify the sizes you want to delete. i.e: --sizes=120x120,50x20'),
    )
    
    def process_field(self, model, field, sizes=None):
        if hasattr(field,"sizes") and type(field).__name__ == 'ImageWithThumbsField':
            for obj in model.objects.all():
                image_field = getattr(obj, field.attname)
                if image_field:
                    image_field.delete_thumbs(sizes=sizes)
    
    def handle_label(self, element, **options):
        from django.db.models import get_models, get_model
        
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
                
        print 'All thumbs for "%s" deleted' % element


"""
class Command(AppCommand):
    help = "Deletes desired thumbnails for specified applications."
    args = "[appname ...]"
    
    option_list = AppCommand.option_list + (
        
        make_option('--sizes', default='all', dest='sizes',
        help='Lets you specify the sizes you want to delete.'),
        
    )
    
    def handle_app(self, app, **options):
        from django.db.models import get_models
        
        # check all models of the app
        for model in get_models(app):
            for field in model._meta.fields:
                if hasattr(field,"sizes") and type(field).__name__ == 'ImageWithThumbsField':
                    for obj in model.objects.all():
                        image_field = getattr(obj, field.attname)
                        if image_field:
                            image_field.delete_thumbs()
            
        #print 'All thumbs %s application deleted'
"""
                    
"""
class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option('--sizes', default='all', dest='sizes',
        help='Lets you specify the sizes you want to delete.'),
    )
    
    
    help = "Deletes desired thumbnails."
    args = '((120,120),(200,100), ...)'
    
    def handle(self, *sizes, **options):
        # deletes ALL thumbnails for a project
        from django.db.models import get_app, get_apps, get_models
        
        for app in get_apps():
            for model in get_models(app):
                for field in model._meta.fields:
                    if hasattr(field,"sizes") and type(field).__name__ == 'ImageWithThumbsField':
                        
                        field.attr_class().delete_thumbs()
                        #field.attr_class(field, field, file).delete_thumbs()
                        #getattr(field, field.attname).delete_thumbs()
                        #getattr(field._file,"delete_thumbs")
"""                            