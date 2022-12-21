from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name='index') ,
  path('posts/', views.PostListView.as_view(), name='posts'),
  path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
  path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
  path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),
  path('categories/', views.CategoryListView.as_view(), name='categories'),
  path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
  path('post/<int:pk>/comment', views.PostCommentCreate.as_view(), name='post-comment'),
  path('blogger/<int:pk>/create_post', views.PostCreate.as_view(), name='post-create'),
  path('post/<int:pk>/update/', views.PostUpdate.as_view(), name='post-update'),
  path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),
  path("post/inactive/", views.InactivePostView.as_view(), name="inactive-posts"),
  path("post/inactive/<int:pk>/restore/", views.RestorePost, name="restore-post"),
]