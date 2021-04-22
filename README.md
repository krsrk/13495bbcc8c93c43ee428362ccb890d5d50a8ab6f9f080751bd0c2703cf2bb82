# Yachay Test


## Deploy

### General

El ambiente de desarrollo se hizo en "Docker", por lo que se tiene que tener "Docker" instalado en la PC
o workstation, asi como tambien "Docker Compose". Se incluyeron tres servicios; uno que representa el backend que es
la imagen de Python, la imagen de Node que representa el frontend y la imagen de MariDb que es la base de datos.

### Instalación

Una vez instalado Docker, se deben seguir los siguientes pasos para levantar el entorno:

1.- Clonar el repositorio: 

```bash
$ git clone https://github.com/krsrk/13495bbcc8c93c43ee428362ccb890d5d50a8ab6f9f080751bd0c2703cf2bb82.git yachay
``` 

2.- Nos cambiamos al repositorio clonado:

```bash
$ cd yachay
``` 

3.- Contruimos las imagenes de los servicios: `docker-compose build`

```bash
$ docker-compose build
``` 

4.- Levantamos los servicios: `docker-compose up -d`

```bash
$ docker-compose up -d
``` 


### Backend

Para levantar el servidor de la API o Backend debemos de ejecutar el siguiente comando:

```bash
$ docker-compose exec api uvicorn main:app --reload --port 8889 --host 0.0.0.0
``` 

La opción **--reload** es para reiniciar el servidor cuando detecte cambios en los scripts de Python, en production no se usa esta opción.

#### Base de datos
Para acceder al servidor de base de datos se debe configurar en algun IDE o visor de base de datos la siguiente información:
* HOST: localhost
* PORT: 8891
* USER: root
* PASS: root

Esta información tambien se encuentra en el archivo **docker-compose.yml** en este proyecto. 

La base de datos tiene le motor de Maria DB, asi que tambien se tiene que tener
instalado el driver de este motor de base de datos, por lo general los IDES o visores de base de datos lo instalan a la hora de configurarlo.

###Frontend

Para levantar el servidor web del frontend se debe ejecutar el siguiente comando:

```bash
$ docker-compose exec front npm run dev
``` 

Para hacer el deploy en production y stagging se debe ejecutar estos comando:

```bash
$ docker-compose exec front npm run build
$ docker-compose exec front npm run start
``` 
