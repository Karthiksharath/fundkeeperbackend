from django.shortcuts import render

from rest_framework import viewsets

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from django.contrib.auth.models import User

from django.utils import timezone

from django.utils.timezone import datetime

from django.db.models import Sum

from api.serializers import UserSerializer,ExpenseSerializer,IncomeSerializer

from rest_framework import authentication,permissions

from api.models import Expense,Income

from api.permissions import OwnerOnly

# viewset , APIview , modelviewset

class Signupview(viewsets.ViewSet):


  def create(self,request,*args,**kwargs):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

      serializer.save()

      return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    else:

      return  Response(data=serializer.errors,status=status.HTTP_404_NOT_FOUND)
    

class ExpenseViewset(viewsets.ModelViewSet):

  queryset = Expense.objects.all()

  serializer_class = ExpenseSerializer

  authentication_classes=[authentication.TokenAuthentication]

  permission_classes = [OwnerOnly]


  def perform_create(self, serializer):

    serializer.save(owner=self.request.user)


  def list(self,request,**kwargs):

    qs = Expense.objects.filter(owner=request.user)

    if 'month' in request.query_params:

      month = request.query_params.get('month')

      qs=qs.filter(created_date__month=month)

    if 'year' in request.query_params:

      year = request.query_params.get('year')

      qs=qs.filter(created_date__year=year)



    if 'category' in request.query_params:

      category=request.query_params.get('category')

      qs=qs.filter(category=category)

    
    if 'priority' in request.query_params:

      priority=request.query_params.get('priority')

      qs=qs.filter(priority=priority)


    if len(request.query_params.keys())==0:

      current_month=timezone.now().month

      current_year=timezone.now().year

      qs=qs.filter(owner=request.user,created_date__month=current_month,created_date__year=current_year)

    serializer = ExpenseSerializer(qs,many=True)

    return Response(data=serializer.data)
  

class ExpenseSummaryView(APIView):

  authentication_classes=[authentication.TokenAuthentication]

  permission_classes = [permissions.IsAuthenticated]

  def get(self,request,*args,**kwargs):


    if "start" in request.query_params and "end" in request.query_params:

      start_date = datetime.strptime(request.query_params.get("start_date"),"%Y-%n-%d").date()

      end_date = datetime.strptime(request.query_params.get("end_date"),"%Y-%n-%d").date()

      all_expense = Expense.objects.filter(owner=request.user,
                                           created_date__range=(start_date,end_date))

    else:

      current_month=timezone.now().month

      current_year=timezone.now().year

      all_expense = Expense.objects.filter(owner=request.user,
                                         created_date__month=current_month,
                                         created_date__year=current_year)
    
    total_expense = all_expense.values("amount").aggregate(total=Sum("amount"))["total"]

    category_summary = all_expense.values('category').annotate(total=Sum('amount')).order_by("-total")

    priority_summary = all_expense.values('priority').annotate(total=Sum('amount')).order_by("-total")

    print(list((category_summary)))


    data = {

       "expense_total":total_expense,
       "category_summary":category_summary,
       "priority_summary":priority_summary
    }

    return Response(data=data)



class IncomeViewset(viewsets.ModelViewSet):

  queryset = Income.objects.all()

  serializer_class = IncomeSerializer

  authentication_classes=[authentication.TokenAuthentication]

  permission_classes = [permissions.IsAuthenticated]


  def perform_create(self, serializer):

    serializer.save(owner=self.request.user)


  def list(self, request, *args, **kwargs):

    qs = Income.objects.filter(owner=request.user)

    if "month" in request.query_params:

      month = request.query_params.get('month')

      qs = qs.filter(created_date__month=month)


    if "year" in request.query_params:

      year = request.query_params.get("year")

      qs=qs.filter(created_date__year=year)


    if "category" in request.query_params:

      category = request.query_params.get("category")

      qs=qs.filter(category=category)


    if len(request.query_params.keys())==0:

      current_month=timezone.now().month

      current_year=timezone.now().year
    
    serializer = IncomeSerializer(qs,many=True)

    return Response(data=serializer.data)
  

class IncomeSummaryView(APIView):

  authentication_classes=[authentication.TokenAuthentication]

  permission_classes=[permissions.IsAuthenticated]


  def get(self,request,*args,**kwargs):

    if "start" in request.query_params and "end" in request.query_params:

      start_date = datetime.strptime(request.query_params.get("start_date"),"%Y-%n-%d").date()

      end_date = datetime.strptime(request.query_params.get("start_date"),"%Y-%n-%d").date()

      all_expense = Income.objects.filter(owner=request.user,created_date__range=(start_date,end_date))

    else:

      current_month = datetime.now().month

      current_year = datetime.now().year

      all_expense = Income.objects.filter(owner=request.user,created_date__month=current_month,created_date__year=current_year)

    total_expense = all_expense.values("amount").aggregate(total=Sum("amount"))['total']

    category_summary = all_expense.values("category").annotate(total=Sum("amount")).order_by("-total")


    data = {"total_expense":total_expense,
            "category_summary":category_summary}
    
    return Response(data=data)




    





  
    




  



















