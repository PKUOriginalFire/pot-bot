FROM python:3.11-slim
RUN pip install 'nonebot2[fastapi]' nonebot-adapter-onebot
COPY . /app
WORKDIR /app/data
CMD ["python", "/app/bot.py"]
