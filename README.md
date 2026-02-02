# Playto Engineering Challenge - Community Feed Prototype

A high-performance threaded discussion platform with a dynamic leaderboard, built to solve specific engineering constraints around database performance and data integrity.

**Live Demo:** http://20.207.201.15:8000/api/leaderboard/  
**Engineering Explainer:** [Read EXPLAINER.md](./EXPLAINER.md)

---

## 🛠 The Stack
* **Backend:** Django & Django REST Framework (DRF)
* **Database:** PostgreSQL 13
* **Infrastructure:** Docker & Docker Compose
* **Cloud:** Azure VM (Ubuntu)

---

## 🚀 Key Engineering Features

### 1. The N+1 Solution (Nested Comments)
Instead of recursive SQL queries for every reply (which kills performance), I implemented **Modified Preorder Tree Traversal (MPTT)** using `django-mptt`.
* **Result:** Fetches an entire comment thread of any depth in **1 SQL query**.
* **Optimization:** Comments are served as a flat list with `parent_id` to offload tree reconstruction to the client.

### 2. Concurrency Control (Race Conditions)
Prevented "Double Likes" at the database level using `unique_together` constraints.
* **Mechanism:** If two requests hit the server simultaneously to "like" the same post, the database integrity check fails one of them, ensuring accurate karma counts.

### 3. Dynamic Leaderboard (Complex Aggregation)
The leaderboard calculates the "Top 5 Users" based on activity in the **last 24 hours only**.
* **Strategy:** No volatile data is stored in the `User` model.
* **Implementation:** Used Django's `Count` with Conditional Filters (`Q` objects) to aggregate scores on-the-fly. This guarantees that if a like is deleted, the score updates instantly.

---

## ⚡ How to Run Locally

This project is fully containerized. You only need Docker installed on your machine.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Dheeraj0-0/playto_challenge.git](https://github.com/Dheeraj0-0/playto_challenge.git)
    cd playto_challenge
    ```

2.  **Start the server:**
    ```bash
    docker-compose up --build
    ```

3.  **Run Migrations (Important for Database):**
    Open a new terminal tab and run:
    ```bash
    docker-compose exec backend python manage.py migrate
    ```

4.  **Create Superuser (Optional - to access Admin Panel):**
    ```bash
    docker-compose exec backend python manage.py createsuperuser
    ```
