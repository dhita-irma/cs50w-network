from django.test import TestCase

from .models import *


class ModelsTestCase(TestCase): 

    def setUp(self):

        # Create Users 
        self.user1 = User.objects.create_user(username='Alpha', password='12345')  # Zero following, zero followers
        self.user2 = User.objects.create_user(username='Beta', password='12345')  # 1 following, 1 follower
        self.user3 = User.objects.create_user(username='Charlie', password='12345')  # 2 followings, 2 followers
        self.user4 = User.objects.create_user(username='Delta', password='12345')

        # Create posts
        self.post1 = Post.objects.create(content="Post 1", creator=self.user1)
        self.post2 = Post.objects.create(content="Post 2", creator=self.user2)

        # User2 follow User3
        UserFollowing.objects.create(user=self.user2, following_user=self.user3)

        # User4 follow User3
        UserFollowing.objects.create(user=self.user4, following_user=self.user3)

        # User3 follow User2 and User4
        UserFollowing.objects.create(user=self.user3, following_user=self.user2)
        UserFollowing.objects.create(user=self.user3, following_user=self.user4)

    def test_post_count(self):
        posts = Post.objects.all()
        self.assertEqual(posts.count(), 2)

    def test_post_like(self):
        Like.objects.create(user=self.user1, post=self.post2)
        post_likes = self.post2.likes.all()
        liked_posts = [liked.post for liked in self.user1.liked_posts.all()]
        self.assertEqual(post_likes.count(), 1)
        self.assertCountEqual(liked_posts, [self.post2])

    def test_post_like_count(self):
        Like.objects.create(user=self.user1, post=self.post2)
        Like.objects.create(user=self.user2, post=self.post2)
        Like.objects.create(user=self.user3, post=self.post2)
        like_count = self.post2.like_count()
        self.assertEqual(like_count, 3)

    def test_follow_one_user(self):
        followings = self.user2.get_following_list()
        followers = self.user2.get_followers_list()
        self.assertEqual(followings, [self.user3])
        self.assertEqual(followers, [self.user3])
    
    def test_following_count_zero(self):
        user1_following = self.user1.following.count()
        self.assertEqual(user1_following, 0)

    def test_following_more_than_one(self):
        user3_followings = self.user3.get_following_list()
        following_count = self.user3.following.count()
        self.assertEqual(user3_followings, [self.user2, self.user4])
        self.assertEqual(following_count, 2)

    def test_followers_count_zero(self):
        user1_followers = self.user1.followers.count()
        self.assertEqual(user1_followers, 0)

    def test_followers_more_than_one(self):
        user3_followers = self.user3.get_followers_list()
        follower_count = self.user3.followers.count()
        self.assertEqual(user3_followers, [self.user2, self.user4])
        self.assertEqual(follower_count, 2)
