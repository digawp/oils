from django.shortcuts import render


def search(request):
    ctx = {
        
    }
    return render(request, 'opac/search.html', ctx)
