FROM python:3.12-slim

ARG GEMINI_API_KEY=key 
ENV GEMINI_API_KEY=$GEMINI_API_KEY

RUN apt-get update 

WORKDIR /crowdcast_app 

COPY requirements.txt /crowdcast_app/requirements.txt 

RUN pip install -r requirements.txt 

COPY src/ /crowdcast_app/src/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]