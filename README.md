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

***

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

***

## 서버 구축 Cafe24, Ubuntu, Python, Django, Nginx, Gunicorn, Mysql, Git, Https
 - 리누스님께서 AWS와 Nginx를 추천해주셨습니다. 우선 처음하는 배포이고, 개인 사비로 서버를 운영하기 때문에 한국의 저렴한 cafe24로 진행했습니다. 차후에는 AWS로 꼭 진행해보겠습니다.^^
 - cafe24의 일반형으로 설치비 22,000원과 매월 5,500원으로 리눅스 가상서버 호스팅을 진행했습니다.
 ![cafe24](https://user-images.githubusercontent.com/66984636/161368147-36507752-0b1c-4fdf-befa-8d5472e6e892.png)

 - os는 Ubuntu 20.04로 설치하였습니다. Git 설치해서 master 브랜치로 배포를 진행하였습니다. 콘솔에 명령어 치다보니 파이참의 감사함을 느꼈네요.
 - 우선 웹서버는 Django의 디버깅용인 runserver를 이용해서 구동했습니다. 외부에서 웹서버에 접근이 안되서 방화벽에서 8000포트 뚫어주려고 했더니, 방화벽 설정이 아예 안되더라구요. cafe24에 문의 남기고 1시간 후에 잘 해결해주었습니다. 
 
 
 ![image](https://user-images.githubusercontent.com/66984636/161368592-7a1a3466-4f4c-4268-9984-f7b54b0b5a5a.png)

 
 
 - 그 다음은 Nginx + Gunicorn 조합으로 웹서버를 구축했습니다. Nginx와 Gunicorn 통신은 성능을 위해 http->socekt으로 변경하였습니다. 파이참에서 편하게 runserver로 하다가 막상 배포하려고 하니 삽질 많이 했습니다. python manage.py collectstatic으로 static 폴더 복사해주고, Nginx에서 static 폴더 경로 잡아주는데 시간을 많이 잡아먹었습니다. Nginx autoindex on....으....윽
![image](https://user-images.githubusercontent.com/66984636/161368670-0abb017a-29e0-4f71-83e1-eb9f234e46cc.png)


 - 웹서버 구축도 다했으니, 이제 끝난줄알았는데.......클립보드 복사 기능이 동작을 안합니다. navigator.clipboard를 사용했는데, http에서는 보안상 사용 불가하더라구요. 클립보드 기능 때문에 https까지 구축했습니다. Let's Encrypt 보안인증서를 사용했고, certbot의 도움으로 비교적 쉽게 구축한 것 같습니다.
 - https로 구축하니 클립보드가 잘 동작해서, 이제 진짜 끝이라고 생각하는 순간 설마하고 IE로 접속해보았습니다. 하지만..결국 아래와 같이 미지원으로 결정했습니다.

 - 지원 익스플로러 : Edge, Chrome
 - 미지원 익스플로러 : Internet Explorer (개발 다 하고 IE로 열었더니 Javscript ES6 미지원때문에 멘붕오더라구요^^ 프론트앤드 개발자분들 존경..)

 - 현재는 네이버 로그인 API를 사용하기 위해 네이버측에 검수요청을 한 상태로써, 네이버 로그인은 저만 가능한 상태입니다.
 - 주저리 생각나는대로 적어봤는데, 여기까지 읽어주셔서 감사합니다..ㅠ.ㅠ
 - 1주일의 기간동안의 개발 완료 후 느낀점은 아..우선 강의부터 제대로 듣고, Github로 공유해주신 프로젝트들 분석해봐야겠다였습니다. ^^*


