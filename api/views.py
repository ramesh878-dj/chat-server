from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, logout as django_logout
from django_filters import rest_framework as filters
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.db.models import Q

from api.serializers import UserSerializer, AddSomedataSerializer, LoginSerializer,LoginSerializer, AddFriendSerializer, FriendsSerializer, LikesSerializer
from api.models import *

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import exceptions
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

class UserFilters(filters.FilterSet):
    username= filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields= ('username', )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    authentication_classes= [BasicAuthentication, SessionAuthentication]
    permission_classes= [IsAuthenticated]
    filterset_class= UserFilters

    @action(methods = ['get'], detail=False)
    def get(self, request):
        return Response(serializer.data)

    @action(methods = ['post'], detail=False)
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class SearchUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    authentication_classes= [BasicAuthentication, SessionAuthentication]
    permission_classes= [IsAuthenticated]
    filter_fields= ('username',)

    @action(methods = ['get'], detail=False)
    def get(self, request):
        return Response(serializer.data)



class AdddataViewSet(viewsets.ModelViewSet):
    queryset = Testtable.objects.all()
    serializer_class= AddSomedataSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    @action(methods = ['get'], detail=False)
    def get(self, request):
        return Response(serializer.data)
    
    @action(methods = ['post'], detail=False)
    def post(self, request):
        data = request.data
        serializer = AddSomedataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# class LoginViewSet(viewsets.ModelViewSet):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         django_login(request, user)
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({"token":token.key}, status=200)
    
# class LogoutViewSet(viewsets.ModelViewSet):
#     authentication_classes= (TokenAuthentication, )
#     def post(self, request):
#         django_logout(request)
#         return Response(status=204)

# class CsrfExcemptSessionAuthentication(SessionAuthentication):
#     def enforce_csrf(self, request):
#         return # none

# class Logout(APIView):
#     authentication_classes = (CsrfExcemptSessionAuthentication, BasicAuthentication)

class CheckUserLoggedIn(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    
    @action(methods = ['get'], detail=False)
    def get(self, request):
        return JsonResponse({"login":True})

class AddMyFriend(viewsets.ViewSet):
    queryset = Friends_table.objects.all()
    serializer_class= AddFriendSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    @action(methods = ['post'], detail=False)
    def post(self, request):
        data= request.data
        user = User.objects.get(username=data['username'])
        if user:
            makefriends={
                "requester_id":user.id,
                "requester_name":user.username,
                "accepter_id":data['accepter_id'],
                "accepter_name":data['accepter_name']
            }
            check_already_friend= Friends_table.objects.filter((Q(requester_id=user.id) & Q(accepter_id=data['accepter_id'])) | (Q(requester_id=data['accepter_id']) & Q(accepter_id=user.id)))
            if not check_already_friend:
                serializer = AddFriendSerializer(data=makefriends)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"request_send":"success"}, status=201)
            else:
                getfriends= Friends_table.objects.get((Q(requester_id=user.id) & Q(accepter_id=data['accepter_id'])) | (Q(requester_id=data['accepter_id']) & Q(accepter_id=user.id)))
                if getfriends.friends_status == 0:
                    return Response({"request_send":"notsuccess", "already_freind":"requested"}, status=201)
                else:
                    return Response({"request_send":"notsuccess", "already_freind":"accepted"}, status=201)
        return Response(serializer.errors, status=400)

class GetMyFriends(viewsets.ViewSet):
    # serializer_class= AddFriendSerializer
    # queryset = Friends_table.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    lookup_field='slug'

    @action(methods = ['get'], detail=True)
    def get(self, request, slug=None):
        userdata=User.objects.get(username=slug)
        if userdata:
            friends = Friends_table.objects.filter((Q(requester_id=userdata.id) | Q(accepter_id=userdata.id)) & Q(friends_status=1))
            print(friends.count())
            serializer= AddFriendSerializer(friends,many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"error":"wrong username"},status=403)
        return Response(serializer.data, status=200)

class RequestsList(viewsets.ViewSet):
    # serializer_class= AddFriendSerializer
    # queryset = Friends_table.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    lookup_field='slug'

    @action(methods = ['get'], detail=True)
    def get(self, request, slug=None):
        userdata=User.objects.get(username=slug)
        if userdata:
            friends = Friends_table.objects.filter(Q(accepter_id=userdata.id) & Q(friends_status=0))
            print(friends.count())
            serializer= AddFriendSerializer(friends,many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"error":"wrong username"},status=403)
        return Response(serializer.data, status=200)

class AcceptFriendRequest(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    @action(methods = ['post'], detail=False)
    def post(self, request):
        data= request.data
        friend_st = Friends_table.objects.get(Q(requester_name=data['friendname']) & Q(accepter_name=data['username']))
        if friend_st:
            if friend_st.friends_status==0:
                Friends_table.objects.filter(Q(requester_name=data['friendname']) & Q(accepter_name=data['username'])).update(friends_status=1)
                return Response({"update":"success"})
            else:
                return Response({"update":"notsuccess", "already_freind":"exists"})
        else:
            return Response({"update":"notsuccess", "friends":"Data not found"})
        
class Like(viewsets.ViewSet):
    @action(methods = ['GET'], detail=False)
    def get(self, request):
        countdata = LikeTable.objects.all()
        serializer= LikesSerializer(countdata, many=True)
        return Response(serializer.data, status=200)

    @action(methods = ['POST'], detail=False)
    def post(self, request):
        last_id= LikeTable.objects.get(id=1)
        count= last_id.likeCount
        count = count+1
        last_id= LikeTable.objects.filter(id=1).update(likeCount=count)
        countdata = LikeTable.objects.all()
        serializer= LikesSerializer(countdata, many=True)
        print('yes')
        return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def users(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors)

@api_view(['GET', 'POST'])
def userslist(request):
    if request.method == 'GET':
        alluser = User.objects.all()
        serializer= UserSerializer(alluser, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            django_login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({"token":token.key, "logged_in":True, "username":request.data['username']}, status=200)
        else:
            return JsonResponse({"error":"Wrong username or password",}, status=401)
   
@csrf_exempt
def logout(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    django_logout(request)
    return JsonResponse({"logout":"logout"},status=200)
