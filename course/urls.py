from django.conf.urls import url
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from django.urls import path

urlpatterns=[
    url(r'^$', views.home, name="home"),
    url(r'login/', views.login_user, name = 'login'),
    url(r'^dashbaord/$', views.dashboard, name = "dashboard"),
    url(r'^logout/$', views.logout_user, name= "logout"),
    url(r'^register/$', views.register_user, name="register"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^profile/$', views.profileUser, name="profile"),
    url(r'^user/(?P<user_id>\d+)/$', views.user_information, name="inform"),
    url(r'^edit_profile/$', views.edit_user_profile, name = "edit_profile"),
    url(r'^change_password/$', views.change_password, name = "change_password"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset' ),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^user_create/$', views.add_users, name="user_create"),
    url(r'^books_list/$', views.books_list, name="books"),
    url(r'^book/(?P<book_id>\d+)/$', views.book_information, name="book_information"),
    url(r'book_issue/(?P<serial_id>\d+)/$', views.book_issue, name="book_issue"),
        url(r'return_Book/(?P<serial_id>\d+)/$', views.return_Book, name="return_Book")
]