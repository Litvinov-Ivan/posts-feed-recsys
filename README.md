# posts-feed-recsys
Выпускной проект курсов [Karpov Courses специализации Start ML](https://karpov.courses/ml-start)

## Описание проекта

Цель - разработка сервиса рекомендательной системы постов в условной социальной сети.

### Исходные данные
Имеются следующие данные:
##### Пользователи сервиса
| Поле      | Описание                        |
|-----------|---------------------------------|
| age       | Возраст                         |
| city      | Город                           |
| country   | Страна                          |
| exp_group | Экспериментальная группа        |
| gender    | Пол                             |
| id        | Идентификатор                   |
| os        | Операционная система устройства |
| source    | Источник трафика                |
Количество зарегистрированных пользователей: ~163 тысячи

##### Новостные посты
| Поле  | Описание      |
|-------|---------------|
| id    | Идентификатор |
| text  | Текст         |
| topic | Тематика      |
Количество постов: ~7 тысяч

##### Логи действий пользователей с постами ленты
| Поле      | Описание                                 |
|-----------|------------------------------------------|
| timestamp | Время                                    |
| user_id   | id пользователя                          |
| post_id   | id поста                                 |
| action    | Совершённое действие - просмотр или лайк |
| target    | Поставлен ли лайк **после** просмотра.   |
Количество записей: ~77 миллионов

### Описание задачи

Необходимо создать готовый к интеграции веб-сервис, возвращающий по запросу зарегистрированного
пользователя персонализированную ленту новостей.

Кроме того, необходимо подготовить инфраструктуру для проведения A\B-тестирования для определения изменения поведения
польователей при выдаче ленты разными алгоритмами.

Ввиду невозможности проведения реального A\B-теста, необходимо смоделировать запросы пользователей к нашему сервису на основе
имеющихся исторических данных и провести статистический анализ.

##### Параметры запроса
| Поле  | Описание                  |
|-------|---------------------------|
| id    | id пользователя           |
| time  | Время запроса             |
| limit | Количество постов в ленте |

##### Параметры отклика (одного поста из ленты)
| Поле  | Описание    |
|-------|-------------|
| id    | id поста    |
| text  | Текст поста |
| topic | Тема поста  |

##### Метрика
Оценка качества обученных алгоритмов будет замеряться по метрике hitrate@5 - есть ли хотя бы один лайк от пользователя в показанной ему ленте.

##### Технические требования и принятые допущения
1. Время отклика сервиса на 1 запрос не должен превышать 0.5 секунд.
2. Сервис не должен занимать более 2 Гб памяти системы.
3. Сервис должен иметь минимум две модели - обученную методом классического ML и с помощью DL.
4. Набор пользователей и постов фиксирован.
5. Временные рамки подаваемых сервису запросов ограничены предельными значениями в логах действий пользователей.

## Описание решения

### Анализ данных
При EDA препятствием стал размер датасета логов пользователей - 77 миллионов строк.
С целью уменьшить потребляемую память из базы данных было выгружено около 6 миллионов записей.
При этом данные выгружались равномерно по юзерам - не более 35 последних действий каждого пользователя.

_Далее этот массив разбили на обучающую, валидационную и тестовую выборку - 4 млн, 1 млн и 1 млн соответственно._

### Выбор алгоритма решения
Так как сервис должен иметь возможность давать рекомендации двумя различными моделями, 
необходимо сделать и обосновать выбор.
1. Рекомендационную модель на методе классического ML решено обучать с помощью CatboostClassifier.
Данный выбор обоснован табличной сущностью данных и необходимостью ранжировать полученные моделью предсказания.
Так как целевым показателем для нас является получение like хотя бы у одного поста в выдаче (согласно метрике hitrate@5),
ранжировать предсказания будем по вероятностям, полученными в классификаторе.
2. Вторая модель представляет собой тот же CatboostClassifier с обучением на полученных с помощью DL эмбеддингами
текстов постов. Эмбеддинги текстов получены с помощью эмбеддингов слов, в свою очередь
полученные обучением Word2Vec и дальнейшими преобразованиями.

### Реализация сервиса
Сервис реализован с помощью FastAPI в виде endpoint "ручки":
1. По POST запросу принимается запрос от пользователя на выдачу ленты.
2. Полученный в запросе JSON обрабатывается, все необходимые признаки приводятся к требуемой для модели форме.
3. Модель делает предсказания для каждого поста и выбираются с наибольшей вероятностью получающие лайк.
4. Сервис возвращает отклик со списком рекомендованных постов.

### Итоговые метрики
### Выводы

## Структура репозитория

```buildoutcfg
|   README.md
|   docker-compose.yaml
|   request-examples.txt
|
├───notebooks
│       data_downloading.ipynb
│       data_processing.ipynb
│       model_training.ipynb
│       dl_model_training.ipynb
|       data_analyze.ipynb
|       
└───posts_feed_service
    │   __init__.py
    │   requirements.txt
    │   app.py
    |   Dockerfile
    │
    ├───data
    │       catboost_model
    │       catboost_model_with_text_embs
    │       post_data.csv
    │       post_data_lemmatized.csv
    │       tfidf_df.csv
    │       user_data.csv
    │       post_data_lemmatized_and_embs.csv
    │
    └───lib
            __init__.py
            config.yaml
            datatypes.py
            utils.py
            model.py
```

| Название папки                            | Описание                                            |
|-------------------------------------------|-----------------------------------------------------|
| [posts_feed_service](posts_feed_service/) | Сервис                                              |
| [-data](posts_feed_service/data) | Папка с предобученными моделями и вспомогательными датасетами|
| [-lib](posts_feed_service/lib) | Папка со вспомогательными модулями                             |
| [notebooks](notebooks/)                   | Ноутбуки                                            |
| [-data_downloading](notebooks/data_downloading.pynb)            | Ноутбук со скачиванием данных |
| [-data_processing](notebooks/data_processing.pynb)               | Ноутбук с обработкой данных  |
| [-model_training](notebooks/model_training.pynb)  | Ноутбук с обучением модели классического ML |
| [-dl_model_training](notebooks/dl_model_training.pynb)|Ноутбук c получением эмбеддингов текстов и обучением с их помощью модели |

## Инструкция для запуска
#### Способ 1
`git clone https://github.com/Litvinov-Ivan/posts-feed-recsys.git` <br />
`cd ./posts-feed-recsys` <br />
`docker-compose up -d` <br />

#### Способ 2
`git clone https://github.com/Litvinov-Ivan/posts-feed-recsys.git` <br />
`cd ./posts-feed-recsys/posts_feed_service` <br />
`pip install --upgrade pip` <br />
`pip install --no-cache-dir -r /requirements.txt` <br />
`uvicorn app:app` <br />

Сервис доступен по http://127.0.0.1:8000/docs, где во вкладке `/feed` можно протестировать запрос на выдачу ленты.
Примеры запросов есть [здесь](request_examples.txt).
