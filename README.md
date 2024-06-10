# Eventcalendar

Тестовий додаток для обліку доставки товарів, зроблено на основі календаря


## Quickstart

Run the following commands to bootstrap your environment:
    
    sudo apt-get update
    sudo apt-get install -y git python3-dev python3-venv python3-pip supervisor nginx vim libpq-dev
    git clone https://github.com/Dudasmit/eventcalendar
    update
    git pull https://github.com/Dudasmit/eventcalendar
    cd eventcalendar
      
    python3 -m venv venv   
    source venv/bin/activate
    pip3 install -r requirements/dev.txt 

    cp .env.template .env
    while read file; do
       export "$file"
       done < .env

Setup locale

sudo dpkg-reconfigure locales

Run the app locally:

    python3 manage.py runserver 0.0.0.0:8000 --settings=eventcalendar.settings

Run the app with gunicorn:

    gunicorn eventcalendar.wsgi -b 127.0.0.1:8000

    gunicorn --bind 127.0.0.1:8000 eventcalendar.wsgi
    
    ps ax|grep gunicorn

    pkill -P1 gunicorn

    sudo systemctl restart gunicorn

    kill pricess

    fuser -k 8000/tcp
    
Collect static files:

    python3 manage.py collectstatic --settings=eventcalendar.settings
    

### IGDB usage:

Get a list of games from IGDB API:
    
    python3 manage.py shell

    >>>> from eventcalendar.utils.igdb_api import IgdbApi
    >>>> IgdbApi().get_games()
    >>>> 


### Setup NGINX:

    sudo vim /etc/nginx/sites-enabled/default:
    
Config file:

    server {
            listen 80 default_server;
            listen [::]:80 default_server;

            location /static/ {
                alias /home/dudasmit/eventcalendar/static/; 
            }

            location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_redirect off;
                add_header P3P 'CP="ALL DSP COR PSAa OUR NOR ONL UNI COM NAV"';
                add_header Access-Control-Allow-Origin *;
            }
    }
    
Restart NGINX:
    
    sudo service nginx restart
    
    
### Setup Supervisor:

    cd /etc/supervisor/conf.d/
    sudo vim eventcalendar.conf
    
Config file:
    
    [program:eventcalendar]
    command = /home/dudasmit/eventcalendar/venv/bin/gunicorn eventcalendar.wsgi  -b 127.0.0.1:8000 -w 4 --timeout 90
    autostart=true
    autorestart=true
    directory=/home/dudasmit/eventcalendar 
    stderr_logfile=/var/log/eventcalendar.err.log
    stdout_logfile=/var/log/eventcalendar.out.log
    
Update supervisor with the new process:
    
    sudo supervisorctl reread
    sudo supervisorctl update
    
To restart the process after the code updates run:

    sudo supervisorctl status eventcalendar
    sudo supervisorctl restart eventcalendar

    
   



Настройка Gunicorn

Откроем для настройки

sudo nano /etc/systemd/system/gunicorn.socket

Пропишем в файле несколько настроек:

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target

Мы создали раздел [Unit] для описания сокета, в разделе [Socket] мы определили расположение сокета и в разделе [Install] нужен для установки сокета в нужное время.

Откроем служебный файл systemd ля настройки работы сервиса:

sudo nano /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=dudasmit
Group=www-data
WorkingDirectory=/var/www/eventcalendar
ExecStart=/var/www/eventcalendar/env/bin/gunicorn \
          --access-logfile - \
          --workers 5 \
          --bind unix:/run/gunicorn.sock \
          eventcalendar.wsgi:application

[Install]
WantedBy=multi-user.target

Не забудьте указать вашего пользователя, ваше название проекта и ваше виртуальное окружение.

Как мне пояснили workers вычисляется как количество ядер процессора * 2 + 1.
Теперь мы запускаем и активируем сокет Gunicorn.

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

И обязательно тестируем, что всё работает!

sudo systemctl status gunicorn.socket




#### Git
Commit the change using
git commit -m "My message"
Stash it.
Stashing acts as a stack, where you can push changes, and you pop them in reverse order.

To stash, type

git stash
Do the merge, and then pull the stash:

git stash pop
Discard the local changes
using 
    git reset --hard
or 
    git checkout -t -f remote/branch

    git rm --cached db.sqlite3
    git commit

Or: Discard local changes for a specific file
using git checkout filename