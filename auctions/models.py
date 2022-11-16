from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBid")

    def __str__(self):
        return str(self.bid)


class Auction_Listings(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bidPrice")
    image = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    watchlist = models.ManyToManyField(User, related_name="watchlist")

    def __str__(self):
        return self.title

class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    listing = models.ForeignKey(Auction_Listings, on_delete=models.CASCADE, related_name="listing")
    message = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"

