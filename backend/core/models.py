from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel, TreeForeignKey

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # CONCURRENCY CONSTRAINT:
        # The database enforces uniqueness. Two requests hitting at the exact
        # same microsecond will result in one passing and one failing (IntegrityError).
        unique_together = ('user', 'content_type', 'object_id')
        indexes = [
            models.Index(fields=['created_at']), # Index for the 24h leaderboard query
        ]

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like) 

class Comment(MPTTModel):
    # N+1 CONSTRAINT:
    # MPTT (Modified Preorder Tree Traversal) allows fetching the whole tree in 1 query.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)

    class MPTTMeta:
        order_insertion_by = ['created_at']