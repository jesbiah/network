FROM python:3
COPY . /usr/src/app
WORKDIR /usr/src/app/project4
RUN pip install -r ../requirements.txt && apt-get update && apt install -y firefox-esr wget && wget https://github.com/mozilla/geckodriver/releases/download/v0.37.1/geckodriver-v0.37.1-linux-aarch64.tar.gz && tar -xzf geckodriver-v0.37.1-linux-aarch64.tar.gz
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]