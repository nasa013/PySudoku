FROM python:3.10-slim

WORKDIR /app

COPY pysudoku/ ./pysudoku/
COPY data/ ./data/


ENTRYPOINT ["python", "-m", "pysudoku"]