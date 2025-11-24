ARG BASE_IMAGE
ARG BASE_IMAGE_VERSION
ARG BASE_IMAGE_VARIANT
FROM ${BASE_IMAGE}:${BASE_IMAGE_VERSION}-${BASE_IMAGE_VARIANT}

## ---------------------------------------------------------
## Argumentos
## ---------------------------------------------------------

ARG NEW_UID
ARG NEW_GID
ARG MY_USER
ARG MY_GROUP

## ---------------------------------------------------------
## Instalar dependencias del sistema
## ---------------------------------------------------------

RUN set -eux && \
apt-get update && \
apt-get install -y \
    git \
    curl \
    nano \
    vim \
    tzdata \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    sudo && \
ln -fs /usr/share/zoneinfo/Europe/Madrid /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

## ---------------------------------------------------------
## Crear usuario y grupo
## ---------------------------------------------------------

RUN groupadd -g ${NEW_GID} -r ${MY_GROUP} && \
useradd -u ${NEW_UID} -m -s /bin/bash -g ${MY_GROUP} ${MY_USER}

## ---------------------------------------------------------
## Actualizar herramientas de gestión de paquetes Python
## (pip: instalador, setuptools: compilador, wheel: paquetes precompilados)
## ---------------------------------------------------------

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

## ---------------------------------------------------------
## Instalar dependencias de Python
## ---------------------------------------------------------

RUN pip install --no-cache-dir \
    Django==5.0.0 \
    mysqlclient==2.2.1 \
    python-dotenv==1.0.0 \
    django-cors-headers==4.3.1

## ---------------------------------------------------------
## Configurar directorio de trabajo
## ---------------------------------------------------------

WORKDIR /var/www/html

## ---------------------------------------------------------
## Copiar el contenido de la aplicación
## ---------------------------------------------------------

COPY --chown=${MY_USER}:${MY_GROUP} . /var/www/html

## ---------------------------------------------------------
## Configurar bash
## ---------------------------------------------------------

RUN echo ". /etc/terminal" | tee -a /home/${MY_USER}/.bashrc /root/.bashrc && \
    chown ${MY_USER}:${MY_GROUP} /home/${MY_USER}/.bashrc
COPY ./server/bash/terminal /etc/terminal
COPY ./server/bash/sudo-user /etc/sudoers.d/sudo-user

## ---------------------------------------------------------
## Configurar scripts
## ---------------------------------------------------------

COPY ./server/scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY ./server/scripts/wait-for-mysql.sh /usr/local/bin/wait-for-mysql.sh
RUN chmod +x /usr/local/bin/entrypoint.sh /usr/local/bin/wait-for-mysql.sh

## ---------------------------------------------------------
## Exponer el puerto 8081
## ---------------------------------------------------------

EXPOSE 8081

## ---------------------------------------------------------
## Comando por defecto con wait wrapper
## ---------------------------------------------------------

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/usr/local/bin/wait-for-mysql.sh", "python", "main.py"]
