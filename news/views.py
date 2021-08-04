from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category
from .forms import NewsForm
from .utils import MyMixin
from comments.models import Comment
from comments.forms import CommentForm

# Create your views here.


class HomeNews(MyMixin, ListView):
    paginate_by = 3
    model = News
    context_object_name = "news"
    template_name = "news/index.html"
    # extra_context = {"title": "Новости"}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная Страница"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)


# class ViewNews(DetailView):
#     model = News
#     pk_url_kwarg = "news_id"
#     context_object_name = "news"
#     template_name = "news/getNews.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["comments"] = Comment.objects.all()
#         context["form"] = CommentForm()
#         return context


def viewDetail(request, news_id):
    news = News.objects.get(pk=news_id)
    comments = news.comment_set.all()
    if request.method == "POST":
        news.comment_set.create(author=request.user, text=request.POST["text"])
        return redirect(news)
    else:
        form = CommentForm()
    context = {"comments": comments, "news": news, "form": form}
    return render(request, "news/getNews.html", context=context)


class GetCategory(ListView):
    paginate_by = 3
    model = News
    pk_url_kwarg = "category_id"
    allow_empty = False
    context_object_name = "news"
    template_name = "news/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs["category_id"])
        return context

    def get_queryset(self):
        return News.objects.filter(
            is_published=True, category_id=self.kwargs["category_id"]
        )


@login_required
def addNews(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            # News.objects.create(**form.cleaned_data)
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
        return render(request, "news/addNews.html", {"form": form})


def getNews(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    return render(
        request,
        "news/getNews.html",
        {
            "news": news,
        },
    )


# def test(request):
#     objects = [
#         1,
#         2,
#         3,
#         4,
#         5,
#         6,
#         7,
#         8,
#     ]
#     p = Paginator(objects, 2)
#     p_num = request.GET.get("page", 1)
#     p_objects = p.get_page(p_num)
#     return render(request, "news/index.html", {"page_obj": p_objects})


# class NewsByCategory(ListView):
#     model = News
#     context_object_name = "news"
#     template_name = "news/category.html"

#     def get_queryset(self):
#         return News.objects.filter(
#             category_id=self.kwargs["category_id"], is_published=True
#         )

# class CreateNews(CreateView):
#     form_class = NewsForm
#     template_name = "news/addNews.html"
