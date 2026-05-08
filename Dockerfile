FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p results/bernhard_run

CMD ["python", "main.py", "--config", "configs/run_config_bernhard.yaml"]
