FROM python:3.10-buster

WORKDIR /app

COPY . .

RUN pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN poetry source add --priority=default mirrors https://pypi.tuna.tsinghua.edu.cn/simple/
RUN poetry install

CMD [ "poetry", "run", "uvicorn", "XYUnionAuth.asgi:application", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80