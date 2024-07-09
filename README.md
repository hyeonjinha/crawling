# 진짜 맛집 찾기
https://github.com/20kee/cloud-term-project
해당 프로젝트를 진행하기 위한 유저별/식당별 평점,리뷰 크롤러 
## 배경
- 각 식당마다 많은 리뷰가 달려있지만 진짜 유의미한 평점 제시가 목표
- 항상 낮은 별점을 주는 사람과 항상 높은 별점을 주는 사람이 매긴 별점은 가치가 다름
- 각 유저별 평균 평점을 이용해 합리적인 평점을 제공하는 서비스 제공
- https://github.com/20kee/cloud-term-project

1. crawler.py : 전체 크롤러 통합
2. review_crawler.py : 각 가게 별 리뷰 + 리뷰 남긴 유저의 정보
3. user_crawler.py : 유저가 작성한 전체 리뷰
