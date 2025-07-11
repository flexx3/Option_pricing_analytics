FROM python:3.12.7


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./Option_pricer_app /code/Option_pricer_app


CMD ["python", "Option_pricer_app/main.py"]
