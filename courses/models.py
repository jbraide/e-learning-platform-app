from django.db import models
from django.contrib.auth.models import User

# creating a model to support multiple content 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# custom model Field
from .fields import OrderField

class Subject(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    class Meta: 
        ordering = ['title', ]

    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
    User, 
    related_name='course_joined',
    blank=True)

    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Specify the ordering w.r.t the Course object
    order = OrderField(blank=True, for_fields=['course'])

    class Meta: 
        ordering = ['order']

    def __str__(self):
            return f'{self.order}. {self.title}'


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        limit_choices_to={
            'model__in':(
                'text', 
                'video',
                'file', 
                'image')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    # Here order is calculated w.r.t Module Field
    order = OrderField(blank=True, for_fields=['modeule'])

    class Meta: 
            ordering = ['order']

# for using the render() method 
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

class ItemBase(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_related')
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title
    
    # this method uses render_to_string() f&n for rendering a 
    # template and return the render content as a string
    def render(self):
        return render_to_string('course/content/{}.html'.format(self._meta_model_name), {'item': self})

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    image = models.ImageField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()


