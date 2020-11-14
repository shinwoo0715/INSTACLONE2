from django.contrib import admin
from .models import Post , Like , Bookmark ,Comment , Tag
from django import forms


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = "__all__"

class LikeInline(admin.TabularInline): # 표의 형식으로 admin 이 정리가 된다. 
    model = Like


class CommentInline(admin.TabularInline): 
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id' , 'author' , 'nickname' , 'content' , 'created_at']
    list_display_links = ['author' , 'nickname' , 'content']
    form = PostForm
    inlines = [LikeInline , CommentInline]

    # 방금 영상에서 실수로 그냥 server를 열었는데 ERROR가 났다. 이유는 우리가 Post Model에다가 nickname을 정의하지 않았기 때문에 정의를 
    # 해야한다.
    def nickname(request , post):
        return post.author.profile.nickname

        # 이러고 서버를 실행하면 admin page에서 에러가 났을것이다. DoesNotExist라고 그러면 settings.py 맨아래로 가서 site뭐시기를 1로 설정



@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id' , 'post', 'user' , 'created_at']
    list_display_links = ['post' , 'user'] # 클릭했을때 link가 있는것 





@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id' , 'post', 'user' , 'created_at']
    list_display_links = ['post' , 'user'] 


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'content' ,'author' , 'created_at']
    list_display_links = ['post' , 'content' , 'author']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display= ['name']
