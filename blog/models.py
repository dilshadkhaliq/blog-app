from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


CHOICES = [
	('draft', 'Draft'),
	('published', 'Published'),
	('private', 'Private')
]


class Post(models.Model):
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	body = models.TextField()
	author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=CHOICES, default='draft')

	tags = TaggableManager()

	def __str__(self):
		return self.title

	class Meta:
		ordering = ('-publish',)
		verbose_name = 'POST'
		verbose_name_plural = 'POSTS'

	def get_absolute_url(self):
		return reverse('blog:post_detail', args=[self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])


class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	name = models.CharField(max_length=25)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return 'comments by {} on {}'.format(self.name, self.post)
