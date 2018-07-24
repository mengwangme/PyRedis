FROM python:3.6-jessie
COPY dist/PyRedis-1.0.0-py3-none-any.whl /root/
COPY pyredis /etc/init.d/
RUN chmod +x /etc/init.d/pyredis
RUN pip install /root/PyRedis-1.0.0-py3-none-any.whl
CMD /etc/init.d/pyredis start && /bin/bash
