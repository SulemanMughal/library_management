from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

class profileModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    contactNumber = models.CharField(max_length=20, blank = False, null=False)
    canPOST = models.BooleanField(default =  False)
    rollNo = models.CharField(max_length = 20, blank = False)
    profileImage = models.ImageField(upload_to = 'Image/Files/',blank=False)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Book(models.Model):
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    edition=models.IntegerField()


    def __str__(self):
        return "%s" %self.title
    


    
class bookModel(models.Model):
    book = models.ForeignKey(Book, on_delete = models.CASCADE)
    serialNumber=models.BigIntegerField()
    status = models.BooleanField(default = True)

    def __str__(self):
        return "%s" %(self.book.title)

class IssueBook(models.Model):
    book =  models.ForeignKey(bookModel, on_delete=models.CASCADE, default='')
    user= models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default='')

    def __str__(self):
        return "%s Issued By %s."%(self.book, self.user.username)


        