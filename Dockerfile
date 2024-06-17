FROM python:3.7.0

LABEL Author=Stars

WORKDIR /home/project

COPY . .

RUN python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt && python manage.py collectstatic --noinput --clear&& python manage.py makemigrations && python manage.py migrate

ENTRYPOINT ["python","manage.py","runserver","[::]:8000"]