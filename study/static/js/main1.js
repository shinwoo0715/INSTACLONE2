// js를 할때 우리가 html 코드를 보면 기본적으로 위에서 아래로 읽어드린다. 그러면 뭐 css 읽고 ...내려가서
// js를 읽고 이런식으로 읽는다고 칠때 알아야할건 일단 우리가 js 문서에 const하고 heart를 정의를 했다.
// 하지만 보면 document에있는 class를 찾을 수가 없다. 위에서 아래로 읽기 때문에 찾을수 없다고 error를
// 일으킨다. 그래서 우리는 body 태그 끝지점 마지막에 script src로 정의를 해야한다.

// 그러면 위에다가 정의하고 사용할수는없나? 있다.
// window.addEventListener('DOMContentLoaded' , function(){
// 이안에 다가 우리가 원하는 코드를 작성하면 위에서 아래를 읽고 그리고 js를 로드하라는 것이다.
// })


// #### 하트를 클릭 했을때 불리 들어도게 해보자! ####
//우리가 icon을 클릭하면 클래스에 on이 추가가되는 코드를작성하자
// const heart = document.querySelector(".sprite_heart_icon_outline");
// 근데 잉렇게 icon대상을 직접적으로 가져오는 것보다 대상의 '부모'에게서 가져오는 것이 효율적이다.

const heart = document.querySelector(".heart_btn");
const header = document.querySelector("#header");
const sidebox = document.querySelector(".side_box");
// const variableWidth =  document.querySelector('.contents_box .contents')
const variableWidth = document.querySelectorAll('.contents_box .contents');
// 여기서 All로 하는 이유는 각각의 게시글모두 적용이 되어야되서 이렇게 querySelectorAll를 해주어야한다.
// 쉽게 얘기해서 python 기준으로 얘기하면 얘네들이 모두 a = [ 1,2,3, 4, 5 ...] 이렇게 들어간다는 것이다.
//그래서 for 구문을 이용해서 모든 게시물을 다룰수있다.
const delegation = document.querySelector('.contents_box');

// function heartToggle(){
//   console.log("hit!");
//   heart.classList.toggle("on");
// }
// heart.addEventListener('click' , heartToggle);



// 자 잘되는 것지만 큰 문제점이 있다. querySelector의 특성상 하나의 Selector만 가져올수 있다.
// 그렇게 되면 게시글이 많아지면 다른게시글에는 좋아요를 클릭할수 없다.
// 그러면 querySelectorAll을 쓰면되는 것이 아니냐 이럴수 있는데 얘특성은 배열로 들어온다는 것이다.
// 그렇게 되면 addEventListener를 각각 지정을 해주어야한다. 아주 번거롭기 때문에 우리는 다른 기술을 쓸것이다.
function scrollFunc() {
  
  //  innerHeight , innerWIdth , outerWidth , outerHeight 를 알고 싶으면 url : [  https://sometimes-n.tistory.com/22 ]
  let scrollHeight = Math.ceil(pageYOffset + window.innerHeight);
  let documentHeight = document.body.scrollHeight;

  // 우리가 스크롤을 얼마나했는지 값을 찾으려면
  console.log("scrollHeight : "+scrollHeight);
  console.log("documentHeight : "+documentHeight);
 

  // 우리가 하나 알아야하는 것이 있다. main.js로다가 우리가 다방면하게 사용할것인데 만약 side_box가 없으면
  // error가 일어납니다. 그래서 조건문을 걸어야합니다.

  if (pageYOffset >= 10) {
    // page를 10이상으로 내리면 header클래스에 on클래스를 만들자
    header.classList.add('on');

    if (sidebox) {  // sidebox가 있을 경우에만 on을 쳐넣어라.( 여기서 on은 css로 fixed를 걸어둔 상태 )
      sidebox.classList.add('on');
    }
    resizeFunc();

  } else if (pageYOffset < 10) {
    header.classList.remove('on');

    if (sidebox) {
      sidebox.classList.remove('on');
      // sidebox가 원위치로 즉 10미만이 될때 우리가 지정해둔 side_box.on 의 left가 지정이 되어있어서
      // 10미만이면 sidebox.on을 없애라 ( left: 1000px ) 얘를 없애야 오른쪽 끝으로 가지 않는다.
      sidebox.removeAttribute('style');
    } 
  }

  // scrollHegith 와 documentHeight 가 같은경우에는 즉 맨~밑으로 내려갔을때 post를 불러와라.
  if ( scrollHeight >= documentHeight ){
    let page = document.querySelector('#page').value;
    
    //  여기서 문제는 계속해서 post가 마오기 때문에 아까 page의 value값을 1개씩
    //올려서 제어를 하자
    
    // 여기서 parseInt  계산을 해주는 애라고 보면된다. 
    document.querySelector("#page").value = parseInt(page) + 1; 
    // page 가 하나씩 나올 때마다 하나씩 page의 value값을 count를 한다. 

    callMorePostAjax(page);

    if (page > 5){
      return;
    }
  }

}


function callMorePostAjax(page){

  
  if (page > 5){
    return;
  }

  $.ajax({
    type: "POST",
    url : "../../templates/post.html",
    data : {
      "page" : page,
    },
    dataType : "html" ,
    success : addMorePostAjax,
    error: function (request, status, error) {
      alert("문제가 발생했습니다.");
    }
  })
}

function addMorePostAjax(data){
  
  delegation.insertAdjacentHTML("beforeend" , data);

}


// sidebox를 fixed하려면 right: 0이 아닌 left로 값을 주어야한다. 그러면 우리가 준 변수를 기준으로 주어야한다.
function resizeFunc() {
  // 화면에 변화를 줄수돌 resize는 출력이된다.
  if (pageYOffset >= 10) {
    // innerWidth : 우리 모니터에 가로길이 그거에 /2 를 변수에 저장하고
    let calcWidth = window.innerWidth / 2 + 165;
    // console.log(window.innerWidth / 2);

    sidebox.style.left = calcWidth + "px";
    // 근데 이렇게 하면 완벽하지만 다시올릴때 left값이 resize로 지정이 되서 오른쪽 끝으로 간다. 이것없애려면
    // left값을 없애는 것도 있고 또 style을 없애는 것이 있다. 하지만 두 번째 것이 더 편하다.
  };// if end

  // css로 반응형을 만들때의 media를 js로 만들어보자
  if (matchMedia('screen and (max-width: 800px)').matches) {
    // 조금씩 편차를 두는 것이 좋다. 그래서 -20 정도 약간 더 작아보이게 해서 px값을 지정을 해준다.

    // variableWidth의 querySelectorAll을 이용한 유사배열 for구문으로 모든 게시물에 width적용하기
    for (let i = 0; i < variableWidth.length; i++) {
      variableWidth[i].style.width = window.innerWidth - 20 + "px"; // 여기서 우리가 -20을한 이유는 모바일로 볼때 약간씩 삐걱거려서
    }

  } // 그러면 이제 800초과가 되었을때에는 width값이 사라져야한다 ( 현재 사라지지 않고 800이 초과가 되도 그대로 width값이
  //남아 있는 것을 알수 있다.) 그래서 else를 사용해보자
  else {
    for (let i = 0; i < variableWidth.length; i++) {

      // contents의 css의 max-width가 614보다 높은 px단위
      if (window.innerWidth >= 600) {
        variableWidth[i].removeAttribute('style');
      }
    }
  }
}

function delegationFunc(e) { // event객체를 받는다 ( 결과 : 내가클릭한 html태그가 나옴 ) 클릭한 대상들이 나온다.
  let elem = e.target;
  console.log("delegation 함수 진입");
  console.log(e.target);

  // 예외적으로 잘못된 부분을 클릭했을 때를 만들어야한다.
  while (!elem.getAttribute('data-name')) { // 아 html 속성중에 data-name자체가 없으면 그냥 함수 end해라 .
    elem = elem.parentNode; // elem의 부모 parentNode라는 것을 찾아야한다.

    if (elem.nodeName === "BODY") { // 만약에 찾다가 body라는게 나오면 elem에게 null을 주고 끝내라. nodeName(TagName이라고 생각하셈)
      elem = null;
      console.log("함수는 실행을 못합니다.");
      return; // return 은 이 함수를 자체를 끝내버리는 속성이있다.
    }
  }


  // ## 여기에는 모두 toggle이 들어가야한다. 클래스를 넣다 뺏다 해야한다.  ##
  // element가 맞냐고 비교를 해야하니까
  // 여기서 matches를 할건데 , classname으로 하면 중복될가능성이 있으니까 data_name을 사용 할것이다.
  if (elem.matches("[data-name='heartbeat']")) { // html코드의 data-name속성이 heartbeat
    // 너가 클릭한 element 대상에 data-name에 heartbeat를 가지고 있으면 이부분을 실행해라.
    console.log("하트!");
    // 근데 이렇게 하면 console창에 아무것도 나오지 않는다. 왜냐 heart-icon에는 data-name자체가없다. 그래서
    //우리가 heart-icon에 추가를 한다. data-name을 iconsField에 icons를 모두 data-name을 추가해보도록하자



    $.ajax({// ajax를 이용해서 좋아요를 눌렀을 때 1이 증가하는 모습을 web으로 보여주자
      type: "POST",
      url: "../data/like.json",
      data: 37,
      dataType: 'json', // 우리가 생각하는 그런 데이터 타입이 맞고 보통 json데이터 타입을 많이씀
      success: function (response) { //위에 있는 type , url 등등이 성공적으로 통신이 되었을때 실행해라
        console.log("response 지나감");

        let likeCount = document.querySelector("#like-count-37");
        likeCount.innerHTML = "좋아요" + response.liek_count + "개";
      },
      error: function (request, status, error) { // error 가 났을 경우를 대비하여 이렇게 예외처리를 해야한다.
        alert("로그인이 필요합니다.");
        // window.location.replace("");
      }
    })


  } else if (elem.matches("[data-name='bookmark']")) {

    console.log("북맠!");

    let pk = elem.getAttribute("name");

    $.ajax({
      type: 'POST',
      url: "../data/bookmark.json",
      data: 37,
      dataType: 'json',
      success: function (response) {
        let bookmarkCount = document.querySelector("#bookmark-count-37");
        bookmarkCount.innerHTML = '북마크' + response.bookmark_count + '개';
      },
      error: function (request, status, error) {
        alert("로그인이 필요합니다.");
      }
    })


  } else if (elem.matches("[data-name='comment']")) { // 댓글 달기
    console.log("진짜");
    // 일단 우리가 input에 작성한 글들을 가져올 수가 있어야 한다.
    let content = document.querySelector("#add-comment-post-37>input[type=text]").value;
    console.log(content);

    if (content.length > 140) {
      alert("댓글은 최대 140자까지 입력이 가능합니다. : " + content.length);
      return;
    }

    $.ajax({
      type: 'POST',
      url: '../../templates/comment.html',
      data: {
        'pk': 37,
        'content': content,
      },
      dataType: 'html',
      success: function (data) {
        document.querySelector('#comment-list-ajax-post37').insertAdjacentHTML("afterbegin", data);
      },
      error: function (request, status, error) {
        alert("문제가 발생했습니다.");
      }
    });

    document.querySelector("#add-comment-post-37>input[type=text]").value = '';

  } else if (elem.matches("[data-name='comment-delete']")) {

    $.ajax({
      type: 'POST',
      url: "../data/delete.json",
      data: {
        'pk': 37,
      },
      dataType: 'json',
      success: function (response) {
        if (response.status) { // 여기서 status는 delete.json으로 가면 
          //status가 있는데 그게 1이냐 0이냐에 따라 삭제가 되었냐 안되었냐로 구분을 지을 것이다. 
          let comt = document.querySelector(".comment-detail");
          comt.remove();
        }
      },
      error: function (request, status, error) {
        alert("문제가 발생했습니다.");
      }
    })

  } else if (elem.matches("[data-name='follow']")) {

    $.ajax({
      type: 'POST',
      url: "../data/follow.json",
      data: {
        'pk': 37,
      },
      dataType: 'json',
      success: function (response) {
        if (response.status) {
          document.querySelector("input.follow").value = '팔로잉'; // input에 follow라는 클래스가 붙어 있으면
        } else {
          document.querySelector("input.follow").value = '팔로워';
        }
      },
      error: function (request, status, error) {
        alert("문제가 발생했습니다.");
      }


    });

  }

  console.log("on 붙이기");
  elem.classList.toggle('on');
}


//새로 고침을 하면 현재는 그자리에 즉 우리가 위치했더 height자리에 있는데 이걸 새로고침을 하면 맨위로 올라가게 해보도록하자
setTimeout(function () {
  // scrollTo(0 , 0) ;// 0의 0으로 돌아가
  scrollTo(0, 0)
}, 100);// 0.01초


// resize 창크기를 줄이면 resize function이 실행이 된다.
// resize를 하는이유는 : 반응형적으로 우리가 창을 움직였을때 또는 모바일로 웹을 볼때
// 우리가 다량의 사진을 스와이프하며 사진을 넘길때 해상도가 깨지거나 약간씩 흔들리는 현상을 볼수 있다.

// article(content)의 좌우값이 reisze를 하게되면 화면 크기에 맞춰서 좌우값이 유지가 되어야한다.
window.addEventListener('resize', resizeFunc);
window.addEventListener('scroll', scrollFunc);

if (delegation) { // contents_box가 다른데는 없을 수도 있기 때문에 이렇게 조건문을 단다.
  // window.addEventListener('click' , delegationFunc);
  console.log("delegation 함수 실행");
  delegation.addEventListener('click', delegationFunc); // 위에서의 window에서만이 아닌 delegation 즉 contents_box
}else{
  console.log("delegation이 없습니다.");
}
