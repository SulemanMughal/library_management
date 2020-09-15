from django.contrib import admin

# Register your models here.


from .models import *


admin.site.register(profileModel)
admin.site.register(Book)
admin.site.register(IssueBook)
admin.site.register(bookModel)