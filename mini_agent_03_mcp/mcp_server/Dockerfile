FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mcp_server ./mcp_server

WORKDIR /app/mcp_server
EXPOSE 8010

CMD ["python", "travel_server.py"]
