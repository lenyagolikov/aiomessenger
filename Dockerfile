FROM snakepacker/python:all as builder

RUN python3.9 -m venv /usr/share/python3/app
RUN /usr/share/python3/app/bin/pip install -U pip

COPY requirements.txt /tmp/
RUN /usr/share/python3/app/bin/pip install -Ur /tmp/requirements.txt

COPY . tmp/
WORKDIR /tmp/

RUN /usr/share/python3/app/bin/pip install .

FROM snakepacker/python:3.9

COPY --from=builder /usr/share/python3/app /usr/share/python3/app

RUN ln -snf /usr/share/python3/app/bin/messenger-* /usr/local/bin/

CMD ["sh", "-c", "messenger-db upgrade head; messenger-api"]

