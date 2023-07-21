from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from news.models import Source, Crypto, Loan, Health, StudentLoan, Sports, General, Science, Business, Technology, \
    Entertainment, HackersHacking, AnonymousHacking


def paginate_news(request, news_list, result_per_page):
    try:
        page_number = int(request.GET.get("page"))
    except Exception as e:
        page_number = 1
        
    all_paginated_news = Paginator(object_list=news_list, per_page=result_per_page)
    
    try:
        paginated_news_list = all_paginated_news.page(page_number)
    except EmptyPage:
        page_number = 1
        paginated_news_list = all_paginated_news.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        paginated_news_list = all_paginated_news.page(page_number)
    
    left_index = page_number - 4
    if left_index < 1:
        left_index = 1
    
    right_index = page_number + 5
    if right_index > all_paginated_news.num_pages:
        right_index = all_paginated_news.num_pages + 1

    pagination_range = range(left_index, right_index)
    
    return paginated_news_list, pagination_range


def get_news_by_topic(topic):
    topic = topic.lower()
    print(topic)
    try:
        if topic == "crypto":
            topic_news = Crypto.objects.all()
            return topic_news, Crypto

        elif topic == "loan":
            topic_news = Loan.objects.all()
            return topic_news, Loan

        elif topic == "health":
            topic_news = Health.objects.all()
            return topic_news, Health

        elif topic == "studentloan":
            topic_news = StudentLoan.objects.all()
            return topic_news, StudentLoan

        elif topic == "sports":
            topic_news = Sports.objects.all()
            return topic_news, Sports

        elif topic == "general":
            topic_news = General.objects.all()
            return topic_news, General

        elif topic == "science":
            topic_news = Science.objects.all()
            return topic_news, Science

        elif topic == "business":
            topic_news = Business.objects.all()
            return topic_news, Business

        elif topic == "technology":
            topic_news = Technology.objects.all()
            return topic_news, Technology

        elif topic == "entertainment":
            topic_news = Entertainment.objects.all()
            return topic_news, Entertainment

        elif topic == "hackers-hacking":
            topic_news = HackersHacking.objects.all()
            return topic_news, HackersHacking

        elif topic == "anonymous-hacking":
            topic_news = AnonymousHacking.objects.all()
            return topic_news, AnonymousHacking
    except Exception as e:
        print(e)


def get_news_detail(topic, pk):
    topic = topic.lower()
    try:
        if topic == "general":
            news = General.objects.get(id=pk)
            return news, General
        elif topic == "crypto":
            news = Crypto.objects.get(id=pk)
            return news, Crypto
        elif topic == "loan":
            news = Loan.objects.get(id=pk)
            return news, Loan
        elif topic == "health":
            news = Health.objects.get(id=pk)
            return news, Health
        elif topic == "studentloan":
            news = StudentLoan.objects.get(id=pk)
            return news, StudentLoan
        elif topic == "sports":
            news = Sports.objects.get(id=pk)
            return news, Sports
        elif topic == "science":
            news = Science.objects.get(id=pk)
            return news, Science
        elif topic == "business":
            news = Business.objects.get(id=pk)
            return news, Business
        elif topic == "technology":
            news = Technology.objects.get(id=pk)
            return news, Technology
        elif topic == "entertainment":
            news = Entertainment.objects.get(id=pk)
            return news, Entertainment
        elif topic == "hackers-hacking":
            news = HackersHacking.objects.get(id=pk)
            return news, HackersHacking
        elif topic == "anonymous-hacking":
            news = AnonymousHacking.objects.get(id=pk)
            return news, AnonymousHacking
    except Exception as e:
        print(e)


def load_fresh_news_database_newsapi(news_api):
    topics = [
        "Crypto",
        "Loan",
        "Health",
        "StudentLoan",
        "Sports",
        "General",
        "Science",
        "Business",
        "Technology",
        "Entertainment",
        "hackers-hacking",
        "anonymous-hacking",
    ]

    for i in range(1, 2):
        for topic in topics:
            response = news_api.get_everything(
                q=topic,
                page_size=100,
                language="en",
                sort_by="publishedAt",
                page=i
            )

            articles = response["articles"]
            for article in articles:
                if article["author"] is None:
                    article["author"] = "Anonymous"

                article_source = article["source"]
                try:
                    source, created = Source.objects.get_or_create(name=article_source["name"])
                    source.source_id = article_source["id"]
                    source.save()
                    if topic == "Crypto":
                        news_article, created = Crypto.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    elif topic == "Loan":
                        news_article, created = Loan.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    elif topic == "Health":
                        news_article, created = Health.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    elif topic == "StudentLoan":
                        news_article, created = StudentLoan.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    elif topic == "Sports":
                        news_article, created = Sports.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    elif topic == "General":
                        news_article, created = General.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    elif topic == "Science":
                        news_article, created = Science.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    elif topic == "Business":
                        news_article, created = Business.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    elif topic == "Technology":
                        news_article, created = Technology.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    elif topic == "Entertainment":
                        news_article, created = Entertainment.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    elif topic == "hackers-hacking":
                        news_article, created = HackersHacking.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    elif topic == "anonymous-hacking":
                        news_article, created = AnonymousHacking.objects.get_or_create(
                            source=source,
                            author=article["author"],
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            urlToImage=article["urlToImage"],
                            content=article["content"],
                            publishedAt=article["publishedAt"]
                            # publishedAt=timezone.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                        )
                        print(f"topic: {topic} news: {news_article}")

                    print('Updated latest news')
                    # print(f"topic: {topic} news: {news_article}")

                except Exception as e:
                    print("Error at: news.utils.load_fresh_news_database_newsapi()")
                    print(e)