from django.db import models
import datetime

from django.contrib.auth.models import User


# Create your models here.
class Ingredient(models.Model):
    TABLESPOON = "tbsp"
    POUNDS = "lbs"
    UNIT = "unit"
    OUNCES = "oz"
    GRAMS = "gram"
    LITER = "liter"
    unit_choices = [
        (TABLESPOON, "Tablespoon"),
        (POUNDS, "Pound"),
        (OUNCES, "Ounce"),
        (UNIT, "Unit"),
        (GRAMS, "Gram"),
        (LITER, "Liter"),
    ]

    user_check = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    quantity = models.FloatField(default=0)
    unit = models.CharField(choices=unit_choices, default=UNIT, max_length=200)
    unit_price = models.FloatField(default=0)

    def get_absolute_url(self):     
        return "/ingredients"
    

    def __str__(self):
        return f"{self.name} - {self.unit} -- ${self.unit_price}"




class MenuItem(models.Model):
    user_check = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    price = models.FloatField(default=0)

    def get_absolute_url(self):
        return "/menu"
    
    def available(self):
        return all(X.enough() for X in self.reciperequirement_set.all())

    def __str__(self):
        return f"{self.title} - ${self.price}"




class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_Required = models.FloatField(default=0)

    def __str__(self):
        return f"""
        Item: [{self.menu_item.__str__()}]; 
        Ingredient: {self.ingredient.name}; 
        Quantity: {self.quantity_Required}
        """
    
    def get_absolute_url(self):
        return "/menu"

    def enough(self):
        return self.quantity_Required <= self.ingredient.quantity




class Purchase(models.Model):
    user_check = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return f"""
        Item: [{self.menu_item.__str__()}]; 
        Time: {self.timestamp}
        """

    def get_absolute_url(self):
        return "/purchases"