from rest_framework.decorators import api_view, permission_classes, parser_classes
from django.contrib.auth.forms import PasswordResetForm
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from news.utils import get_news_by_topic, get_news_detail, load_fresh_news_database_newsapi
from .serializers import NewsByTopicSerializer, AccountModelSerializer, ImageUploadTestSerializer, UserModelSerializer
from news.models import Source
from news.views import REACT_APP_NEWS_API1, REACT_APP_NEWS_API2, REACT_APP_NEWS_API3
from newsapi import NewsApiClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth  import login
from user.forms import CustomUserCreationForm, UpdateAccountForm
from user.models import Account
from django.contrib.auth.hashers import check_password
from rest_framework.parsers import FormParser, MultiPartParser

@api_view(["POST"])
def imageUploadTestView(request):
    serialized = ImageUploadTestSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=200)
    return Response(serialized.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_account_info(request):
    account = Account.objects.get(owner=request.user.id)
    serialized = AccountModelSerializer(instance=account, many=False)
    return Response(serialized.data, status=200)


@api_view(["POST"])
def api_login_user_view(request):
    username = request.data["username"]
    password = request.data["password"]

    user = ""

    try:
        user = User.objects.get(username=username)
    except Exception as e:
        return Response({"error": "User does not exists"}, status=400)

    if user.check_password(raw_password=password):
        refresh_token = RefreshToken.for_user(user=user)
        token = AccessToken.for_user(user=user)
        return Response({"message": "Logged in successfully", "refresh": str(refresh_token), "access": str(token)}, status=200)
    return Response({"error": "Invalid credential. Please provide valid credentials"}, status=400)


@api_view(["POST"])
def api_register_user_view(request):
    form = CustomUserCreationForm(request.data)
    if form.is_valid():
        user = form.save()
        login(request, user)
        token = str(AccessToken.for_user(user=user))
        return Response({"success": "User registered successfully", "access": token}, status=200)
    return Response({"errors": form.errors}, status=400)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def api_update_profile_view(request):
    account = Account.objects.get(id=request.user.account.id)
    serialized = AccountModelSerializer(instance=account, many=False)
    if request.method == "POST":
        form = UpdateAccountForm(request.data, request.FILES, instance=account)
        if form.is_valid():
            form.save()
            return Response({"message": "Successfully updated account"}, status=200)
        return Response(form.errors, status=400)
    return Response(serialized.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_news_topic_view(request, topic):
    news_by_topic, topic_class = get_news_by_topic(topic=topic)
    serialized = NewsByTopicSerializer(instance=news_by_topic, model=topic_class, many=True)
    return Response({"data": serialized.data, "topic": topic}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_news_detail_view(request, pk, topic):
    news, topic_class = get_news_detail(topic=topic, pk=pk)
    serialized = NewsByTopicSerializer(instance=news, model=topic_class, many=False)
    return Response({"data": serialized.data, "topic": topic}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def api_delete_all_refresh_view(request):
    deleted = Source.objects.all().delete()
    try:
        news_api = NewsApiClient(api_key=REACT_APP_NEWS_API2)
        loaded = load_fresh_news_database_newsapi(news_api)
    except Exception as e:
        print(e)
    news_by_topic, topic_class = get_news_by_topic(topic="general")
    serialized = NewsByTopicSerializer(instance=news_by_topic, model=topic_class, many=True)
    return Response(serialized.data)


# To reset password if forgotten
@api_view(["POST"])
def api_password_reset_sent_view(request):
    email = request.data.get("email")
    try:
        user = User.objects.get(email=email)
    except Exception as e:
        print(e)
        return Response({"errors": f"User with the email[{email}] not found. {e}"}, status=400)
    
    form = PasswordResetForm(request.data)
    if form.is_valid():
        form.save(request=request)
        return Response({"Head":"Password reset sent", "message1":"We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.", "message2":"If you don’t receive an email, please make sure you’ve entered the address you registered with, and check your spam folder."})
    return Response({"errors": form.errors}, status=400)


# To change password
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_change_password_view(request):
    password1 = request.data.get("password1")
    password2 = request.data.get("password2")

    if len(password1) < 5 or len(password2) < 5:
        return Response({"Error": "Password length should be 5 or more characters"}, status=400)

    user = User.objects.get(id=request.user.id)
    if not user.check_password(request.data.get("old_password")):
        return Response({"Error": "Old password didn't match"}, status=400)

    if password1 != password2:
        return Response({"Error": "Confirm password miss-match. Confirm your password"})

    user.password = make_password(password=password1)
    user.save()
    refresh = RefreshToken.for_user(user=user)
    token = str(refresh.access_token)
    login(request, user)
    return Response({"success": "Password changed successfully.", "refresh": str(refresh), "access": token})
