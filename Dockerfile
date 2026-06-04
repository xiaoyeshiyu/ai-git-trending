# Stage 1: Build frontend
FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build-only

# Stage 2: Final image
FROM python:3.12-slim
WORKDIR /app

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist/

RUN mkdir -p /app/output

VOLUME ["/app/output"]

EXPOSE 5001

ENV PYTHONUNBUFFERED=1

CMD ["python", "backend/app.py", "--host", "0.0.0.0", "--port", "5001", "--mode", "full"]
