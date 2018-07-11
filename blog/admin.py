from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'publish', 'slug', 'author', 'status')
	list_filter = ('publish', 'created', 'updated', 'author')
	search_fields = ('title', 'body')
	prepopulated_fields = {'slug': ('title', )}
	ordering = ['status', 'publish']
	raw_id_fields = ('author', )


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'created', 'active', 'post')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'body', 'email')


admin.site.register(Comment, CommentAdmin)
