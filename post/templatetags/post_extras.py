from django import template
import re

# register는 유효한 tag library를 만들기 위한 모듈 레벨의 인스턴스 객체이다.
register = template.Library()

@register.filter
def add_link(value):
    content = value.content # 전달된 value객체의 content멤버변수를 가져온다. 
    tags = value.tag_set.all() # 전달된 value객체의 tag_set전체를 가져오는 queryset을 리턴한다. 

    for tag in tags:
        # content = re.sub(pattern , repl , content) # content를 pattern으로 검수를 해서 repl로 치환을 할것이다.

        #content = re.sub(r'\#'+tag.name+r'\b', '<a href="/post/explore/tags/'+tag.name+'">#'+tag.name+'</a>', content) 
        content = re.sub(r'\#'+tag.name+r'\b', '<a href="/post/explore/tags/'+tag.name+'">#'+tag.name+'</a>', content)

        # re.sub(pattern, repl, string)	string에서 pattern과 매치하는 텍스트를 repl로 치환한다
        
        return content  # 원하는 문자열로 치환이 완료된 content를 리턴한다.

        
