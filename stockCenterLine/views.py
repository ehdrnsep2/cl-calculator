from django.conf import settings
from django.contrib import messages,auth
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from stockCenterLine.oauth.providers.naver import NaverLoginMixin


def index(request):
    return redirect(reverse('stockCenterLine:clcalc'))


def login(request):
    return render(request, 'stockCenterLine/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect(reverse('stockCenterLine:index'))
    return redirect(reverse('stockCenterLine:login'))


class CenterLineCalc(generic.View):
    template_name = 'stockCenterLine/clcalc.html'
    failure_url = settings.LOGIN_URL

    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            return HttpResponseRedirect(reverse(self.failure_url))

        weight = float(request.POST['weight'])
        min_value = int(request.POST['min'])
        max_value = int(request.POST['max'])
        unit = int(request.POST['unit'])
        selected = []

        for i in range(14):
            selected_name = 'selected' + str(i)
            status = 'false'
            if selected_name in request.POST:
                on_off = request.POST[selected_name]
                if on_off == 'on':
                    status = 'true'
            selected.append(status)

        selected_text = ','.join(selected)

        setting = user.setting_set.first()
        setting.min_value = min_value
        setting.max_value = max_value
        setting.unit = unit
        setting.selected = selected_text
        setting.weight = weight
        setting.save()

        monitoring = user.monitoring_set.first()
        monitoring.setting_count += 1
        monitoring.save()

        return render(request, self.template_name, {'user': user, 'setting': setting})

    def get(self, request):
        user = request.user
        setting = None

        if user.is_authenticated:
            setting = user.setting_set.first()

        return render(request, self.template_name, {'user': user, 'setting': setting})


class NaverCallback(NaverLoginMixin, generic.View):
    client_id = settings.NAVER_CLIENT_ID
    secret_key = settings.SECRET_KEY
    success_url = settings.LOGIN_REDIRECT_URL
    failure_url = settings.LOGIN_URL
    required_profiles = ['email', 'name']
    model = get_user_model()

    def get(self, request, *args, **kwargs):

        provider = kwargs.get('provider')

        if provider == 'naver':  # 프로바이더가 naver 일 경우
            csrf_token = request.GET.get('state')
            code = request.GET.get('code')
            # _compare_salted_tokens 찾을 수 없음...
            # if not _compare_salted_tokens(csrf_token, request.COOKIES.get('csrftoken')):  # state(csrf_token)이 잘못된 경우
            #     messages.error(request, '잘못된 경로로 로그인하셨습니다.', extra_tags='danger')
            #     return HttpResponseRedirect(self.failure_url)
            is_success, error = self.login_with_naver(csrf_token, code)
            if not is_success:  # 로그인 실패할 경우
                messages.error(request, error, extra_tags='danger')
            return HttpResponseRedirect(reverse(self.success_url if is_success else self.failure_url))

        return HttpResponseRedirect(reverse(self.failure_url))

    def set_session(self, **kwargs):
        for key, value in kwargs.items():
            self.request.session[key] = value
