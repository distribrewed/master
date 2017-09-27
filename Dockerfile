FROM distribrewed/core:x64

# For psycopg2
RUN apk add --no-cache postgresql-dev g++

ENV APP_DIR=/opt/project/distribrewed
ENV PLUGIN_DIR=${APP_DIR}/masters \
    MASTER_PLUGIN_CLASS=DistribrewedMaster

COPY requirements.txt ${TMP_DIR}/requirements.txt
RUN pip install -r ${TMP_DIR}/requirements.txt && rm -rf ${TMP_DIR}/*

COPY /distribrewed ${APP_DIR}
WORKDIR ${APP_DIR}

CMD ["-A", "distribrewed", "worker", "-B", "-l", "info", "--concurrency", "4", "-s /tmp/celerybeat-schedule"]