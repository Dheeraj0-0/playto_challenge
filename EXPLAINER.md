# Playto Engineering Challenge - Explainer

## 1. The Tree (Solving the N+1 Problem)
I chose **`django-mptt` (Modified Preorder Tree Traversal)** to model the threaded comments.

* **The Problem:** Standard recursive relationships (parent-child) require a new database query for every comment layer to fetch children. For a thread with 50 nested comments, this results in 50+ SQL queries (The N+1 Nightmare), killing performance.
* **The Solution:** MPTT stores `lft` (left) and `rght` (right) integer values for each node. This allows us to fetch an entire discussion thread—regardless of depth—in **exactly one SQL query**:
    ```python
    # Fetches the whole tree efficiently
    Comment.objects.filter(tree_id=X).get_descendants()
    ```
* **Serialization:** I serve the comments as a flat list with `parent_id` references. This offloads the computational cost of reconstructing the tree structure to the Client (Frontend), keeping the Server CPU usage low.

## 2. The Math (24h Leaderboard Aggregation)
To adhere to the constraint of *not* storing volatile "daily karma" in a simple integer field, I calculated it on-the-fly using **Conditional Aggregation**.

This ensures data integrity: if a "Like" is deleted, the user's score updates instantly without needing background cron jobs to recalculate.

**The QuerySet:**
```python
User.objects.annotate(
    post_points=Count(
        'posts__likes',
        filter=Q(posts__likes__created_at__gte=last_24h)
    ) * 5,
    comment_points=Count(
        'comments__likes',
        filter=Q(comments__likes__created_at__gte=last_24h)
    ) * 1
).annotate(
    total_karma=F('post_points') + F('comment_points')
).order_by('-total_karma')[:5]
