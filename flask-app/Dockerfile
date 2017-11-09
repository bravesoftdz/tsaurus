FROM python:3
LABEL maintainer="dina" description="sample web app for tsaurus"

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["app.py"]

