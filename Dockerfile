FROM python:3.10.6-slim

RUN pip install openai sqlite-web

COPY *.py /app/
COPY *.db /app/

EXPOSE 8001

WORKDIR /app/
ENTRYPOINT [ "python",  "deus.py" ]
