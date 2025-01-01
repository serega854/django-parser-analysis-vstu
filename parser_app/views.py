from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def parse_library(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Only POST requests are allowed."})

    # Получаем фамилию из POST-запроса
    try:
        body = json.loads(request.body)
        surname = body.get("surname", "")
        if not surname:
            return JsonResponse({"success": False, "error": "Surname is required."})
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON."})

    # Путь к WebDriver
    driver_path = "./msedgedriver.exe"

    # Настройка WebDriver
    service = Service(driver_path)
    driver = webdriver.Edge(service=service)
    wait = WebDriverWait(driver, 20)

    try:
        # 1. Открываем сайт
        driver.get("http://library.vstu.ru/")


        # 2. Наводим мышку на "Преподавателям и сотрудникам"
        menu_item = driver.find_element(By.CSS_SELECTOR, 'li#menu-451-1 > a')
        actions = ActionChains(driver)
        actions.move_to_element(menu_item).perform()


        # 3. Кликаем на "БД 'Публикации сотрудников ВолгГТУ'"
        publications_link = driver.find_element(By.CSS_SELECTOR, 'li#menu-452-1 > a')
        publications_link.click()


        # 4. Кликаем на "Сетевая версия БД 'Публикации сотрудников ВолгГТУ'"
        network_version_link = driver.find_element(By.CSS_SELECTOR, 'a[href*="publ_2/index.php?command=search2"]')
        network_version_link.click()

        # 5. Заполняем форму поиска
        fio_input = driver.find_element(By.ID, "fio")
        fio_input.send_keys(surname)  # Вводим фамилию из запроса

        # 6. Нажимаем кнопку "Найти"
        find_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Найти"]')
        find_button.click()


        # 7. Проверяем наличие результатов
        try:

            results_div = driver.find_element(By.ID, "LIST")
            articles = results_div.find_elements(By.TAG_NAME, "p")
            articles_data = [article.text for article in articles]
        except Exception:
            articles_data = []

        # 8. Разворачиваем таблицу с "Сводный отчет"
        try:
            expand_table_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ptr[onclick=\"ch_disp('VIEW')\"]"))
            )
            expand_table_button.click()
            time.sleep(2)  # Небольшая пауза, чтобы таблица успела загрузиться
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Error expanding table: {str(e)}"})

        # 9. Парсинг таблицы
        table_data = []

        try:
            view_div = driver.find_element(By.ID, "VIEW")
            rows = view_div.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                table_data.append([cell.text for cell in cells])
        except Exception as e:
            table_data = []

        # Возвращаем данные в JSON
        return JsonResponse({
            "success": True,
            "surname": surname,
            "articles": articles_data,
            "table": table_data,
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

    finally:
        driver.quit()
