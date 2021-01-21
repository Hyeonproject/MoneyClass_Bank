FROM python:3.9

RUN pip install fastapi uvicorn python-jose[cryptography] tortoise-orm[aiomysql]

EXPOSE 80

COPY ./bankapi /bankapi

CMD ["uvicorn", "bankapi.main:app", "--host", "0.0.0.0", "--port", "80"]