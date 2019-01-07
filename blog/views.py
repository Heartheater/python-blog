from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    #if no Post is found with the given pk(primary key),
    #this will display a 'page not found' error page
    post = get_object_or_404(Post, pk=pk) #Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if(request.method == "POST"):
        form = PostForm(request.POST)
        if(form.is_valid()):
            #save the form
            post = form.save(commit=False)
            #add an author and publish date
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            #finally, redirect the page to the new post's detail page
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if(request.method == "POST"):
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})