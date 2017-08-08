# -*- encoding: utf-8 -*-
"""
    django-thumbs by Antonio Melé
    http://zenx.es
    http://django.es

    extended by Daniel Vera Rodríguez
    https://github.com/daniel-vera-rguez
"""
# project
from django_thumbs.management.utils import ThumbsCommand


class Command(ThumbsCommand):
    help = "Deletes desired thumbnails for "
    "specified applications [appname ...], models [appname.modelname ...] "
    "or specific fields [appname.modelname.fieldname ...]."

    def action(self, image_field, sizes):
        image_field.delete_thumbs(sizes=sizes)


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
