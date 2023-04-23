# Um Dockerfile para o ambiente de desenvolvimento
FROM python:3.10.2-slim

RUN apt update && apt install -y --no-install-recommends \
                                  default-jre \
                                  git \
                                  zsh \
                                  curl \
                                  wget

# cria um usuário chamado python
RUN useradd -ms /bin/bash python

# entra como o usuário python
USER python

RUN pip install pdm

# Trabalha na pasta HOME do usuário python
WORKDIR /home/python/app

ENV MY_PYTHON_PACKAGES=/home/python/app/__pypackages__/3.10
# adiciona o diretório ao PYTHONPATH para encontrar os módulos dentro do src/
# colons separated
ENV PYTHONPATH=/home/python/app/src
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:${MY_PYTHON_PACKAGES}/bin

RUN echo 'eval "$(pdm --pep582)"' >> ~/.bashrc

# Coloca apenas o CMD pois é container de desenvolvimento e não é um serviço
# Aponta para o tail /dev/null para manter o container de pé
CMD [ "./.docker/entrypoint.sh" ]
