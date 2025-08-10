FROM python:3.13-slim AS builder

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv

RUN python3 -m venv .venv

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

FROM python:3.13-slim AS prod

WORKDIR /app

COPY requirements.txt .

COPY --from=deps /app/.venv /app/.venv

RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser
    
USER appuser

COPY . .    

EXPOSE 8000

ENV PATH="/app/.venv/bin:$PATH"

CMD ["fastapi", "run", "main.py"]