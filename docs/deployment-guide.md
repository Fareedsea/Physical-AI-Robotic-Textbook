# Deployment Guide

This guide covers the deployment of the Physical AI & Humanoid Robotics Textbook to production environments.

## Architecture Overview

The application consists of two main components that can be deployed independently:

1. **Frontend**: Static Docusaurus site (deployed to GitHub Pages or static hosting)
2. **Backend**: FastAPI application (deployed to container platform or VM)

## Prerequisites

### System Requirements

#### Backend Server
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 10GB available space (more if storing large vector indexes)
- **OS**: Linux (Ubuntu 20.04+ recommended)
- **Python**: 3.8+ with pip
- **Optional**: NVIDIA GPU with CUDA for accelerated embeddings

#### Static Hosting (Frontend)
- Any static file hosting service (GitHub Pages, Netlify, Vercel, S3, etc.)

## Deployment Options

### Option 1: GitHub Pages + Self-Hosted Backend (Recommended)

This is the simplest deployment option using GitHub Pages for the frontend and a self-hosted server for the backend.

#### Frontend Deployment (GitHub Pages)

1. **Configure GitHub Actions**:
   Ensure `.github/workflows/deploy.yml` exists with the following content:
   ```yaml
   name: Deploy to GitHub Pages

   on:
     push:
       branches: [main]

   jobs:
     deploy:
       name: Deploy to GitHub Pages
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-node@v3
           with:
             node-version: 18
             cache: npm
         - name: Install dependencies
           run: npm install
         - name: Build website
           run: npm run build
         - name: Deploy to GitHub Pages
           uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./build
   ```

2. **Configure Docusaurus** (`docusaurus.config.ts`):
   ```javascript
   const config = {
     // ... other config
     url: 'https://your-username.github.io',
     baseUrl: '/your-repo-name/',
     organizationName: 'your-username',
     projectName: 'your-repo-name',
     deploymentBranch: 'gh-pages',
     // ... rest of config
   };
   ```

3. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Configure GitHub Pages deployment"
   git push origin main
   ```

#### Backend Deployment (Self-Hosted)

1. **Prepare the server**:
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python and pip
   sudo apt install python3 python3-pip python3-venv -y

   # Install system dependencies
   sudo apt install build-essential libffi-dev libssl-dev -y
   ```

2. **Deploy the backend**:
   ```bash
   # Clone the repository
   git clone https://github.com/your-org/physical-ai-textbook.git
   cd physical-ai-textbook/backend

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Install production server (like gunicorn)
   pip install gunicorn
   ```

3. **Set up environment variables**:
   Create `/etc/environment` or use a `.env` file:
   ```bash
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   MAX_TOKENS=500
   TEMPERATURE=0.7
   DOCS_PATH=/path/to/your/website/docs
   INDEX_PATH=/path/to/your/data/textbook_index.faiss
   METADATA_PATH=/path/to/your/data/textbook_metadata.pkl
   ```

4. **Create systemd service** (`/etc/systemd/system/textbook-backend.service`):
   ```ini
   [Unit]
   Description=Physical AI Textbook Backend
   After=network.target

   [Service]
   User=your-user
   WorkingDirectory=/path/to/physical-ai-textbook/backend
   EnvironmentFile=/path/to/your/.env
   ExecStart=/path/to/physical-ai-textbook/backend/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

5. **Start the service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable textbook-backend
   sudo systemctl start textbook-backend
   sudo systemctl status textbook-backend
   ```

### Option 2: Containerized Deployment

#### Using Docker

1. **Create Dockerfile for backend** (`backend/Dockerfile`):
   ```Dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
   ```

2. **Build and run the container**:
   ```bash
   cd backend
   docker build -t physical-ai-backend .
   docker run -d -p 8000:8000 -e EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2 physical-ai-backend
   ```

#### Using Docker Compose

1. **Create docker-compose.yml**:
   ```yaml
   version: '3.8'

   services:
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       environment:
         - EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
         - MAX_TOKENS=500
         - TEMPERATURE=0.7
       volumes:
         - ./data:/app/data
         - ./my-website/docs:/app/docs
       restart: unless-stopped
   ```

2. **Deploy with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

### Option 3: Cloud Platform Deployment

#### Using AWS

1. **Deploy backend to AWS Elastic Beanstalk**:
   - Prepare the application bundle
   - Create an Elastic Beanstalk application
   - Deploy using the EB CLI

2. **Deploy frontend to S3 + CloudFront**:
   - Build the frontend: `npm run build`
   - Upload to S3 bucket
   - Configure CloudFront distribution

#### Using Google Cloud Run

1. **Deploy backend**:
   ```bash
   gcloud run deploy textbook-backend \
     --source ./backend \
     --platform managed \
     --region us-central1 \
     --set-env-vars EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   ```

#### Using Azure Container Instances

1. **Deploy using Azure CLI**:
   ```bash
   az container create \
     --resource-group my-resource-group \
     --name textbook-backend \
     --image your-registry/textbook-backend:latest \
     --dns-name-label your-unique-name \
     --environment-variables EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
   ```

## Configuration

### Environment Variables

#### Backend Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EMBEDDING_MODEL` | No | `sentence-transformers/all-MiniLM-L6-v2` | Model for generating embeddings |
| `MAX_TOKENS` | No | `500` | Maximum tokens for responses |
| `TEMPERATURE` | No | `0.7` | Temperature for response generation |
| `DOCS_PATH` | No | `my-website/docs` | Path to textbook documents |
| `INDEX_PATH` | No | `backend/data/textbook_index.faiss` | Path to vector index |
| `METADATA_PATH` | No | `backend/data/textbook_metadata.pkl` | Path to metadata file |
| `HF_HOME` | No | `~/.cache/huggingface` | Hugging Face cache directory |
| `LOG_LEVEL` | No | `INFO` | Logging level |

#### Frontend Configuration

Update `docusaurus.config.ts` with your backend API URL:

```javascript
const config = {
  // ... other config
  themeConfig: {
    // ... other theme config
    api: {
      baseUrl: 'https://your-backend-domain.com/api'
    }
  }
};
```

### SSL/HTTPS Configuration

For production deployment, configure SSL certificates:

#### Using Nginx as Reverse Proxy

1. **Install Nginx**:
   ```bash
   sudo apt install nginx
   ```

2. **Configure SSL** (using Certbot for Let's Encrypt):
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

3. **Nginx configuration** (`/etc/nginx/sites-available/textbook`):
   ```nginx
   server {
       listen 443 ssl;
       server_name your-domain.com;

       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

       location /api/ {
           proxy_pass http://localhost:8000/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location / {
           root /path/to/your/website/build;
           index index.html;
       }
   }
   ```

## Scaling Considerations

### Horizontal Scaling

1. **Backend Scaling**:
   - Use a load balancer (AWS ALB, Google Cloud Load Balancer)
   - Deploy multiple backend instances
   - Use shared storage for vector indexes (NFS, S3, etc.)

2. **Frontend Scaling**:
   - Use CDN for static assets
   - Implement caching strategies

### Performance Optimization

1. **Caching**:
   - Implement response caching for API endpoints
   - Use Redis for session storage
   - Cache embedding computations

2. **Database Optimization**:
   - Optimize vector search parameters
   - Use quantized indexes for faster search
   - Implement proper indexing strategies

## Monitoring and Logging

### Backend Monitoring

1. **Logging Configuration**:
   - Configure structured logging
   - Set up log rotation
   - Forward logs to centralized logging system

2. **Health Checks**:
   - Implement health check endpoints
   - Monitor response times
   - Track error rates

### Frontend Monitoring

1. **Performance Monitoring**:
   - Track page load times
   - Monitor API response times
   - Error tracking and reporting

## Security Considerations

### API Security

1. **Rate Limiting**:
   - Implement rate limiting per IP/user
   - Use tools like SlowAPI for FastAPI

2. **Input Validation**:
   - Validate all API inputs
   - Implement proper sanitization

3. **Authentication** (if needed):
   - Implement JWT-based authentication
   - Use OAuth for third-party integration

### Infrastructure Security

1. **Network Security**:
   - Use private networks
   - Configure proper firewall rules
   - Implement DDoS protection

2. **Secrets Management**:
   - Use environment variables for secrets
   - Implement secrets management (AWS Secrets Manager, HashiCorp Vault)

## Backup and Recovery

### Data Backup

1. **Vector Index Backup**:
   ```bash
   # Backup vector store files
   tar -czf vector-index-backup-$(date +%Y%m%d).tar.gz data/textbook_index.faiss data/textbook_metadata.pkl
   ```

2. **Configuration Backup**:
   - Version control for configuration files
   - Regular backup of environment configurations

### Recovery Procedures

1. **Disaster Recovery Plan**:
   - Document recovery procedures
   - Test backup restoration regularly
   - Implement automated backup verification

## Maintenance

### Regular Maintenance Tasks

1. **Update Dependencies**:
   - Regularly update Python packages
   - Update Node.js dependencies
   - Monitor security advisories

2. **Content Updates**:
   - Update textbook content as needed
   - Re-index vector store after content changes
   - Test search functionality

3. **Performance Monitoring**:
   - Monitor system performance
   - Optimize queries and indexes
   - Scale resources as needed

### Troubleshooting

#### Common Issues

1. **High Memory Usage**:
   - Monitor embedding model memory usage
   - Consider using smaller models or quantization
   - Implement proper resource limits

2. **Slow Response Times**:
   - Optimize vector search parameters
   - Implement caching strategies
   - Scale backend instances

3. **Deployment Failures**:
   - Check environment variable configuration
   - Verify file permissions
   - Review application logs

## Rollback Procedures

### Deployment Rollback

1. **Version Control**:
   - Use Git tags for releases
   - Maintain deployment branches

2. **Rollback Process**:
   ```bash
   # Backend rollback
   git checkout previous-stable-version
   docker-compose up -d --build

   # Frontend rollback
   git checkout previous-stable-version
   npm run build && npm run deploy
   ```

## Support and Operations

### Operational Runbooks

1. **Daily Operations**:
   - Monitor system health
   - Check logs for errors
   - Verify backup completion

2. **Incident Response**:
   - Define incident response procedures
   - Establish escalation paths
   - Document common troubleshooting steps

### Contact Information

- **Technical Support**: [your-support-email@domain.com]
- **Emergency Contact**: [emergency-contact-info]
- **Documentation**: [link-to-internal-docs]