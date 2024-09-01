from django.db import models
from users.models import UserDetails
from django.db.models import Q

from .constants import FriendRequestStatus


class FriendRequestManager(models.Manager):
    def get_friends(self, user):
        return UserDetails.objects.filter(
            Q(sent_requests__to_user=user,
              sent_requests__status=FriendRequestStatus.ACCEPTED.value) |
            Q(received_requests__from_user=user,
              received_requests__status=FriendRequestStatus.ACCEPTED.value)
        ).distinct()

    def get_pending_requests(self, user):
        return self.filter(to_user=user, status='pending')

    def has_request(self, from_user, to_user):
        return self.filter(from_user=from_user, to_user=to_user).exists()
