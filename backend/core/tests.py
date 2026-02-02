from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from .models import Post, Like

class LeaderboardTestCase(TestCase):
    def test_leaderboard_ignores_old_karma(self):
        """
        Test that the leaderboard only counts karma from the last 24 hours.
        """
        # 1. Setup: Create a Player and a Fan
        player = User.objects.create_user(username="pro_gamer")
        fan = User.objects.create_user(username="fan_boy")
        
        # 2. Setup: Create content
        post_fresh = Post.objects.create(author=player, content="Fresh Post")
        post_stale = Post.objects.create(author=player, content="Old Post")
        post_ctype = ContentType.objects.get_for_model(Post)

        # 3. Action: Give a FRESH Like (Right now) -> Should be worth +5 Points
        Like.objects.create(
            user=fan,
            content_type=post_ctype,
            object_id=post_fresh.id
        )

        # 4. Action: Give a STALE Like (25 hours ago) -> Should be worth 0 Points
        # We create it, then manually hack the timestamp to be in the past
        old_like = Like.objects.create(
            user=fan,
            content_type=post_ctype,
            object_id=post_stale.id
        )
        old_like.created_at = timezone.now() - timedelta(hours=25)
        old_like.save()

        # 5. Verification: Check the Leaderboard API
        response = self.client.get('/api/leaderboard/')
        
        # The player should be in the list
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Player should have exactly 5 Karma (Fresh Like), NOT 10 (Fresh + Stale)
        self.assertEqual(data[0]['username'], 'pro_gamer')
        self.assertEqual(data[0]['total_karma'], 5)
