from django.db import models
import random, os
from forum import settings
from django.contrib.auth.models import User


class ForumUser(User):
    GENDER_CHOICES = (
        ('', 'Выбор пола'),
        ('M', 'Мужчина'),
        ('F', 'Женщина'),)
    city = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to="avatars")

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.avatar.path):
            os.remove(self.avatar.path)
        super(ForumUser, self).delete(*args,**kwargs)

    def random_avatar(self):
        list_images = os.listdir(path=settings.RANDOM_AVATARS)
        if self.gender == 'M':
            male_avatars = list(filter(lambda gender: gender.startswith('boy'), list_images))
            return settings.RANDOM_AVATARS_URL + random.choice(male_avatars)
        else:
            female_avatars = list(filter(lambda gender: gender.startswith('girl'), list_images))
            return settings.RANDOM_AVATARS_URL + random.choice(female_avatars)

    @property
    def reputation(self):
        likes_thread = Thread.objects.filter(user=self.id)
        likes_post = Post.objects.filter(user=self.id)
        total_likes = 0
        total_dislikes = 0
        for item in list(likes_thread) + list(likes_post):
            total_likes += item.likes.count()
            total_dislikes += item.dislikes.count()
        return total_likes - total_dislikes

    @property
    def thread_count(self):
        return Thread.objects.filter(user=self.id).count()

    @property
    def post_count(self):
        return Post.objects.filter(user=self.id).count()


class Thread(models.Model):
    title = models.CharField(max_length=24)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ForumUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    likes = models.ManyToManyField(ForumUser, related_name="thread_likes", blank=True)
    dislikes = models.ManyToManyField(ForumUser, related_name="thread_dislikes", blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(Thread, self).delete(*args,**kwargs)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()

    @property
    def post_count(self):
        return Post.objects.filter(thread=self.id).count()


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    title = models.CharField(max_length=24)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ForumUser, on_delete=models.CASCADE)
    likes = models.ManyToManyField(ForumUser, related_name="post_likes", blank=True)
    dislikes = models.ManyToManyField(ForumUser, related_name="post_dislikes", blank=True)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def dislikes_count(self):
        return self.dislikes.count()
