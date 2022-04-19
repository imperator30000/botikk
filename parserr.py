# Всё что связано с парсингом
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import common
from time import sleep

# Всё что связано с голосом
import speech_recognition as sr  # Распознавание речи
from speech_recognition import UnknownValueError

from fuzzywuzzy import process  # частичное сравнение

import pyttsx3  # голос бота

import random  # для вывода рандомных картинок

import sqlite3 as sq  # для базы данных с серверами


class Ass_bot:
    def __init__(self):
        self.otvet_text = ''
        # Таблица с серверами и количеством использования бота
        with sq.connect("discord_bot.db") as self.con:
            cur = self.con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Top_servers (
                id INTEGER auto_increment primary key,
                name TEXT,
                number_of_uses TEXT
                )""")
        self.con.commit()

        # self.chrome_options = Options()
        # self.chrome_options.add_argument("--headless")  # Скрытый режим браузера
        # self.driver = webdriver.Chrome(options=self.chrome_options)  # открываем окно браузера в скрытом режиме
        # self.driver = webdriver.Chrome()
        self.golos = pyttsx3.init()  # голос бота

        # словарь со всеми командами и вариантами ответов
        self.opts = {
            "language": {
                "ru": ("русский", "russian"),
                "en": ("английский", "english")
            },
            "otv": {"a_yes": 'да', "a_no": 'нет', "Я не знаю": "a_dont_know", "a_probably": 'возможно частично',
                    "a_probaly_not": 'скорее нет не совсем', "end_game": 'закончить игру'},
            "menu": {"a_propose_yes": "a_propose_no", "Нет": 'нет'}
        }
        # self.main(self.comparison(self.opts["language"])[2]) # Акинатор
        # self.png()  # Рандомная картинка

    # def chek(self,  text):
    #     for key in self.opts["language"]:
    #         for i in self.opts['language'][key]:
    #             if text == i:
    #                 return key

    # def listener(self):  # Распознавание речи
    #     r = sr.Recognizer()
    #     with sr.Microphone() as sourse:
    #         audio = r.listen(sourse)
    #         try:
    #             sentence = r.recognize_google(audio, language="ru-RU")
    #             print(sentence)  # то что услышал бот
    #         except UnknownValueError:
    #             print(1)  # бот ничего не услышал перезапуск функции
    #             sentence = self.listener()
    #     return sentence.lower()

    def comparison(self, text, arr):  # функция проверки ответа пользователя
        name = process.extractOne(text, arr)
        if name[1] < 80:  # Проверка на правильный ввод
            print(name)
            return [False, False, False]
        print(name)
        return name

    def main(self, lan="ru"):  # определяем язык бота
        global driver
        driver = webdriver.Chrome()
        driver.get(f"https://" + lan + ".akinator.com")
        sleep(5)  # Даём сайту полностью  загрузится
        try:
            driver.find_element(By.CLASS_NAME, "btn-play").click()  # Начинаем игру
        except common.exceptions.ElementNotInteractableException:
            driver.find_elements(by=By.CLASS_NAME, value="modal-content")[1].find_element(
                by=By.CLASS_NAME, value="modal-header").find_element(
                by=By.CLASS_NAME, value="close").click()
            sleep(2)
            driver.find_element(By.CLASS_NAME, "btn-play").click()
        print(driver.current_url)
        self.question()

    # def speak(self, text):
    #     self.golos.say(text)
    #     self.golos.runAndWait()

    def otvet(self, text):
        global driver
        sleep(3)
        if text == "end_game":
            driver.quit()
            return "end_game"
        if text:
            driver.find_element(By.ID, text).click()  # отвечаем на вопрос
            return True
        # driver.close()

    def question(self):
        global driver
        sleep(3)
        try:  # проверяем идёт ли у нас игра или нет
            # Если не смогли получить вопрос выходим из цикла игра
            question = driver.find_element(by=By.CLASS_NAME, value="bubble-body").text
            return question  # Вопрос
        except common.exceptions.NoSuchElementException:
            return False

    def end_game(self):
        global driver
        sleep(3)
        who_1 = driver.find_element(by=By.CLASS_NAME, value="sub-bubble-propose").text  # Я думаю это
        who_2 = driver.find_element(by=By.CLASS_NAME, value="proposal-title").text  # Имя персонажа
        m = who_1.lower() + " " + who_2
        image = driver.find_element(by=By.CLASS_NAME, value='proposal-area').find_element(
            by=By.TAG_NAME, value="img"
        ).get_attribute('src')
        return m, image  # имя +  картинка

    def nuw_game(self, name):
        global driwer
        if name == "a_propose_yes":
            self.main()
        else:
            driver.quit()

    def menu_win(self, name):
        global driver
        print(name)
        if name == "a_propose_yes":
            driver.find_element(By.ID, name[2]).click()
        else:  # Если нет
            driver.find_element(By.ID, name[2]).click()
            return driver.find_element(by=By.CLASS_NAME,
                                       value="sub-bubble-propose").text  # Желаете ли вы продолжить?

    def next(self, name):
        if name == "a_propose_yes":
            driver.find_element(By.ID, name).click()
            self.question()
        else:
            driver.quit()

    def png(self, text):
        driver = webdriver.Chrome()
        m = "Картинка не найдена"
        driver.get("https://yandex.ru/")
        search = driver.find_element(by=By.XPATH, value='//*[@id="text"]')
        search.send_keys(text)
        search.submit()
        sleep(2)
        driver.find_elements(by=By.CLASS_NAME, value="service__name")[1].click()
        sleep(5)
        driver.switch_to.window(driver.window_handles[1])
        v = driver.find_elements(by=By.CSS_SELECTOR, value="div.serp-item__preview")[1:]
        try:
            m = v[random.randint(0, len(v))].find_element(by=By.TAG_NAME, value="img"
                                                          ).get_attribute('src')
        except IndexError:
            driver.quit()
        driver.quit()
        return m
