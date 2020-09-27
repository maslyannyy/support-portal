# Инструкция по установке

Установить пакеты системы

	sudo apt-get install python3-pip python-dev python3-venv libpq-dev nginx git

Перейти в домашний каталог

	cd /home

Склонировать репозиторий

	git clone https://github.com/maslyannyy/support-portal.git

Перейти в папку с проктом

	cd support-portal

Развернуть виртуальное окружение

	python3 -m venv .venv

Активировать виртуальное окружение

	source .venv/bin/activate

Установить python-пакеты

	pip install -r requirements.txt
	
Собрать миграции и БД

    python3 manage.py makemigrations

    python3 manage.py migrate
	
На этом проект готов для разработки.
Далее шаги по настройке продакшен окружения.

В support-portal.conf, gunicorn/support-portal.service прописать текущего системного пользователя. В support-portal.conf дополнительно имя сервера

Собрать статик файлы

    python manage.py collectstatic

Скопировать конфиг сайта

	sudo cp support-portal.conf /etc/nginx/sites-enabled/

Прописать таймауты в /etc/nginx/nginx.conf

	http {
		proxy_connect_timeout   3600;
		proxy_send_timeout      3600;
		proxy_read_timeout      3600;
		send_timeout            3600;
		uwsgi_read_timeout      3600;
	}

Запустить nginx

	sudo /etc/init.d/nginx start 

Скопировать сервис сайта

	sudo cp gunicorn/support-portal.service /etc/systemd/system/

Перезагрузить systemctl

	systemctl daemon-reload

Запустить сервис

	systemctl start support-portal
	
Запустить автозапуск
    
    systemctl enable support-portal
