# Arquitectura del proyecto de datos abiertos

La instalación de ckan se realizó sobre el directorio `/root`.

## Instalación de CKAN en servidor Debian

### Descarga de proyecto ckan:

El proyecto de CKAN se puede descargar en el siguiente enlace:

[CKAN github](https://github.com/ckan/ckan)

El tag que se está utilizando es 2.9.6

El directorio en el que es clonado es `/root/ckan`.

### HTTPS

Para habilitar HTTPS, es necesario agregar los archivos requeridos por
el servidor, usar la tabla como referencia:

| Archivo en repositorio                 | Directorio en el servidor |
| -------------------------------------- | ------------------------- |
| [nginx/nginx.conf](./nginx/nginx.conf) | /srv/nginx/nginx.conf     |
| Certificado SSL (lo provee GAMLP)      | /srv/nginx/cert.pem       |
| Llave de certificado (lo provee GAMLP) | /srv/nginx/key.pem        |

### Añadiduras al proyecto de CKAN

Para mantener el código original y a la vez extender funcionalidades extra,
se ha creado un archivo override de docker compose para poder agregar el servicio de HTTPS y autoheal.

Para ello se debe de copiar el archivo [`docker/docker-compose.override.yml`](./docker/docker-compose.override.yml) a `/root/ckan/contrib/docker/docker-compose.override.yml`.

### Servicio de systemd de CKAN

Para asegurarnos del funcionamiento de CKAN al momento de levantar el servidor
hemos instalado un servicio de systemd que indica al OS de debian que
arranque el servicio CKAN al momento de iniciar la máquina.

Todos los archivos necesarios están dentro del directorio `systemd`,
y deben ser copiados según la siguiente tabla:

| Archivo en repositorio                           | Directorio en servidor           |
| ------------------------------------------------ | -------------------------------- |
| [systemd/ckan.service](./systemd/ckan.service)   | /etc/systemd/system/ckan.service |
| [systemd/start-ckan.sh](./systemd/start-ckan.sh) | /root/start-ckan.sh              |

Después de copiar los archivos, se debe sincronizar systemd, habiliar el
servicio e iniciarlo:

```sh
$ systemctl daemon-reload
$ systemctl enable ckan.service
$ systemctl start ckan.service
```

## Instalación de plugins

### Acceso a contenedor y virtual env
Para instalar los plugins, seguir las guías de instalación de cada plugin.
Los comandos deben ejecutarse, por lo general, dentro del contenedor de
CKAN y en el virtualenv designado para ckan:
```sh
# en el servidor de debian
host-server~$ cd /root/ckan/contrib/docker
host-server~$ docker compose exec -it ckan /bin/bash

# Dentro del contenedor
ckan-container~$ source /usr/lib/ckan/venv/bin/activate
(venv) ckan-container~$ 
# Archivo de ckan.ini está en: /etc/ckan/production.ini
# A partir de acá seguir instrucciones de instalación de cada plugin
```
### Datapusher
Los detalles se encuentran dentro de la [Guía de instalación de CKAN](https://docs.google.com/presentation/d/1IZ8epOv1hPF0hhXg9ECA9oYPhC0sHkSmat-g1RO0mhY/edit?usp=sharing)

### Plugin la paz
Clonar el repositorio en el contenedor de CKAN, la copia existente se encuentra en: `/usr/lib/ckan/portal-de-datos-abiertos`

Actualizar repositorio e instalar usando `pip`:
```sh
(venv) ckan-container~$ cd /usr/lib/ckan/portal-de-datos-abiertos
(venv) ckan-container~$ git pull # se pedirá usuario y contraseña
(venv) ckan-container~$ python setup.py install # Instalará los nuevos cambios al venv
# Añadir lapaz a la lista de plugins en production.ini
```
```
```

Al finalizar los comandos, reiniciar el contenedor de ckan
```sh
(venv) ckan-container~$ exit

# En el host (debian):
host-server~$ docker compose restart ckan
```

### Plugin visualize
Clonar en el contenedor el siguiente repositorio:
[CKAN extension visualize](https://github.com/jper92/ckanext-visualize.git) e instalar:

[Acceder al contenedor y virtual env como está descrito anteriormente](#acceso-a-contenedor-y-virtual-env)

Ejecutar los comandos para clonar e instalar:
```sh
$ git clone https://github.com/jper92/ckanext-visualize
$ cd ckanext-visualize
$ python setup.py install
# Añadir visualize a la lista de plugins en production.ini
``` 
En debian, reiniciar contenedor de ckan:

```sh
$ docker compose restart ckan
```

### Plugin pages
Este plugin permite la adición de páginas a CKAN
Seguir la [Guía de instalación de pages](https://github.com/ckan/ckanext-pages#installation).

Ojo: El plugin pages recientemente dejó de soportar python 2.7, por lo que es necesario utilizar la versión 0.3.7:
```sh
$ pip install -e git+https://github.com/ckan/ckanext-pages@0.3.7#egg=ckanext-pages
```
