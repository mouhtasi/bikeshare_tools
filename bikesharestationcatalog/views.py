from django.shortcuts import render


def catalog_home(request):

    return render(request, 'bikesharestationcatalog/catalog.html')
