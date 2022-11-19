from django.urls import path

from banks.views import BankFormView, BranchFormView, AllView, BranchDetail, Jsondict, JsonList

app_name = 'banks'

urlpatterns = [
    path('add/', BankFormView.as_view(), name='add'),
    path('<pk>/branches/add/', BranchFormView.as_view(), name='branches_add'),
    path('all/', AllView.as_view()),
    path('<pk>/details/', BranchDetail.as_view()),
    path('branch/<pk>/details/', Jsondict.as_view()),
    path('<pk>/branches/all/', JsonList.as_view()),
]