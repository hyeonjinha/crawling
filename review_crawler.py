#import crawler
import json
import time
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# css 찾을때 까지 10초대기
def css_time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait


def xpath_time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait


def user_review_crawler():

    time.sleep(1)

	# (3) 각 요소들 전체 긁어오기
    review_list = driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem')
    names = driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem > .group_tit > .tit_evaluation > .link_txt')
    #ratings = driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem > .rating > .score > em')
    created_dates = driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem > .rating > .num_date')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem > .desc_directory')

    tmp_review_dict = {f'{user_name}' : []} 
    for index in range(len(review_list)):
		# 식당 이름
        restaurant_name = names[index].text
        print(restaurant_name)
       
		# 별점
        style_attr = driver.find_element(By.CSS_SELECTOR, f'#other\.review > ul > li:nth-child({index+1}) > div.rating > span.score > span.backgroundStar > span').get_attribute('style')
        
        try:
            width_match = re.search(r'width: (\d+(\.\d+)?)px', style_attr)
            width_percentage = float(width_match.group(1))
        except:
            width_match = re.search(r'width: (\d+)px', style_attr)
            width_percentage = int(width_match.group(1))
          
        review_score = round((width_percentage / 68) * 5) # width 값에 따라 점수 계산 (예: 100% -> 5점)
        print(review_score)

        # 리뷰 내용    
        description = descriptions[index].text
        print(description)

        # 생성일자
        created_date = created_dates[index].text
        print(created_date)

        # dict에 데이터 집어넣기
        dict_temp = {
            'restaurantName': restaurant_name,
            'reviewScore': review_score,
            'description': description,
            'createdAt': created_date,
        }

        tmp_review_dict[f'{user_name}'].append(dict_temp)
        

    user_reviews_dict['유저별 리뷰 정보'].append(tmp_review_dict)
    print(f'{user_name} ...완료')


def review_crawler():
    
    # css를 찾을때 까지 10초 대기
    css_time_wait(10, '#info\.other > div.header > div > div.FavoriteOtherMethodType')

    # (2) 후기 탭 클릭
    review_tab = driver.find_element(By.XPATH, '//*[@id="info.other"]/div[1]/div/div[3]/ul/li[2]/a')
    review_tab.send_keys(Keys.ENTER)

    sleep(1)

    # 리뷰 리스트
    review_list = driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem')
    
    # 유저 이름
    global user_name 
    user_name = driver.find_elements(By.CSS_SELECTOR, '#info\.other > div.header > div > div.FavoriteOtherProfile > div.wrap_user > strong')

    # dictionary 생성

    # 시작시간
    start = time.time()
    print('[크롤링 시작...]')

    # 페이지 리스트만큼 크롤링하기
    page = 1    # 현재 크롤링하는 페이지가 전체에서 몇번째 페이지인지
    page2 = 0   # 1 ~ 5번째 중 몇번째인지
    error_cnt = 0


    while 1:
        # 페이지 넘어가며 출력
        try:
            page2 += 1
            print("**", page, "**")

            # (7) 페이지 번호 클릭
            try:
                driver.find_element(By.XPATH, f'//*[@id="other.review.page.no{page2}"]').send_keys(Keys.ENTER)
            except:
                print('단일 페이지')
            
            # 주차장 리스트 크롤링
            user_review_crawler()

            # 해당 페이지 리뷰 리스트
            review_list = driver.find_elements(By.CSS_SELECTOR, '.list_body > .FavoriteEvaluationItem')

            # 한 페이지에 장소 개수가 15개 미만이라면 해당 페이지는 마지막 페이지
            if len(review_list) < 15:
                break
            # 다음 버튼을 누를 수 없다면 마지막 페이지
            if not driver.find_element(By.XPATH, '//*[@id="other.review.page.next"]').is_enabled():
                break

            # (8) 다섯번째 페이지까지 왔다면 다음 버튼을 누르고 page2 = 0으로 초기화
            if page2 % 5 == 0:
                driver.find_element(By.XPATH, '//*[@id="other.review.page.next"]').send_keys(Keys.ENTER)
                page2 = 0

            page += 1

        except Exception as e:
            error_cnt += 1
            print(e)
            print('ERROR!' * 3)
            if error_cnt > 10:
                break


    print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
    #print(user_reviews_dict)
    #return user_reviews_dict

with open('C:.\\data\\user_profile_links_dict.json', 'r') as f:

    json_data = json.load(f)

links = json_data['links']

global user_reviews_dict
user_reviews_dict = {'유저별 리뷰 정보': []}

for link in links:
    driver = webdriver.Chrome() # 크롬창 숨기기
    driver.get(link)
    review_crawler()
    driver.quit()

try:
    with open('data/user_reviews_dict.json', 'w', encoding='utf-8') as f:
        json.dump(user_reviews_dict, f, indent=4, ensure_ascii=False)
except Exception as e:
    print('Error occurred while saving the data:', str(e))
