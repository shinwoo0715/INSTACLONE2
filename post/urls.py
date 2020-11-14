from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
    path("" , post_list , name='post_list'),
    path("new" , post_new , name='post_new'), # 새로운 post를 만들때 
    path('edit/<int:pk>/' , post_edit , name="post_edit"), # post를 수정할때 edit페이지로 수정하는데 아무글이나 수정하면 안되기때문에 
    path("delete/<int:pk>/", post_delete , name="post_delete"),
    
    # ajax의 url통신을 위한 like, bookmark를 작성 
    path("like" , post_like ,name='post_like'),
    path('bookmark' , post_bookmark , name='post_bookmark'),

    path('comment/new' , comment_new , name='comment_new'),
    path('comment/delete' , comment_delete , name='comment_delete'),
    path('comment_detail/new', comment_new_detail, name='comment_new_detail'),

    path("explore/tags/<tag>/",post_list, name='post_search'),

    path("<int:pk>/" , post_detail , name='post_detail'),

    path("<username>/list/detail" , my_post_list , name='my_post_list'),
]