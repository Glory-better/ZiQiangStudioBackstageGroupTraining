#文件:blog/views.py

from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from config.models import SideBar
from .models import Post,Category,Tag
from comment.forms import CommentForm
from comment.models import Comment


class CommonViewMixin:
	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context.update({
		'sidebars':SideBar.get_all(),
		})
		context.update(Category.get_navs())
		return context

class IndexView(CommonViewMixin,ListView):
	queryset=Post.objects.filter(status=Post.STATUS_NORMAL).select_related('owner').select_related('category')
	paginate_by=5
	context_object_name='post_list'
	template_name='blog/list.html'

class CategoryView(IndexView):
	def get_context_data(self,**kwargs):
		category_id=self.kwargs.get('category_id')
		category=get_object_or_404(Category,pk=category_id)
		eontext.update({
		'category':category,
		})
		return context
	
	def get_queryset(self):
		"""重写queryset,根据分类过滤"""
		queryset=super().get_queryset()
		category_id=self.kwargs.get('category_id')
		return queryset.filter(category_id=category_id)
	
	
class TagView(IndexView):
	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		tag_id=self.kwargs.get('tag_id')
		tag=get_object_or404(Tag,pk=tag_id)
		context.update({
		'tag':tag,
		})
		return context
		
	def get_queryset(self):
		"""重写queryset,根据标签过滤"""
		queryset=super().get_queryset()
		tag_id=self.kwargs.get('tag_id')
		return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin,DetailView):
	queryset=Post.latest_posts()
	template_name='blog/detail.html'
	context_object_name='post'
	pk_url_kwarg='post_id'
	
#	def get_context_data(self,**kwargs):
#		context=super().get_context_data(**kwargs)
#		context.update({
#		'conment_form':CommentForm,
#		'comment_list':Commnet.get_by_target(self.request.path),
#		})
#		return context

class SearchView(IndexView):
	def get_context_data(self):
		context=super().get_context_data()
		context.update({
		'keyword': self.request.GET.get('keyword', '')
		})
		return context
		
	def get_queryset(self):
		queryset=super().get_queryset()
		keyword=self.request.GET.get('keyword')
		if not keyword:
			return queryset
		return queryset.filter(Q(title_icontains=keyword)|Q(desc_icontains=keyword))
		
class AuthorView(IndexView):
	def get_queryset(self):
		queryset=super().get_queryset()
		author_id=self.kwargs.get('owner_id')
		return queryset.filter(owner_id=author_id)
# Create your views here.
