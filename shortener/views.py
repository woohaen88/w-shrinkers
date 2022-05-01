from django.shortcuts import redirect, render, get_object_or_404
from shortener.forms import SigninForm, SignupForm, urlCreationForm
from shortener.models import Users as UserModel, ShortenedUrls
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
        "welcome_msg": "hi hi hi hi hi hi hi hi hi hi",
    }
    return render(request, 'base.html', context=context)


# url: urls, name="url_list"
def url_list(request):
    get_list = ShortenedUrls.objects.order_by("-created_at").all()
    return render(request, "url_list.html", {"list": get_list})


# signup
# url: signup, name="signup"
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        msg = "올바르지 않은 데이터입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원가입완료"
            return redirect('index')
    else:
        form = SignupForm()
    context = {"form": form}
    return render(request, 'signup.html', context)


# url: signin, name="signin"
def signin(request):
    is_ok = False
    msg = "올바른 유저 ID와 패스워들 입력하시오"
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
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

    context = {"form": form,
               "msg": msg,
               "is_ok": is_ok}
    return render(request, "signin.html", context=context)


# url: signout, name="signout"
def signout(request):
    logout(request)
    return redirect('signin')


# url: urls, name="list_view"
@login_required
def list_view(request):
    page = int(request.GET.get("p", 1))
    users = UserModel.objects.all().order_by("-id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "boards.html", {"users": users})


    # url: urls/create, name="url_create"


@login_required
def url_create(request):
    msg = None
    if request.method == 'POST':
        form = urlCreationForm(request.POST)
        if form.is_valid():
            msg = f"{form.cleaned_data.get('nick_name')} 생성완료"
            messages.add_message(request, messages.INFO, msg)
            form.save(request)
            return redirect("url_list")
        else:
            form = urlCreationForm()
    else:
        form = urlCreationForm()


    context = {"form": form}
    return render(request, "url_create.html", context)


# url_change
@login_required
def url_change(request, action, url_id):
    # post 요청
    if request.method == 'POST':
        url_data = ShortenedUrls.objects.filter(id=url_id)
        if url_data.exists(): # url data가 있으면
            if url_data.first().created_by_id != request.user.id: # url_data의 id비교
                msg = "자신이 소유하지 않은  url입니다."
            elif action == 'delete':
                msg = f"{url_data.first().nick_name} 삭제 완료!"
                url_data.delete()
                messages.add_message(request, messages.INFO, msg)
            elif action == 'update':
                msg = f"{url_data.first().nick_name} 수정 완료!"
                form = urlCreationForm(request.POST)
                form.update_form(request, url_id)
                messages.add_message(request, messages.INFO, msg)


        else:
            msg = "해당 URL정보를 찾을 수 업습니다."

    # get 요청
    elif request.method == 'GET' and action == 'update':
        url_data = ShortenedUrls.objects.filter(pk=url_id).first()
        form = urlCreationForm(instance=url_data)
        return render(request, "url_create.html", {"form": form, "is_update": True})


