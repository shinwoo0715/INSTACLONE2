from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth import authenticate , login # authenticate : 로그인 인증관련 기능,
from django.contrib.auth import logout as django_logout
from .forms import SignupForm , LoginForm
from .models import Profile , Follow
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def signup(request):
    if request.method == 'POST' : 
        print("post를 지남")
        form = SignupForm(request.POST , request.FILES) # 뒤에 request.FILE을 받은 이유는 우리가 회원가입을 할때
        if form.is_valid():
            user = form.save()
            print("is_valid()추가")
            
            return redirect('accounts:login')
        
        else :
            print("is_valid가 되지 않음")
            return redirect("/post")
    else : # request.POST로 들어오지 않았다는 것은 오류사항이다. 
        print("데이터는 유효하지 않습니다.")
        form = SignupForm()
    
        print("post전달 완료 return 부분임")
    return render(request, 'accounts/signup.html' , {
        'form'  : form ,
    })
    

def login_check(request ):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        name = request.POST.get('username') # username으로 보내진 값을 변수에 저장
        pwd = request.POST.get("password")

        print("name : ",name)
        print("pwd : ", pwd)
        user = authenticate(username=name , password=pwd) 

        if user is not None:
            login(request , user)
            print("로그인 성공")
            return redirect('/post')
        else: 
            print("로그인 실패")
            return render(request , 'accounts/login_fail.html')
    else:
        form = LoginForm()
        return render(request , 'accounts/login.html' , {'form' : form})

def logout(request): # logout은 매우 간단하다 우리가 아까 import한 auth 이다. 
    django_logout(request)
    return redirect('post')


@login_required
@require_POST
def follow(request):
    from_user = request.user.profile
    pk = request.POST.get("pk")
    to_user = get_object_or_404(Profile , pk=pk)
    follow , created = Follow.objects.get_or_create(from_user=from_user , to_user=to_user)

    if created:
        message = '팔로우'
        status = 1
    else: 
        follow.delete()
        message = '팔로우 취소'
        status = 0
    
    context = {
        'message' : message,
        'status' : status,
    }
    return HttpResponse(json.dumps(context) , content_type='application/json')