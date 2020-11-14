from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['username' , 'password']



class SignupForm(UserCreationForm):
    username = forms.CharField(label='사용자명', widget=forms.TextInput(attrs={
        'pattern': '[a-zA-Z0-9]+',
        'title': '특수문자, 공백 입력불가',
    }))
    
    nickname = forms.CharField(label='닉네임')
    picture = forms.ImageField(label='프로필 사진', required=False)
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)
        
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if Profile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('이미 존재하는 닉네임 입니다.')
        return nickname
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('사용중인 이메일 입니다.')
        return email

    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if not picture:
            picture = None
        return picture
    
    def save(self):
        user = super().save()
        Profile.objects.create(
            user=user,
            nickname=self.cleaned_data['nickname'],
            picture=self.cleaned_data['picture'],
        )
        return user


#  class SignupForm(UserCreationForm):
#     username = forms.CharField(label="사용자명" , widget=forms.TextInput(attrs={
#         "pattern" : "[a-zA-Z0-9]+",
#         "title" : "특수문자 , 공백 입력불가 다시 확인해주세요.",
#     }))

#     nickname = forms.CharField(label='닉네임')
#     picture = forms.ImageField(label='프로필사진' , required=False) # required꼭 필요한것이 아니다. ( 프로필 사진) 

#     class Meta(UserCreationForm.Meta): # Meta라는 부분은 그대로 보내준다고 보면된다.
#         fields = UserCreationForm.Meta.fields + ("email" , )

#     def clean_nickname(self) : # 이것은 !! 유효성 검사이다. 내가 적은 nickname인 존재하는지 확인하는 함수
#         nickname = self.cleaned_data.get('nickname') # 입력한 nickname을 nickname변수에 넣어 검사
#         if Profile.objects.filter(nickname=nickname).exists():
#             raise forms.ValidationError("이미 존재하는 닉네임 입니다.")
#         return nickname
    
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         User = get_user_model() # user모델을 통채로 가져와서 user에 넣습니다.
#         if User.objects.filter(email=email).exists(): # exists로 확인해서 이미존재한다면 실행해라
#             raise forms.ValidationError('사용중인 이메일 입니다.')
#         return email
    
#     def clean_picture(self):
#         picture = self.cleaned_data.get("picture")
#         if not picture: # picture에 아무것도 없다면 None을 주어라
#             picture = None
#         return picture

#     def save(self):
#         user = super().save()
#         Profile.objects.create(
#             user=user,
#             nickname = self.cleaned_data['nickname'],
#             picture = self.cleaned_data['picture']
#         )
#         print("return되기 직전")
#         return user