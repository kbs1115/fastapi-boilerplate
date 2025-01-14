# Dockerfile
FROM python:3.10-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y build-essential

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설치
RUN pip install poetry

# Poetry 설정: 가상 환경을 생성하지 않도록 설정
RUN poetry config virtualenvs.create false

# 의존성 설치
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-interaction --no-ansi

# 소스 코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 실행 명령어
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
