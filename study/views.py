from django.shortcuts import render , redirect , get_object_or_404


def index(request):
    print("index.html 진입")

    return render(request , 'index.html')


def layout(request):
  return render(request  ,'layout.html')


def post_like(request, pk):
  post = get_object_or_404(Post, pk=pk)
  # 중간자 모델 Like 를 사용하여, 현재 post와 request.user에 해당하는 Like 인스턴스를 가져온다.
  post_like, post_like_created = post.like_set.get_or_create(user=request.user)

  if not post_like_created:
    post_like.delete()

    return redirect('post:post_list')