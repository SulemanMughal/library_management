from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import *
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from datetime import datetime

def home(request):
    return render(request, 'course/home.html')


def login_user(request):
    if request.method!= 'POST':
        form = loginForm()
    else:
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'Usename or password may have been entered incorrectly.')
                return redirect('login')
    
    return render(request, 'course/login.html', {'form' : form})


@login_required()
def dashboard(request):
    users  =User.objects.all()
    profiles = profileModel.objects.all()
    books = bookModel.objects.all()
    issueBooks = IssueBook.objects.filter(user=request.user)
    context={
        'users' : users,
        'profiles' : profiles,
        'books' : books,
        'issueBooks' : issueBooks,
    }
    if request.user.is_superuser:
        return render(request, 'course/dashboard.html', context)
    return render(request, 'course/dashboard_1.html', context)



def logout_user(request):
    logout(request)
    return redirect('home')



    
def register_user(request):
    if request.method!='POST':
        form = registerForm()
        form_2 = profileInformForm()
    else:
        form = registerForm(request.POST)
        form_2 = profileInformForm(request.POST, request.FILES)
        if form.is_valid() & form_2.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email']
            user.save()
            profile = profileModel.objects.create(user = user)
            profile.contactNumber = form_2.cleaned_data['contactNumber']
            profile.rollNo = form_2.cleaned_data['rollNo']
            profile.profileImage = form_2.cleaned_data['profileImage']
            profile.save()
            current_site = get_current_site(request)
            message = render_to_string('course/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your account.'
            #to_email = form.cleaned_data.get('email')
            to_email = form.cleaned_data.get('email').lower()
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            #return HttpResponse('Please confirm your email address to complete the registration.')
            return render(request, 'course/acc_active_email_confirm.html')
    return render(request, 'course/register.html', {'form' : form, 'form_2' : form_2})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def profileUser(request):
    profile = profileModel.objects.get(user= User.objects.get(username=request.user.username))
    context = {
        'user' : request.user,
        'profile' : profile,
    }
    return render(request, 'course/profile.html', context)


@login_required
def user_information(request, user_id):
    user = User.objects.get(id = user_id)
    profile = profileModel.objects.get(user=user)
    context={
        'user' : user,
        'profile' : profile,
    }
    return render(request, 'course/user_information.html', context)

@login_required
def edit_user_profile(request):
    user = User.objects.get(username= request.user.username)
    profile = profileModel.objects.get(user = user)
    if request.method != 'POST':
        form_1 = EditProfileForm(instance = user)
        form_2 = profileInformForm(instance = profile)
    else:
        form_1 = EditProfileForm(request.POST,instance = user)
        form_2 = profileInformForm(request.POST,request.FILES, instance = profile)
        if form_1.is_valid() & form_2.is_valid():
            user = form_1.save(commit=False)
            # user.set_password(form_1.cleaned_data['password'])
            user.email = form_1.cleaned_data['email']
            user.save()
            profile.contactNumber = form_2.cleaned_data['contactNumber']
            profile.rollNo = form_2.cleaned_data['rollNo']
            profile.profileImage = form_2.cleaned_data['profileImage']
            profile.save()
            return redirect('profile')
    
    context={
        'form_1' : form_1,
        'form_2' : form_2,
    }
    return render(request, 'course/edit_profile.html', context)

@login_required()
def change_password(request):
    if request.method!='POST':
        form = PasswordChangeForm(user = request.user)
    else:
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    
    context={
        'form': form,
    }
    return render(request, 'course/change_password.html' , context)

@login_required
def add_users(request):
    if request.method!='POST':
        form = registerForm()
        form_2 = profileInformForm()
    else:
        form = registerForm(request.POST)
        form_2 = profileInformForm(request.POST, request.FILES)
        if form.is_valid() & form_2.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email']
            user.save()
            profile = profileModel.objects.create(user = user)
            profile.contactNumber = form_2.cleaned_data['contactNumber']
            profile.rollNo = form_2.cleaned_data['rollNo']
            profile.profileImage = form_2.cleaned_data['profileImage']
            profile.save()
            return redirect('dashboard')
    
    context = {
        'form' : form,
        'form_2' : form_2,
    }
    return render(request, 'course/user_create_form.html', context)

@login_required
def books_list(request):
    books = Book.objects.all()
    context = {
        'books' : books,
    }
    return render(request, 'course/books_list.html', context)

@login_required
def book_information(request, book_id):
    book = Book.objects.get(id=book_id)
    book_model = bookModel.objects.filter(book = book)
    context={
        'book' : book,
        'book_model' : book_model,
    }
    return render(request, 'course/book_information.html', context)

@login_required
def book_issue(request, serial_id):
    book = bookModel.objects.get(serialNumber = serial_id)
    user  = User.objects.get(username= request.user.username)
    borrowBook = IssueBook.objects.create(book=book , user=user)
    borrowBook.save()
    book_1 = bookModel.objects.filter(serialNumber=serial_id).update(status = False)
    return HttpResponseRedirect(reverse('book_information', args=[book.book.id]))

def return_Book(request, serial_id):
    book = bookModel.objects.get(serialNumber = serial_id)
    user  = User.objects.get(username= request.user.username)
    borrowBook = IssueBook.objects.get(book=book , user=user)
    borrowBook.delete()
    book_1 = bookModel.objects.filter(serialNumber=serial_id).update(status = True)
    return HttpResponseRedirect(reverse('book_information', args=[book.book.id]))
