from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import time
import random

# tempo di download di una pagina (in secondi)
DOWNLOAD_TIME = 2

# tempi di attesa inerenti alle varie azioni (in secondi)
LIKE_TIME = 20
FOLLOW_TIME = 20
COMMENT_TIME = 20


class InstagramBot:

    # inizializzazione
    # username = username dell'utente
    # password = password dell'utente
    def __init__ (self, username, password):
        self.username = username
        self.password = password
        #inoltre dobbiamo inizializzare anche il driver
        self.driver = webdriver.Firefox()
    

    # effettuo login
    def login(self):
        
        # accedo alla pagina di login
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(DOWNLOAD_TIME)

        # cerco pulsante di login
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(DOWNLOAD_TIME)

        # inserisco nome e password
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


    # clicco like sulla pagina corrente 
    # ritorna vero o falso per controllare se ha funzionato
    def hit_like(self):
        driver = self.driver
        
        try:
            # cerca il tasto like e lo clicca
            driver.find_element_by_xpath("//button[@class='coreSpriteHeartOpen oF4XW dCJp8']").click()
            return True
        except NoSuchElementException:
            return False


    # clicco follow sulla pagina corrente
    # ritorna vero o falso per controllare se ha funzionato
    def hit_follow(self):
        driver = self.driver

        try:
            # cerca il tasto  follow e lo clicca
            driver.find_element_by_xpath("//button[@class='oW_lN oF4XW sqdOP yWX7d       ']").click()
            return True
        except NoSuchElementException:
            return False       


    # prendi url delle foto da una pagina di ricerca di un hashtag, li restituisce in un vettore
    # scrolls = numeri di scrolls da fare della pagina (33 link con 0 scrolls + 9 per scroll)
    # hashtag = hashtag ricercato senza # all'inizio
    def get_hashtag_posts(self, scrolls, hashtag):
        driver = self.driver

        # vado sull'hashag richiesto
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(DOWNLOAD_TIME)

        # scorro la pagina 
        for i in range(0, scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(DOWNLOAD_TIME)

        # prendo i riferimenti alle foto caricate
        a_vector = driver.find_elements_by_tag_name("a")
        pic_hrefs = [elem.get_attribute("href") for elem in a_vector]
        pic_hrefs = [href for href in pic_hrefs if "?tagged=" + hashtag in href]

        return pic_hrefs


