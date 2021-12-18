from django.shortcuts import render


def handle_not_found(request, exception):
    return render(request, "404.html")


def handle_server_error(request):
    return render(request, "500.html")
