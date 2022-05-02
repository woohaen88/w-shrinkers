from django.contrib import messages
from django.contrib.auth.decorators import login_required
from shortener.forms import urlCreationForm
from shortener.models import ShortenedUrls, Statistic
from django.shortcuts import render, redirect, get_object_or_404
from ratelimit.decorators import ratelimit
from django.contrib.gis.geoip2 import GeoIP2

# url: urls, name="url_list"
from shortener.utils import url_count_changer


def url_list(request):
    get_list = ShortenedUrls.objects.order_by("-created_at").all()
    context = {"list": get_list}
    return render(request, "url_list.html", context)


@login_required
def url_create(request):
    msg = None
    if request.method == 'POST':
        form = urlCreationForm(request.POST)
        if form.is_valid():
            msg = f"{form.cleaned_data.get('nick_name')} 생성완료"
            messages.add_message(request, messages.INFO, msg)
            form.save(request)
            return redirect("urls:url_list")
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
        if url_data.exists():  # url data가 있으면
            if url_data.first().created_by_id != request.user.id:  # url_data의 id비교
                msg = "자신이 소유하지 않은  url입니다."
            else:
                if action == "delete":
                    msg = f"{url_data.first().nick_name} 삭제 완료!"
                    try:
                        url_data.delete()
                    except Exception as e:
                        print(e)
                    else:
                        url_count_changer(request, False)
                if action == "update":
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
        context = {
            "form": form,
            "is_update": True
        }
        return render(request, "url_create.html", context)


@ratelimit(key="ip", rate="10/s")
def url_redirect(request, prefix, url):
    was_limited = getattr(request, "limited", False)
    if was_limited:
        return redirect("index")
    get_url = get_object_or_404(ShortenedUrls, prefix=prefix, shortened_url=url)
    is_permanent = False
    target = get_url.target_url
    if get_url.creator.organization:
        is_permanent = True

    if not target.startswith("https://") and not target.startswith("http://"):
        target = "https://" + get_url.target_url

    custom_params = request.GET.dict() if request.GET.dict() else None
    history = Statistic()
    history.record(request, get_url, custom_params)
    return redirect(target, permanent=is_permanent)