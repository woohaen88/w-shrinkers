from django.shortcuts import redirect, render, get_object_or_404
from shortener.forms import SigninForm, SignupForm
from shortener.models import Users as UserModel
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def index(request):
    print(request.user.pay_plan.name)
    user = UserModel.objects.filter(username=request.user.email).first()
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


# signin
def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():            
            email = form.cleaned_data.get("email")
            user = UserModel.objects.get(email=email)
            raw_password = form.cleaned_data.get("password")
            if user.check_password(raw_password):
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, "아이디나 비번 틀림")

    else:
        form = SigninForm()

    context = {"form" : form}
    return render(request, "signin.html", context=context)

def signout(request):
    logout(request)
    return redirect('signin')