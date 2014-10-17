Barachiel's Server
=============================

How to
------

Clone the repo:
```bash
$ git clone git@github.com:maxrevilo/barachiel-server.git
```

Clone submodules:
```bash
$ git submodule init
$ git submodule update
```

Install dependencies:
```bash
$ pip install -r requirements.txt
```

Finally, create the local settings file from the template:
```bash
$ cp barachiel/settings/dev.py.dist barachiel/settings/dev.py
```

Development
------

### Endpoints
https://www.getpostman.com/collections/34aa7e80c34fb254bdc7

### Testing
To run the http server:
```shell
$ python -Wall manage.py test
```
