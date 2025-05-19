FROM python:3.12.10-slim-bookworm

WORKDIR /app

COPY . /app

RUN apt update -y
RUN pip install -r requirements.txt
RUN python3 main.py

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501"]