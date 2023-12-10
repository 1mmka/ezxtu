from django.urls import path, reverse_lazy
from .views import SignUpView,VerifyEmailView, VerificationSuccess, VerificationError, Login, HomePageView, LogOutView, CheckSubRubricDetails, SubrubricDetailsView, ViewUsersPosts, DeleteUserPost, CreateUserPost, UpdateUserPost, CheckedUserPost, ViewUserAnnouncements
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetView , LogoutView

urlpatterns = [
    path('main-page', HomePageView.as_view(), name='home'),
    path('view-rubric-subrubrics/<int:pk>', HomePageView.as_view(), name='view-subrubrics'),
    path('logout', LogOutView.as_view(), name='logout'),
    path('subrubric-details/<int:pk>', CheckSubRubricDetails.as_view(), name='subrubric'),
    path('subrubric-info/<int:pk>', SubrubricDetailsView.as_view(), name='subrubric-info'),
    path('profile/<int:pk>', ViewUsersPosts.as_view(), name='user-profile'),
    path('delete/<int:post_pk>', DeleteUserPost, name='delete-post'),
    path('create-post',CreateUserPost.as_view(),name='create'),
    path('update-post/<int:pk>',UpdateUserPost.as_view(),name='update'),
    path('checked/<int:post_pk>',CheckedUserPost,name='checked'),
    path('annoucements/<int:pk>',ViewUserAnnouncements.as_view(),name='view-announcements'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/<int:user_id>/<str:token>', VerifyEmailView.as_view(), name='verify'),
    path('verify/success', VerificationSuccess.as_view(), name='verify_success'),
    path('verify/error', VerificationError.as_view(), name='verify_error'),
    path('', Login.as_view(), name='login'),
    path('reset/', PasswordResetView.as_view(template_name='password_reset.html'), name='reset'),
    path('reset/<uidb64>/<str:token>', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),  name='password_reset_confirm'),
    path('reset/done/', PasswordResetDoneView.as_view(template_name='reset_done.html'), name='password_reset_done'),
    path('reset/complete/', PasswordResetCompleteView.as_view(template_name='reset_complete.html'), name='password_reset_complete'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
]
