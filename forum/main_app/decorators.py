from django.urls import reverse
from django.shortcuts import redirect
from .models import Post


def check_post_user_id(old_function):
    def new_function(request, *args, **kwargs):
        try:
            post = Post.objects.get(user=request.user, id=request.POST['post_id'])
        except Exception:
            return redirect(reverse('main:index', kwargs={'page_number': 1}))
        return old_function(request, *args, **kwargs)
    return new_function
