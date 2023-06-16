FROM python:3.10
COPY ./flask ./
RUN pip install -r requirements.txt
CMD flask run --host=0.0.0.0