from django.db import models

# Create your models here.
class Notification(models.Model):
    NOTI_TYPE_CHOICES = [
        ('comment', 'Comment'),
        ('like', 'Like'),
        ('bookmark', 'Bookmark'),
    ]
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='notifications')
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, null=True, blank=True)
    noti_type = models.CharField(max_length=10, choices=NOTI_TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} - {self.noti_type}"
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
