# BikeShare Tools

These are a set of tools to do some fun things with the [Toronto Open Data BikeShare API](https://www1.toronto.ca/wps/portal/contentonly?vgnextoid=ad3cb6b6ae92b310VgnVCM10000071d60f89RCRD ) or data. Right now it just creates heatmaps but more interesting things may come.

## Getting Started

### Installing

Install the dependencies
```
$ pip install Django beautifulsoup4 uwsgi
$ pip install git+https://github.com/python-visualization/folium

```
There seems to be a bug in folium I'll soon be sending a PR for, and another bug has been fixed already but not released, so pip installing from the repo is preferred.

Clone this project's repo into your preferred folder.

## Deployment

```
$ python manage.py migrate
$ python manage.py collectstatic
```

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

## Built With

* [Django](https://www.djangoproject.com/) - The web framework
* [folium](http://python-visualization.github.io/folium/) - The mapping framework
* [BikeShare Toronto Open Data](https://www1.toronto.ca/wps/portal/contentonly?vgnextoid=ad3cb6b6ae92b310VgnVCM10000071d60f89RCRD) - API data used for mapping

## Authors

* [Imad Mouhtassem](https://github.com/mouhtasi) - Initial Work