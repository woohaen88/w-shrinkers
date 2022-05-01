from django.shortcuts import redirect, render, get_object_or_404
from shortener.forms import SigninForm, SignupForm
from shortener.models import Users as UserModel
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    user = UserModel.objects.filter(id=request.user.id).first()
    email = user.email if user else "Anonymous Email!"

    if not request.user.is_authenticated:
        email = "Anonymous Email!"

    context = {
        "welcome_msg" : "hi hi hi hi hi hi hi hi hi hi",        
    }
    return render(request, 'index.html', context=context)


def url_list(request):
    return render(request, "url_list.html")



# signup
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        msg = "올바르지 않은 데이터입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password =form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원가입완료"
            return redirect('index')                
    else:
        form = SignupForm()
    context = {"form" : form}
    return render(request, 'signup.html', context)


# signin
def signin(request):
    is_ok = False
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():            
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            msg = "올바른 유저 ID와 패스워들 입력하시오"
            try:
                user = UserModel.objects.get(email=email)
            except Exception:
                pass
            else:
                if user.check_password(raw_password):
                    msg = None
                    login(request, user)
                    is_ok = True
                    request.session["remember_me"] = remember_me  
        else:
            messages.error(request, "아이디나 비번 틀림")

    else:
        form = SigninForm()

    context = {"form" : form,
               "msg" : msg,
               "is_ok" : is_ok}
    return render(request, "signin.html", context=context)

def signout(request):
    logout(request)
    return redirect('signin')


@login_required
def list_view(request):
    page = int(request.GET.get("p", 1))
    users = UserModel.objects.all().order_by("-id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "boards.html", {"users": users})
