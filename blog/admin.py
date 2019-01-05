from django.contrib import admin
# import the Post model
from .models import Post

# then register Post so it will be visible on the admin page
admin.site.register(Post)
