from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import time
import random

# time to download a page (in seconds)
DOWNLOAD_TIME = 4

# different time for each action (in seconds)
LIKE_TIME = 20
FOLLOW_TIME = 20
COMMENT_TIME = 20
SCROLL_TIME = 0.5

# the bot sleep a random time between 1 and 3 seconds
def wait_suspect_time():
    time.sleep(random.randint(1,3))


class InstagramBot:

    # inizializzazione
    # username = username dell'utente
    # password = password dell'utente
    def __init__ (self, username, password):
        self.username = username
        self.password = password
        #inoltre dobbiamo inizializzare anche il driver
        self.driver = webdriver.Firefox()
    

    # login
    def login(self):
        
        # access to the login page
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(DOWNLOAD_TIME)

        # look for the login button
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(DOWNLOAD_TIME)

        # insert name and password
        username_box = driver.find_element_by_xpath("//input[@name='username']")
        username_box.clear()
        for letter in self.username:
            username_box.send_keys(letter)
            time.sleep(random.randint(1,7)/28)

        password_box = driver.find_element_by_xpath("//input[@name='password']")
        password_box.clear()
        for letter in self.password:
            password_box.send_keys(letter)
            time.sleep(random.randint(1,7)/28)
        
        time.sleep(1)
        password_box.send_keys(Keys.RETURN)


    # hit like in current page 
    # return true or false to check the correct workflow
    def hit_like(self):
        driver = self.driver
        
        try:
            # search like button and click it
            driver.find_element_by_xpath("//button[@class='coreSpriteHeartOpen oF4XW dCJp8']").click()
            return True
        except NoSuchElementException:
            return False


    # click follow in the current page
    # return true or false to check the correct workflow
    def hit_follow(self):
        driver = self.driver

        try:
            # search follow button and click it
            driver.find_element_by_xpath("//button[@class='oW_lN oF4XW sqdOP yWX7d       ']").click()
            return True
        except NoSuchElementException:
            return False       


    # take photos' urls forma an hashtag page
    # scrolls = number of scrolls to do in a page (usually 33 link with 0 scrolls + 9 per scroll)
    # hashtag = hashtag searched (without #)
    # return a vector with all the photos' urls
    def get_hashtag_posts(self, scrolls, hashtag):
        driver = self.driver

        # search the hashtag
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(DOWNLOAD_TIME)

        # scroll the page to load the photos
        for i in range(0, scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(DOWNLOAD_TIME)

        # taka the links to the photos
        a_vector = driver.find_elements_by_tag_name("a")
        pic_hrefs = [elem.get_attribute("href") for elem in a_vector]
        pic_hrefs = [href for href in pic_hrefs if "?tagged=" + hashtag in href]

        return pic_hrefs


    # take photos' urls from a profile page
    # scrolls = number of scrolls to do in a page (usually 33 link with 0 scrolls + 9 per scroll)
    # user = name of the user to look for
    # ritorna un vettore con gli url delle foto nella pagina
    def get_user_posts(self, scrolls, user):
        driver = self.driver
        
        # go to the user page
        driver.get("https://www.instagram.com/" + user + "/")
        time.sleep(DOWNLOAD_TIME)

        for i in range(0, scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(DOWNLOAD_TIME)
        
        a_vector = driver.find_elements_by_tag_name("a")
        pic_hrefs = [elem.get_attribute("href") for elem in a_vector]
        pic_hrefs = [href for href in pic_hrefs if "taken-by=" + user in href]

        return pic_hrefs


    # comment the post of the page with a random sentence in comments[]
    # commets = a vector that contains comments
    # return true or false to check the correct workflow
    def comment_post(self, comments):
        driver = self.driver

        try:
            # search the text box
            comment_button = driver.find_element_by_xpath("//button[@class='oF4XW dCJp8']")
            comment_button.click()

            comment_box_elem = driver.find_element_by_xpath("//textarea[@aria-label='Aggiungi un commento...']")
            comment_box_elem.click()
            comment_box_elem.send_keys('')
            comment_box_elem.clear()
            wait_suspect_time()

            # comment a random comment from the vector
            commento = comments[random.randint(0, len(comments) -1)]
            for lettera in commento:
                comment_box_elem.send_keys(lettera)
                time.sleep(random.randint(1, 7) / 28)
            wait_suspect_time
            comment_box_elem.send_keys(Keys.RETURN)

            return True

        except Exception:
            return False


    # take followers names froma a user page
    # scrolls = number of scrolls to do in the followers pop-up (a scroll is done each SCROLL_TIME)
    # user = name of the user from which take the names
    # return a vector containing the names
    def get_followers_names(self, scrolls, user):
        driver = self.driver

        # go to the user page
        driver.get("https://www.instagram.com/" + user + "/")
        time.sleep(DOWNLOAD_TIME)

        # click followers button
        driver.find_element_by_xpath("//a[@href='/"+ user +"/followers/']").click()
        time.sleep(DOWNLOAD_TIME)

        # scroll the pop-up
        for i in range(0, scrolls):
            driver.execute_script("arguments[0].scrollTop = arguments[1];", driver.find_element_by_class_name("j6cq2"), 10000*i)
            time.sleep(SCROLL_TIME)

        # take the names
        a_vector = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate _0imsa ']")
        names = [elem.get_attribute("title") for elem in a_vector]

        return names
        

    # take the name of the person that has the post open in the page
    def get_name_from_post(self):
        driver = self.driver

        nome = "not-found"

        try: 
            # search and save the name
            nome = driver.find_element_by_xpath("//a[@class='FPmhX notranslate nJAzx']")
            nome = nome.get_attribute("title")
        except Exception:
            pass
        
        return nome
    

    # click unfollow on the current page
    # return true or false to check the correct workflow
    def hit_unfollow(self):
        driver = self.driver

        try:
            driver.find_element_by_xpath("//button[@class='_5f5mN    -fzfL     _6VtSN     yZn4P   ']").click()
            return True
        except:
            return False

