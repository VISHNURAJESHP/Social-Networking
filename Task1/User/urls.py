from rest_framework.views import APIView
from django.urls import path
from .views import UserRegistrationView,LoginView,SearchView, SendFriendRequestView, AcceptsRequstView, RejectRequstView, PendingRequestsView,FriendListView

urlpatterns = [
    path('login',LoginView.as_view(), name='login-view'),
    path('userregister',UserRegistrationView.as_view(), name='user-register'),
    path('search/<str:keyword>', SearchView.as_view(),name='search_friend'),
    path('send_friend_request/<int:to_user_id_sent>', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('accept_friend_request/<int:request_id>', AcceptsRequstView.as_view(), name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>', RejectRequstView.as_view(), name='reject_friend_request'),
    path('pending_request',PendingRequestsView.as_view(), name='Pending_friends_request'),
    path('friends',FriendListView.as_view(), name='friends_list')
]
