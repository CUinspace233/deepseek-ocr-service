FROM python:3.11-slim

WORKDIR /app

RUN set -xe; \
    . /etc/os-release; \
    rm -f /etc/apt/sources.list.d/debian.sources; \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian ${VERSION_CODENAME} main contrib non-free" > /etc/apt/sources.list; \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian ${VERSION_CODENAME}-updates main contrib non-free" >> /etc/apt/sources.list; \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security ${VERSION_CODENAME}-security main contrib non-free" >> /etc/apt/sources.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV DEEPSEEK_API_KEY=""

EXPOSE 8600

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8600"]
