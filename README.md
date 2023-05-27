# Aplicaciones en la nube - MISW4204

## Generalidades del proyecto

### Nombre

BACKEND REST + PROCESAMIENTO ASÍNCRONO

### Descripción

Una nueva compañía de cloud denominada cloud conversion tool (ver ejemplo similar real
enhttps://www.online-convert.com/) desea crear una aplicación web que será ofrecida gratuitamente a
usuarios de internet para que estos puedan subir abiertamente diferentes formatos multimedia de
archivos y cambiarles su formato o realizar procesos de compresión.

El modelo general de funcionamiento de la aplicación se basa en crear una cuenta en el portal web y
acceder al administrador de archivos. Una vez la cuenta ha sido creada, el usuario puede subir archivos y
solicitar el cambio de formato de estos para descargarlos. La aplicación web le permite a un usuario
convertir archivos multimedia en línea de un formato a otro, seleccionando únicamente el formato
destino.

En el alcance inicial de la aplicación, no se tendrá una interfaz gráfica de usuario, sino que se comunicará
directamente con la API REST. Para esto, se debe crear un API REST que permita a los usuarios subir archivos y
convertirlos a los formatos listados a continuación:

* ZIP, 7Z, TAR.GZ, TAR.BZ2

## Integrantes

- [Brayan Henao](https://github.com/brayanhenao)
- [Felipe Cerquera](https://github.com/pipeCer)
- [Erik Loaiza](https://github.com/erikloaiza)
- [Rodrigo Escobar](https://github.com/ocralo)

# Contenido del proyecto

## Estructura del proyecto

Como equipo, decidimos adoptar la siguiente estructura de proyecto, la cual se muestra a continuación. Esta estructura
ha sido tomada de múltiples fuentes,
incluido [este artículo](https://auth0.com/blog/best-practices-for-flask-api-development) de Auth0.

Esta estructura nos permite tener un proyecto bien organizado y fácil de mantener y escalar. Además, nos permite aplicar
principios de diseño de software como el principio de responsabilidad única y el principio de segregación de interfaces.

```bash
├── .github
    ├── workflows <all github actions>
├── apm
    ├── grafana <all grafana dashboards>
    ├── prometheus <all prometheus config>
├── app
    ├── common <all common files>
    ├── models <all models>
    ├── routes <all API routes with their controllers>
    ├── schema <all schema files>
    ├── service <all services (business logic)>
    ├── .gcloudignore
    ├── app.py
    ├── app.yaml
    ├── celery_jobs.py <deprecated file with old celery config>
    ├── config.py
    ├── Dockerfile
    ├── requirements.txt
    ├── worker.py
    ├── worker.yaml
├── docker-compose <all docker-compose files>
├── load-test <all load test files using jmeter>

```

### Descripción de la estructura

- **.github**: Contiene los archivos de configuración de GitHub Actions.
- **apm**: Contiene los paneles de control de Grafana y la configuración de Prometheus.
    - **grafana**: Contiene todos los paneles de control de Grafana.
    - **prometheus**: Contiene la configuración de Prometheus.
- **app**: Contiene todos los archivos relacionados con la aplicación.
    - **common**: Contiene archivos comunes para toda la aplicación, como constantes, excepciones, etc.
    - **models**: Contiene los modelos de la base de datos usando SQLAlchemy.
    - **routes**: Contiene los archivos de rutas de la API, donde se describen los controladores de cada ruta expuesta.
      Estos archivos se encargan de recibir las solicitudes, validarlas y llamar al controlador correspondiente. Se
      utilizan los blueprints de Flask para organizar las rutas.
    - **schema**: Contiene los archivos de esquemas de la API.
    - **service**: Contiene los archivos de servicios de la API que contienen la lógica de negocio de la aplicación.
    - **.gcloudignore**: Archivo que especifica los archivos a ignorar para Google Cloud.
    - **app.py**: Archivo principal de la aplicación.
    - **app.yaml**: Archivo de configuración de la aplicación para el despliegue en Google App Engine.
    - **celery_jobs.py**: Archivo obsoleto con la antigua configuración de Celery.
    - **config.py**: Archivo de configuración de la aplicación.
    - **Dockerfile**: Archivo de configuración para construir la imagen de Docker.
    - **requirements.txt**: Archivo de dependencias del proyecto.
    - **worker.py**: Archivo relacionado con el worker que procesa los archivos.
    - **worker.yaml**: Archivo de configuración del worker para el despliegue en Google App Engine.
- **docker-compose**: Contiene todos los archivos de docker-compose.
- **load-test**: Contiene todos los archivos de prueba de carga utilizando JMeter.

## Ejecución de la aplicación

Para ejecutar la aplicación, es necesario tener instalado:

- **Python** 3.10+

Y se deben instalar los requisitos necesarios utilizando el siguiente comando:

```bash
pip install -r requirements.txt
```

**Nota:** En el servidor WEB y en el worker, se debe establecer la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS `
con la ruta a la cuenta de servicio.

### Ejecutar el worker

Para ejecutar el worker, se debe utilizar el siguiente comando:

```bash
python app/worker.py
```

Se deben tener las siguientes variables de entorno para su correcto funcionamiento:

- `SUBSCRIPTION_ID`: ID de la suscripción en Pub/Sub
- `PROJECT_ID`: ID del proyecto en GCP

### Ejecutar el servidor web

```bash
gunicorn app:app -w 4 --access-logfile - --error-logfile - --log-level info
```

Se deben tener las siguientes variables de entorno para su correcto funcionamiento:

- `DB_URI`: URI de la base de datos Cloud SQL

## Despliegue en Google Cloud Platform (App Engine)

Para la entrega final, se decidió desplegar la aplicación en Google Cloud Platform utilizando App Engine, la solución
PaaS que nos permite desplegar aplicaciones de forma rápida y sencilla, permitiendo escalar la aplicación de manera
automática.

En el archivo `<service>.yaml` se encuentra la configuración del despliegue de cada servicio, utilizando las siguientes
características:

- **runtime**: `python310`
    - Especifica la versión de Python utilizada en el entorno de ejecución.
- **service**: `web` o `worker`
    - Define el servicio como una aplicación web.
- **instance_class**: `F4_1G` para el servicio web y `F4` para el servicio worker
    - Especifica la clase de instancia utilizada para el servicio. En este caso, se utiliza una instancia de tipo F4 con
      1 GB de memoria.
- **service_account**: `entrega-5@aplicaciones-en-la-nube-382813.iam.gserviceaccount.com`
    - Define la cuenta de servicio utilizada por la aplicación para acceder a los recursos de Google Cloud.
- **entrypoint**: `gunicorn <service> -w 4 --access-logfile - --error-logfile - --log-level info`
    - Especifica el punto de entrada para la aplicación. En este caso, se utiliza Gunicorn como servidor WSGI y se
      configuran algunos parámetros relacionados con el logging y el número de workers.
- **env_variables**:
    - Define variables de entorno utilizadas por la aplicación.
    - **PROJECT_ID**: `"aplicaciones-en-la-nube-382813"`
        - Especifica el ID del proyecto de Google Cloud.
- **automatic_scaling**:
    - Configura el escalado automático del servicio.
    - **max_instances**: `3`
        - Establece el número máximo de instancias en 3, lo que significa que el servicio puede escalar hasta 3
          instancias.
    - **min_instances**: `1`
        - Establece el número mínimo de instancias en 1, lo que garantiza que siempre haya al menos una instancia en
          ejecución.
- **vpc_access_connector**:
    - Define un conector de acceso VPC para el servicio.
    - **name**: `"projects/aplicaciones-en-la-nube-382813/locations/us-central1/connectors/db-connector"`
        - Especifica el nombre del conector de acceso VPC utilizado por el servicio para acceder a la base de datos
          usando una IP privada.

Para desplegar la aplicación en Google Cloud Platform, es necesario tener instalado:

- **Google Cloud SDK** 356.0.0+
- **Python** 3.10+

### Despliegue de la aplicación

Para desplegar la aplicación, ejecuta el siguiente comando:

```bash
gcloud app deploy app.yaml
```

### Despliegue del worker

Para desplegar el worker, ejecuta el siguiente comando:

```bash
gcloud app deploy worker.yaml
```

## Documentacion de la API en Postman

En el siguiente enlace se encuentra la documentación de la API en Postman:

https://documenter.getpostman.com/view/5708228/2s93XvV4bZ
