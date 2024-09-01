from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q

from .constants import FriendRequestStatus
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from users.serializers import UserDetailModelSerializer
from .throttles import FriendRequestThrottle


class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        from_user = request.user
        to_user_id = int(request.data.get('to_user_id'))

        if from_user.id == to_user_id:
            return Response({"error": "You cannot send a friend request to yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=from_user, to_user_id=to_user_id).exists():
            return Response({"error": "Friend request already sent."},
                            status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest(from_user=from_user, to_user_id=to_user_id)
        friend_request.save()

        return Response(
        {"success": "Friend request sent."},
            status=status.HTTP_201_CREATED
        )


class AcceptRejectFriendRequestAPIView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        friend_request_id = int(request.data.get('friend_request_id'))
        action = request.data.get('action')  # 'accept' or 'reject' friend request
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user)
            if action == 'accept':
                friend_request.status = FriendRequestStatus.ACCEPTED.value
                friend_request.save()
                return Response({"success": "Friend request accepted."}, status=status.HTTP_200_OK)
            elif action == 'reject':
                friend_request.status = FriendRequestStatus.REJECTED.value
                friend_request.save()
                return Response({"success": "Friend request rejected."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)


class ListFriendsAPIView(generics.ListAPIView):
    serializer_class = UserDetailModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.get_friends(user=self.request.user)


class ListPendingFriendRequestsAPIView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.get_pending_requests(user=self.request.user)

