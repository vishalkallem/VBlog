from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


def upload_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    image = models.ImageField(upload_to=upload_path, width_field="widthField", height_field="heightField",
                              null=True, blank=True)
    widthField = models.IntegerField(default=0)
    heightField = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={"slug": self.slug})


def slug_generator(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = instance.__class__.objects.filter(slug=slug)
    if qs.exists():
        new_slug = f"{slug}-{qs.first().user}"
        return slug_generator(instance, new_slug=new_slug)
    return slug


def set_post_slug(sender, instance, *args, **kwargs):
    if sender and not instance.slug:
        instance.slug = slug_generator(instance)


pre_save.connect(set_post_slug, sender=Post)
