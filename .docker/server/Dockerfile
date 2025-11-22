ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

## ---------------------------------------------------------
## Argumentos (valores del archivo .env)
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
## Actualizar pip y instalar herramientas base
## ---------------------------------------------------------

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

## ---------------------------------------------------------
## Configurar directorio de trabajo
## ---------------------------------------------------------

WORKDIR /app

## ---------------------------------------------------------
## Copiar requirements.txt e instalar dependencias Python
## ---------------------------------------------------------

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

## ---------------------------------------------------------
## Copiar el contenido de la aplicación
## ---------------------------------------------------------

COPY --chown=${MY_USER}:${MY_GROUP} . /app

## ---------------------------------------------------------
## Configurar bash
## ---------------------------------------------------------

RUN echo ". /etc/terminal" | tee -a /home/${MY_USER}/.bashrc /root/.bashrc && \
    chown ${MY_USER}:${MY_GROUP} /home/${MY_USER}/.bashrc
COPY ./server/bash/terminal /etc/terminal
COPY ./server/bash/sudo-user /etc/sudoers.d/sudo-user

## ---------------------------------------------------------
## Exponer el puerto 5000 (Flask por defecto)
## ---------------------------------------------------------

EXPOSE 5000

## ---------------------------------------------------------
## Comando por defecto
## ---------------------------------------------------------

CMD ["python", "app.py"]
