from django.shortcuts import render
import requests


async def index(request):
    data = {
        'source': 'https://placehold.co/300x300'
    }

    log = ['log1', 'log2', 'log3']
    
    return render(request, 'index.html', {'data': data, 'log': log})
