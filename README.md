# Описание
Простой CDN сервер на базе связки Nginx+Lua и немного Python.

- Upload/Download файлов
- Upload progress
- Video streaming (.mp4)
- Resize/Crop/Blur изображений

> В репозитории предоставлены конфигурационные файлы для обеспечения функциональности и не включают в себя тонкостей, специфичных для каждого проекта.

## Попробовать
```sh
$ git clone https://github.com/pirsipy/cdn.git
$ cd cdn
$ vagrant up
```

## Список ресурсов
|Описание                    |URL                                        |Тип запроса|
|:---------------------------|:------------------------------------------|:----------|
|Upload файлов               |`http://localhost:8080/upload/`            |`POST`     |
|Upload progress             |`http://localhost:8080/progress/`          |`GET`      |
|Download файлов             |`http://localhost:8080/<path>`             |`GET`      |
|Video streaming             |`http://localhost:8080/<path>.mp4`         |`GET`      |
|Resize/Crop/Blur изображений|`http://localhost:8080/<path>.<image type>`|`GET`      |

### Upload файлов
Загрузка файла(ов) на сервер.

Для трэкинга прогресса загрузки необходимо передавать заголовок запроса `X-Progress-Id: <unique_id>` или аналогичный GET-параметр: `http://localhost:8080/upload/?X-Progress-Id=<unique_id>`.
> В качестве `<unique_id>` рекомендуется генерировать `uuid`.

> Возможна передача нескольких файлов одним запросом.

Пример ответа:
```json
[
    {
        "type": "image/jpeg",
        "url": "http://localhost:8080/a0/41/c9/be59f980ef.jpg",
        "name": "example.jpg",
        "md5": "a61abd29931707236bfeae95fda21a3e",
        "size": "145400"
    }
 ]
```

### Upload progress
Получение информации о статусе передачи контента на сервер.

Для получения информации нужно использовать `X-Progress-Id`, указанный при запросе передачи контента на сервер, следующим образом:
```
http://localhost:8080/progress/?X-Progress-Id=<unique_id>
```

Пример ответа:
```json
{ "state" : "uploading", "received" : 388360, "size" : 2154474 }
```

### Download файлов
Получение загруженного файла по ссылке, сгенерированной при загрузке контента на сервер.

Пример ссылки:
```
http://localhost:8080/a0/41/c9/be59f980ef.jpg
```

### Video streaming
В случае, когда контентом является видео в формате `mp4`, данные передаются по технологии `streaming`, что позволяет:

- Использовать `HTTP` статус `206 Partial Content` для получения чисти контента, т.е. так называемой "перемотки".
- Использовать `GET` параметр `start` с указанием значения в секундах для определения начала воспроизведения.
- Использовать `GET` параметр `end` с указанием значения в секундах для определения конца воспроизведения.

Примеры запросов:
```
http://localhost:8080/e0/1c/88/0cd65b8f50.mp4
http://localhost:8080/e0/1c/88/0cd65b8f50.mp4?start=200
http://localhost:8080/e0/1c/88/0cd65b8f50.mp4?end=500
http://localhost:8080/e0/1c/88/0cd65b8f50.mp4?start=300&end=600
```

### Resize/Crop/Blur изображений

> При первичном запросе генерируется файл по заданным параметрам. Последующие аналогичные запросы используют уже имеющийся файл. Своего рода кэширование.

#### Resize/Crop изображений

Изменение размера/Обрезание части изображений с помощью `GET` параметра `size`.

```lua
"500x300"       -- Изменение размера изображения с сохранением соотношения сторон,
                --  ширина не превышает 500px, а высота 300px
"500x300!"      -- Изменение размера изображения до 500px на 300px,
                --  игнорируя соотношение
"500x"          -- Изменение ширины изображения до 500px,
                --  сохраняя соотношение
"x300"          -- Изменение высоты изображения до 300px,
                --  сохраняя соотношение
"50%x20%"       -- Изменение ширины изображения до 50% и высоты до 20%
                --  относительно оригинала
"500x300c"      -- Изменение размера изображения до 500px на 300px, но обрезая
                --  верхнюю или нижнюю часть, сохраняя соотношение сторон
"500x300+10+20" -- Обрезание части изображения до 500px на 300px
                --   с позиционированием 10,20
```

Примеры запросов:
```
http://localhost:8080/a0/41/c9/be59f980ef.jpg?size=500x300
http://localhost:8080/a0/41/c9/be59f980ef.jpg?size=500x300!
http://localhost:8080/a0/41/c9/be59f980ef.jpg?size=500x
http://localhost:8080/a0/41/c9/be59f980ef.jpg?size=x300
http://localhost:8080/a0/41/c9/be59f980ef.jpg?size=50%x20%
http://localhost:8080/a0/41/c9/be59f980ef.jpg?size=500x300c
http://localhost:8080/a0/41/c9/be59f980ef.jpg?size=500x300+10+20
```

#### Blur изображений

Наложение фильтра `blur` на изображение с помощью одноименного `GET` параметра `blur`, в котором задается уровень `от 1 до 100`.

Пример запроса:
```
http://localhost:8080/a0/41/c9/be59f980ef.jpg?blur=5
```

Возможно комбинирование описанных параметров:
```
http://localhost:8080/a0/41/c9/be59f980ef.jpg?size=500x300&blur=5
```

## Установка

> Работоспособность проверена на `CentOS 7` и предоставлена в виде `vagrant` образа [pirsipy/cdn](https://vagrantcloud.com/pirsipy/cdn).

Обновление системы и установка зависимостей

```sh
$ sudo yum update -y
$ sudo yum groupinstall -y "Development tools"
$ sudo yum install -y ImageMagick ImageMagick-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel pcre-devel
```

Установка `Python 3.4` (рекомендуется)

Переключение во временную директорию

```sh
$ cd /tmp
```

Загрузка, компиляция и установка `Python 3.4`

```sh
$ wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
$ tar xf Python-3.4.3.tgz
$ cd Python-3.4.3
$ ./configure --prefix=/usr/local --enable-shared
$ make
$ sudo make install
$ sudo echo /usr/local/lib >> /etc/ld.so.conf.d/local.conf
$ sudo ldconfig
```

Переключение во временную директорию

```sh
$ cd /tmp
```

Загрузка `upload-module` для `Nginx` ([http://wiki.nginx.org/HttpUploadModule](http://wiki.nginx.org/HttpUploadModule))

```sh
$ git clone https://github.com/vkholodkov/nginx-upload-module.git --branch 2.2
```

Загрузка `upload-progress-module` для `Nginx` ([http://wiki.nginx.org/HttpUploadProgressModule](http://wiki.nginx.org/HttpUploadProgressModule))

```sh
$ git clone https://github.com/masterzen/nginx-upload-progress-module.git
```

Загрузка готовой сборки `Nginx` с набором остальных необходимых компонентов ([http://openresty.org](http://openresty.org))

```sh
$ wget http://openresty.org/download/ngx_openresty-1.7.10.1.tar.gz
```

Конфигурирование, компиляция и установка

```sh
$ tar xzf ngx_openresty-1.7.10.1.tar.gz
$ cd ngx_openresty-1.7.10.1
$ ./configure --with-http_mp4_module --add-module=/tmp/nginx-upload-module --add-module=/tmp/nginx-upload-progress-module
$ make
$ sudo make install
$ sudo ln -s /usr/local/bin/python3 /usr/bin/
$ sudo ln -s /usr/local/bin/pip3 /usr/bin/
```

Создание ссылки (для удобства) на исполняемый файл `nginx`

```sh
$ sudo ln -s /usr/local/openresty/nginx/sbin/nginx /usr/sbin/
```

## Настройка

> Некоторые из указанных настроек несут лишь рекомендуемый характер.

Добавим в систему пользователя `webmaster`, от имени которого будем производить запуск необходимых компонентов

```sh
$ sudo useradd webmaster
```

Добавим директории для логирования

```sh
$ mkdir /home/webmaster/logs
$ mkdir /home/webmaster/logs/nginx
```

Подключение дополнительного репозитория `epel`

```sh
$ sudo yum install -y epel-release
```

Установка `supervisor` для атоматического запуска необходимых компонентов

```sh
$ sudo yum install -y supervisor
```

Автоматический запуск `supervisor` при загрузке сервера

```sh
$ sudo systemctl enable supervisord
```

Изменение настроек `supervisor`. Заменить содержимое файла `/etc/supervisord.conf` на:

```ini
[unix_http_server]
file=/tmp/supervisor.sock
username=user
password=123

[supervisord]
logfile=/home/webmaster/logs/supervisord.log
logfile_maxbytes=50MB
logfile_backups=5
loglevel=info
pidfile=/tmp/supervisord.pid
nodaemon=false
minfds=1024
minprocs=200
user=webmaster

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock
username=user
password=123
history_file=~/.sc_history

[include]
files = /home/webmaster/app/*.ini
```

Изменение настроек `nginx`. Заменить содержимое файла `/usr/local/openresty/nginx/conf/nginx.conf` на:

```
user webmaster;
worker_processes 1;
daemon off;

error_log  /home/webmaster/logs/nginx/error.log;
pid        /tmp/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    access_log    /home/webmaster/logs/nginx/access.log;

    sendfile           on;
    keepalive_timeout  65;
    gzip               on;

    include /home/webmaster/app/*.conf;
}
```

Gist с файлами настроек: [https://gist.github.com/vilisov/2656f0bf5f7e0ce5632f](https://gist.github.com/vilisov/2656f0bf5f7e0ce5632f)

## Запуск

Склонировать репозиторий в директорию `/home/webmaster/app`

```sh
$ cd /home/webmaster
$ git clone https://github.com/pirsipy/cdn.git app
```

Установка python зависимостей

```sh
$ cd /home/webmaster/app
$ sudo pip3 install -r requirements.txt
```

Запускаем `supervisor`

```sh
$ sudo service supervisord start
```

Или перезапускаем, если уже был запущен

```sh
$ sudo service supervisord restart
```

После запуска результат выполнения команды

```sh
$ supervisorctl status
```

должен выглядеть примерно так:

```
cdn:nginx                        RUNNING    pid 2907, uptime 3:47:24
cdn:upload                       RUNNING    pid 2909, uptime 3:47:24
```

## Основные настройки и пути к файлам

Файл `/home/webmaster/app/nginx.conf`

|Переменная/Директива|Описание                                              |
|:-------------------|:-----------------------------------------------------|
|listen              |Порт, на котором будет запущен сервер                 |
|$BASE_PATH          |Основной путь к директории, куда склонен репозиторий  |
|$files              |Дериктория, в которую будут загружаться файлы         |
|$cache              |Директория для кэширования преобразованных изображений|
|client_max_body_size|Максимальный размер запроса к серверу                 |
|$limit_rate         |Ограничение на скорость отдачи контента от сервера    |
|upload_limit_rate   |Ограничение на скорость загрузки контента на сервер   |

Файл `/home/webmaster/app/server.py`

|Переменная          |Описание                                              |
|:-------------------|:-----------------------------------------------------|
|BASE_PATH           |Дериктория, в которую будут загружаться файлы         |

# P.S.

В данном описании команды с префиксом `sudo` означают запуск с паравами `root` пользователя. О настройке данной возможности есть много информации в интернете. Если все же не получилось настроить, то данные команды можно выполнять авторизовавшись под пользователем `root`.

При использовании `vagrant` возможна длительная загрузка данных на виртуальную машину при использовании ресурса `http://localhost:8080/upload/`. Это связано с медленной синхронизацией смонтированной директории.

# Контакты

По всем вопросам можно обращаться любым удобным способом:

|VK                                                        |Email                                              |Skype       |
|:---------------------------------------------------------|:--------------------------------------------------|:-----------|
|[https://vk.com/stas.vilisov](https://vk.com/stas.vilisov)|[st@pirsipy.com](mailto:st@pirsipy.com?subject=CDN)|stas.pirsipy|

@2015 [Pirsipy](https://pirsipy.com)
