from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post
from .forms import CommentForm, EmailPostForm
from taggit.models import Tag
from django.db.models import Count
from django.db.models import Q
from django.core.mail import send_mail


def post_list(request, tag_slug=None):
	query = request.GET.get('q')
	if query:
		object_list = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
	else:
		object_list = Post.objects.filter(status='published')
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])
	paginator = Paginator(object_list, 3)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	total_posts = Post.objects.count()
	latest_posts = Post.objects.filter(status='published').order_by('-publish')[:3]
	most_comment = Post.objects.annotate(total=Count('comments')).order_by('-total')[:5]

	context = {'page': page, 'posts': posts, 'tag': tag, 'total_posts': total_posts, 'latest_posts': latest_posts, 'most_comment': most_comment}
	return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
	comments = post.comments.filter(active=True)
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = CommentForm()
	post_tags_id = post.tags.values_list('id', flat=True)
	similar_post = Post.objects.filter(tags__in=post_tags_id).exclude(id=post.id)
	similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
	total_posts = Post.objects.count()
	latest_posts = Post.objects.filter(status='published').order_by('-publish')[:3]
	most_comment = Post.objects.annotate(total=Count('comments')).order_by('-total')[:5]
	template = 'blog/post/detail.html'
	context = {'post': post, 'comment_form': comment_form, 'comments': comments, 'similar_post': similar_post,'total_posts': total_posts, 'latest_posts': latest_posts, 'most_comment': most_comment}
	return render(request, template, context)


def share_email(request, id):
	post = get_object_or_404(Post, id=id)
	sent = False
	if request.method == 'POST':
		form = EmailPostForm(data=request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommend you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comment'])
			send_mail(subject, message, 'admin@gmail.com', (cd['to'],))
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share_post.html', {'post': post, 'form': form, 'sent': sent})


