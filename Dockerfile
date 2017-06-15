FROM resin/raspberrypi3-alpine-python:3-slim

ENV DJANGO_SETTINGS_MODULE=twisted_brew.settings \
    PROJECT_DIR=/distribrewed \
    TMP_DIR=/tmp_dir

COPY ./requirements.txt ${TMP_DIR}/requirements.txt

RUN pip install -r ${TMP_DIR}/requirements.txt && rm -r ${TMP_DIR}

COPY ./distribrewed ${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}
CMD ["python","-u","manage.py","twisted_brew","./config/twisted_brew.yml"]