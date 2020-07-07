from django.urls import path, include
from rest_framework import routers
from api.views import *

router= routers.DefaultRouter()
router.register('useraccount', UserViewSet, basename='useraccount')
router.register('search', SearchUser, basename='search')
router.register('test', AdddataViewSet, basename='test')
router.register('loggedin', CheckUserLoggedIn, basename='login')
router.register('addfrd', AddMyFriend, basename='addfriend')
router.register('friendslist', GetMyFriends, basename='friends')
router.register('requestslist', RequestsList, basename='requests')
router.register('accept', AcceptFriendRequest, basename='accept')
router.register('givelike', Like, basename='like')
# router.register('login', LoginViewSet, basename='login')
# router.register('logout', LogoutViewSet, basename='logout')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', users),
    path('userlist/', userslist),
    path('login/', login),
    path('givelike/', addlike),
    path('logout/', logout),
]