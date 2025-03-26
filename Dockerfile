FROM ubuntu:22.04
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    sudo \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN python3 -m pip install --upgrade pip && \
    pip install fastapi Jinja2 uvicorn  pydantic  scipy numpy PyQt6 librosa matplotlib scikit-learn fastdtw python-multipart
    
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]