FROM python

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY requirements.txt requirements.txt
COPY poetry.lock pyproject.toml /app/

RUN apt-get update && apt-get install build-essential default-jdk -y
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

RUN pip install --no-cache-dir -r requirements.txt
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY /app /app
COPY /models /app/models

CMD [ "python", "server.py"]