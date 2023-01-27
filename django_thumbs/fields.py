# -*- encoding: utf-8 -*-
"""
    django-thumbs by Antonio Melé
    http://antoniomele.es
    http://django.es
"""
import io
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from .utils import generate_thumbnail


class ImageWithThumbsFieldFile(ImageFieldFile):
    """
    See ImageWithThumbsField for usage example.
    """
    def __init__(self, *args, **kwargs):
        super(ImageWithThumbsFieldFile, self).__init__(*args, **kwargs)

        if self.field.sizes:
            def get_size(self, size):
                if not self:
                    return ''
                else:
                    split = self.url.rsplit('.',1)
                    thumb_url = '%s.%sx%s.%s' % (split[0],w,h,split[1])
                    return thumb_url

            try:
                for size in self.field.sizes:
                    (w,h) = size
                    setattr(self, 'url_%sx%s' % (w,h), get_size(self, size))
            except:
                # s3 storage and other storages problem
                pass
        # get the custom thumbnailing function if available or use the default one
        self.thumbnail_function = getattr(self.field, 'thumbnail_function', generate_thumbnail)

    def save(self, name, content, save=True):
        super(ImageWithThumbsFieldFile, self).save(name, content, save)
        if self.field.sizes:
            self.create_thumbs(content=content)

    def delete(self, save=True):
        name=self.name
        self.delete_thumbs()
        super(ImageWithThumbsFieldFile, self).delete(save)

    def create_thumbs(self, content=None, sizes=None, method='new'):
        """
            method can be:
                new         New thumbs are created (creates all thumbnails only if they don't exist, raises exception if a file that has to be created already exists)
                missing     Only missing thumbs will be created (creates just thumbnails that don't exist yet and lets the existing thumbnails intact)
                regenerate  All thumbs will be regenerated (overwirtes all existing thumbnails)
        """
        if content == None:
            content = io.BytesIO(self.storage.open(self.name, 'rb').read())

        if sizes == None:
            sizes = self.field.sizes

        if sizes:
            for size in sizes:
                (w,h) = size
                
                split = self.name.rsplit('.',1)
                
                # for example: 180x.jpg or x180.jpg or 200x180.jpg
                thumb_name = '%s.%sx%s.%s' % (split[0],w,h,split[1])
                
                if method == 'regenerate':
                    if self.storage.exists(thumb_name):
                        self.delete(thumb_name)
                        
                elif method == 'new':
                    if self.storage.exists(thumb_name):
                        raise ValueError('There is already a file named %s' % thumb_name)
                
                if not self.storage.exists(thumb_name):
                    # you can use another thumbnailing function if you like but it has to return a ContentFile object with the thumbnail
                    thumb_content = self.thumbnail_function(content, size, split[1])
                    thumb_name_ = self.storage.save(thumb_name, thumb_content)    
                        
                    """
                        if not thumb_name == thumb_name_:
                            raise ValueError('There is already a file named %s' % thumb_name)
                    """

    def delete_thumbs(self, sizes=None):
        # deletes thumbnails of the desired sizes
        if sizes==None:
            # if not sizes given delete thumbnails of ALL sizes
            sizes = self.field.sizes
        
        if sizes != None:
            for size in sizes:
                (w,h) = size
                split = self.name.rsplit('.',1)
                thumb_name = '%s.%sx%s.%s' % (split[0],w,h,split[1])
                try:
                    self.storage.delete(thumb_name)
                except:
                    pass


class ImageWithThumbsField(ImageField):
    attr_class = ImageWithThumbsFieldFile
    """
    Usage example:
    ==============
    photo = ImageWithThumbsField(upload_to='images', sizes=((125,125),(300,200),)
    
    To retrieve image URL, exactly the same way as with ImageField:
        my_object.photo.url
    To retrieve thumbnails URL's just add the size to it:
        my_object.photo.url_125x125
        my_object.photo.url_300x200
    
    Note: The 'sizes' attribute is not required. If you don't provide it, 
    ImageWithThumbsField will act as a normal ImageField
        
    How it works:
    =============
    For each size in the 'sizes' atribute of the field it generates a 
    thumbnail of that size and stores it following this format:
    
    available_filename.[width]x[height].extension

    Where 'available_filename' is the available filename returned by the storage
    backend for saving the original file.
    
    Following the usage example above: For storing a file called "photo.jpg" it saves:
    photo.jpg          (original file)
    photo.125x125.jpg  (first thumbnail)
    photo.300x200.jpg  (second thumbnail)
    
    With the default storage backend if photo.jpg already exists it will use these filenames:
    photo_.jpg
    photo_.125x125.jpg
    photo_.300x200.jpg
    
    Note: django-thumbs assumes that if filename "any_filename.jpg" is available 
    filenames with this format "any_filename.[widht]x[height].jpg" will be available, too.
    
    Methods:
    ========
    All this methods take an optional "sizes" attribute to specify which sizes to create/delete/regenerate.
    If no sizes are given the "sizes" specified in the model field are used.
    
    my_object.photo.create_thumbs(sizes=((120,120),))
    my_object.photo.create_missing_thumbs()
    my_object.photo.regenerate_thumbs()
    my_object.photo.delete_thumbs()
    
    Management commands:
    ====================
    These commands can be used with manage.py of your project in order to create/delete/regenerate thumbnails in bulk.
    
    create-thumbs
    =============
    Requires at least 1 item as input. Creates the thumbnails for the specified item.
    The item can be an app, a app.model or a app.model.field: manage.py create-thumbs app1 app2
    
    Examples:
    ---------
    Create all thumbs for all models of apps app1 and app2: manage.py create-thumbs app1 app2 --method=new
    Regenerate all thumbnails for an app: manage.py create-thumbs app1 --method=regenerate
    manage.py create-thumbs app1.my_model app2 --method=missing --sizes=120x120,600x400
    manage.py create-thumbs app1.my_model app2 --method=missing --sizes=120x120,600x400
    
    delete-thumbs
    =============
    
    Takes the same arguments as create-thumbnails
    
    Examples:
    ---------
    
    To do:
    ======
    - Create an admin widget to show current thumbnail
    
    """
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, sizes=None, **kwargs):
        self.verbose_name=verbose_name
        self.name=name
        self.width_field=width_field
        self.height_field=height_field
        self.sizes = sizes
        super(ImageField, self).__init__(**kwargs)
