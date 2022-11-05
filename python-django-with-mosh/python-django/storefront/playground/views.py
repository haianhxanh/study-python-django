from django.shortcuts import render
from django.http import HttpResponse

# return HttpResponse('Hello World')
# instead of returning the whole HttpResponse we will render the html from our templates
def say_hello(request):
    return render(request, 'hello.html', {'name': 'Hanka'})