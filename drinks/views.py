from multiprocessing import context
import random
from typing import List
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import DetailView
from django.urls import reverse
from pickle import NONE
from drinks.models import Drinks, Ingredients, Lists

class Home(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        # Get gets search param
        name = self.request.GET.get("ingredient")
        curr_rand_drink =RandomNumber()
        context['curr_rand_drink'] = curr_rand_drink
        # If param, will filter by param
        if name != None:
            context['ingredients'] = Ingredients.objects.filter(ingredient__icontains=name).values()
            context["header"] = f'Ingredients containing "{name}"'
        else:
            context['ingredients'] = Ingredients.objects.all().values()
            context["header"] = "Ingredients"
        return context

class Index(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        # Get gets search param
        name = self.request.GET.get("drink_name")
        curr_rand_drink =RandomNumber()
        context['curr_rand_drink'] = curr_rand_drink
        if name != None:
            context['drinks'] = Drinks.objects.filter(drink_name__icontains=name).values()
            context["headerC"] = f'Cocktails containing "{name}"'
        else:
            context['drinks'] = Drinks.objects.all().values()
        return context

class DrinksCreate(CreateView):
    model = Drinks
    fields = ['drink_name','drink_ingredients', 'recipie', 'glass', 'tags']
    template_name = 'create_cocktail.html'
    def get_success_url(self):
        return reverse('cocktail_show', kwargs={'pk': self.object.pk})

class ListCreate(CreateView):
    model = Lists
    fields = ['list_title','list_descriptions']
    template_name = 'list_create.html'
    def get_success_url(self):
        return reverse('list_show', kwargs={'pk': self.object.pk})

class CocktailShow(DetailView):
    model = Drinks
    template_name = 'cocktail_show.html'
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        curr_rand_drink =RandomNumber()
        context['curr_rand_drink'] = curr_rand_drink
        return context

class ListShow(DetailView):
    model = Lists
    template_name = 'list_show.html'
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        curr_rand_drink =RandomNumber()
        context['curr_rand_drink'] = curr_rand_drink
        return context

class CocktailUpdate(UpdateView):
    model = Drinks
    fields = ['drink_name','drink_ingredients', 'recipie', 'glass', 'tags']
    template_name = 'cocktail_update.html'
    # success_url = '/index/'
    def get_success_url(self):
        return reverse('cocktail_show', kwargs={'pk': self.object.pk})

class ListUpdate(UpdateView):
    model = Lists
    fields = ['list_title','list_descriptions']
    template_name = 'list_update.html'
    # success_url = '/index/'
    def get_success_url(self):
        return reverse('list_show', kwargs={'pk': self.object.pk})

class MyPage(TemplateView):
    template_name = "my_page.html"
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['lists'] = Lists.objects.all().values()
        curr_rand_drink =RandomNumber()
        context['curr_rand_drink'] = curr_rand_drink
        return context

class About(TemplateView):
    template_name = 'about.html'
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        curr_rand_drink =RandomNumber()
        context['curr_rand_drink'] = curr_rand_drink
        return context

def ing_search(request):
    mying = Ingredients.objects.filter(ingredient__icontains='i').values
    template = loader.get_template('ing_search.html') 
    curr_rand_drink =RandomNumber()
    context = {  
        'curr_rand_drink' : curr_rand_drink,
        'mying' : mying,
    }
    return HttpResponse(template.render(context, request))

def RandomNumber():
    var = list(Drinks.objects.all())
    rand_drink = random.sample(var,1)
    print(type(rand_drink[0].id))
    return(int(rand_drink[0].id))
    


