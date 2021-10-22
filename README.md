## Что нужно для локального запуска
После клона проекта нужно установить виртуальное окружение и активировать его
Нужно установить проект как пакет: pip install -e '.[dev]', находясь в руте проекта (где лежит setup)
messenger > utils > db: поменять данные к БД на свою, либо передать через переменные окружения
Прописать messenger-db upgrade head
Далее messenger-api для запуска


## Что нужно для запуска тестов
Открыть conftest.py, лежащий в папке тестов
В фикстуре postgres поменять db_user на своего
При коннекте в таблице template1 - указать свой пароль (template1, postgres менять не нужно)
В корне проекта нужно прописать pytest (в pytest.ini лежит --cov=messenger)
Тесты долгие - каждый раз создается и удаляется БД, лучше его не останавливать, иначе БД не удалится
Но если лень ждать - CTRL+C и ручками удаляете базу (она всего лишь одна будет, и то не факт)


## Аутентификация сделана на сессиях
Логика лежит в utils > auth.py
С помощью aiohttp-session и cryptography
Хранилище: encryptstorage
Он умный и не пустит плохого клиента
Чтобы пользоваться основными функционалом, нужно зарегистрироваться и залогиниться
При логауте сессия удаляется


## Поиск не полнотекстовый, но тоже сойдет
Ищет с помощью contains, возвращает сначала новые сообщения
В функции, которая занимается поиском (последняя в файле search_messages_in_chat.py) поставлены
asyncio.sleep, это помогает следить за статусом таски
Сначала крейтите таску, потом проверяете его статус и результат
Через 10 секунд таска должна перейти в IN PROCESS, затем в SUCCESS, и результаты появятся
Если лень ждать - удаляете 2 строчки кода с слипами, и сразу смотрите статус и результат


## Логи пишутся в stdout и в файл
logger > logs


## RateLimit
Реализован на основе паттерна: Корзины и токены
У клиента 10 токенов, он после каждого запроса их тратит
Токены восстанавливаются в зависимости от времени выполнения запросов
Хорошо подходит против ботов - их спам НЕ полностью прекращается, а регулируется
Если, например, бот сделал 10 запросов в секунду, то его дальнейшая отправка сообщений
ограничивается, 1 запрос в 1 секунду.
На добросовестных пользователей никак не сказывается
