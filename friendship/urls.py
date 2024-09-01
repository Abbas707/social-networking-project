from django.urls import path
from .views import (
    SendFriendRequestAPIView,
    AcceptRejectFriendRequestAPIView,
    ListFriendsAPIView,
    ListPendingFriendRequestsAPIView
)

urlpatterns = [
    path('friend-request/send/', SendFriendRequestAPIView.as_view(),
         name='send-friend-request'),
    path('friend-request/respond/', AcceptRejectFriendRequestAPIView.as_view(),
         name='respond-friend-request'),
    path('friends/', ListFriendsAPIView.as_view(), name='list-friends'),
    path('friend-requests/pending/', ListPendingFriendRequestsAPIView.as_view(),
         name='list-pending-friend-requests'),
]
