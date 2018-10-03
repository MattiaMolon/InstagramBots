from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import time
import random

# tempo di download di una pagina (in secondi)
DOWNLOAD_TIME = 4

# tempi di attesa inerenti alle varie azioni (in secondi)
LIKE_TIME = 20
FOLLOW_TIME = 20
COMMENT_TIME = 20
SCROLL_TIME = 0.5

# fa sleep per un numero casuale da 1 a 3 secondi
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
    # ritorna vero o falso per controllarne il corretto funzionamento
    def hit_like(self):
        driver = self.driver
        
        try:
            # cerca il tasto like e lo clicca
            driver.find_element_by_xpath("//button[@class='coreSpriteHeartOpen oF4XW dCJp8']").click()
            return True
        except NoSuchElementException:
            return False


    # clicco follow sulla pagina corrente
    # ritorna vero o falso per controllarne il corretto funzionamento
    def hit_follow(self):
        driver = self.driver

        try:
            # cerca il tasto  follow e lo clicca
            driver.find_element_by_xpath("//button[@class='oW_lN oF4XW sqdOP yWX7d       ']").click()
            return True
        except NoSuchElementException:
            return False       


    # prendi url delle foto da una pagina di ricerca di un hashtag
    # scrolls = numeri di scrolls da fare della pagina (33 link con 0 scrolls + 9 per scroll)
    # hashtag = hashtag ricercato senza # all'inizio
    # ritorna un vettore con gli url delle foto nella pagina
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


    # prendi url delle foto da un profilo di uno user
    # scrolls = numeri di scrolls da fare della pagina (33 link con 0 scrolls + 9 per scroll)
    # user = nome dello user da cui prendere le foto
    # ritorna un vettore con gli url delle foto nella pagina
    def get_user_posts(self, scrolls, user):
        driver = self.driver
        
        # vado nella pagina dello user richiesto
        driver.get("https://www.instagram.com/" + user + "/")
        time.sleep(DOWNLOAD_TIME)

        for i in range(0, scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(DOWNLOAD_TIME)
        
        a_vector = driver.find_elements_by_tag_name("a")
        pic_hrefs = [elem.get_attribute("href") for elem in a_vector]
        pic_hrefs = [href for href in pic_hrefs if "taken-by=" + user in href]

        return pic_hrefs


    # commenta il post corrente con una frase casuale all'interno di comments
    # commets = un vettore contenente i commenti (1 solo nel caso si voglia sempre lo stesso)
    # ritorna vero o falso per controllarne il corretto funzionamento
    def comment_post(self, comments):
        driver = self.driver

        try:
            # cerco la casella di testo e commento
            comment_button = driver.find_element_by_xpath("//button[@class='oF4XW dCJp8']")
            comment_button.click()

            comment_box_elem = driver.find_element_by_xpath("//textarea[@aria-label='Aggiungi un commento...']")
            comment_box_elem.click()
            comment_box_elem.send_keys('')
            comment_box_elem.clear()
            wait_suspect_time()

            # commento un commento casuale in comments
            commento = comments[random.randint(0, len(comments) -1)]
            for lettera in commento:
                comment_box_elem.send_keys(lettera)
                time.sleep(random.randint(1, 7) / 28)
            wait_suspect_time
            comment_box_elem.send_keys(Keys.RETURN)

            return True

        except Exception:
            return False


    # prende nomi dei followers da un determinato user
    # scrolls = numero di scrolls da fare sul pop up dei followers (ogni scroll viene fatto in un tempo SCROLL_TIME)
    # user = nome dello user da cui prendere i nomi
    # ritorna un vettore con i nomi degli utenti ottenuti
    def get_followers_names(self, scrolls, user):
        driver = self.driver

        # vado sulla pagina dello user da cui prendere i followers
        driver.get("https://www.instagram.com/" + user + "/")
        time.sleep(DOWNLOAD_TIME)

        # clicco sul pulsante dei followers
        driver.find_element_by_xpath("//a[@href='/"+ user +"/followers/']").click()
        time.sleep(DOWNLOAD_TIME)

        # eseguo gli scrolls richiesti
        for i in range(0, scrolls):
            driver.execute_script("arguments[0].scrollTop = arguments[1];", driver.find_element_by_class_name("j6cq2"), 10000*i)
            time.sleep(SCROLL_TIME)

        # prendo i nomi
        a_vector = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate _0imsa ']")
        names = [elem.get_attribute("title") for elem in a_vector]

        return names
        

    # prende il nome della persona a cui appartiene il post all'interno della pagina del post
    def get_name_from_post(self):
        driver = self.driver

        nome = "not-found"

        try: 
            # cerco il nome e lo salvo
            nome = driver.find_element_by_xpath("//a[@class='FPmhX notranslate nJAzx']")
            nome = nome.get_attribute("title")
        except Exception:
            pass
        
        return nome
    

    # clicca unfollow sulla pagina corrente
    # ritorna vero o falso per controllarne il corretto funzionamento
    def hit_unfolow(self):
        driver = self.driver

        try:
            driver.find_element_by_xpath("//button[@class='_5f5mN    -fzfL     _6VtSN     yZn4P   ']").click()
            return True
        except:
            return False

