ARG PYTHON_VERSION=3.10.11
FROM python:${PYTHON_VERSION}-slim AS base
LABEL authors="sibe"

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


COPY . .

CMD ["python", "message_checker/receive.py"]