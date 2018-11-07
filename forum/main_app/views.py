from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ForumUser, Thread, Post
from .forms import ForumUserCreationForm, ThreadCreateForm, CreatePostForm, ForumUserUpdateForm
from .decorators import check_post_user_id


class ForumUserFormView(FormView):

    form_class = ForumUserCreationForm
    success_url = "/accounts/login"
    template_name = "registration.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.avatar = user.random_avatar()
        user.save()
        return super(ForumUserFormView, self).form_valid(form)


class IndexView(View):

    template_name = 'index.html'

    def get(self, request, page_number):
        query = Thread.objects.all().order_by('-date')
        if query.count() != 0:
            query_page = Paginator(query, 9)
            try:
                pages = query_page.page(page_number)
            except PageNotAnInteger:
                pages = query_page.page(1)
            except EmptyPage:
                pages = query_page.page(query_page.num_pages)
            args = {"query": pages}
        else:
            args = {"none": "Нет записей"}
        return render(request, self.template_name, args)


class ThreadView(View):

    template_name = 'thread.html'

    def get(self, request, pk):
        form = CreatePostForm()
        thread = Thread.objects.get(id=pk)
        posts = Post.objects.filter(thread=thread)
        args = {"thread": thread, "posts": posts, "form": form}
        return render(request, self.template_name, args)

    @method_decorator(login_required)
    def post(self, request, pk):
        form = CreatePostForm(request.POST)
        thread = Thread.objects.get(id=pk)
        posts = Post.objects.filter(thread=thread)
        args = {"thread": thread, "posts": posts, "form": form}
        if form.is_valid():
            post = form.save(commit=False)
            post.user = ForumUser.objects.get(username=request.user)
            post.thread = thread
            post.save()
            return redirect(reverse('main:thread', kwargs={'pk': thread.id}))
        return render(request, self.template_name, args)


class CreateThreadView(View):

    template_name = "create_thread.html"

    @method_decorator(login_required)
    def get(self, request):
        form = ThreadCreateForm()
        args = {"form": form}
        return render(request, self.template_name, args)

    @method_decorator(login_required)
    def post(self, request):
        form = ThreadCreateForm(request.POST, request.FILES)
        args = {"form": form}
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = ForumUser.objects.get(username=request.user)
            thread.image = request.FILES.get('image')
            thread.save()
            return redirect(reverse('main:thread', kwargs={'pk': thread.id}))
        return render(request, self.template_name, args)


class ProfileView(View):

    template_name = 'profile.html'

    @method_decorator(login_required)
    def get(self, request):
        form = ForumUserUpdateForm(request=request)
        profile = ForumUser.objects.get(username=request.user)
        args = {"profile": profile, "form": form}
        return render(request, self.template_name, args)

    @method_decorator(login_required)
    def post(self, request):
        form = ForumUserUpdateForm(request.POST, request.FILES, request=request)
        profile = ForumUser.objects.get(username=request.user)
        args = {"profile": profile, "form": form}
        if form.is_valid():
            profile.email = form.cleaned_data.get('email')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.city = form.cleaned_data.get('city')
            if form.cleaned_data.get('avatar') == None:
                pass
            else:
                profile.avatar = form.cleaned_data.get('avatar')
            profile.save()
            return redirect('main:profile')
        return render(request, self.template_name, args)


@login_required
@check_post_user_id
@require_POST
def delete_post(request):
    id = request.POST['post_id']
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        post.delete()
        return redirect(reverse('main:thread', kwargs={'pk': post.thread.id}))


@login_required
def delete_thread(request, pk):
    try:
        thread = Thread.objects.get(user=request.user, id=pk).delete()
    except Exception as e:
        pass
    return redirect(reverse('main:index', kwargs={'page_number': 1}))



@login_required
@require_POST
def like_and_dislike(request):
    if request.method == 'POST':
        user = ForumUser.objects.get(username=request.user)
        pk = request.POST.get('pk')
        if request.POST.get('model') == 'thread':
            model = get_object_or_404(Thread, id=pk)
        else:
            model = get_object_or_404(Post, id=pk)

        if request.POST.get('type') == 'like':
            if model.likes.filter(id=user.id).exists():
                model.likes.remove(user)
            else:
                model.likes.add(user)
            response = {'likes_count': model.likes_count}
        else:
            if model.dislikes.filter(id=user.id).exists():
                model.dislikes.remove(user)
            else:
                model.dislikes.add(user)
            response = {'dislikes_count': model.dislikes_count}
    return JsonResponse(response)


class AboutForumUserView(View):

    template_name = 'about.html'

    def get(self, request, pk):
        forumuser = ForumUser.objects.get(id=pk)
        args = {"user": forumuser }
        return render(request, self.template_name, args)


def redirect_to_index(request):
    return redirect('main:index', page_number=1)


def handler404(request):
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html')
    response.status_code = 500
    return response
