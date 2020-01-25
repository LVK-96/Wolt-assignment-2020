FROM python:alpine
WORKDIR /code
RUN pip install pipenv
COPY . .
RUN pipenv install --dev --system
ENV FLASK_APP=app/app
ENV FLASK_ENV=development
EXPOSE 5000
CMD flask run --host=0.0.0.0
