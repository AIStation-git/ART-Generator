from django.urls import path
from .views import   UpdateCreditView
#for dashboard
urlpatterns = [
    #buy credit
    path('', UpdateCreditView.as_view(), name='buy'),

]