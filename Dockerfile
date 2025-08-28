FROM python:3.12-slim


RUN apt-get update && apt-get install -y \
    firefox-esr \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /usr/src/app


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]

