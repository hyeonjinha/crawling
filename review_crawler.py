import json
import time
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
        
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait

def review_print():
    print("후기 크롤링 시작")
    # css를 찾을때 까지 10초 대기
    time_wait(10, '#mArticle > div.cont_essential > div:nth-child(1) > div.place_details')
    driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div[2]/a[2]').send_keys(Keys.ENTER)
    more = (driver.find_element(By.CSS_SELECTOR, '#mArticle > div.cont_evaluation > div.evaluation_review > .link_more')).text
    while(more != "후기 접기"):
        driver.find_element(By.CSS_SELECTOR,'#mArticle > div.cont_evaluation > div.evaluation_review > .link_more').send_keys(Keys.ENTER)
        more = (driver.find_element(By.CSS_SELECTOR, '#mArticle > div.cont_evaluation > div.evaluation_review > .link_more')).text
        print(more)
        time.sleep(0.3)
    
    
def review_crawler():
    # 리뷰어 정보
    review_list = driver.find_elements(By.CSS_SELECTOR, '.evaluation_review > .list_evaluation > li')
    # 유저 개인 프로필
    user_profiles = driver.find_elements(By.CSS_SELECTOR, '.evaluation_review > .list_evaluation > li > .profile_info')

    # 유저 평균평점, 후기 개수
    user_info = driver.find_elements(By.CSS_SELECTOR, '.unit_info > .txt_desc')

    # 후기 생성 날짜
    review_created = driver.find_elements(By.CSS_SELECTOR, '.unit_info > .time_write')
    
    # 유저 이름
    user_names = driver.find_elements(By.CSS_SELECTOR, '.unit_info > .link_user > .inner_user > .txt_username')

    # 유저 레벨
    user_levels = driver.find_elements(By.CSS_SELECTOR, '.unit_info > .link_user > .inner_user > .badge_info > .txt_badge')

    for i in range(len(review_list)):
        user_review_cnt_index = i * 2
        user_review_avg_index = i * 2 + 1
        print(f"review_list{i} 출력")

        #유저 아이디
        user_id = review_list[i].get_attribute('data-userid')
        print(user_id)

        #유저 이름
        user_name = user_names[i].text
        print(user_name)

        #유저 평균 평점
        user_review_avg = user_info[user_review_avg_index].text
        print(user_review_avg)

        #유저 레벨
        user_level = user_levels[i].text
        print(user_level)

        #유저 리뷰개수
        user_review_cnt = user_info[user_review_cnt_index].text
        print(user_review_cnt)

        dict_temp = {
            'userId': user_id,
            'userName': user_name,
            'averageScore': user_review_avg,
            'level': user_level,
            'reviewCount': user_review_cnt
        }

        user_dict['유저 정보'].append(dict_temp)
        print(f'유저 {user_name} 정보 ...완료')


        #리뷰 생성 날짜
        review_created_date = review_created[i].text
        print(review_created_date)
        
        # 유저 평점 계산
        style_attr = driver.find_element(By.CSS_SELECTOR, '#mArticle > div.cont_evaluation > div.evaluation_review > ul > li:nth-child(1) > div.star_info > div > span > span').get_attribute('style')
        width_match = re.search(r'width: (\d+)%', style_attr)
        width_percentage = int(width_match.group(1))
        score = round((width_percentage / 100) * 5) # width 값에 따라 점수 계산 (예: 100% -> 5점)
        print(score)

        # 리뷰 내용
        try:
            user_description = driver.find_element(By.CSS_SELECTOR, f'#mArticle > div.cont_evaluation > div.evaluation_review > ul > li:nth-child({i+1}) > div.comment_info > p > span').text
            print(user_description)
        except:
            user_description = ''
            print("리뷰 내용 오류")

        dict_temp = {
            'reviewScore': score,
            'description': user_description,
            'normScore' : "normScore", # 추후 추가
            'userId': user_id,
            'restaurnatId': "restaurant_id", # 추후 추가
            #'averageScore': average_score,
            'level': user_level,
            'createAt': review_created_date
        }

        restaurant_review_dict['식당 리뷰 정보'].append(dict_temp)
        print(f'{user_name} ...완료')

        # 유저별 리뷰 모으기
        #profile_info = user_profiles[i].click()
        


url = 'https://place.map.kakao.com/19714690'
driver = webdriver.Chrome() # 크롬창 숨기기
driver.get(url)

user_dict = {'유저 정보': []}
restaurant_review_dict = {'식당 리뷰 정보': []}
# 모든 리뷰 보이게 하기
review_print()
time.sleep(3)
# 가게 별 리뷰 크롤링
review_crawler()

with open('data/user_dict.json', 'w', encoding='utf-8') as f:
    json.dump(user_dict, f, indent=4, ensure_ascii=False)

with open('data/restaurant_review_dict.json', 'w', encoding='utf-8') as f:
    json.dump(restaurant_review_dict, f, indent=4, ensure_ascii=False)