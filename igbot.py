from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no sandbox')
#options=chrome_options
webdriver = webdriver.Chrome(ChromeDriverManager().install())
sleep(2)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

username = webdriver.find_element_by_name('username')
username.send_keys('katiehanksxo')
password = webdriver.find_element_by_name('password')
password.send_keys('Follow me don't steal my password!')
button_login = webdriver.find_element_by_css_selector('#loginForm > div > div:nth-child(3) > button')
button_login.click()
sleep(3)

try:
    not_now = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
    not_now.click()
except NoSuchElementException:
    webdriver.close()
    print('Fail, Try Again')
try:
    really_not_now = webdriver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm')
    really_not_now.click()
except NoSuchElementException:
    webdriver.close()
    print('Fail, Try Again')
    
hashtag_list = ['miamifoodies','miamifood']
#Keep track of how many folks you follow
new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0

for hashtag in hashtag_list:
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')

    first_thumbnail.click()
    sleep(randint(1, 2))

    for x in range(1, 400):
        username = webdriver.find_element_by_css_selector(
            'body > div._2dDPU.CkGkG > div.zZYga > div > article > header > div.o-MQd > div.PQo_0 > div.e1e1d > span > a').text

        if username not in prev_user_list:
            # If we already follow, do not unfollow
            if webdriver.find_element_by_css_selector(
                    'body > div._2dDPU.CkGkG > div.zZYga > div > article > header > div.o-MQd > div.PQo_0 > div.bY2yH > button').text == 'Follow':

                webdriver.find_element_by_css_selector(
                    'body > div._2dDPU.CkGkG > div.zZYga > div > article > header > div.o-MQd > div.PQo_0 > div.bY2yH > button').click()

                new_followed.append(username)
                followed += 1

                # Liking the picture
                button_like = webdriver.find_element_by_css_selector(
                    'body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button')

                button_like.click()
                likes += 1
                sleep(randint(18, 25))

                # Comments and tracker
                comm_prob = randint(1, 10)
                print('{}_{}: {}'.format(hashtag, x, comm_prob))
                if comm_prob > 7:
                    comments += 1
                    webdriver.find_element_by_css_selector(
                        'body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span._15y0l > button').click()
                    comment_box = webdriver.find_element_by_css_selector(
                        'body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.sH9wk._JgwE > div > form > textarea')

                    if (comm_prob < 7):
                        comment_box.send_keys('loves it!')
                        sleep(1)
                    elif (comm_prob > 6) and (comm_prob < 9):
                        comment_box.send_keys('thats hot')
                        sleep(1)
                    elif comm_prob == 9:
                        comment_box.send_keys('sanassa!')
                        sleep(1)
                    elif comm_prob == 10:
                        comment_box.send_keys('loves it')
                        sleep(1)
                    # Enter to post comment
                    comment_box.send_keys(Keys.ENTER)
                    sleep(randint(22, 28))
            else:
                print('Error with Follow Button')

            # Next picture
            webdriver.find_element_by_link_text('Next').click()
            sleep(randint(23, 28))

        else:
            print('Error with Username')
            webdriver.find_element_by_link_text('Next').click()
            sleep(randint(21, 27))

print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))

webdriver.close()
