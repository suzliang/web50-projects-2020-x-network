from django.test import TestCase
from django.test import Client, TestCase
from .models import *

# Create your tests here.
class AllTestCase(TestCase):
    def setUp(self):
        # Create users
        u1 = User.objects.create(username="d", password="e")
        u2 = User.objects.create(username="e", password="f")

        # Create likes
        l1 = Like(num=0)
        l1.save()

        # Create comments
        c1 = Comment(user=u2, comment='hi to you too')
        c1.save()

        # Create followings
        f1 = Following(user=u1)
        f1.save()
        f2 = Following(user=u2)
        f2.save()

        # Create posts
        p1 = Post.objects.create(user=u1, text="hi", likes=l1)

    def test_posts_count(self):
        self.assertEqual(Post.objects.all().count(), 1)
    
    def test_likes(self):
        p = Post.objects.get(id=1)
        l = Like.objects.get(id=1)
        u2 = User.objects.get(id=2)

        l.users.add(u2)
        l.num += 1
        l.save()
        p.likes = l
        p.save()
        
        li = p.likes.users.values_list('id', flat=True)
        us = User.objects.filter(id__in = li)

        self.assertTrue(u2 in us)
        self.assertEqual(p.likes.num, 1)

    def test_comments(self):
        p = Post.objects.get(id=1)
        c = Comment.objects.get(id=1)
        p.comments.add(c)

        ci = p.comments.values_list('id', flat=True)
        cs = Comment.objects.filter(id__in = ci)

        self.assertTrue(c in cs)

    def test_following(self):
        u1 = User.objects.get(id=1)
        u2 = User.objects.get(id=2)

        f1 = Following.objects.get(id=1)
        f1.following.add(u2)

        fi = f1.following.values_list('id', flat=True)
        us = User.objects.filter(id__in = fi)

        self.assertTrue(u2 in us)

    def test_follower(self):
        u1 = User.objects.get(id=1)
        u2 = User.objects.get(id=2)

        f2 = Following.objects.get(id=2)
        f2.followers.add(u1)

        fi = f2.followers.values_list('id', flat=True)
        us = User.objects.filter(id__in = fi)

        self.assertTrue(u1 in us)