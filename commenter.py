from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import time
import random

class CommenterBot:

    def __init__ (self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)

        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(random.randint(1,3))

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

    # funzione che permette di fare unfollow ai tuoi seguaci
    def execute_comments(self, nomi, post):
        time.sleep(2)
        driver = self.driver
        driver.get(post)
        time.sleep(2)

        comment_button = driver.find_element_by_xpath("//button[@class='oF4XW dCJp8']")
        comment_button.click()

        time.sleep(random.randint(1,3))
        comment_box_elem = driver.find_element_by_xpath("//textarea[@aria-label='Aggiungi un commento...']")
        comment_box_elem.click()
        comment_box_elem.send_keys('')
        comment_box_elem.clear()

        indice = 0
        commenti = 0
        for nome in nomi:

            # scrivo il nome che sto guardando
            comment_box_elem.send_keys("@")
            for lettera in nome:
                comment_box_elem.send_keys(lettera)
                time.sleep(random.randint(1, 7) / 28)
            comment_box_elem.send_keys(' ')

            nomi.remove(nome)
            indice += 1

            if indice == 5:
                comment_box_elem.send_keys(Keys.RETURN)
                indice = 0
                time.sleep(2)
                driver.refresh()
                time.sleep(2)
                comment_button = driver.find_element_by_xpath("//button[@class='oF4XW dCJp8']")
                comment_button.click()

                time.sleep(random.randint(1,3))
                comment_box_elem = driver.find_element_by_xpath("//textarea[@aria-label='Aggiungi un commento...']")
                comment_box_elem.click()
                comment_box_elem.send_keys('')
                comment_box_elem.clear()

                commenti+=1

            if commenti==3:
                driver.close()
                return True


            
   


# prendo i nomi dalla lista
lista = []
f = open("", "r")
for linea in f:
    lista.append(linea)

# post da mirare
post = ""

# bot vero e proprio
#commenter = CommenterBot("pippo.pasticcio", "MM")
#commenter = CommenterBot("best_food_official_2018", "mm")
#commenter = CommenterBot("carlomagnoquelloverofood", "mm")
for i in range(0, 50):
    commenter = CommenterBot("name", "password")
    commenter.login()
    commenter.execute_comments(lista, post)

