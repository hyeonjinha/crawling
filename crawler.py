import json
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# --크롬창을 숨기고 실행-- driver에 options를 추가해주면된다
# options = webdriver.ChromeOptions()
# options.add_argument('headless')

url = 'https://map.kakao.com/'
driver = webdriver.Chrome() # 크롬창 숨기기
driver.get(url)
key_word = '부산 금정구 부산대학교 주변 식당'  # 검색어

# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait

# 주차장 정보 출력
def parking_list_print():

    time.sleep(0.2)

	# (3) 장소 목록
    parking_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')
    names = driver.find_elements(By.CSS_SELECTOR, '.head_item > .tit_name > .link_name')
    types = driver.find_elements(By.CSS_SELECTOR, '.head_item > .subcategory')
    address_list = driver.find_elements(By.CSS_SELECTOR, '.info_item > .addr')
    rating = driver.find_elements(By.CSS_SELECTOR, '.rating > .score > .num')
    counts = driver.find_elements(By.CSS_SELECTOR, '.rating > .review')

    for index in range(len(parking_list)):
        print(index)

		# (4) 장소명
        restaurant_name = names[index].text
        print(restaurant_name)

		# (5) 장소 유형
        restaurant_type = types[index].text
        print(restaurant_type)

		# (6) 주소
        address = address_list.__getitem__(index).find_elements(By.CSS_SELECTOR, 'p')
        
        new_addr = address.__getitem__(0).text
        print(new_addr)
        
        old_addr = address.__getitem__(1).text[5:]
        print(old_addr)

        # (7) 별점
        
        average_score = rating[index].text
        print(average_score)

        # (8) 리뷰 개수
        
        review_count = counts[index].text
        review_count = review_count[3:]
        print(review_count)

        # dict에 데이터 집어넣기
        dict_temp = {
            'name': restaurant_name,
            'restaurant_type': restaurant_type,
            'averageScore': average_score,
            'normScore' : "norm_score", # 추가 예정
            'reviewCount': review_count,
            'address1': new_addr,
            'address2': old_addr
        }

        restaurant_dict['식당 정보'].append(dict_temp)
        print(f'{restaurant_name} ...완료')
        
# css를 찾을때 까지 10초 대기
time_wait(10, 'div.box_searchbar > input.query')

# (1) 검색창 찾기
search = driver.find_element(By.CSS_SELECTOR, 'div.box_searchbar > input.query')
search.send_keys(key_word)  # 검색어 입력
search.send_keys(Keys.ENTER)  # 엔터버튼 누르기

sleep(1)

# (2) 장소 탭 클릭
place_tab = driver.find_element(By.CSS_SELECTOR, '#info\.main\.options > li.option1 > a')
place_tab.send_keys(Keys.ENTER)

sleep(1)

# 주차장 리스트
parking_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')

# dictionary 생성
restaurant_dict = {'식당 정보': []}
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
        driver.find_element(By.XPATH, f'//*[@id="info.search.page.no{page2}"]').send_keys(Keys.ENTER)

		# 주차장 리스트 크롤링
        parking_list_print()

		# 해당 페이지 주차장 리스트
        parking_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')
		# 한 페이지에 장소 개수가 15개 미만이라면 해당 페이지는 마지막 페이지
        if len(parking_list) < 15:
            break
		# 다음 버튼을 누를 수 없다면 마지막 페이지
        if not driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').is_enabled():
            break

        # (8) 다섯번째 페이지까지 왔다면 다음 버튼을 누르고 page2 = 0으로 초기화
        if page2 % 5 == 0:
            driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').send_keys(Keys.ENTER)
            page2 = 0

        page += 1

    except Exception as e:
        error_cnt += 1
        print(e)
        print('ERROR!' * 3)

        if error_cnt > 5:
            break

print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
driver.quit()  # 작업이 끝나면 창을 닫는다.

# json 파일로 저장
with open('data/restaurant.json', 'w', encoding='utf-8') as f:
    json.dump(restaurant_dict, f, indent=4, ensure_ascii=False)