from django.db import models

# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('user.Profile', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image', blank=True, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    view = models.PositiveIntegerField(default=0)
    like = models.ManyToManyField('user.User', related_name='likes_user', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    def save(self, *args, **kwargs):
        if not self.profile:
            self.profile = self.user.profile
        super().save(*args, **kwargs)
