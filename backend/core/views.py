from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Q, F
from django.utils import timezone
from .models import Post, Comment, Like, User
from .serializers import PostSerializer, UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        # OPTIMIZATION: 
        # We prefetch 'comments' so we don't hit the DB again.
        # We also select_related 'author' to avoid N+1 on authors.
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class LeaderboardView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        # THE MATH:
        # 1. Get time 24 hours ago
        last_24h = timezone.now() - timezone.timedelta(hours=24)

        # 2. Aggregation Query
        # We use Count with a filter (Q object) to only count likes from the last 24h.
        return User.objects.annotate(
            post_points=Count(
                'posts__likes', 
                filter=Q(posts__likes__created_at__gte=last_24h)
            ) * 5,
            comment_points=Count(
                'comment__likes', 
                filter=Q(comments__likes__created_at__gte=last_24h) # Note: 'comment' is the related_name default for User
            ) * 1
        ).annotate(
            total_karma=F('post_points') + F('comment_points')
        ).filter(total_karma__gt=0).order_by('-total_karma')[:5]