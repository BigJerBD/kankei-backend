FROM python:3.7

ENV KANKEI_WEB_SETTINGS  ./src/settings/prod.py

COPY . /kankei_backend/

WORKDIR /kankei_backend/
RUN pip install --trusted-host pypi.python.org -r ./requirements.txt
EXPOSE 5000
CMD ["python", "src/server.py"]

