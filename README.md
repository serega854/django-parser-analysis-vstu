# Распаковка

## Создаем виртуальное окружение
#### python -m venv venv

## Активируем виртаульное окружение
#### venv\Scripts\activate

## Устанавливаем все зависимости
#### pip install -r requirements.txt

## Выполняем миграцию базы данных  
#### python manage.py makemigrations
#### python manage.py migrate

## Запускаем сервер
#### python manage.py runserver

#### чтобы парсер работал на компьютере должен быть браузер microsoft edge (либо нужно заменить вебдрайвер в корне проекта "msedgedriver.exe" и использование файла в контролере приложения views.py)

# Пример работы приложения (гифка загружается примерно минуту)
 
#### На главной странице в поиск можно написать ФИО автора, парсер сохраняет фио автора, статьи, типы статей, год публикации с сайта http://library.vstu.ru/
#### На главной странице можно нажать "Подробнее" и посмотреть информацию по выбранному автору
#### На главной странице можно нажать "Удалить" и удалить выбранного автора из базы данных
#### На главной странице можно через чек-бокс выделить нескольких авторов и нажать "Анализ выбранных авторов", чтобы увидеть таблицу агрегирующих значений и график типы статей по годам

![приложение](https://github.com/serega854/django-parser-analysis-vstu/blob/main/for_gif_to_github/приложение.gif)





# Пример работы rest-api (гифка загружается примерно минуту)

![рест](https://github.com/serega854/django-parser-analysis-vstu/blob/main/for_gif_to_github/рест.gif)

#### POST Запрос для парсинга http://127.0.0.1:8000/parse_library/
{
    "surname": "Дятлов М.Н."
}

#### GET запроса для деталей по автору http://127.0.0.1:8000/author_details/{id}
#### GET запрос для анализа выбранных авторов http://127.0.0.1:8000/analyze_authors/?ids={id}
#### DEL запрос для удаления выбранного автора http://127.0.0.1:8000/delete_author/32/
X-CSRFToken : {csrt-token}
Cookie : csrftoken={csrt-token}
У меня
X-CSRFToken AREjpX47ij6ZxrFY3WDDqgTq1QH74JOyWAg9lZBsp9gmH0yJYXhA76qUUGsMWUHf
Cookie : csrftoken=AREjpX47ij6ZxrFY3WDDqgTq1QH74JOyWAg9lZBsp9gmH0yJYXhA76qUUGsMWUHf



