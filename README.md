<p align="center">
   <img src="./img/header.png" height=120>
</p>

[![Website shields.io](https://img.shields.io/website-up-down-success-red/http/shields.io.svg)](https://ghoschts-django-twitter.herokuapp.com/)
[![Django CI](https://github.com/GHOSCHT/Django-Twitter/workflows/Django%20CI/badge.svg)](https://github.com/GHOSCHT/Django-Twitter/actions?query=workflow%3A%22Django+CI%22)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c5ae7c129cb44bd7be166710410c7e06)](https://www.codacy.com/manual/GHOSCHT/Django-Twitter?utm_source=github.com&utm_medium=referral&utm_content=GHOSCHT/Django-Twitter&utm_campaign=Badge_Grade)


## Getting Started

### Installation

1.  Clone the repo

```sh
git clone https://github.com/GHOSCHT/material-ui-todo-list.git
```

2.  Install all required modules

```sh
pipenv install
```

3.  Collect all static files

```sh
py manage.py collectstatic
```

4. Set environment variables listed below:

-   **consumer_key**, **consumer_secret**, **access_token**, **access_token_secret** for Twitter API authentication
-   **secret_key**
-   **HEROKU_DEPLOY** when deployed on heroku (value isn't important)


## Development server

Start the development server

```sh
py manage.py runserver
```

## Built With

-   [Django](https://www.djangoproject.com/)
-   [Tweepy](https://www.tweepy.org/)

## License

Distributed under the MIT License. See `LICENSE` for more information.
