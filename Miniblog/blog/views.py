from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import get_object_or_404, redirect, render 
from django.shortcuts import HttpResponseRedirect

from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DeleteView, UpdateView, View

from .forms import CommentForm
from .models import Blogger, Category, Comment, Post


def index(request):
    num_post = Post.objects.all().count()
    num_blogger= Blogger.objects.all().count()
    num_category = Category.objects.all().count()
    num_comment= Comment.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_post': num_post,
        'num_blogger': num_blogger,
        'num_category': num_category,
        'num_comment': num_comment,
        'num_visits': num_visits,
        }
    
    #rendering html template with the data in the context
    return render(request, 'index.html', context=context)

class PostListView(generic.ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/post_list.html'
    queryset = Post.objects.all()
    
class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 5
    context_object_name = 'category_list'
    template_name = 'blog/category_list.html'
    queryset = Category.objects.all()
        
        
class PostDetailView(generic.DetailView):
   model = Post
   template_name = 'blog/post_detail.html'
   
class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'blog/category_detail.html'
    
class BloggerListView(generic.ListView):
    model = Blogger
    paginate_by = 5
    context_object_name = 'blogger_list'
    #your own name for the list as a template variable
    queryset = Blogger.objects.all()
    
    template_name = 'blog/blogger_list.html'
    
class BloggerDetailView(generic.DetailView):
    model = Blogger
    template_name = 'blog/blogger_detail.html'
    
#    
#
#@login_required()
#def comment(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    
#    if request.method == 'POST':
#        form = CommentForm(request.POST)
#        if form.is_valid():
#            comment = form.save(commit=False)
#            comment.post = post
#            comment.name = request.user
#            comment.save()
#            
#            return redirect('post-detail', pk=post.pk)
#    else:
#        form = CommentForm()
#    return render(request, 'blog/comment_form.html', {'post':post, 'form':form})

#or use
class PostCommentCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a blog comment. Requires login. 
    """
    model = Comment
    fields = ['name', 'email', 'comment']

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(PostCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(Post, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        #Add logged-in user as author of comment
        form.instance.author = self.request.user
        #Associate comment with blog based on passed id
        form.instance.post=get_object_or_404(Post, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(PostCommentCreate, self).form_valid(form)

    def get_success_url(self): 
        """
        After posting comment return to associated blog.
        """
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk'],})
    
    
# Create your views here.



class PostCreate(PermissionRequiredMixin,CreateView):
    model = Post
    fields = ['blogger', 'category', 'title', 'intro', 'body']
    
    permission_required = 'post.create'
     

class PostUpdate(PermissionRequiredMixin,UpdateView):
    model = Post
    fields = ['blogger', 'category', 'title', 'intro', 'body', 'status']
    permission_required = 'post.update'

class PostDelete(PermissionRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('posts')
    permission_required = 'post.delete'
    
class InactivePostView(generic.ListView):
    model = Post
    context_object_name = 'inactive_post_list'
    template_name = 'blog/inactivepost_list.html'
    queryset = Post.deleted_objects.all()
    
class RestorePost(PermissionRequiredMixin):
    model = Post
    success_url = reverse_lazy('posts')
    permission_required = 'post.restore'
    
    
def restorecomment(request, slug, pk):
    comment = get_object_or_404(Comment,id=pk)
    if request.method == "POST":
        comment.is_delete = False
        comment.save()
        return HttpResponseRedirect(reverse("blog:article-details", args=[slug]))

    context = {"obj" : comment.comment_description()}
    return render(request, "blog/restore.html", context)





