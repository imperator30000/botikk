# Всё что связано с парсингом
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import common
from time import sleep
from fuzzywuzzy import process  # частичное сравнение
import random  # для вывода рандомных картинок


class Ass_bot:
    def __init__(self, name):
        name = str(name)
        self.name = name
        self.run = False
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Скрытый режим браузера
        self.driver = webdriver.Chrome(options=self.chrome_options)  # открываем окно браузера в скрытом режиме
        # self.driver = webdriver.Chrome()

        # словарь со всеми командами и вариантами ответов
        self.opts = {
            "language": {
                "ru": ("русский", "russian"),
                "en": ("английский", "english")
            },
            "otv": {"a_yes": 'да', "a_no": 'нет', "Я не знаю": "a_dont_know", "a_probably": 'возможно частично',
                    "a_probaly_not": 'скорее нет не совсем', "end_game": 'закончить игру'},
            "menu": {"a_propose_yes": "да", "a_propose_no": "нет"}
        }

    def comparison(self, text, arr):  # функция проверки ответа пользователя
        name = process.extractOne(text, arr)
        if name[1] < 80:  # Проверка на правильный ввод
            print(name)
            return [False, False, False]
        print(name)
        return name

    def main(self, lan="ru"):  # определяем язык бота
        self.driver.get(f"https://" + lan + ".akinator.com")
        self.run = True
        sleep(3)  # Даём сайту полностью  загрузится
        try:
            self.driver.find_element(By.CLASS_NAME, "btn-play").click()  # Начинаем игру
        except common.exceptions.ElementNotInteractableException:
            self.driver.find_elements(by=By.CLASS_NAME, value="modal-content")[1].find_element(
                by=By.CLASS_NAME, value="modal-header").find_element(
                by=By.CLASS_NAME, value="close").click()
            sleep(3)
            self.driver.find_element(By.CLASS_NAME, "btn-play").click()
        print(self.driver.current_url)
        self.question()

    def otvet(self, text):
        sleep(3)
        if text == "end_game":
            self.driver.quit()
            self.run = False
            return "end_game"
        if text:
            self.driver.find_element(By.ID, text).click()  # отвечаем на вопрос
            return True

    def question(self):
        sleep(3)
        try:  # проверяем идёт ли у нас игра или нет
            # Если не смогли получить вопрос выходим из цикла игра
            question = self.driver.find_element(by=By.CLASS_NAME, value="bubble-body").text
            return question  # Вопрос
        except common.exceptions.NoSuchElementException:
            return False  # Не удалось получить вопрос

    def end_game(self):
        sleep(3)

        who_1 = self.driver.find_element(by=By.CLASS_NAME, value="sub-bubble-propose").text  # Я думаю это
        who_2 = self.driver.find_element(by=By.CLASS_NAME, value="proposal-title").text  # Имя персонажа
        m = who_1.lower() + " " + who_2
        image = self.driver.find_element(by=By.CLASS_NAME, value='proposal-area').find_element(
            by=By.TAG_NAME, value="img"
        ).get_attribute('src')
        return m, image, False  # имя +  картинка + запрет на переход  в первую  часть функции

    def nuw_game(self, name):
        if name == "a_propose_yes":
            return True, False
        else:
            self.run = False
            self.driver.quit()
            return False, False

    def f(self):
        sleep(3)
        self.driver.find_element(By.CLASS_NAME, value="proposal-answers"
                                 ).find_element(By.ID, "a_propose_no").click()
        sleep(3)
        self.driver.find_element(By.CLASS_NAME, value="proposal-answers"
                                 ).find_element(By.ID, "a_continue_yes").click()


class Picture:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Скрытый режим браузера
        self.driver = webdriver.Chrome(options=self.chrome_options)  # открываем окно браузера в скрытом режиме
        # self.driver = webdriver.Chrome()

    def png(self, text):
        self.driver.get("https://yandex.ru/")
        try:
            search = self.driver.find_element(by=By.XPATH, value='//*[@id="text"]')
        except common.exceptions.NoSuchElementException:  # Если вылезла капча
            return "Вы словили капчу"
        search.send_keys(text)
        search.submit()
        sleep(3)
        self.driver.find_elements(by=By.CLASS_NAME, value="service__name")[1].click()
        sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])
        v = self.driver.find_elements(by=By.CSS_SELECTOR, value="div.serp-item__preview")
        try:
            m = v[random.randint(0, len(v))].find_element(by=By.TAG_NAME, value="img"
                                                          ).get_attribute('src')
        except IndexError:  # Если картинок не найденовы
            self.driver.quit()
            return "Картинка не найдена"
        print(m)
        self.driver.quit()
        return m
