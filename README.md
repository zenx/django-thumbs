# django-thumbs
Lightweight Django application for generating thumbnails for your `ImageField` fields.

## Thumbnails in 10 seconds
1. Add  `django_thumbs` to the `INSTALLED_APPS` setting
2. Replace your `ImageField` with a `ImageWithThumbsField` and define a `sizes` attribute.

*models.py*

    from django_thumbs.fields import ImageWithThumbsField
   
    THUMBNAIL_SIZES = ((125,125), (300,200), (640, 0))
   
    class MyModel(models.Model):
        image = ImageWithThumbsField(upload_to='images/', sizes=THUMBNAIL_SIZES)

### Generate thubmnails for existing images

You can change back to `ImageField` anytime.


## Features

* Seamlessly integration with your existing `ImageField`'s
* Works perfectly with any `StorageBackend` such as Amazon S3
* Generates thumbnails just after image is uploaded into memory
* Deletes related thumbnails when the image file is deleted
* Provides easy access to the thumbnails' URLs (similar method as with ImageField)
* Seamlessly integration with your existing `ImageFields`

## Installation

1. Import it in your models.py and replace `ImageField` with `ImageWithThumbsField`.
2. Add a `sizes` attribute with a list of sizes you want to use for the thumbnails
3. Make sure your have defined `MEDIA_ROOT` and `MEDIA_URL` in your `settings.py`

That's it!

## Usage

Replace your `ImageField` with a `ImageWithThumbsField` and define a `sizes` attribute.
You can change back to `ImageField` anytime.


*models.py*

    from django.db import models
    from django_thumbs.fields import ImageWithThumbsField

    class Person(models.Model):
        photo = ImageWithThumbsField(upload_to='images', sizes=((125,125), (300,200), (640, 0))
        second_photo = ImageWithThumbsField(upload_to='images')


In this example we have a Person model with 2 image fields.

You can see the field second_photo doesn't have a sizes attribute. This field works exactly the same way as a normal ImageField.
The field photo has a sizes attribute specifying desired sizes for the thumbnails. This field works the same way as ImageField but it also creates the desired thumbnails when uploading a new file and deletes the thumbnails when deleting the file.
With ImageField you retrieve the URL for the image with: someone.photo.url With ImageWithThumbsField you retrieve it the same way. You also retrieve the URL for every thumbnail specifying its size: In this example we use someone.photo.url_125x125 and someone.photo.url_200x200 to get the URL of both thumbnails.

If you set width or height to `0` django-thumbs will resize adjusting the size to the only size different than `0`.

## Uninstall

At any time you can go back and use ImageField again without altering the database or anything else. Just replace ImageWithThumbsField with ImageField again and make sure you delete the sizes attribute. Everything will work the same way it worked before using django-thumbs. Just remember to delete generated thumbnails in the case you don't want to have them anymore.
