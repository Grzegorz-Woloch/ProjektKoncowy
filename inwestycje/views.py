from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from inwestycje.models import Category, Product
from .forms import AddProductForm, LoginForm, ProductModifyForm, CategoryForm, CategoryModifyForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage


def logout_view(request):
    logout(request)
    return redirect('/')


class ProduktyObecne(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(user_id=request.user.id)
        suma = sum([x.profitability for x in products])
        return render(request, 'local_page.html', {'products': products, 'suma': suma})


class ShowThisProduct(LoginRequiredMixin, View):
    def get(self, request, id):
        product = Product.objects.get(pk=id)
        return render(request, 'this_product.html', {'product': product})


class ModifyThisProduct(PermissionRequiredMixin, View):
    permission_required = 'cms.change_product'

    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        form = ProductModifyForm(instance=product)
        return render(request, 'modify.html', context={
            'form': form,
            'product_id': product.id})

    def post(self, request, id):
        form = ProductModifyForm(request.POST, instance=Product.objects.get(pk=id))
        if form.is_valid():
            form.save()
            return redirect('/products')
        return redirect(f"/products{request.POST.get('product_id')}/?error")


class CreateViewWithUser(CreateView):

    def create_object(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return obj

    def form_valid(self, form):
        self.object = self.create_object(form)
        self.object.save()
        return super(CreateView, self).form_valid(form)


class AddProduct(LoginRequiredMixin, CreateViewWithUser):
    form_class = AddProductForm
    template_name = "add_product_form.html"
    success_url = "/products"

    # def get(self, request):
    #     form = AddProductForm()
    #     return render(request, 'add_product_form.html', context={'form': form})
    #
    # def post(self, request):
    #     form = AddProductForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/products')
    #     return render(request, 'add_product_form.html', context={
    #         'form': form,
    #         'error_message': "Wypełnij poprawnie wszystkie pola",
    #     })


class LoginFormView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return redirect('/')
            login(request, user)
            return redirect('products/')
        return render(request, 'login_form.html', context={
            'form': form,
            'error_message': "Wypełnij poprawnie wszystkie pola",
        })


class DeleteObject(LoginRequiredMixin, View):

    def get(self, request, id=None):
        if id is None:
            return render(request, 'delete_product.html', context={})
        product = Product.objects.get(pk=id)
        product.delete()
        return redirect('/products/')


class CategoryForProduct(LoginRequiredMixin, View):
    def get(self, request, id):
        category = Category.objects.get(pk=id)
        return render(request, 'this_product.html', {'category': category})


class AddCategory(LoginRequiredMixin, CreateViewWithUser):
    form_class = CategoryForm
    template_name = "add_category.html"
    success_url = "/products"


class ModifyThisCategory(LoginRequiredMixin, View):
    permission_required = 'cms.change_category'

    def get(self, request, id):
        category = get_object_or_404(Category, pk=id)
        form = CategoryModifyForm(instance=category)
        return render(request, 'modify_category.html', context={
            'form': form,
            'category': category})

    def post(self, request, id):
        form = CategoryModifyForm(request.POST, instance=Category.objects.get(pk=id))
        if form.is_valid():
            form.save()
            return redirect('/products')
        return redirect(f"/products{request.POST.get('category_id')}/?error")


# class ShowCategories(LoginRequiredMixin, View):
#         def get(self, request):
#             category = Category.objects.all()
#             return render(request, 'this_category.html', {'category': category})


class ShowCategories(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'this_category.html', {'categories': categories, })
