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

chrome_options = Options()
chrome_options.add_argument("--headless")  # Скрытый режим браузера
driver = webdriver.Chrome(options=chrome_options)  # открываем окно браузера в скрытом режиме
# driver = webdriver.Chrome()

r = sr.Recognizer()  # Распознавание речи

opts = {
    "language": {
        "ru": ("русский", "russian"),
        "en": ("английский", "english")
    },
    "otv": {"a_yes": 'да', "a_no": 'нет', "Я не знаю": "a_dont_know", "a_probably": 'возможно частично',
            "a_probaly_not": 'скорее нет не совсем', "end_game": 'закончить игру'},
    "menu": {"a_propose_yes": "a_propose_no", "Нет": 'нет'}
}


def listener():  # Распознавание речи
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as sourse:
        audio = r.listen(sourse)
        try:
            querty = r.recognize_google(audio, language="ru-RU")
            print(querty)
        except UnknownValueError:
            print(1)
            querty = listener()
    return querty.lower()


def comparison(arr):
    name = process.extractOne(listener(), arr)
    while name[1] < 80:  # Проверка на правильный ввод
        name = process.extractOne(listener(), arr)
    print(name)
    return name


def main(lan="ru"):  # определяем язык бота
    driver.get(f"https://" + lan + ".akinator.com")
    # print(f"https://" + lan + ".akinator.com")
    sleep(3)  # Даём сайту полностью  загрузится
    driver.find_element(By.CLASS_NAME, "btn-play").click()  # Начинаем игру
    print("Начало игры")
    game()


def game():
    flag = True
    print(driver.current_url)  # Текущая ссылка
    while flag:  # цикл игры
        sleep(3)
        # print(driver.page_source)  # HTML код
        try:  # проверяем идёт ли у нас игра или нет
            # Если не смогли получить вопрос выходим из цикла игра
            question = driver.find_element(by=By.CLASS_NAME, value="bubble-body").text
            print(question)  # Вопрос
        except common.exceptions.NoSuchElementException:
            flag = False
        if not flag:
            break
        sleep(3)
        print("otvet")
        name = comparison(opts["otv"])
        if name[2] == "end_game":
            driver.close()
            break
        driver.find_element(By.ID, name[2]).click()  # отвечаем на вопрос
        # driver.close()
    if not (name[2] == "end_game"):
        end_game()


def end_game():
    sleep(3)
    who_1 = driver.find_element(by=By.CLASS_NAME, value="sub-bubble-propose").text  # Я думаю это
    who_2 = driver.find_element(by=By.CLASS_NAME, value="proposal-title").text  # Имя персонажа
    print(who_1.lower() + " " + who_2)
    image = driver.find_element(by=By.CLASS_NAME, value='proposal-area').find_element(
        by=By.TAG_NAME, value="img"
    ).get_attribute('src')
    print(image)

    print(opts["menu"])  # я угадал?  Да\Нет
    name = comparison(opts["menu"])
    if name[2] == "a_propose_yes":
        driver.find_element(By.ID, name[2]).click()
        print("Хотите Начать новую игру?")

        name = comparison(opts["menu"])
        if name[0] == "a_propose_yes":
            main()
        else:
            driver.close()
    else:  # Если нет
        driver.find_element(By.ID, name[2]).click()
        print(driver.find_element(by=By.CLASS_NAME, value="sub-bubble-propose").text)  # Желаете ли вы продолжить?
        print("Закончить игру?")

        name = comparison(opts["menu"])
        if name == "a_propose_yes":
            driver.find_element(By.ID, name).click()
            game()
        else:
            driver.close()


if __name__ == "__main__":
    main(comparison(opts["language"])[2])
