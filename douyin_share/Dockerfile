FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY main.py ./

RUN pip install fastapi uvicorn requests

EXPOSE 8050

CMD uvicorn main:app --host=0.0.0.0 --port=8050
