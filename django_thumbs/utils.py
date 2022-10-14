# -*- encoding: utf-8 -*-
"""
    django-thumbs by Antonio Melé
    http://antoniomele.es
    http://django.es
"""
from PIL import Image
from django.core.files.base import ContentFile
try:
    from io import StringIO
except:
    from cStringIO import StringIO


def generate_thumbnail(img, thumb_size, format):
    """
    Generates a thumbnail image and returns a ContentFile object with the thumbnail
    
    Parameters:
    ===========
    img         File object
    
    thumb_size  desired thumbnail size, ie: (200,120)
    
    format      format of the original image ('jpeg','gif','png',...)
                (this format will be used for the generated thumbnail, too)
    """
    
    img.seek(0) # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(img)
    
    # convert to RGB if necessary
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')
        
    # get size
    thumb_w, thumb_h = thumb_size
    
    # If you want to generate a square thumbnail
    xsize, ysize = image.size
    
    if thumb_w == thumb_h and xsize != ysize:
        # quad
        # get minimum size
        minsize = min(xsize,ysize)
        # largest square possible in the image
        xnewsize = (xsize-minsize)/2
        ynewsize = (ysize-minsize)/2
        # crop it
        image = image.crop((xnewsize, ynewsize, xsize-xnewsize, ysize-ynewsize))
        # load is necessary after crop                
        image.load()
        # thumbnail of the cropped image (with ANTIALIAS to make it look better)
        image.thumbnail(thumb_size, Image.ANTIALIAS)
    else:
        # If fixed width and proportional height
        if thumb_h == 0:
            wpercent = float(thumb_w)/float(xsize)
            thumb_h = int(ysize*wpercent)
        
        # If fixed height and proportional width
        if thumb_w == 0:
            hpercent = float(thumb_h)/float(ysize)
            thumb_w = int(xsize*hpercent)
        
        else:
            x1 = y1 = 0
            x2, y2 = image.size

            w_ratio = 1.0 * x2/thumb_w
            h_ratio = 1.0 * y2/thumb_h

            if h_ratio > w_ratio:
                y1 = int(y2/2-thumb_h*w_ratio/2)
                y2 = int(y2/2+thumb_h*w_ratio/2)
            else:
                x1 = int(x2/2-thumb_w*h_ratio/2)
                x2 = int(x2/2+thumb_w*h_ratio/2)
            image = image.crop((x1,y1,x2,y2))
            image.load()
            
        # not quad
        image.thumbnail((thumb_w, thumb_h), Image.ANTIALIAS)
        
        # resize small images
        w, h = image.size
        if xsize < thumb_w or ysize < thumb_h:
            image = image.resize((thumb_w, thumb_h))
            image.load()
                
        
    io = StringIO()
    # PNG and GIF are the same, JPG is JPEG
    if format.upper()=='JPG':
        format = 'JPEG'
    
    image.save(io, format)
    return ContentFile(io.getvalue())
