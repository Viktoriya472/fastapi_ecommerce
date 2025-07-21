FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUNBUFFERED=1


WORKDIR /usr/src/app

COPY req.txt .
RUN pip install --upgrade pip && pip install -r req.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port","80"]

