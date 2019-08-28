FROM harbor.wise-paas.io/distroless/python3:latest
WORKDIR /redmine
ADD . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD [ "python", "./app.py" ]