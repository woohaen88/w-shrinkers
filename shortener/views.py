from django.shortcuts import redirect, render
from shortener.forms import SignupForm
from shortener.models import Users as UserModel
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    print(request.user.pay_plan.name)
    user = UserModel.objects.filter(username="admin").first()
    email = user.email if user else "Anonymous Email!"

    if not request.user.is_authenticated:
        email = "Anonymous Email!"

    context = {
        "welcome_msg" : "hi hi hi hi hi hi hi hi hi hi",
        "email" : email
    }
    return render(request, 'index.html', context=context)



# signup
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password =form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')                
    else:
        form = SignupForm()
    context = {"form" : form}
    return render(request, 'signup.html', context)