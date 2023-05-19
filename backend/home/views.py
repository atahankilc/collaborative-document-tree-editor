from django.views import View
from django.shortcuts import render, redirect


class Home(View):
    @staticmethod
    def get(request):
        context = {}
        if 'token' in request.COOKIES:
            context['token'] = request.COOKIES['token']
        return render(request, 'home/base.html', context)


class InvalidPath(View):

    @staticmethod
    def get(request, invalid_path):
        return redirect('home')
