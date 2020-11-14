from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import re
from django.conf import settings
from django.db import models 

# Create your models here.

def photo_path(instance , filename):
    from time import strftime
    from random import choice
    import string

    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1] 
    return '{}/{}/{}.{}'.format(strftime('post/%Y/%m/%d/') ,instance.author.username , pid , extension)



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete= models.CASCADE) 
    photo = ProcessedImageField(upload_to=photo_path,
                                            processors=[ResizeToFill(600 , 600)],
                                            format = 'JPEG',
                                            options={'qualty' : 90})
    content = models.CharField(max_length=140 , help_text='최대 길이 140자까지 입력이 가능합니다.')

    tag_set = models.ManyToManyField('Tag' , blank=True)

    # like와 bookmark를 담아줄 field가 필요하다.
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL , blank=True , related_name='like_user_set', through='Like') 
        # throught : Like클래스와 연결 , post.like_user_set으로 접근이 가능하다.

    bookmark_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL , blank=True , related_name='bookmark_user_set', through='Bookmark')  


    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add는 최초에 생성될때 사용하고
    updated_at = models.DateTimeField(auto_now=True) # 업데이트를 할때 현재시간을 재주는 auto_now

    class Meta:
        ordering = ['-created_at'] # 정렬순서를 created_at을 기준으로 정렬해라.
    
    def tag_save(self):
        tags = re.findall(r'#(\w+)\b' , self.content)  #re : 정규표현식 매칭되는 모든 경우를 return한다.

        if not tags:
            return
        
        for t in tags:
            tag, tag_created = Tag.objects.get_or_create(name=t)  # name에 새로운 tag가 추가되었을때 t를 추출해서
            # name에 넣는다.

            self.tag_set.add(tag)    # tag_set 에 tag를 추가한다. 




    # 데코레이터를 활용을 할것이다.
    @property
    def like_count(self):
        return self.like_user_set.count()

    @property
    def bookmark_count(self):
        return self.bookmark_user_set.count()


    def __str__(self):
        return self.content



class Like(models.Model): # like와 bookmark 의 구조가 거의 동일하기 때문에 like를 만들고 복붙을 할예정 
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)     #post 가 삭제가 되면 거기에 딸려있는 like도 삭제가 되기때문에
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = (
            ("user" , 'post') # user와 post는 unique한 관계를 갖게 되어라. 
        )


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE)     #post 가 삭제가 되면 거기에 딸려있는 like도 삭제가 되기때문에
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = (
            ("user" , 'post') # user와 post는 unique한 관계를 갖게 되어라. 
        )

class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE) 
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    content = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.content


class Tag(models.Model):
    name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.name