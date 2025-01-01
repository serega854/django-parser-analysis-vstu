from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Author, PublicationStatistics, Publication
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

    # Проверка существования автора
    if Author.objects.filter(full_name=surname).exists():
        return JsonResponse({
            "success": False,
            "error": "Author with this surname already exists in the database."
        })

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

        # 7. Парсинг публикаций
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
            time.sleep(2)
        except Exception:
            pass

        # 9. Парсинг таблицы
        table_data = []
        try:
            view_div = driver.find_element(By.ID, "VIEW")
            rows = view_div.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                table_data.append([cell.text for cell in cells])
        except Exception:
            pass

        # 10. Парсинг количества публикаций
        try:
            publication_count_element = driver.find_element(By.XPATH, "//p[b[contains(text(), 'Количество публикаций:')]]")
            publication_count = int(publication_count_element.text.split(':')[-1].strip())
        except Exception:
            publication_count = 0

        # Сохранение в базу данных
        author = Author.objects.create(full_name=surname, publication_count=publication_count)

        for article in articles_data:
            Publication.objects.create(author=author, title=article)

        for row in table_data:
            if len(row) < 17:
                continue
            year, *values = row
            try:
                year = int(year)
                stats = [int(value) if value.isdigit() else 0 for value in values]
                PublicationStatistics.objects.create(
                    author=author,
                    year=year,
                    monograph=stats[0],
                    textbook=stats[1],
                    tutorial=stats[2],
                    tutorial_griff=stats[3],
                    article_russian_journal=stats[4],
                    article_foreign_journal=stats[5],
                    izvestia_vstu=stats[6],
                    journals_vstu=stats[7],
                    article_russian_collection=stats[8],
                    article_foreign_collection=stats[9],
                    theses=stats[10],
                    educational_complex=stats[11],
                    deposited_manuscript=stats[12],
                    patent_document=stats[13],
                    certificate=stats[14],
                    other_publications=stats[15],
                )
            except ValueError:
                continue

        return JsonResponse({
            "success": True,
            "message": "Data parsed and saved successfully.",
            "surname": surname,
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

    finally:
        driver.quit()

def parse_view(request):
    if request.method == "GET":
        return render(request, "parser_app/parser.html")

