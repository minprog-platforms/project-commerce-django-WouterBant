from django.contrib import admin
from .models import User, Category, Auction_Listings, Comments, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction_Listings)
admin.site.register(Comments)
admin.site.register(Bid)