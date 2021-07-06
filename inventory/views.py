from inventory.models import Ingredient
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from django.urls import reverse_lazy
from .forms import add_ingredient, add_menu, add_purchase, update_ingredient, add_required_ingredient, UserCreateForm
from django.shortcuts import redirect
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


# Create your views here.

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class FirstView(TemplateView):
    template_name = "inventory/initial.html"


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredient_list"] = Ingredient.objects.filter(user_check=self.request.user)
        context["menu_items"] = MenuItem.objects.filter(user_check=self.request.user)
        context["purchase_log"] = Purchase.objects.filter(user_check=self.request.user)
        return context


class IngredientsList(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/inventory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredient_list"] = Ingredient.objects.filter(user_check=self.request.user)
        return context


class IngredientsDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/inventory_delete_form.html"
    success_url = reverse_lazy('inventory')


class IngredientsAdd(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "inventory/inventory_add_form.html"
    success_url = reverse_lazy('inventory')
    form_class = add_ingredient

    def post(self, request):
        curr_user = request.user        
        name = request.POST['name']
        quantity = request.POST['quantity']
        unit = request.POST['unit']
        unit_price = request.POST['unit_price']
        ingredient = Ingredient(user_check=curr_user, name=name, quantity=quantity, unit=unit, unit_price=unit_price)

        ingredient.save()
        return redirect("/inventory")


class IngredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/inventory_update_form.html"
    success_url = reverse_lazy('inventory')
    form_class = update_ingredient


class MenuList(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/menu.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = MenuItem.objects.filter(user_check=self.request.user)
        return context



class MenuDelete(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = "inventory/menu_delete_form.html"
    success_url = reverse_lazy('menu_list')


class MenuAdd(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = "inventory/menu_add_form.html"
    success_url = reverse_lazy('menu_list')
    form_class = add_menu

    def post(self, request):
        curr_user = request.user        
        title = request.POST['title']
        price = request.POST['price']
        menuitem = MenuItem(user_check=curr_user, title=title, price=price)

        menuitem.save()
        return redirect("/menu")




class RequiredIngredientsAdd(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = "inventory/requiredingredients_add_form.html"
    success_url = reverse_lazy('menu_list')
    form_class = add_required_ingredient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_item"] = MenuItem.objects.filter(user_check=self.request.user)
        context["ingredient"] = Ingredient.objects.filter(user_check=self.request.user)
        return context


    def post(self, request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        ingredient_id = request.POST["ingredient"]
        ingredient = Ingredient.objects.get(pk=ingredient_id)
        quantity_Required = request.POST["quantity_Required"]
        recipe_requirement = RecipeRequirement(menu_item=menu_item, ingredient=ingredient, quantity_Required=quantity_Required)

        recipe_requirement.save()
        return redirect("/menu")




class Purchase_Log(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["purchase_log"] = Purchase.objects.filter(user_check=self.request.user)
        return context


class PurchaseDelete(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = "inventory/purchase_delete_form.html"
    success_url = reverse_lazy('purchase_log')


class PurchaseAdd(LoginRequiredMixin, TemplateView):
    model = Purchase
    template_name = "inventory/purchase_add_form.html"
    success_url = reverse_lazy('purchase_log')
    form_class = add_purchase

    template_name = "inventory/purchase_add_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [
            X for X in MenuItem.objects.filter(user_check=self.request.user) if X.available()]
        return context

    def post(self, request):
        curr_user = request.user
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(user_check=curr_user, menu_item=menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.quantity -= requirement.quantity_Required
            required_ingredient.save()

        purchase.save()
        return redirect("/purchase_log")


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["purchases"] = Purchase.objects.filter(user_check=self.request.user)
        revenue = Purchase.objects.filter(user_check=self.request.user).aggregate(
            revenue=Sum("menu_item__price"))["revenue"]
        total_cost = 0
        for purchase in Purchase.objects.filter(user_check=self.request.user):
            for recipe_requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += recipe_requirement.ingredient.unit_price * \
                    recipe_requirement.quantity_Required

        context["revenue"] = revenue
        context["total_cost"] = total_cost
        if revenue is not None:
            context["profit"] = revenue - total_cost
        return context


def logout_view(request):
    logout(request)
    return redirect("/")
