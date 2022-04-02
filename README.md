# 주식 CenterLine 계산기
주식 차트 매매(급등주 눌림 매매)시 매수 타점을 계산하여 결과를 클립보드로 복사하는 사이트입니다.   
기능은 크게 2가지 입니다.   
매수 타점 계산은 클라이언트단(Javascript)에서 수행하고, 서버에는(Django, Mysql) 설정값들을 보관합니다.   
설정값을 보관하기 위해 네이버 로그인 API를 사용하였습니다.   

Link : https://ehdrnsep.cafe24.com/stockcenterline

***

개발목적 : Django를 이용한 간단한 웹개발 학습   
개발기간 : 2022년 3월 26일 ~ 4월 2일 (7일..ㅠㅠ결과물을 보면 자괴감이...)   
학습스펙 : 파이썬 2일, Django 2일   
개발일지 : 아래에 간단하게 개발을 하며 느낀점을 작성하겠습니다.   
   
   
   
## 화면 개발 Html, Bootstrap, Javascript, JQuery
 - 해당 웹은 주로 모바일에서 사용되므로, 반응형 웹을 위해 Bootstrap을 사용하였습니다.
 - 파이참으로 Django 프로젝트 생성 후 DB 모델링 안하고 Html부터 작성하였습니다.
 - CSS는 날 잡고 학습해야되겠다는 생각이 들었습니다. Checkbox Size 키우느냐고 쓴게 다네요..
 ```css
 input[type=checkbox] {
    transform: scale(1.5);
}

.titleWrap{
    display:inline-block;
}
 ```
 - Javascript는 무난하게 다룬거 같고, JQuery에 대한 학습이 필요하다 느꼈습니다.


## 서버 개발 Django, Python, Mysql
 - 화면을 만들고, DB 모델링하고 연동하려니 후회가 들었습니다. Django의 ModelForm을 활용하지 못해서 아쉬웠고, 설정값 저장을 POST로 직접 처리했는데 이게 맞나 싶었습니다.
```python
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
        ...
```
 - 네이버 로그인 API를 참조한 블로그에서 Mixin 이란 네이밍으로 설계한 클래스를 분석했습니다. Django에서는 상속을 Mixin이라고 부르는 것 같았고, Django 학습 2일의 한계를 느꼈습니다.
 - 네이버 로그인 요청 후 Callback이 오면 django.contrib.auth.login 함수를 이용해 로그인 처리를 하고, session을 설정하였습니다. 로그인 처리와 세션 관리가 굉장히 편했습니다.
 - DB에는 User를 Foreignkey로 설정값들을 보관하였습니다.
```python
from django.contrib.auth.models import User
from django.db import models


class Monitoring(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query_count = models.IntegerField('계산횟수', default=0)
    setting_count = models.IntegerField('환경저장횟수', default=0)

    def __str__(self):
        return f"{self.user.username} ({self.query_count})"


class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField('가중치')
    max_value = models.IntegerField('최대값')
    min_value = models.IntegerField('최소값')
    unit = models.IntegerField('단위')
    selected = models.CharField('선택여부', max_length=100)

    def __str__(self):
        return f"{self.user.username} settings"
```
 - Setting 클래스의 selected 라는 필드를 처음에는 Json 형태로 관리하려고 했었습니다. {'항목1':'True', '항목2':False...} 이런식으로 Json 형태로 보관했다가 Javascript에서는 True와 False가 소문자여서 lower 처리를 해서 구현을 했었습니다. 그런데 '항목1','항목2'에 대한 관리가 귀찮게 느껴져서, Json->CharField로 바꾸고, 소문자 boolean으로 이루어진  문자열로 보관하도록 수정하였습니다.
```python
{% if user.is_authenticated %}
    let selected = [{{ setting.selected | safe }}]
    if (valueNames.length == selected.length) {
        for (let i = 0; i < valueNames.length; i++) {
            checkeStatus[i] = selected[i]
        }
    }
{% endif %}
```

## 배포 cafe24, Ubuntu
 
 - 지원 익스플로러 : Edge, Chrome
 - 미지원 익스플로러 : Internet Explorer (개발 다 하고 IE로 열었더니 Javscript ES6 미지원때문에 멘붕오더라구요^^ 프론트앤드 개발자분들 존경..)

프론트앤드 : html, bootstrap4, javascript, jquery
백엔드 : django, 
