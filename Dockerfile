FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -m -u 1000 user
USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user:user . $HOME/app

RUN pip install --no-cache-dir -r requirements.txt uv
RUN uv sync --no-install-project

EXPOSE 7860

CMD ["python", "server/app.py"]
