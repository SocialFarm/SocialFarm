from django.db import models

# get_facebook_client lets us get the current Facebook object
# from outside of a view, which lets us have cleaner code
from facebook.djangofb import get_facebook_client

class UserManager(models.Manager):
    """Custom manager for a Facebook User."""
    
    def get_current(self):
        """Gets a User object for the logged-in Facebook user."""
        facebook = get_facebook_client()
        user, created = self.get_or_create(id=int(facebook.uid))
        if created:
            # we could do some custom actions for new users here...
            pass
        return user

class User(models.Model):
    """A simple User model for Facebook users."""

    id = models.IntegerField(primary_key=True)
    rep = models.TextField(null=True)

    objects = UserManager()

class BuisManager(models.Manager):
    """Custom manager for a Buisiness."""
    
    def get_bid(self, bname, badmodel):
        business, created = self.get_or_create(name=bname, admodel=badmodel)
        if created:
            # Run the query again to get auto gen business.id from DB
            business, created = self.get_or_create(name=bname)
        return business

class Business(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=28, unique=True)
    purpose = models.TextField()
    creat_date = models.DateTimeField(auto_now_add=True)
    chair = models.IntegerField(null=True, blank=True)
    admodel = models.IntegerField()
    board = models.TextField(null=True)
    members = models.TextField(null=True)
    cont_rep = models.IntegerField(default=0)
    board_rep = models.IntegerField(default=0)
    other_rep = models.IntegerField(default=0)
    cont_pay = models.IntegerField(default=0)
    board_pay = models.IntegerField(default=0)
    other_pay = models.IntegerField(default=0)

    objects = BuisManager()

class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    creat_date = models.DateTimeField(auto_now_add=True)
    uid = models.IntegerField(null=True, blank=True)
    suid = models.IntegerField(null=True, blank=True)
    bid = models.ForeignKey(Business)
    status = models.IntegerField(null=True, blank=True)
    desc = models.TextField()
    hide = models.IntegerField()
    type = models.CharField(max_length=20)
