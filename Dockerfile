# syntax=docker/dockerfile:1

FROM registry.access.redhat.com/ubi8/python-39
ENV APP_ROOT=/opt/app-root
ENV PATH=${APP_ROOT}/bin:${PATH} HOME=${APP_ROOT}
COPY bin/ ${APP_ROOT}/bin/
USER 10001
WORKDIR ${APP_ROOT}
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
COPY . .
USER root
RUN chmod -R u+x ${APP_ROOT}/bin && \
    chgrp -R 0 ${APP_ROOT} && \
    chmod -R g=u ${APP_ROOT} /etc/passwd
USER 10001
WORKDIR ${APP_ROOT}
# Maintained in bin/uid_entrypoint.sh. This makes sure the arbitrary user name works in OpenShift deployments.
ENTRYPOINT [ "uid_entrypoint.sh" ]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]