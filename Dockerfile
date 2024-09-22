FROM python:3.9-slim

WORKDIR /Task-Manager-using-Flask

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "todo_project/run.py"]