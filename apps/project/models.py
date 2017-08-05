
from __future__ import unicode_literals
from django.db import models
import re, bcrypt

NAME_REGEX = re.compile(r'[a-zA-Z]')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def register(self, post):
        print post
        first_name = post["first"]
        last_name = post["last"]
        username = post["alias"]
        email = post["email"].lower()
        password = post["password"]
        confirm = post["confirm"]

        # empty strings
        successful = True
        errors = []

        if not NAME_REGEX.match(first_name) or len(first_name) < 2:
            errors.append('First Name can only contain letters and must have at least 2 characters')
            successful = False
            # firstMatch = "First name can only..."
            #passedVAlues.append
        if not NAME_REGEX.match(last_name) or len(last_name) < 2:
            errors.append('Last Name can only contain letters and must have at least 2 characters')
            successful = False
        if not len(username) > 0:
            errors.append('Username cannot be empty')
            successful = False
        if not EMAIL_REGEX.match(email) or len(email) < 1:
            errors.append('Email is not valid')
            successful = False
        if not len(password) >= 8:
            errors.append('Password must be at least 8 characters')
            successful = False
        if not password == confirm:
            errors.append('Passwords do not match')
            successful = False
        if User.objects.filter(email=email).exists():
            errors = ['User with inputted email already exists']
            successful = False

        # only pass back the strings that aren't ""
        if successful == True:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=first_name, last_name=last_name, username = username,
                                        email=email, password=hashed)
            passedValues = [True, user.id]
            return passedValues
        else:
            passedValues = [False, errors]
            return passedValues


    def login(self, post):
        email = post['email'].lower()
        password = post['password']
        logged = [False]
        passedValues = []
        if User.objects.filter(email=email).exists():

            user = User.objects.get(email = email)
            # print "input password = " + bcrypt.hashpw(password.encode(), user.password.encode())
            # print "saved password = " + bcrypt.hashpw(user.password.encode(), user.password.encode())
            if not user.password == bcrypt.hashpw(password.encode(), user.password.encode()):
                logged = [False]
            else:
                logged = [True, user.first_name, user.id]
        return logged

    def edit(self, post, userID):
        email = post['email']
        first = post['first']
        last = post['last']
        current = post['current']
        password = post['password']
        confirm = post['confirm']
        valid = []

        user = User.objects.get(id = userID)

class User(models.Model):
    username = models.CharField(max_length = 30)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class SolutionManager(models.Manager):
    def createSolution(self, post, userID, promptID):
        one = post['one']
        two = post['two']
        three = post['three']

        user = User.objects.get(id = userID)
        prompt = Prompt.objects.get(id = promptID)

        Solution.objects.create(content = one, user = user, prompt = prompt)
        Solution.objects.create(content = two, user = user, prompt = prompt)
        Solution.objects.create(content = three, user = user, prompt = prompt)

class Prompt(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Solution(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name = "solutions")
    prompt = models.ForeignKey(Prompt, related_name = "solutions")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = SolutionManager()

class Collaboration(models.Model):
    name = models.CharField(max_length = 30)
    users = models.ManyToManyField(User, related_name = "collaborations")
    solution = models.ForeignKey(Solution, related_name = "collaborations")

class Like(models.Model):
    user = models.ForeignKey(User, related_name = "likes")
    solution = models.ForeignKey(Solution, related_name = "likes")

class Following(models.Model):
    user = models.ForeignKey(User, related_name = "following")
    following_user = models.ForeignKey(User, related_name = "follower")
