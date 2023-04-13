## Estructura del proyecto

Como equipo decidimos adoptar la estructura de proyecto que se muestra a continuación, tomada de múltiples fuentes,
entre ellas [este artículo](https://auth0.com/blog/best-practices-for-flask-api-development/) por parte de Auth0.

Esta estructura nos permite tener un proyecto bien organizado y que sea fácil de mantener y escalar, además de aplicar principios de diseño de software como el principio de responsabilidad única y el principio de segregación de interfaces.

```bash
app
├── .github
│   └── workflows
│       └── auto-merge-feature.yml
│       └── create-release.yml
├── common
│   ├── <all common file>
├── models
│   ├── <all models>
├── routes
│   ├── <all API routes with their controllers>
├── schema
│   ├── <all schema files>
├── service
├── <all services (business logic)>
├── .gitignore
├── app.py
├── config.py
├── README.md
├── requirements.txt
```

### Descripción de la estructura

- **.github**: Contiene los archivos de configuración de Github Actions.
- **app**: Contiene todos los archivos relacionados con la API.
  - **common**: Contiene archivos comunes a toda la aplicación, como constantes, excepciones, etc.
  - **models**: Contiene los modelos de la base de datos usando SQLAlchemy.
  - **routes**: Contiene los archivos de rutas de la API, en la cual se describen los controladores de cada servicio expuesto. Estos archivos se encargan de recibir la petición, validarla y llamar al servicio correspondiente. Se utilizaron los blueprints de Flask para organizar las rutas.
  - **schema**: Contiene los archivos de esquemas de la API usando Marshmallow.
  - **service**: Contiene los archivos de servicios de la API que contienen la lógica de negocio de la aplicación.
- **.gitignore**: Contiene los archivos que deben ser ignorados por Git.
- **app.py**: Archivo principal de la aplicación.
- **config.py**: Archivo de configuración de la aplicación.
- **README.md**: Archivo de documentación del proyecto.
- **requirements.txt**: Archivo de dependencias del proyecto.

## Ejecución de la aplicación

Para ejecutar la aplicación se debe tener instalado:

- **Python** 3.10+
- **Redis** 7.0.10
- **Redis-cli** 7.0.10

> Documentación de como instalar `Redis` en  [linux](https://redis.io/docs/getting-started/installation/install-redis-on-linux/), [windows](https://redis.io/docs/getting-started/installation/install-redis-on-windows/) y [mac](https://redis.io/docs/getting-started/installation/install-redis-on-mac-os/)

Por otro lado, se debe tener redis ejecutandose y celery

> Documentación de como ejecutar `Celery` en [linux](https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#starting-the-worker), [windows](https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#starting-the-worker) y [mac](https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#starting-the-worker)

```bash
celery -A app.celery worker --loglevel=info
```

> Documentación de como ejecutar redis en [linux](https://redis.io/topics/quickstart), [windows](https://redis.io/topics/quickstart) y [mac](https://redis.io/topics/quickstart)

```bash
redis-server
```

Posteriormente, se ejecutan los siguientes comandos:

```bash
pip install -r requirements.txt
gunicorn app:app
```

## Documentacion de la API en Postman

En el siguiente link se encuentra la documentación de la API en Postman:

https://documenter.getpostman.com/view/5708228/2s93XvV4bZ