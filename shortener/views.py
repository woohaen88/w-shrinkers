from django.shortcuts import render
from shortener.models import Users as UserModel

# Create your views here.
def index(request):
    user = UserModel.objects.filter(username="admin").first()
    email = user.email if user else "Anonymous Email!"

    if not request.user.is_authenticated:
        email = "Anonymous Email!"

    context = {
        "welcome_msg" : "hi hi hi hi hi hi hi hi hi hi",
        "email" : email
    }
    return render(request, 'index.html', context=context)