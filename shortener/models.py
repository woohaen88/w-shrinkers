import random
import string
from typing import Dict

from django.contrib.gis.geoip2 import GeoIP2
from django.db import models
from django.contrib.auth.models import User
from shortener.model_utils import dict_filter, dict_slice, location_finder



# Create your models here.

class TimeStampedModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # 기본적으로 이 테이블을 만들려고함
    class Meta:
        abstract = True


class PayPlan(TimeStampedModel):
    name = models.CharField(max_length=20)
    price = models.IntegerField()


class Organization(TimeStampedModel):
    class Industries(models.TextChoices):
        PERSONAL = 'personal'
        RETAIL = 'retail'
        MANUFACTURING = 'manufacturing'
        IT = 'it'
        OTHERS = 'others'

    name = models.CharField(max_length=50)  # 회사이름
    industry = models.CharField(max_length=15, choices=Industries.choices, default=Industries.OTHERS)
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True)


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True)
    url_count = models.IntegerField(default=0)



class EmailVerification(TimeStampedModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, null=True)
    verified = models.BooleanField(default=False)


class Categories(TimeStampedModel):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE)


class ShortenedUrls(TimeStampedModel):
    class UrlCreatedVia(models.TextChoices):
        WEBSITE = "web"
        TELEGRAM = "telegram"

    def rand_string():
        str_pool = string.digits = string.ascii_letters
        return ("".join([random.choice(str_pool) for _ in range(6)])).lower()

    def rand_letter():
        str_pool = string.ascii_letters
        return random.choice(str_pool).lower()

    nick_name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, null=True)
    prefix = models.CharField(max_length=50, default=rand_letter)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    target_url = models.CharField(max_length=2000)
    click = models.BigIntegerField(default=0)
    shortened_url = models.CharField(max_length=6, default=rand_string)
    created_via = models.CharField(max_length=8, choices=UrlCreatedVia.choices, default=UrlCreatedVia.WEBSITE)
    expired_at = models.DateTimeField(null=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "prefix",
                    "shortened_url",
                ]
            )
        ]

    def clicked(self):
        self.click += 1
        self.save()


# statistic
class Statistic(TimeStampedModel):
    class ApproachDevice(models.TextChoices):
        PC = "pc"
        MOBILE = "mobile"
        TABLET = "tablet"

    shortened_url = models.ForeignKey(ShortenedUrls, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    web_browser = models.CharField(max_length=50)
    device = models.CharField(max_length=6, choices=ApproachDevice.choices)
    device_os = models.CharField(max_length=30)
    country_code = models.CharField(max_length=2, default="XX")
    country_name = models.CharField(max_length=100, default="UNKNOWN")
    custom_params = models.JSONField(null=True)

    def record(self, request, url: ShortenedUrls, params: Dict):
        self.shortened_url = url
        self.ip = request.META["REMOTE_ADDR"]
        self.web_browser = request.user_agent.browser.family


        if request.user_agent.is_mobile:
            self.device = self.ApproachDevice.MOBILE
        elif request.user_agent.is_tablet:
            self.device = self.ApproachDevice.TABLET
        else:
            self.device = self.ApproachDevice.PC

        self.device_os = request.user_agent.os.family
        t = TrackingParams.get_tracking_params(url.id)
        self.custom_params = dict_slice(dict_filter(params, t), 5)
        try:
            country = location_finder(request)
            self.country_code = country.get("country_code", "XX")
            self.country_name = country.get("country_name", "UNKNOWN")
        except:
            pass
        url.clicked()
        self.save()


class TrackingParams(TimeStampedModel):
    shortened_url = models.ForeignKey(ShortenedUrls, on_delete=models.CASCADE)
    params = models.CharField(max_length=20)

    @classmethod
    def get_tracking_params(cls, shortened_url_id:int):
        # flat = True  => ["email_id", "ref_by"]
        # flat = False(default) => [{"params": "email_id"}, {"params": "ref_by"}]
        return cls.objects.filter(shortened_url_id=shortened_url_id).values_list("params", flat=True)