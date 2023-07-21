from django.shortcuts import render, redirect
from newsapi import NewsApiClient
from news.models import Source, Crypto, Loan, Health, StudentLoan, Sports, General, Science, Business, Technology, \
    Entertainment, HackersHacking, AnonymousHacking
from django.contrib.auth.decorators import login_required
from .utils import paginate_news, get_news_by_topic, get_news_detail, load_fresh_news_database_newsapi

REACT_APP_NEWS_API1 = '9027043c7575452a8ca346f8d1fb03e9'
REACT_APP_NEWS_API2 = 'a3b4e31fd807487a9cc9604c57338132'
REACT_APP_NEWS_API3 = 'b680990980264f2daadab2f6b5cca5ba'

RESULT_PER_PAGE_NEWS = 20


@login_required(login_url="login")
def refresh_news_view(request):
    news_api = NewsApiClient(api_key=REACT_APP_NEWS_API2)

    load_fresh_news_database_newsapi(news_api=news_api)
                # print("=========================================================================================="
                #       "=============================")
    return redirect(to="home")


@login_required(login_url="login")
def homepage_view(request):
    general_news = General.objects.all()
    paginate_general_news, pagination_range = paginate_news(request=request, news_list=general_news, result_per_page=RESULT_PER_PAGE_NEWS)

    topic = "general"
    ctx = {"general_news": paginate_general_news, "topic": topic, "pagination_range": pagination_range}
    return render(request, template_name="news/index.html", context=ctx)


@login_required(login_url="login")
def news_detail_view(request, pk, topic):
    news, topic_class = get_news_detail(topic=topic, pk=pk)

    ctx = {"news": news, "topic": topic}
    return render(request, template_name="news/news-detail.html", context=ctx)


@login_required(login_url="login")
def news_topic(request, topic):
    topic_news, topic_class = get_news_by_topic(topic=topic)

    topic_news, pagination_range = paginate_news(request=request, news_list=topic_news, result_per_page=RESULT_PER_PAGE_NEWS)

    ctx = {"topic_news": topic_news, "topic": topic, "pagination_range": pagination_range}
    return render(request, template_name="news/news-topic.html", context=ctx)


@login_required(login_url="login")
def delete_all_refresh_news(request):
    Source.objects.all().delete()
    refresh_news_view(request)
    return redirect(to="home")
