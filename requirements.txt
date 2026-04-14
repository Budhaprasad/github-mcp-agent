FROM python:3.11-slim

# Install system + node
RUN apt-get update && apt-get install -y \
    curl git build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install MCP GitHub server
RUN npm install -g @modelcontextprotocol/server-github

CMD ["python", "github_agent.py"]
