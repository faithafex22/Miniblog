from django.db import models

# Create your models here.
import uuid
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class DeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)
    


class Blogger(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=10, null=True)
    phone_no = models.IntegerField( null=True)
    
    @property
    def posts(self):
        return Post.active_objects.filter(blogger_id=self.pk)
    
    class Meta:
        ordering = ['first_name', 'last_name', ]
        
    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
 
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    
    @property
    def posts(self):
        return Post.active_objects.filter(category_id=self.pk)
    
    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
      return reverse('category-detail', args=[str(self.id)]) 
    
    
class Post(models.Model):
    
    #ACTIVE = 'active'
    #DRAFT = 'draft'
    
    #CHOICES_STATUS = (
        #(ACTIVE, 'Active'),
        #(DRAFT, 'Draft')
    #)
    
    blogger = models.ForeignKey(Blogger, on_delete = models.SET_NULL, null=True)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE )
    title = models.CharField(max_length=200)
    intro = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    is_active = models.BooleanField(default=True)
    
    #@property
    #def posts(self):
        #return Post.active_objects
 
    objects = models.Manager()
    active_objects = ActiveManager()
    deleted_objects = DeleteManager()
    

    def comment(self):
        return Comment.active_objects.filter(post_id=self.pk)
    
    class Meta:
        ordering = ('-created_at',)
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])
    
        
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE )
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()
    deleted_objects = DeleteManager()
    
    #@property
    #def comments(self):
        #return Comment.active_objects
 
 
    class Meta:
        ordering = ('-created_at',) 
        
    def __str__(self):
        return self.name
        