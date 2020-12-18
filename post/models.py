from django.db import models
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.conf import settings 
from django.utils.timezone import now

User = settings.AUTH_USER_MODEL


# Create your models here.
class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(blank=True, upload_to='profile/')

class Category(models.Model):
    category = models.CharField(blank=False, max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category
    

class Post(models.Model):
    title = models.CharField(blank=False, max_length=250)
    slug = AutoSlugField(populate_from='title')
    post_category = models.ForeignKey(Category, blank=False, on_delete=models.CASCADE)
    post_image = models.ImageField(default='post_image/df.jpeg', upload_to='post_image/')
    author = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    post = RichTextField(blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.title +' | '+ str(self.author)

class Comment(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, blank=False, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    created_date = models.DateTimeField(default=now, editable=False)

