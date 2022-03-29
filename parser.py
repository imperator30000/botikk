from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import common
from time import sleep

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()
language = {
    "ru": ["русский", "russian"],
    "en": ["английский", "english"],
}


def get_key(d, value):  # Функция поиска ключа если несколько значений
    for k, v in d.items():
        for i in v:
            if i == value:
                return k
    return False


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

        html_list = driver.find_element(by=By.CLASS_NAME, value="database-selection")
        items = html_list.find_elements(by=By.TAG_NAME, value="li")
        otv = {"a_yes": [items[0].text],
               "a_no": [items[1].text],
               "a_dont_know": [items[2].text],
               "a_probably": [items[3].text],
               "a_probaly_not": [items[4].text]}  # Список возможных  ответов
        print(otv)

        name = input()
        while not get_key(otv, name):  # Проверка на правильный ввод
            name = input()
        print(name)
        driver.find_element(By.ID, get_key(otv, name)).click()  # отвечаем на вопрос
        # driver.close()
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
    html_list = driver.find_element(by=By.CLASS_NAME, value="proposal-answers")
    items = html_list.find_elements(by=By.TAG_NAME, value="a")
    otv = {
        "a_propose_yes": [items[0].text],
        "a_propose_no": [items[1].text]
    }
    print(otv)  # я угадал?  Да\Нет

    name = input()
    while not get_key(otv, name):
        name = input()
    if name == "Да":
        driver.find_element(By.ID, get_key(otv, name)).click()
        print("Хотите Начать новую игру?")
        otv = {
            "Да": ["Да"],
            "Нет": ["Нет"]
        }
        name = input()
        while not get_key(otv, name):
            name = input()
        if name == "Да":
            main()
        else:
            driver.close()
    else:  # Если нет
        driver.find_element(By.ID, get_key(otv, name)).click()
        print(driver.find_element(by=By.CLASS_NAME, value="sub-bubble-propose").text)  # Желаете ли вы продолжить?
        otv = {
            "a_continue_yes": ["Да"],
            "a_continue_no": ["Нет"]
        }
        print("Закончить игру?")
        name = input()
        while not get_key(otv, name):
            name = input()
        if name == "Да":
            driver.find_element(By.ID, get_key(otv, name)).click()
            game()
        else:
            driver.close()


if __name__ == "__main__":
    main(get_key(language, input()))
