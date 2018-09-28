# da selenium importo varie librerie che mi serviranno in seguito, non so a cosa servono
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


# la libreria time mi permette di manipolare il tempo, mi serve per poter per esempio controllare il timeout 
# del pc per quando riguarda il refresh della pagina web
import time
import random

# creo la classe di cui ho bisogno per far funzionare il bot
class InstagramBot:

    # definisco il costruttore della classe attraverso init.
    # self è identico a this per java o c++ mentre gli altri argomenti sono le variabili della classe
    def __init__ (self, username, password):
        self.username = username
        self.password = password
        #inoltre dobbiamo inizializzare anche il driver
        self.driver = webdriver.Firefox()


    def closeBrowser(self):
        #questo comando chiude la finestra del browser
        self.driver.close()


    # creiamo la funzione che ci permetterà di accedere alla pagina web desiderata in questo caso instagram
    def login(self):
        driver = self.driver

        # il metodo get carica la pagina specificata sul driver
        driver.get("https://www.instagram.com/")

        # ci serve del tempo per aspettare che la pagina si carichi
        time.sleep(2)

        # creo un login button con il pulsante puntato dalla xpath della pagina
        # questa cpath significa -> trova nell'html un qualsiasi elemento a (il tag),
        # che abbia un attributo con nome href e che sia uguale a 'account/login'
        # controllando nell'html l'unico tag simile si riferisce al pulsante di login
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()

        # diamo di nuovo del tempo a browser
        time.sleep(random.randint(1,3))

        # facciamo stessa cosa del pulsante ma con le caselle di testo del login
        username_box = driver.find_element_by_xpath("//input[@name='username']")
        # pulisco la casella di testo
        username_box.clear()
        # send_keys simula la scrittura da tastiera nel caso sia una casella di testo
        for letter in self.username:
            username_box.send_keys(letter)
            time.sleep(random.randint(1,7)/28)

        #stessa cosa con la casella della password
        password_box = driver.find_element_by_xpath("//input[@name='password']")
        password_box.clear()
        for letter in self.password:
            password_box.send_keys(letter)
            time.sleep(random.randint(1,7)/28)
        
        time.sleep(1)
        password_box.send_keys(Keys.RETURN)

    
    # funzione che ci permette di mettere mi piace alle foto di un hashtag
    def like(self, hashtag):
        time.sleep(2)
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # per poter caricare più foto è necessario scorrere la pagina
        for i in range(1, 3):
            # faccio eseguire al driver il comando per scorrere la pagina
            # execute_script serve per eseguire da parte del browser del codice javascript
            # in questo caso usiamo la funzione window.scrollTo(x,y) ce scorre la pagina corrente
            # delle coordinate specificate, nel nostro caso 0 sull'asse delle x e l'altezza 
            # della pagina su quella delle y
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # adesso cerchiamo all'interno della pagina tutti i link alle foto che ci interessano
        # cerco tutti gli elementi con il tag "a"
        a_vector = driver.find_elements_by_tag_name("a")
        # prendo tutti gli href degli elementi in a_vector
        pic_hrefs = [elem.get_attribute("href") for elem in a_vector]
        # filtro il vettore con solo gli href che hanno al loro interno l'hashtag
        # tradotta la riga dopo significa prendo gli href per ogni href all'interno di 
        # pics_href solamente se l'hashtag è presente nella stringa che lo rappresenta
        pic_hrefs = [href for href in pic_hrefs if hashtag in href]

        # controllo se è andato a buon fine
        # print(hashtag + " photos : " + str(len(pics_href)))

        # scorro il vettore e metto mi piace alle foto trovate
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                # cerca il tasto identificato dal testo Like e lo clicca
                driver.find_element_by_xpath("//button[@class='coreSpriteHeartOpen oF4XW dCJp8']").click()
                # 18 perchè è il tempo per istagram che serve a limitare i like in un ora
                # tradotto significa che fa 200 like all'ora
                time.sleep(2)
            except Exception:
                time.sleep(2)


    # funzione che ci permette di mettere follow alle foto di un hashtag
    def follow(self, hashtag, scrolls):
        time.sleep(2)
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        for i in range(1, scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        a_vector = driver.find_elements_by_tag_name("a")
        pic_hrefs = [elem.get_attribute("href") for elem in a_vector]
        pic_hrefs = [href for href in pic_hrefs if hashtag in href]

        # scorro il vettore e metto follow alle foto trovate
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                # cerca il tasto identificato dal testo follow e lo clicca
                driver.find_element_by_xpath("//button[@class='oW_lN oF4XW sqdOP yWX7d       ']").click()
                time.sleep(18)
            except Exception:
                time.sleep(2)

    
    # funzione che permette di fare unfollow ai tuoi seguaci
    def unfollow(self):
        time.sleep(2)
        driver = self.driver
        driver.get("https://www.instagram.com/" + self.username + "/")
        time.sleep(2)
        driver.find_element_by_xpath("//a[@href='/"+ self.username +"/following/']").click()
        time.sleep(2)

        unfollow_buttons = driver.find_elements_by_xpath("//button[@class='oF4XW sqdOP  L3NKy   _8A5w5   ']")
        for button in unfollow_buttons:
            button.click()
            time.sleep(1)
            driver.find_element_by_xpath("//button[@class='aOOlW -Cab_   ']").click()
            time.sleep(random.randint(1,3))

        # funzione che ci permette di mettere follow alle foto di un hashtag
    
    #funzione che commenta sulle foto di uno "user" il "comment"
    def commentAllPhotos(self, user, commenti):
        time.sleep(2)
        driver = self.driver
        driver.get("https://www.instagram.com/" + user + "/")
        time.sleep(2)

        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        a_vector = driver.find_elements_by_tag_name("a")
        pic_hrefs = [elem.get_attribute("href") for elem in a_vector]
        pic_hrefs = [href for href in pic_hrefs if "taken-by=" + user in href]

        # scorro il vettore e metto follow alle foto trovate
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            try:
                comment_button = lambda: driver.find_element_by_xpath("//button[@class='oF4XW dCJp8']")
                comment_button().click()
            except NoSuchElementException:
                pass
            
            try:
                time.sleep(random.randint(1,3))
                comment_box_elem = lambda: driver.find_element_by_xpath("//textarea[@aria-label='Aggiungi un commento...']")
                comment_box_elem().click()
                comment_box_elem().send_keys('')
                comment_box_elem().clear()

                indice = random.randint(0,len(commenti)-1)
                for letter in commenti[indice]:
                    comment_box_elem().send_keys(letter)
                    time.sleep(random.randint(1, 7) / 28)
                
                time.sleep(random.randint(1,3))
                # tre volte perchè uno mi serve per selezionare il nome, il secondo per confermare e il terzo per inviare
                comment_box_elem().send_keys(Keys.RETURN) 
                time.sleep(random.randint(1,2))
                

            except StaleElementReferenceException and NoSuchElementException as e:
                print(e)          

            




IB = InstagramBot("greatfood____2018", "mm")
IB.login()
# IB.like("like4like")

# IB.follow("foodporn", 5)

# for i in range(1, 4):
#   IB.unfollow()
lista = []
f = open("commenti.txt", "r")
for linea in f:
    lista.append(linea)

IB.commentAllPhotos("username", lista)
