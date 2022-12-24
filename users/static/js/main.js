window.addEventListener('scroll', function() {
    const scrollY = this.window.pageYOffset;
    var scrolled = scrollY >= 10; //스크롤된 상태; true or false
    document.querySelector("header").classList.toggle('header_sticky', scrolled);
});

document.addEventListener("DOMContentLoaded", function(){
    user_email = localStorage.getItem("email")
    if(user_email){
        document.querySelector("header .nav-right.navbar_menu").innerHTML = `
            <li class="navbar_item">
                <a href="/mypage.html">
                    MYPAGE
                </a>
            </li>
            <li class="navbar_item">
                <button type=button class="nav_link" onclick="handleLogout()">
                    SIGN OUT
                </button>
            </li>
        `
        const disallow_path = ['/users/signin.html','/users/signup.html']
        const link_pathname =  document.location.pathname;
        if(disallow_path.includes(link_pathname)){
            alert("이미 로그인되어 있습니다");
            location.href = "https://www.mmop-perfume.com/";
        }
    }else{
        const disallow_path = ['/mypage.html','/create_review.html']
        const link_pathname =  document.location.pathname;
        if(disallow_path.includes(link_pathname)){
            alert("로그인한 유저만 접근 가능합니다! 로그인해주세요 :)")
            location.href = "https://www.mmop-perfume.com/users/signin.html";
        }
    }
});


// profile tab jquery
$('.tab_item').on("click",function(e){
    e.preventDefault(); 
    const target_content_id = $(this).find("a").attr("href");
    $(".tab_item").removeClass('active');
    $(this).addClass("active");
    $(".tab_content").removeClass("active");
    $(target_content_id).addClass("active");
})

$(".none_link").on("click",function(e){
    e.preventDefault();
});

async function handleSurveyCheck(){
    const response = await fetch('https://api.mmop-perfume.com/perfume/survey/',{
        headers: {
            "Authorization":"Bearer " + localStorage.getItem("access"),
        },
        method: 'GET',
    }).then(response => {
        if(!response.ok){
            if(response.status==401){
                location.href="https://www.mmop-perfume.com/survey.html"
            }
            throw new Error(`${response.status} 에러가 발생했습니다.`);    
        }
        return response.json()
    }).then(result => {
        const response_json = result;
        if(response_json.length){
            location.href="https://www.mmop-perfume.com/recommend.html"
        }else{
            location.href="https://www.mmop-perfume.com/survey.html"
        }
    }).catch(error => {
        console.warn(error.message)
    });
}

// 1-2. 찜 버튼 클릭 - 찜 지정/해제
async function clickLike(e, el){
    e.preventDefault(); 

    perfume_id = target = el.closest(".item_card").getAttribute("id").replace("perfume_","");
    const response = await fetch('https://api.mmop-perfume.com/perfume/'+perfume_id+'/like/', {
        headers: {
            "Authorization":"Bearer " + localStorage.getItem("access"),
        },
        method: 'POST',
    })
    .then(response => {
        if(!response.ok){
            if(response.status==401){
                alert("로그인한 유저만 접근 가능합니다! 로그인해주세요 :)")
            }
            else if(response.status==404){
                alert("경로가 잘못되었습니다! 다시 입력해주세요 :)")
                location.href="https://www.mmop-perfume.com/";
            }
            throw new Error(`${response.status} 에러가 발생했습니다.`);    
        }
        return response.json()
    }).then(result => {
        const like_status = el.querySelector("i").classList.contains("bi-suit-heart-fill");
        el.querySelector("i").className = like_status ? "bi bi-suit-heart" : "bi bi-suit-heart-fill";
    }).catch(error => {
        console.warn(error.message);
    });
}

// signout
function handleLogout(){
    localStorage.clear()
    alert("로그아웃 되었습니다.")
    location.reload()
};

function gnbSearchPerfume(){
    const search_keyword = document.getElementById("gnb_searchinput").value;
    const search_url = "https://www.mmop-perfume.com/search.html?search="+search_keyword;
    location.href = search_url;
}

document.getElementById("gnb_searchinput").addEventListener("keypress", function(event){
    if(event.keyCode == 13){
        gnbSearchPerfume();
    }
});
