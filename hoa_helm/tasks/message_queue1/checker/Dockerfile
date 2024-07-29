ARG PYTHON_VERSION=3.10.11
FROM python:${PYTHON_VERSION}-slim AS base
LABEL authors="sibe"
LABEL description="status checker for task message_queue1\
this image runs a python script that checks for the presence of a message in a queue\
and exits gracefull if that message was found. In other cases, a status code != 0 is\
returned (e.g no message found, queue not found)."

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


COPY . .

CMD ["python", "message_checker/receive.py"]