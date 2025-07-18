FROM python

WORKDIR /app

ENV PYTHONPATH=/app
COPY poetry.lock pyproject.toml requirements.txt /app/
COPY /protobuf /app/protobuf
COPY /reddit_scrapper /app/reddit_scrapper
COPY /service /app/service
COPY /models /app/models

RUN apt-get update && apt-get install build-essential default-jdk -y
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

RUN pip install --no-cache-dir -r requirements.txt
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root


CMD [ "python", "-m", "reddit_scrapper.main" ]