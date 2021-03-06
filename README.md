# BikeShare Tools

These are a set of tools to do some fun things with the [Toronto Open Data BikeShare API](https://www1.toronto.ca/wps/portal/contentonly?vgnextoid=ad3cb6b6ae92b310VgnVCM10000071d60f89RCRD ) or data. Right now it just creates heatmaps but more interesting things may come.

## Getting Started

### Installing

Install the dependencies
```
$ pip install -r requirements.txt
```
There seems to be a bug in folium I'll soon be sending a PR for, and another bug has been fixed already but not released, so pip installing from the repo is preferred.

Clone this project's repo into your preferred folder.

## Deployment

```
$ python manage.py migrate
$ python manage.py collectstatic
```

Generate a [new secret key](https://www.miniwebtool.com/django-secret-key-generator/) and place it in bikeshare_tools/.env with your Postgres User and Pass
```
export SECRET_KEY="---"
export DB_USER="user"
export DB_PASS="pass"
```

This project uses python-dotenv to safely store Django and DB credentials. To load them in your current session to use runserver run ```$ source bikeshare_tools/.env``` to load the environment variables. This can be automatically run by uWSGI as a service by using the Environment variable shown later below.

Run the project with uWSGI:
```
$ uwsgi -ini uwsgi.ini
```
This will create a socket in the project folder which Nginx/Apache etc can proxy to.

If using nginx
```
 location /bikeshare/static {
    alias /home/nap/bikeshare_tools/bikeshare_tools/static;
  }

  location /bikeshare {
    uwsgi_pass  unix:/home/nap/bikeshare_tools/bikeshare_tools.sock;
    include /home/nap/bikeshare_tools/uwsgi_params;
  }
```
will route for the URL domain.tld/bikeshare/

A systemd service can be setup to automatically deal with running uWSGI.
On Debian in /lib/systemd/system/uwsgi-bikeshare.service
```
[Unit]
Description=uWSGI for bikeshare Django project

[Service]
EnvironmentFile=/home/nap/bikeshare_tools/bikeshare_tools/.env
ExecStart=/home/nap/.virtualenvs/bikeshare_tools/bin/uwsgi --ini /home/nap/bikeshare_tools/uwsgi.ini
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
which can then be started with
```
$ sudo service uwsgi-bikeshare start
```

## Built With

* [Django](https://www.djangoproject.com/) - The web framework
* [folium](http://python-visualization.github.io/folium/) - The mapping framework
* [mapbox](https://www.mapbox.com/) - Another mapping framework
* [BikeShare Toronto Open Data](https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#84045f23-7465-0892-8889-7b6f91049b29) - API data used for mapping
* [Pure.css](https://purecss.io/) - CSS used for the layout

## Authors

* [Imad Mouhtassem](https://github.com/mouhtasi) - Initial Work