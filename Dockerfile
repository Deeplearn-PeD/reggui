FROM ubuntu:24.04

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# to run poetry directly as soon as it's installed
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PGURL="postgresql://postgres:eueueu@db:5432/regdbot"

RUN apt-get update && apt-get install -y python3 python3-pip curl git
RUN apt-get install -y build-essential ca-certificates
RUN apt-get install -y libmpv2
RUN ln -s /usr/lib/x86_64-linux-gnu/libmpv.so.2 /usr/lib/x86_64-linux-gnu/libmpv.so.1
RUN apt-get install -y sox uvicorn

# Change shell to bash
SHELL ["/bin/bash", "-c"]

RUN useradd -m reggie
RUN usermod -aG sudo reggie

RUN curl -sSL https://install.python-poetry.org | python3 -

#USER libby

COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .
COPY reggui /reggui/
COPY ./Docker/poetry_install.sh /scripts/poetry_install.sh
COPY ./Docker/entrypoint.sh /scripts/entrypoint.sh


RUN /scripts/poetry_install.sh

RUN . .venv/bin/activate



ENTRYPOINT ["/bin/bash","-c","/scripts/entrypoint.sh"]
#CMD ["uvicorn", "libbygui.main:run", "--host", "0.0.0.0", "--port", "8860"]




