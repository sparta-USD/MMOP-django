![Screenshot 2022-12-28 at 9 53 1](https://user-images.githubusercontent.com/12287842/209815571-7c1f2521-5f39-44c2-a89a-d951f5ff9bbd.png)

## 🦕 팀원 소개
USD팀은 ’Ulsan(울산), Seoul(서울), Daejeon(대전) 사람들이 모여 달러를 휩쓸자!’ 라는 포부를 담은 팀입니다.
<br>
|Type|Name|Position| Github|
|:------:|:------:|:-------:|:-------:|
|팀장|이현지|`BE` `FE` `PM`|https://github.com/LeeHyunji|
|팀원|박수인|`BE` `FE`|https://github.com/ssuin52|
|팀원|이동영|`BE` `FE`|https://github.com/kvkvd12|
|팀원|정현주|`BE` `FE`|https://github.com/hyunjooooojung|
|팀원|최해민|`BE` `FE`|https://github.com/haeminchoi2|

<br>

## ⏱ 개발기간
- 2022.12.01 ~ 22.12.28 (4주)

<br>

## 👏 서비스 소개
### MMOP : Make My Own Perfume  👉 [MMOP 바로가기](https://www.mmop-perfume.com) 
  - "  **MMOP**  " 나만의 커스텀 향수를 제작하고 나의 취향에 맞는 향수를 추천 받아볼 수 있는 플랫폼입니다.

<br> 

### 서비스 주요 기능

![서비스 주요 기능](https://user-images.githubusercontent.com/12287842/209777769-06e965ac-2bfc-44de-abe6-8a8a77785112.png)

#### **1. 향수 비교 분석 기능**
- 영국 기반의 온라인 향수 리소스 플랫폼인  Basenotes에 기반한 데이터를 크롤링해 수집해 향수 상세 정보를 제공합니다.
    - 인기있는 브랜드 데이터 73개
    - 인기있는 향수  데이터 3595개
    - 향 데이터 3752개
- 유저가 원하는 향수를 찾기 위해서 제품명/브랜드명/향이름_영문/향이름_한글 검색을 지원합니다.
- 유저의 니즈에 맞게 향수를 비교하기 위해 최신순/인기순/리뷰순 으로 정렬을 지원합니다.
- 각 향수마다 리뷰를 작성할 수 있고 유저가 향수 리뷰를 비교 분석 할 수 있습니다.
- 유저가 선호하는 제품을 찜 선택할 수 있어서 본인의 취향을 비교할 수 있습니다.


#### **2. 향수 추천 시스템**
- 향수 선호도 설문이나 작성된 리뷰 제품의 향 데이터를 바탕으로 
TF-IDF 로 제품을 분석하여(Content-based Recommendation)을 하여 기존에 유저가 사용했던 향수나 선호하는 향수와 비슷한 향을 가진 향수를 추천합니다.
- 특정 제품의 특징을 추출해 TF-IDF 로 제품을 분석(Content-based Recommendation) 해당 제품과 유사한 향수를 추천해 줍니다.


#### **3. 커스텀 향수 제작**
- 향 선택/ 용기 선택 / 패키지 로고 디자인 선택의 3단계를 거쳐 커스텀 향수 제작 프로세스가 진행됩니다.
- 커스텀 제작 가능한 900여개 향 / 50여개의 용기 데이터를 사용하여 유저의 취향을 반영한 커스텀 향수를 제작할 수 있습니다.
- 향 데이터 기반으로 유저가 선호하는 향수와 비슷하게 커스텀 하여 제작할 수 있습니다.


#### **4. 회원**
- 카카오 소셜 로그인 API를 통한 간편 로그인 기능

<br>
<br>

## 🎬 서비스 시연 영상
[![ USD팀 - MMOP 시연영상](https://img.youtube.com/vi/a4ZZ7-G4N5g/0.jpg)](https://youtu.be/a4ZZ7-G4N5g)

<br>
<br>


## 📚 서비스 아키텍처
![Web App Reference Architecture V2 (3)](https://user-images.githubusercontent.com/12287842/209769210-aa431409-81f1-4b12-b4be-60565a9bf30d.png)

<br>
<br>

## 🛠 서비스 기술 스택
### Front
<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> <img src="https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jQuery&logoColor=black"> <img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white"> <img src="https://img.shields.io/badge/kakao Develop-FFCD00?style=for-the-badge&logo=kakao&logoColor=white"> <img src="https://img.shields.io/badge/Swiper-6332F6?style=for-the-badge&logo=Swiper&logoColor=white">

### Backend
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/Django REST framework-A30000?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JWT&logoColor=white">
<img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=Ubuntu&logoColor=white"> <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"> <img src="https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=NGINX&logoColor=white"> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=PostgreSQL&logoColor=white"> <img src="https://img.shields.io/badge/Amazon EC2-FF9900?style=for-the-badge&logo=Amazon EC2&logoColor=white"> <img src="https://img.shields.io/badge/Amazon Load Balancer-FF9900?style=for-the-badge&logo=Amazon AWS&logoColor=white"> <img src="https://img.shields.io/badge/Amazon S3-569A31?style=for-the-badge&logo=Amazon S3&logoColor=white"> <img src="https://img.shields.io/badge/Amazon CloudFront-569A31?style=for-the-badge&logo=Amazon AWS&logoColor=white"> <img src="https://img.shields.io/badge/Amazon Route53-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white">


### Tool
<img src="https://img.shields.io/badge/GIT-F05032?style=for-the-badge&logo=Git&logoColor=white"> <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white">

<br>

## 📗 DB설계
![USD팀  최종프로젝트 - MMOP](https://user-images.githubusercontent.com/12287842/209769638-c6b9e8d4-7b6d-4646-8828-a7f3116d594f.png)

<br>

## 📕 API명세서
### <a href="https://github.com/sparta-USD/MMOP-django/wiki/API-%EB%AA%85%EC%84%B8%EC%84%9C#users%EC%95%B1-api">User 앱 API</a>
title | method | url 
-- | -- | -- 
로그인 API | POST | `/users/signin/`
이메일 인증 API | POST | `/users/activate/<str:uidb64>/<str:token>/`
회원가입 API | POST | `/users/signup/`
카카오로그인 API | POST | `/users/oauth/callback/kakao/`
비밀번호 초기화 메일 전송 API | POST | `/users/password_reset/`
비밀번호재설정 API | POST | `/users/password_reset_confirm/<uidb64>/<token>`
마이페이지 조회 API | GET | `/users/`
개인정보 및 비밀번호 수정 API | PUT | `/users/`

<br>

### <a href="https://github.com/sparta-USD/MMOP-django/wiki/API-%EB%AA%85%EC%84%B8%EC%84%9C#perfume%EC%95%B1-api">Custom_Perfume 앱 API</a>
title | method | url 
-- | -- | -- 
커스텀 향수 목록 조회  API | GET | `/custom_perfume/`
커스텀 향수 생성 API | POST | `/custom_perfume/`
커스텀 향수 상세 조회 API | GET | `/custom_perfume/<int:custom_perfume_id>/`
커스텀 향수 삭제 API | DELETE | `/custom_perfume/<int:custom_perfume_id>/`

<br>

### <a href="https://github.com/sparta-USD/MMOP-django/wiki/API-%EB%AA%85%EC%84%B8%EC%84%9C#custom_perfume-%EC%95%B1-api">Perfume 앱 API</a>
title | method | url 
-- | -- | -- 
향수 목록 조회 API | GET | `/perfume/`
향수 목록 simple API | GET | `/perfume/simple/`
향수 추천 선호도조사 조회 API | GET | `/perfume/survey/`
향수 추천 선호도조사 생성 API | POST | `/perfume/survey/`
향수 추천 리스트 조회 API | GET | `/perfume/recommend/`
특정향수에 따른 추천향수 리스트 조회 API | GET | `/perfume/<int:perfume_id>/recommend/`
브랜드 목록 조회 API | GET | `/perfume/brand/`
브랜드 상세 조회 API | GET | `/perfume/brand/<int:brand_id>/`
브랜드 랜덤 조회 API | GET | `/perfume/brand/random/`
리뷰 목록 조회 API | GET | `/perfume/<int:perfume_id>/reviews/`
리뷰 생성 API | POST | `/perfume/<int:perfume_id>/reviews/`
리뷰 수정 API | PUT | `/perfume/reviews/<int:review_id>/`
리뷰 삭제 API | DELETE | `/perfume/reviews/<int:review_id>/`
찜 생성 API | POST | `perfume/<int:perfume_id>/like/`
찜 해제 API | DELETE | `perfume/<int:perfume_id>/like/`

<br>

## 🗣 사용자 피드백
<a href="https://github.com/sparta-USD/MMOP-django/wiki/%EC%82%AC%EC%9A%A9%EC%9E%90-%ED%94%BC%EB%93%9C%EB%B0%B1">👉 사용자 피드백 보러가기 </a>

<br>

## 🎯 트러블 슈팅
<a href="https://github.com/sparta-USD/MMOP-django/wiki/%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85">👉 트러블 슈팅 보러가기 </a>
