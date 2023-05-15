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

E instalar los requerimientos necesarios con el comando:

```bash
pip install -r requirements.txt
```

**Nota:** En el servidor WEB y en el worker se deben tener establecida la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS` con el path a la cuenta de servicio.

### Ejecutar el worker

Para ejecutar el worker, se debe ejecutar el comando. 

```bash
python app/worker.py
```

Se deben tener las siguientes variables de entorno para su funcionamiento:

- `SUBSCRIPTION_ID`: ID de la suscripción en Pub/Sub
- `PROJECT_ID`: ID del proyecto en GCP


### Ejecutar el servidor web


```bash
gunicorn app:app -w 4 --access-logfile - --error-logfile - --log-level info
```


Se deben tener las siguientes variables de entorno para su funcionamiento:

- `DB_URI`: URI de la base de datos Cloud SQL

## Documentacion de la API en Postman

En el siguiente link se encuentra la documentación de la API en Postman:

https://documenter.getpostman.com/view/5708228/2s93XvV4bZ
