[![Build Status](https://travis-ci.com/anisimovih/Message_sending_emulator.svg?branch=master)](https://travis-ci.com/anisimovih/Message_sending_emulator.svg?branch=master)

# Эмулятор отправки сообщений.

Программа реализует микросервис по [тестовому заданию](Test_task_discription.pdf), эмулирующий отправку сообщений в популярные мессенджеры(Viber, Telegram, WhatsApp).

Для эмуляции реальной работы, на отправку однго сообщения выделяется случайное значение от 1 до 3 секунд. В случае неудачной отправки (вероятность 10%), приложение попытается отправить сообщение еще 4 раза.
Данные параметры можно поменять в файле [tasks.py](message_sender/tasks.py).

## Используемые библиотеки.
Разработка производилась с использованием фреймворка Django. Фреймворк выбран из соображений наибольшего знакомства и описания вакансии.

Отправленные сообщения хранятся в базе данных PostgreSQL. Критерии выбора аналогичны предыдущему пункту.

Ассинхронной обработкой отправки сообщений заниманимается Celery. Данная очередь была выбрана исходя из наличия подробной документации и высокой популярности для данного рода задач.

В качестве брокера сообщений выбран Redis, как один из стандартных брокеров Celery.

Для валидации параметров используется JSON Schema. Выбор обусловлен постоянным использованием Json формата в запросах.

## API.
### Описание.
REST API работает по протоколу HTTP и представляет собой набор методов, с помощью которых совершаются запросы и возвращаются ответы для каждой операции. Все ответы приходят в виде JSON структур.

### Рассылка сообщений.
Для рассылки сообщений отправляется POST запрос по ссылке:
http://127.0.0.1:8000/api/
Параметры запроса:

|    От одного до трех мессенджеров    | Список из объектов, содержащих параметры | |
| ------------- |:------------------| :-----|
| **Viber/Telegram/WhatsApp**       | Название мессенджера |(минимум - 1, максимум - все 3) |
|               | **user_id**    | ID пользователя (int) |
|               | **message**    | Сообщение пользователю(string) |
|               | **date_time***  |    Дата и время отправки(string в формате "YYYY-MM-DDThh:mm:ss±hh:mm") |

Пример запроса на отправку двух моментальных и 1 отложенного сообщения в два мессенджера:
```json
{
    "Telegram": [
        {
            "user_id": 1067000,
            "message": "message_1",
            "date_time": "2019-12-30T16:09:00+03:00"
        },
        {
            "user_id": 10670500,
            "message": "message_1"
        }
    ],
    "WhatsApp": [
        {
            "user_id": 10264904,
            "message": "message_1"
        }
    ]
}
```

В ответ приходит список, содержащий статусы добавления в очередь отправки каждого сообщения.
Возможные статусы:

* ADDED - сообщение добавлено в очередь отправки.
* PENDING - сообщение с такими параметрами уже зарезервировано для отложенной отправки.
* SENDING - сообщение с такими параметрами отправляется.
* ALREADY SENT - сообщение с такими уже отправлено.

Пример ответа: 
```json
{"results": ["PENDING", "ALREADY SENT", "ADDED IN QUEUE"]}
```

### Поверка статуса сообщения.
Для проверки статуса сообщения отправляется GET запрос по ссылке:
http://127.0.0.1:8000/api/
Параметры запроса:

|    От одного до трех мессенджеров    | Список из объектов, содержащих параметры | |
| ------------- |:------------------| :-----|
| **Viber/Telegram/WhatsApp**       | Название мессенджера |(минимум - 1, максимум - все 3) |
|               | **user_id**    | ID пользователя (int) |
|               | **message**    | Сообщение пользователю(string) |

Пример запроса на проверку статуса трех сообщений из двух мессенджеров:
```json
{
    "Telegram": [
        {
            "user_id": 1067000,
            "message": "message_1"
        },
        {
            "user_id": 10670500,
            "message": "message_1"
        }
    ],
    "WhatsApp": [
        {
            "user_id": 10264904,
            "message": "message_1"
        }
    ]
}
```

В ответ приходит список, содержащий статус отвправки каждого сообщения.
Возможные статусы:
* PENDING - сообщение зарезервировано для отложенной отправки.
* SENDING - сообщение отправляется.
* SENT - сообщение отправлено.
* NOT FOUND - cообщение с такими параметрами не найдено.

Пример ответа:
```json
{"results": ["PENDING", "SENT", "NOT FOUND"]}
```

### Отмена отложенной отправки.
Для отмены отправки отложенного сообщения отправляется PUT запрос по ссылке:
http://127.0.0.1:8000/api/
Параметры запроса:

|    От одного до трех мессенджеров    | Список из объектов, содержащих параметры | |
| ------------- |:------------------| :-----|
| **Viber/Telegram/WhatsApp**       | Название мессенджера |(минимум - 1, максимум - все 3) |
|               | **user_id**    | ID пользователя (int) |
|               | **message**    | Сообщение пользователю(string) |

Пример запроса на проверку статуса трех сообщений из двух мессенджеров:
```json
{
    "Telegram": [
        {
            "user_id": 1067000,
            "message": "message_1"
        },
        {
            "user_id": 10670500,
            "message": "message_1"
        }
    ],
    "WhatsApp": [
        {
            "user_id": 10264904,
            "message": "message_1"
        }
    ]
}
```

В ответ приходит список, содержащий результаты отмены каждого сообщения
Возможные статусы:
* CANCELED - сообщение удалено из очереди отложенной отправки.
* NOT FOUND - сообщение с таким id нет в очереди отложенной отправки.

Пример ответа: 
```json
{"results": ["CANCELED", "NOT FOUND", "CANCELED"]}
```

## Инструкции по развертыванию.
Для развертывания приложения предлагается использовать [Docker Compose](https://docs.docker.com/compose/).
Инструкцию по установке можно посмотреть [здесь](https://docs.docker.com/compose/install/).

Перейдя через консоль в корень приложения, следует исполнить команду:
````
$ sudo docker-compose up --build
````
Composer создаст и запустит приложение в мультиконтейнере.

Для корректного запуска следующие порты должны быть свободны:
* 6379 - для Redis.
* 5432 - для PostgreSQL.
* 8000 - для общения с самим приложением.

После этого можно начинать общаться с приложением через API, описанный выше.





















