from django.conf import settings # settings를 가져온다.
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



def user_path(instance, filename): # instance : 포토 모델 , filename : 사용자가 올린 file이름받아오자
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)] # 이게 뭔지 알려면 media의 사진을 보면 
    #알수 있듯이 8자리의 난수 즉 아무 숫자 8자를 만들고 그사진의 이름으로 저장~! 
    pid = ''.join(arr)
    extension = filename.split('.')[-1] # 파일이름의 확장자를 가져올꺼임 ㅅㄱ
    return 'accounts/{}/{}.{}'.format(instance.user.username , pid , extension) # user.username에 맞는 폴더를 하나 만들어 주고 
    



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE) # 사용자 정보를 관리할수 있는 user model을 제공한다.
    # on_delete에서 models.CASCADE가 사용된건 USER가 같을 수는 없기 때문에 USER 하나라는 것을 지정하는것이다. 
    nickname = models.CharField('별명' , max_length=20 , unique=True) # unique 다른 사람 들과 겹치지 않고 유니크를 True로 지정하자
    # 사진

    follow_set = models.ManyToManyField("self" ,
                                                        blank=True,
                                                        through="Follow",
                                                        symmetrical=False)# 비대칭 관계로 적용한다. 즉 한쪽이 팔로우를 했는데 한쪽은 안할수도 있기때문에 
    

    picture = ProcessedImageField(upload_to=user_path, # upload_to : 어디다가 저장할래
                                processors=[ResizeToFill(150, 150)],
                                 format='JPEG',
                                 options={'quality' : 90},
                                 blank=True,) # 저장할때 사진의 크기  
    about = models.CharField(max_length=300 , blank=True) # blank = True라는 것은 비워도 된다는 것을 말한다.
    GENDER_C = ( # 성별을 입력할수 있는 SELECTOR 박스를 만들자 
       ('선택안함' , '선택안함'),
       ('여성' , '여성'),
       ('남성' , '남성'),
    )
    
    gender = models.CharField('성별(선택사항)' , 
                             max_length=10 , choices=GENDER_C,
                             default='N')
    
    def __str__(self): # 외래키 설정 (외래키가 뭔말인지는 잘모르겠지만 일단 오케이)
        return self.nickname

    @property
    def get_follower(self):
        # for문을 돌려 follower_user의 내용을 전체다 가져오고 for문을 돌려서 i.from_user에 넣는것이다. 
        return [i.from_user for i in self.follower_user.all()] # 여기서 follower_user는 방금 밑에다가 추가한 Follow클래스에 related_name에 지정되어 있다.
                                                                        # 또 self.는 즉 profile내용중에~ 이런 의미

    @property
    def get_following(self):
        return [i.to_user for i in self.follow_user.all()]

    @property
    def follower_count(self):
        return len(self.get_follower)
    
    @property
    def following_count(self):
        return len(self.get_following)

    def is_follower(self , user):
        return user in self.get_follower

    def is_following(self , user):
        return user in self.get_following


class Follow(models.Model):
    from_user = models.ForeignKey(Profile,
                                            related_name='follow_user', # 일종의 태그같은 거라고 생각함된다. 팔로잉 , 팔로우 한 사용자의 숫자를 불러올때 이 걸사용한다.
                                            on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile ,
                                            related_name='follower_user',
                                            on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} -> {}".format(self.from_user , self.to_user)
    
    class Meta:
        unique_together = (
            ('from_user' , 'to_user') # 요 두개가 unique한 관계를 갖게된다.
        )