# Всё что связано с парсингом
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import common
from time import sleep

# Всё что связано с голосом
import speech_recognition as sr
from speech_recognition import UnknownValueError
from fuzzywuzzy import process
import pyttsx3


class Bot:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Скрытый режим браузера
        self.driver = webdriver.Chrome(options=self.chrome_options)  # открываем окно браузера в скрытом режиме
        self.driver = webdriver.Chrome()

        self.golos = pyttsx3.init()

        self.opts = {
            "language": {
                "ru": ("русский", "russian"),
                "en": ("английский", "english")
            },
            "otv": {"a_yes": 'да', "a_no": 'нет', "Я не знаю": "a_dont_know", "a_probably": 'возможно частично',
                    "a_probaly_not": 'скорее нет не совсем', "end_game": 'закончить игру'},
            "menu": {"a_propose_yes": "a_propose_no", "Нет": 'нет'}
        }
        self.main(self.comparison(self.opts["language"])[2])

    def listener(self):  # Распознавание речи
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as sourse:
            audio = r.listen(sourse)
            try:
                sentence = r.recognize_google(audio, language="ru-RU")
                print(sentence)
            except UnknownValueError:
                print(1)
                sentence = self.listener()
        return sentence.lower()

    def comparison(self, arr):  # функция проверки ответа пользователя
        name = process.extractOne(self.listener(), arr)
        while name[1] < 80:  # Проверка на правильный ввод
            name = process.extractOne(self.listener(), arr)
        print(name)
        return name

    def main(self, lan="ru"):  # определяем язык бота
        self.driver.get(f"https://" + lan + ".akinator.com")
        # print(f"https://" + lan + ".akinator.com")
        sleep(3)  # Даём сайту полностью  загрузится
        self.driver.find_element(By.CLASS_NAME, "btn-play").click()  # Начинаем игру
        self.speak("Начало игры")
        self.game()

    def speak(self, text):
        self.golos.say(text)
        self.golos.runAndWait()

    def game(self):
        flag = True
        print(self.driver.current_url)  # Текущая ссылка
        while flag:  # цикл игры
            sleep(3)
            # print(driver.page_source)  # HTML код
            try:  # проверяем идёт ли у нас игра или нет
                # Если не смогли получить вопрос выходим из цикла игра
                question = self.driver.find_element(by=By.CLASS_NAME, value="bubble-body").text
                self.speak(question)  # Вопрос
            except common.exceptions.NoSuchElementException:
                flag = False
            if not flag:
                break
            sleep(3)
            print("otvet")
            name = self.comparison(self.opts["otv"])
            if name[2] == "end_game":
                self.driver.close()
                break
            self.driver.find_element(By.ID, name[2]).click()  # отвечаем на вопрос
            # driver.close()
        if not (name[2] == "end_game"):
            self.end_game()

    def end_game(self):
        sleep(3)
        who_1 = self.driver.find_element(by=By.CLASS_NAME, value="sub-bubble-propose").text  # Я думаю это
        who_2 = self.driver.find_element(by=By.CLASS_NAME, value="proposal-title").text  # Имя персонажа
        self.speak(who_1.lower() + " " + who_2)
        image = self.driver.find_element(by=By.CLASS_NAME, value='proposal-area').find_element(
            by=By.TAG_NAME, value="img"
        ).get_attribute('src')
        print(image)

        self.speak(self.opts["menu"])  # я угадал?  Да\Нет
        name = self.comparison(self.opts["menu"])
        if name[2] == "a_propose_yes":
            self.driver.find_element(By.ID, name[2]).click()
            self.speak("Хотите Начать новую игру?")

            name = self.comparison(self.opts["menu"])
            if name[0] == "a_propose_yes":
                self.main()
            else:
                self.driver.close()
        else:  # Если нет
            self.driver.find_element(By.ID, name[2]).click()
            self.speak(self.driver.find_element(by=By.CLASS_NAME,
                                                value="sub-bubble-propose").text)  # Желаете ли вы продолжить?
            self.speak("Закончить игру?")

            name = self.comparison(self.opts["menu"])
            if name == "a_propose_yes":
                self.driver.find_element(By.ID, name).click()
                self.game()
            else:
                self.driver.close()


if __name__ == "__main__":
    a = Bot()
