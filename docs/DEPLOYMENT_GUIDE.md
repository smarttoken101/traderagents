# TradingAgents Deployment Guide

## Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Local Deployment](#local-deployment)
3. [Production Deployment](#production-deployment)
4. [Container Deployment](#container-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Monitoring & Logging](#monitoring--logging)
7. [Security Considerations](#security-considerations)
8. [Performance Optimization](#performance-optimization)
9. [Troubleshooting](#troubleshooting)

## Deployment Overview

The TradingAgents framework supports multiple deployment patterns:

- **Local Development**: Single-machine development environment
- **Production Server**: Dedicated server deployment
- **Container Deployment**: Docker containerization
- **Cloud Deployment**: AWS, GCP, Azure deployment
- **Hybrid Deployment**: Multi-cloud and on-premise combinations

### Deployment Requirements

#### Minimum System Requirements
- **CPU**: 2 cores, 2.4 GHz
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 10 GB available space
- **Network**: Stable internet connection for API access
- **OS**: Linux (Ubuntu 20.04+), macOS, Windows 10+

#### Recommended Production Requirements
- **CPU**: 8 cores, 3.0 GHz
- **RAM**: 16 GB minimum, 32 GB recommended
- **Storage**: 100 GB SSD
- **Network**: High-speed internet (100+ Mbps)
- **OS**: Linux (Ubuntu 22.04 LTS)

## Local Deployment

### Development Setup

```bash
# Clone repository
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents

# Create virtual environment
conda create -n tradingagents python=3.13
conda activate tradingagents

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your_openai_api_key"
export FINNHUB_API_KEY="your_finnhub_api_key"

# Run basic test
python main.py
```

### Local Configuration

Create `.env` file for local development:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key
FINNHUB_API_KEY=your_finnhub_api_key
TRADINGAGENTS_RESULTS_DIR=./results
TRADINGAGENTS_LOG_LEVEL=INFO
TRADINGAGENTS_DEBUG=false
```

Load environment variables:

```bash
# Install python-dotenv
pip install python-dotenv

# Load in Python
from dotenv import load_dotenv
load_dotenv()
```

## Production Deployment

### Production Server Setup

#### 1. System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.13
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev -y

# Install system dependencies
sudo apt install git curl build-essential -y
```

#### 2. Application Setup

```bash
# Create application user
sudo useradd -m -s /bin/bash tradingagents
sudo mkdir -p /opt/tradingagents
sudo chown tradingagents:tradingagents /opt/tradingagents

# Switch to application user
sudo -u tradingagents -i

# Deploy application
cd /opt/tradingagents
git clone https://github.com/TauricResearch/TradingAgents.git .
python3.13 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Environment Configuration

```bash
# Create production environment file
sudo -u tradingagents tee /opt/tradingagents/.env << EOF
OPENAI_API_KEY=your_production_openai_key
FINNHUB_API_KEY=your_production_finnhub_key
TRADINGAGENTS_RESULTS_DIR=/opt/tradingagents/results
TRADINGAGENTS_LOG_LEVEL=INFO
TRADINGAGENTS_CACHE_DIR=/opt/tradingagents/cache
TRADINGAGENTS_ENV=production
EOF

# Set secure permissions
sudo chmod 600 /opt/tradingagents/.env
```

#### 4. Service Configuration

Create systemd service file:

```bash
# /etc/systemd/system/tradingagents.service
sudo tee /etc/systemd/system/tradingagents.service << EOF
[Unit]
Description=TradingAgents Framework
After=network.target

[Service]
Type=simple
User=tradingagents
Group=tradingagents
WorkingDirectory=/opt/tradingagents
Environment=PATH=/opt/tradingagents/venv/bin
EnvironmentFile=/opt/tradingagents/.env
ExecStart=/opt/tradingagents/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable tradingagents
sudo systemctl start tradingagents
```

## Container Deployment

### Docker Setup

#### 1. Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 tradingagents && \
    chown -R tradingagents:tradingagents /app
USER tradingagents

# Create directories
RUN mkdir -p /app/results /app/cache /app/logs

# Expose port (if needed for web interface)
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV TRADINGAGENTS_RESULTS_DIR=/app/results
ENV TRADINGAGENTS_CACHE_DIR=/app/cache

# Run application
CMD ["python", "main.py"]
```

#### 2. Create Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  tradingagents:
    build: .
    container_name: tradingagents
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - FINNHUB_API_KEY=${FINNHUB_API_KEY}
      - TRADINGAGENTS_LOG_LEVEL=INFO
    volumes:
      - ./results:/app/results
      - ./cache:/app/cache
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - tradingagents-network

  redis:
    image: redis:7-alpine
    container_name: tradingagents-redis
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - tradingagents-network

networks:
  tradingagents-network:
    driver: bridge

volumes:
  redis_data:
```

#### 3. Build and Deploy

```bash
# Create environment file
echo "OPENAI_API_KEY=your_key" > .env
echo "FINNHUB_API_KEY=your_key" >> .env

# Build and run
docker-compose up -d

# View logs
docker-compose logs -f tradingagents

# Scale if needed
docker-compose up -d --scale tradingagents=3
```

### Kubernetes Deployment

#### 1. Create Namespace

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: tradingagents
```

#### 2. Create ConfigMap

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tradingagents-config
  namespace: tradingagents
data:
  TRADINGAGENTS_LOG_LEVEL: "INFO"
  TRADINGAGENTS_RESULTS_DIR: "/app/results"
  TRADINGAGENTS_CACHE_DIR: "/app/cache"
```

#### 3. Create Secret

```yaml
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: tradingagents-secrets
  namespace: tradingagents
type: Opaque
data:
  OPENAI_API_KEY: <base64-encoded-key>
  FINNHUB_API_KEY: <base64-encoded-key>
```

#### 4. Create Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tradingagents
  namespace: tradingagents
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tradingagents
  template:
    metadata:
      labels:
        app: tradingagents
    spec:
      containers:
      - name: tradingagents
        image: tradingagents:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: tradingagents-config
        - secretRef:
            name: tradingagents-secrets
        volumeMounts:
        - name: results-storage
          mountPath: /app/results
        - name: cache-storage
          mountPath: /app/cache
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
      volumes:
      - name: results-storage
        persistentVolumeClaim:
          claimName: results-pvc
      - name: cache-storage
        persistentVolumeClaim:
          claimName: cache-pvc
```

## Cloud Deployment

### AWS Deployment

#### 1. ECS Deployment

```json
{
  "family": "tradingagents",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "tradingagents",
      "image": "your-registry/tradingagents:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "TRADINGAGENTS_LOG_LEVEL",
          "value": "INFO"
        }
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:openai-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/tradingagents",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 2. Lambda Deployment

```python
# lambda_handler.py
import json
import os
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

def lambda_handler(event, context):
    """AWS Lambda handler for TradingAgents."""
    
    # Configure for Lambda
    config = DEFAULT_CONFIG.copy()
    config.update({
        "results_dir": "/tmp/results",
        "cache_dir": "/tmp/cache",
        "online_tools": True,
        "max_debate_rounds": 1,  # Optimize for Lambda timeout
    })
    
    # Extract parameters
    ticker = event.get('ticker', 'AAPL')
    date = event.get('date', '2024-05-10')
    
    try:
        # Initialize and run analysis
        ta = TradingAgentsGraph(config=config)
        final_state, decision = ta.propagate(ticker, date)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'ticker': ticker,
                'date': date,
                'decision': decision,
                'final_report': final_state.get('final_trade_decision', '')
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
```

### Google Cloud Deployment

#### Cloud Run Deployment

```yaml
# cloudrun.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: tradingagents
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/memory: "2Gi"
        run.googleapis.com/cpu: "2"
    spec:
      containers:
      - image: gcr.io/project-id/tradingagents
        ports:
        - containerPort: 8080
        env:
        - name: TRADINGAGENTS_LOG_LEVEL
          value: "INFO"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai-key
        resources:
          limits:
            memory: "2Gi"
            cpu: "2000m"
```

## Monitoring & Logging

### Application Monitoring

#### 1. Health Check Endpoint

```python
# health.py
from flask import Flask, jsonify
import os
import psutil

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint."""
    try:
        # Check system resources
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        # Check environment variables
        api_keys_present = all([
            os.getenv('OPENAI_API_KEY'),
            os.getenv('FINNHUB_API_KEY')
        ])
        
        status = {
            'status': 'healthy',
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
            'api_keys_configured': api_keys_present,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if memory_usage > 90 or disk_usage > 90:
            status['status'] = 'warning'
        
        return jsonify(status), 200
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

#### 2. Prometheus Metrics

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
analysis_counter = Counter('tradingagents_analyses_total', 'Total analyses performed')
analysis_duration = Histogram('tradingagents_analysis_duration_seconds', 'Analysis duration')
active_analyses = Gauge('tradingagents_active_analyses', 'Currently active analyses')
api_call_counter = Counter('tradingagents_api_calls_total', 'Total API calls', ['provider'])

def monitor_analysis(func):
    """Decorator to monitor analysis performance."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        active_analyses.inc()
        analysis_counter.inc()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            analysis_duration.observe(duration)
            active_analyses.dec()
    
    return wrapper

# Start metrics server
start_http_server(8090)
```

### Logging Configuration

```python
# logging_config.py
import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging():
    """Configure logging for production."""
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Configure formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Configure handlers
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(simple_formatter)
    console_handler.setLevel(logging.INFO)
    handlers.append(console_handler)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/tradingagents.log',
        maxBytes=50*1024*1024,  # 50MB
        backupCount=5
    )
    file_handler.setFormatter(detailed_formatter)
    file_handler.setLevel(logging.DEBUG)
    handlers.append(file_handler)
    
    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/errors.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=3
    )
    error_handler.setFormatter(detailed_formatter)
    error_handler.setLevel(logging.ERROR)
    handlers.append(error_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=handlers
    )
    
    # Configure specific loggers
    logging.getLogger('openai').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)
```

## Security Considerations

### API Key Management

```python
# secure_config.py
import os
from cryptography.fernet import Fernet

class SecureConfig:
    """Secure configuration management."""
    
    def __init__(self):
        self.cipher_suite = Fernet(self._get_encryption_key())
    
    def _get_encryption_key(self):
        """Get or generate encryption key."""
        key_file = '/etc/tradingagents/encryption.key'
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(key)
            os.chmod(key_file, 0o600)
            return key
    
    def encrypt_value(self, value):
        """Encrypt a configuration value."""
        return self.cipher_suite.encrypt(value.encode())
    
    def decrypt_value(self, encrypted_value):
        """Decrypt a configuration value."""
        return self.cipher_suite.decrypt(encrypted_value).decode()
```

### Network Security

```bash
# Configure firewall
sudo ufw enable
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw deny 8080/tcp  # Block direct access to app

# SSL/TLS configuration with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com

# Configure reverse proxy (Nginx)
sudo tee /etc/nginx/sites-available/tradingagents << EOF
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/tradingagents /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

## Performance Optimization

### Caching Configuration

```python
# cache_config.py
import redis
from functools import wraps
import json
import hashlib

class CacheManager:
    """Redis-based cache manager."""
    
    def __init__(self, redis_url='redis://localhost:6379/0'):
        self.redis_client = redis.from_url(redis_url)
        self.default_ttl = 3600  # 1 hour
    
    def cache_result(self, ttl=None):
        """Decorator to cache function results."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                key_data = f"{func.__name__}:{args}:{kwargs}"
                cache_key = hashlib.md5(key_data.encode()).hexdigest()
                
                # Try to get from cache
                cached_result = self.redis_client.get(cache_key)
                if cached_result:
                    return json.loads(cached_result)
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                cache_ttl = ttl or self.default_ttl
                self.redis_client.setex(
                    cache_key, 
                    cache_ttl, 
                    json.dumps(result, default=str)
                )
                
                return result
            return wrapper
        return decorator

# Usage
cache_manager = CacheManager()

@cache_manager.cache_result(ttl=1800)  # 30 minutes
def get_market_data(ticker, date):
    # Expensive market data retrieval
    pass
```

### Load Balancing

```bash
# HAProxy configuration
# /etc/haproxy/haproxy.cfg
global
    daemon
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend tradingagents_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/tradingagents.pem
    redirect scheme https if !{ ssl_fc }
    default_backend tradingagents_backend

backend tradingagents_backend
    balance roundrobin
    server app1 127.0.0.1:8001 check
    server app2 127.0.0.1:8002 check
    server app3 127.0.0.1:8003 check
```

## Troubleshooting

### Common Issues

#### 1. Memory Issues
```bash
# Monitor memory usage
free -h
ps aux --sort=-%mem | head

# Fix: Increase memory or optimize configuration
export TRADINGAGENTS_MAX_WORKERS=2
export TRADINGAGENTS_CACHE_SIZE=100
```

#### 2. API Rate Limiting
```python
# Implement exponential backoff
import time
import random

def with_retry(max_retries=3, base_delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
            
        return wrapper
    return decorator
```

#### 3. Disk Space Issues
```bash
# Monitor disk usage
df -h
du -sh /opt/tradingagents/*

# Clean up old results
find /opt/tradingagents/results -mtime +30 -delete
find /opt/tradingagents/logs -name "*.log.*" -mtime +7 -delete
```

### Performance Monitoring

```bash
# System monitoring script
#!/bin/bash
# monitor.sh

echo "=== TradingAgents System Monitor ==="
echo "Date: $(date)"
echo

echo "=== System Resources ==="
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2 $3 $4 $5}'

echo "Memory Usage:"
free -h

echo "Disk Usage:"
df -h /opt/tradingagents

echo

echo "=== Application Status ==="
systemctl status tradingagents --no-pager -l

echo

echo "=== Recent Errors ==="
tail -n 10 /opt/tradingagents/logs/errors.log

echo

echo "=== API Response Times ==="
curl -w "Time: %{time_total}s\n" -s -o /dev/null http://localhost:8080/health
```

This deployment guide provides comprehensive instructions for deploying TradingAgents in various environments, from development to production-scale cloud deployments. Choose the deployment method that best fits your requirements and infrastructure.