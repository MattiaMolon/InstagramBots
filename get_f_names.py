from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import time
import random

class FNamesBot:

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
    def getNames(self, username, scroll_time):
        time.sleep(2)
        driver = self.driver
        driver.get("https://www.instagram.com/" + username + "/")
        time.sleep(2)
        driver.find_element_by_xpath("//a[@href='/"+ username +"/followers/']").click()
        time.sleep(2)

        for i in range(0,scroll_time*2):
            driver.execute_script("arguments[0].scrollTop = arguments[1];", driver.find_element_by_class_name("j6cq2"), 10000*i)
            time.sleep(0.5)
        
        a_vector = driver.find_elements_by_xpath("//a[@class='FPmhX notranslate _0imsa ']")
        names = [elem.get_attribute("title") for elem in a_vector]
        return names



fn = FNamesBot("carlomagnoquelloverofood", "mm")
fn.login()
# in media prende 1500 nomi in 60 secondi
names = fn.getNames("usernameTarget", 60)

# scrivo tutto su di un file
# con open apro il file che mi interessa, con a effettuo un append e 
# con + creo il file nel caso non esista
f = open("/names/mike.txt", "a+")
print("names retrieved : " + str(len(names)) )
for name in names:
    f.write(name + "\n")
f.write("\n")
f.close()
