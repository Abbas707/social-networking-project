from users.models import UserDetails
from django.db import models
from .constants import FriendRequestStatus
from .managers import FriendRequestManager


STATUS_CHOICES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')]


class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserDetails, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserDetails, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=FriendRequestStatus.choices(), default='pending')

    objects = FriendRequestManager()

    def __str__(self):
        return f"Friend request from {self.from_user} to {self.to_user}"

    class Meta:
        unique_together = ('from_user', 'to_user')
