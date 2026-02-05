#!/usr/bin/env bash
# Generate .env.template for Project Chimera
cat > .env.template << 'EOF'
# Project Chimera Environment Variables
DATABASE_URL=postgresql://user:password@localhost:5432/chimera
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
MCP_SENSE_TOKEN=your_mcp_token_here
COINBASE_API_KEY=your_coinbase_key_here
COINBASE_API_SECRET=your_coinbase_secret_here
LOG_LEVEL=INFO
ENVIRONMENT=development
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
EOF
