FROM alpine:3.6
ENV TZ=Asia/Tehran

RUN apk apk update && \
    apk add tzdata curl bash python3 && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip && \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo "${TZ}" > /etc/timezone && \
    touch /.python_history && \
    chgrp -R 0        /.python_history /var/log /var/run /var/tmp && \
    chmod -R g=u,a+rx /.python_history /var/log /var/run /var/tmp && \
    rm -rf /var/cache/apk/* 

WORKDIR /usr/src/app
COPY ./src .
RUN pip install --no-cache-dir -r dependencies.txt && \
    chgrp -R 0 . && \
    chmod -R g=u .

RUN mkdir /usr/src/app/tweets/
USER 1001
ENTRYPOINT ["python", "bigbrother.py"]
