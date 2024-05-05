import crawler
import json
import time
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def user_review_crawler():

    time.sleep(0.2)

	# (3) 각 요소들 전체 긁어오기
    review_list = crawler.driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem')
    names = crawler.driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem > .group_tit > .tit_evaluation > .link_txt')
    ratings = crawler.driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem > .rating > .score > em')
    created_dates = crawler.driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem > .rating > .num_date')
    descriptions = crawler.driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem > .desc_directory')

    for index in range(len(review_list)):
        print(index)

		# 식당 이름
        restaurant_name = names[index].text
        names[index].send_keys(Keys.ENTER)
        print(restaurant_name)

		# 별점
        review_score = ratings[index].text
        print(review_score)

        # 리뷰 내용
        description = descriptions[index].text
        print(description)

        # 생성일자
        created_date = created_dates[index].text
        print(created_date)

        # dict에 데이터 집어넣기
        dict_temp = {
            'returantName': restaurant_name,
            'reviewScore': review_score,
            'description': description,
            'createdAt': created_date,
        }

        user_reviews_dict[f'{user_name}'].append(dict_temp)
        print(f'{restaurant_name} ...완료')

def review_crawler():
    
    # css를 찾을때 까지 10초 대기
    crawler.time_wait(10, '.FavoriteOther > .header > .FavoriteOtherMethodType > .ACTIVE > a')

    # (2) 후기 탭 클릭
    review_tab = crawler.driver.find_element(By.CSS_SELECTOR, '.FavoriteOther > .header > .FavoriteOtherMethodType > .ACTIVE > a')
    review_tab.send_keys(Keys.ENTER)

    sleep(1)

    # 리뷰 리스트
    review_list = crawler.driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem')
    
    # 유저 이름
    global user_name 
    user_name = crawler.driver.find_elements(By.CSS_SELECTOR, '#info\.other > div.header > div > div.FavoriteOtherProfile > div.wrap_user > strong')

    # dictionary 생성
    global user_reviews_dict
    user_reviews_dict = {f'{user_name}': []}

    # 시작시간
    start = time.time()
    print('[크롤링 시작...]')

    # 페이지 리스트만큼 크롤링하기
    page = 1    # 현재 크롤링하는 페이지가 전체에서 몇번째 페이지인지
    page2 = 0   # 1 ~ 5번째 중 몇번째인지
    error_cnt = 0


    if len(review_list) < 15:
        user_review_crawler()
    else:
        while 1:
            # 페이지 넘어가며 출력
            try:
                page2 += 1
                print("**", page, "**")

                # (7) 페이지 번호 클릭
                crawler.driver.find_element(By.XPATH, f'//*[@id="info.search.page.no{page2}"]').send_keys(Keys.ENTER)
                
                # 주차장 리스트 크롤링
                user_review_crawler()

                # 해당 페이지 리뷰 리스트
                review_list = crawler.driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem')

                # 한 페이지에 장소 개수가 15개 미만이라면 해당 페이지는 마지막 페이지
                if len(review_list) < 15:
                    break
                # 다음 버튼을 누를 수 없다면 마지막 페이지
                if not crawler.driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').is_enabled():
                    break

                # (8) 다섯번째 페이지까지 왔다면 다음 버튼을 누르고 page2 = 0으로 초기화
                if page2 % 5 == 0:
                    crawler.driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').send_keys(Keys.ENTER)
                    page2 = 0

                page += 1

            except Exception as e:
                error_cnt += 1
                print(e)
                print('ERROR!' * 3)

                if error_cnt > 5:
                    break

    print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
    
    return user_reviews_dict