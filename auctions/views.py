from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Auction_Listings, Comments, Bid


def index(request):
    list_of_listings = Auction_Listings.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "list": list_of_listings,
        "cats": Category.objects.all()
    })

def display_category(request):
    if request.method == "POST":
        cat = request.POST['category']
        cats = Category.objects.get(name=cat)
        list_of_listings = Auction_Listings.objects.filter(active=True, category=cats)
        return render(request, "auctions/index.html", {
            "list": list_of_listings,
            "cats": Category.objects.all()
        })

def addBid(request, id):
    newBid = request.POST['newBid']
    data = Auction_Listings.objects.get(pk=id)
    inwatchlist = request.user in data.watchlist.all()
    allComments = Comments.objects.filter(listing=data)
    isOwner = request.user.username == data.owner.username
    if int(newBid) > data.price.bid:
        updateBId = Bid(user=request.user, bid=int(newBid))
        updateBId.save()
        data.price = updateBId
        data.save()
        return render(request, "auctions/listing.html", {
            "data": data,
            "message": "Bid accepted",
            "accepted": True,
            "allComments": allComments,
            "watchlist": inwatchlist,
            'isOwner': isOwner
        })
    return render(request, "auctions/listing.html", {
                "data": data,
                "message": "Bid failed",
                "accepted": False,
                "allComments": allComments,
                "watchlist": inwatchlist,
                'isOwner': isOwner
            })

def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "cats": Category.objects.all()
        })
    user = request.user
    title = request.POST['title']
    description = request.POST['description']
    price = request.POST['price']
    image_url = request.POST['image url']
    category = Category.objects.get(name=request.POST['category'])
    bid = Bid(bid=float(price),user=user)
    bid.save()
    new_list = Auction_Listings(
        title = title,
        description = description,
        price = bid,
        image = image_url,
        category = category,
        owner = user
    )
    new_list.save()
    return HttpResponseRedirect(reverse(index))

def listing(request, title):
    if request.method == "GET":
        try:
            data = Auction_Listings.objects.get(title=title)
            watchlist=request.user in data.watchlist.all()
        except:
            data = None
            watchlist = False
        allComments = Comments.objects.filter(listing=data)
        isOwner = request.user.username == data.owner.username
        return render(request, "auctions/listing.html", {
            'data': data,
            'watchlist': watchlist,
            'allComments': allComments,
            'isOwner': isOwner
        })

def closeAuction(request, id):
    data = Auction_Listings.objects.get(pk=id)
    data.active = False
    data.save
    allComments = Comments.objects.filter(listing=data)
    isOwner = request.user.username == data.owner.username
    return render(request, "auctions/listing.html", {
            'data': data,
            'watchlist': watchlist,
            'allComments': allComments,
            'isOwner': isOwner,
            'update': True,
            'message': "Auction Closed"
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def removeWatchlist(request, title):
    data = Auction_Listings.objects.get(title=title)
    userNow = request.user
    data.watchlist.remove(userNow)
    return HttpResponseRedirect(reverse("listing", args=(title,)))

def addWatchlist(request, title):
    data = Auction_Listings.objects.get(title=title)
    userNow = request.user
    data.watchlist.add(userNow)

    return HttpResponseRedirect(reverse("listing", args=(title,)))

def watchlist(request):
    userNow = request.user
    data = userNow.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "list": data
    })

def addComment(request, id):
    userNow  = request.user
    data = Auction_Listings.objects.get(pk=id)
    title = data.title
    message = request.POST['newComment']

    newComment = Comments(
        author=userNow,
        listing=data,
        message=message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(title, )))