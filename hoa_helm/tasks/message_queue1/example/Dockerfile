ARG PYTHON_VERSION=3.10.11
FROM python:${PYTHON_VERSION}-slim AS base
LABEL authors="sibe"

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . .

CMD ["python", "message_sender/send.py"]