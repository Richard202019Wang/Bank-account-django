from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import FormView, ListView, DetailView
from .models import Bank, Branch
from banks.forms import AddForm, AddBranchForm


# Create your views here.

class BankFormView(FormView):
    template_name = 'banks/add.html'
    form_class = AddForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:

            return HttpResponse('UNAUTHORIZED', status=401)
        else:
            return TemplateResponse(request, 'banks/add.html', {'form': AddForm()})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse('UNAUTHORIZED', status=401)
        elif request.user.is_authenticated:
            input_bank = AddForm(request.POST)
            if not input_bank.is_valid():
                return TemplateResponse(request, 'banks/add.html', {'form': input_bank})
            else:
                created_bank = input_bank.save(commit=False)
                created_bank.bank = request.user
                created_bank.save()
                return HttpResponseRedirect(f"/banks/{created_bank.auto_increment}/details/")
        else:
            return HttpResponseNotFound()

    def form_valid(self, form):
        return super().form_valid(form)


class BranchFormView(FormView):
    template_name = "banks/branches_add.html/"
    form_class = AddBranchForm

    def get(self, request, pk):
        if request.user.is_authenticated:
            check_back = get_object_or_404(Bank, pk=pk)
            if request.user.id != check_back.bank.id:
                return HttpResponseForbidden()
            return TemplateResponse(request, 'banks/branches_add.html', {'form': AddBranchForm(), 'pk':pk})
        elif not request.user.is_authenticated:
            return HttpResponse('UNAUTHORIZED', status=401)

        else:
            return HttpResponseNotFound()

    def post(self, request, pk):
        if request.user.is_authenticated:
            check_back = get_object_or_404(Bank, pk=pk)
            if request.user.id != check_back.bank.id:
                return HttpResponseForbidden()
            input_branch = AddBranchForm(request.POST)
            if input_branch.is_valid():
                created_branch = input_branch.save(commit=False)
                created_branch.save()
                check_back.branches.add(created_branch)
                return HttpResponseRedirect(f"/banks/branch/{created_branch.auto_increment}/details/")
            return TemplateResponse(request, 'banks/branches_add.html', {'form': input_branch, 'pk': pk})
        else:
            return HttpResponse('UNAUTHORIZED', status=401)

    def form_valid(self, form):
        return super().form_valid(form)


class AllView(ListView):
    template_name = "banks/all.html"
    queryset = Bank.objects.all()
    context_object_name = "banks"


class BranchDetail(DetailView):
    template_name = "banks/details.html/"
    model = Bank

    def get_context_data(self, *args, **kwargs):
        context = super(BranchDetail,
                        self).get_context_data(**kwargs)
        return context


class Jsondict(DetailView):
    model = Branch

    def get(self, request, pk):
        check_branch = get_object_or_404(Branch, pk=pk)
        branch_dict = {
            "id": check_branch.auto_increment,
            "name": check_branch.name,
            "transit_num": check_branch.transit_num,
            "address": check_branch.address,
            "email": check_branch.email,
            "capacity": check_branch.capacity,
            "last_modified": check_branch.last_modified
        }
        return JsonResponse(branch_dict)


class JsonList(DetailView):
    model = Branch

    def get(self, request, pk):
        check_banks = get_object_or_404(Bank, pk=pk)
        total_bank_info = []
        for bank in check_banks.branches.all():
            total_bank_info += [{
                "id": bank.auto_increment,
                "name": bank.name,
                "transit_num": bank.transit_num,
                "address": bank.address,
                "email": bank.email,
                "capacity": bank.capacity,
                "last_modified": bank.last_modified
            }]

        return JsonResponse(total_bank_info, safe=False)















