FROM python:3.12


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./powerplantapp /code/powerplantapp

ENV PYTHONPATH /code:$PYTHONPATH

CMD ["fastapi", "run", "powerplantapp/api/post.py", "--port", "8888"]