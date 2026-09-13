FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN mkdir -p uploads backend

EXPOSE 3000

ENV PORT=3000

CMD ["python", "backend/server.py"]
