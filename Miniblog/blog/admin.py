from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Post, Comment, Category, Blogger

# Register your models here.

class PostInline(admin.TabularInline):
    model = Post
    extra = 0

class BloggerAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email',  'first_name', 'last_name', 'phone_no' )
    
    fields = ['first_name', 'last_name', 'username', 'password', 'email', 'phone_no'] 
    
    inlines = [PostInline]
admin.site.register(Blogger, BloggerAdmin )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comment', 'post')
    
admin.site.register(Comment, CommentAdmin)

class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline]
admin.site.register(Category, CategoryAdmin)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display =('title', 'blogger', 'category', 'created_at')
    inlines = [CommentInline]

admin.site.register(Post, PostAdmin)