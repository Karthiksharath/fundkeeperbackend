from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken

router = DefaultRouter()

router.register('register',views.Signupview,basename='routers')

router.register('expenses',views.ExpenseViewset,basename='expense')

router.register('income',views.IncomeViewset,basename='income')


urlpatterns = [ 
   
   path('token/',ObtainAuthToken.as_view(),name='Token'),
   
   path('expenses/summary/',views.ExpenseSummaryView.as_view(),name='ex_summary'),

   path('incomes/summary/',views.IncomeSummaryView.as_view(),name='in_summary'),

]+router.urls