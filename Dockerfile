FROM python:3.9


COPY  requirements* ./
COPY . app

RUN pip install -r requirements.txt

RUN useradd appuser && chown -R appuser /app
USER appuser
WORKDIR /app
EXPOSE 80
CMD    ["python", "bot.py"]
