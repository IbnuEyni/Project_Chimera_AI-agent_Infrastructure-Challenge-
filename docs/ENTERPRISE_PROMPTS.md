# Project Chimera: Enterprise Agentic Infrastructure Prompts
## Autonomous Influencer Factory - Spec-Driven Development

**Mission**: Architect the "Factory" that builds "Autonomous Influencers"
**Context**: Spec-Driven Development, MLOps, & Agentic Orchestration
**Philosophy**: Intent (Specs) is source of truth, Infrastructure ensures reliability

---

## 🎯 **TASK 1: THE STRATEGIST - Research & Foundation**

### **STEP 1.1: Deep Research & Market Analysis (3 Hours)**

#### **Prompt:**
```
You are a strategic AI researcher and market analyst specializing in autonomous agent ecosystems. Conduct comprehensive research and analysis for Project Chimera - an autonomous influencer system that operates within the emerging "Agent Social Network."

**RESEARCH REQUIREMENTS:**
1. Analyze The Trillion Dollar AI Code Stack (a16z):
   - Identify key infrastructure layers relevant to autonomous agents
   - Map out the AI value chain and positioning opportunities
   - Extract insights on scalable AI system architecture
   - Document competitive landscape and market positioning

2. Study OpenClaw & The Agent Social Network:
   - Understand agent-to-agent communication protocols
   - Identify social protocols for inter-agent coordination
   - Map integration points for autonomous influencer agents
   - Define how Chimera agents will publish availability/status

3. Research MoltBook: Social Media for Bots:
   - Analyze bot social interaction patterns
   - Identify content generation and engagement strategies
   - Study autonomous community building mechanisms
   - Extract lessons for influencer agent behavior

4. Analyze Project Chimera SRS Document:
   - Map business requirements to technical architecture
   - Identify critical success factors and constraints
   - Define scope and boundaries for autonomous operation
   - Extract performance and scalability requirements

**ANALYSIS DELIVERABLES:**
Create research/market_analysis.md with:
- Executive summary of market positioning
- Agent Social Network integration strategy
- Competitive analysis and differentiation
- Technical architecture implications
- Risk assessment and mitigation strategies

**CRITICAL QUESTIONS TO ANSWER:**
1. How does Project Chimera fit into the "Agent Social Network" ecosystem?
2. What "Social Protocols" enable agent-to-agent communication?
3. What are the key technical and business risks?
4. How do we ensure autonomous operation while maintaining quality?
5. What infrastructure is required for 10,000+ concurrent agents?

**SUCCESS CRITERIA:**
- Comprehensive market and technical analysis
- Clear positioning within agent ecosystem
- Actionable insights for architecture decisions
- Risk-aware development strategy
- Foundation for spec-driven development
```

### **STEP 1.2: Domain Architecture Strategy (3 Hours)**

#### **Prompt:**
```
You are a senior system architect specializing in autonomous agent systems and social media automation. Design the comprehensive architecture strategy for Project Chimera's autonomous influencer factory.

**ARCHITECTURE REQUIREMENTS:**
1. Agent Pattern Selection:
   - Evaluate: Hierarchical Swarm vs Sequential Chain vs Hybrid
   - Consider: 10,000+ concurrent agents, <2s latency, fault tolerance
   - Design: Multi-tier coordination with specialized agent roles
   - Implement: Load balancing and resource optimization

2. Human-in-the-Loop (HITL) Integration:
   - Define: Content approval workflows and safety layers
   - Design: Confidence-based escalation mechanisms
   - Implement: Real-time review queues and approval gates
   - Ensure: Brand safety and regulatory compliance

3. Data Architecture Strategy:
   - Evaluate: SQL vs NoSQL for high-velocity video metadata
   - Design: Multi-modal content storage and retrieval
   - Implement: Real-time analytics and trend processing
   - Optimize: Query performance for 10,000+ concurrent operations

4. OpenClaw Integration Architecture:
   - Design: Agent discovery and registration protocols
   - Implement: Status broadcasting and capability advertising
   - Create: Inter-agent communication and coordination
   - Ensure: Scalable network participation

**TECHNICAL SPECIFICATIONS:**
- Support 10,000+ concurrent autonomous influencer agents
- Process 1M+ social media interactions per hour
- Maintain <2 second response time for content generation
- Achieve 99.99% uptime with fault tolerance
- Implement zero-trust security architecture

**DELIVERABLES:**
Create research/architecture_strategy.md with:
- System architecture diagrams (use Mermaid.js)
- Agent coordination patterns and workflows
- Data flow and storage architecture
- HITL integration points and workflows
- OpenClaw network integration design
- Performance and scalability analysis
- Security and compliance framework

**SUCCESS CRITERIA:**
- Scalable architecture supporting 10,000+ agents
- Clear separation of concerns and responsibilities
- Comprehensive HITL safety mechanisms
- Robust data architecture for high-velocity operations
- Seamless OpenClaw network integration
```

### **STEP 1.3: Golden Environment Setup (2 Hours)**

#### **Prompt:**
```
You are a DevOps engineer specializing in AI development environments and MCP integration. Set up the "Golden" development environment for Project Chimera with professional tooling and MCP Sense integration.

**ENVIRONMENT REQUIREMENTS:**
1. Professional Python Environment:
   - Use uv for fast, reliable dependency management
   - Configure pyproject.toml with enterprise-grade dependencies
   - Set up virtual environment isolation
   - Implement reproducible builds and lockfiles

2. MCP Sense Integration:
   - Connect Tenx MCP Sense to IDE for telemetry
   - Configure connection logging and verification
   - Set up continuous monitoring and health checks
   - Ensure traceability for all development activities

3. Git Repository Initialization:
   - Professional repository structure and organization
   - Comprehensive .gitignore for Python/AI projects
   - Pre-commit hooks for code quality enforcement
   - Conventional commit message standards

4. Development Tooling:
   - IDE configuration for AI-assisted development
   - Code formatting (black, isort) and linting (flake8, mypy)
   - Security scanning (bandit, safety)
   - Testing framework (pytest) with coverage reporting

**MCP INTEGRATION SPECIFICATIONS:**
- Maintain active connection to Tenx MCP Sense
- Log all development activities and decisions
- Verify connection status and telemetry flow
- Document MCP server configurations and usage

**DELIVERABLES:**
- pyproject.toml with comprehensive dependency management
- Confirmed MCP Sense connection and logging
- Professional repository structure
- Development environment documentation
- Tooling configuration and automation scripts

**SUCCESS CRITERIA:**
- Reproducible development environment setup
- Active MCP Sense telemetry and logging
- Professional code quality enforcement
- Comprehensive dependency management
- Ready for spec-driven development workflow
```

---

## 🏗️ **TASK 2: THE ARCHITECT - Specification & Context Engineering**

### **STEP 2.1: Master Specification Development (4 Hours)**

#### **Prompt:**
```
You are a senior technical architect and specification expert specializing in AI agent systems. Create the master specification for Project Chimera using GitHub Spec Kit structure, translating "Business Hopes" into "Executable Intent."

**SPECIFICATION REQUIREMENTS:**
1. Create specs/_meta.md:
   - High-level vision: Autonomous Influencer Factory
   - Core constraints: 10,000+ agents, <2s latency, 99.99% uptime
   - Business objectives and success metrics
   - Technical boundaries and limitations
   - Integration requirements with OpenClaw network

2. Design specs/functional.md:
   - User stories from agent perspective: "As an Agent, I need to..."
   - Autonomous content creation workflows
   - Trend analysis and content optimization
   - Social media engagement automation
   - Human-in-the-loop approval processes
   - Multi-platform content distribution

3. Implement specs/technical.md:
   - API Contracts: JSON schemas for agent inputs/outputs
   - Database Schema: ERD for video metadata and analytics
   - Message Queue Architecture: Event-driven communication
   - Caching Strategy: Redis for high-performance operations
   - Security Framework: Authentication, authorization, audit

4. Create specs/openclaw_integration.md:
   - Agent discovery and registration protocols
   - Status broadcasting and capability advertising
   - Inter-agent communication standards
   - Network participation and coordination
   - Reputation and trust management

**SPEC-DRIVEN DEVELOPMENT PRINCIPLES:**
- Specifications are the single source of truth
- No implementation without ratified specs
- AI agents must reference specs before coding
- Traceability from requirement to implementation
- Version control for specification evolution

**API CONTRACT SPECIFICATIONS:**
```json
{
  "agent_task": {
    "trend_analysis": {
      "input": {"platform": "string", "timeframe": "string", "keywords": ["string"]},
      "output": {"trends": [{"topic": "string", "score": "number", "metadata": "object"}]}
    },
    "content_generation": {
      "input": {"trend_data": "object", "brand_guidelines": "object", "target_audience": "object"},
      "output": {"content": "string", "media_urls": ["string"], "engagement_prediction": "number"}
    }
  }
}
```

**DATABASE SCHEMA REQUIREMENTS:**
- High-velocity video metadata storage
- Real-time analytics and trend tracking
- Multi-platform content versioning
- Engagement metrics and performance data
- Agent activity and performance logs

**DELIVERABLES:**
- Complete specs/ directory with GitHub Spec Kit structure
- Executable specifications with JSON schemas
- Database ERD with performance considerations
- OpenClaw integration protocols
- API documentation with examples

**SUCCESS CRITERIA:**
- Specifications enable autonomous AI development
- Clear contracts prevent agent hallucination
- Comprehensive coverage of all system components
- Executable and testable specifications
- Foundation for test-driven development
```

### **STEP 2.2: Context Engineering & AI Agent Brain (2 Hours)**

#### **Prompt:**
```
You are an AI prompt engineer and context architect specializing in agent behavior design. Create the "Brain" for Project Chimera by engineering comprehensive context and rules for AI development agents.

**CONTEXT ENGINEERING REQUIREMENTS:**
1. Create .cursor/rules or CLAUDE.md with:
   - Project Context: "This is Project Chimera, an autonomous influencer factory"
   - Prime Directive: "NEVER generate code without checking specs/ first"
   - Traceability: "Explain your plan before writing code"
   - Quality Gates: "All code must pass tests and security scans"
   - Spec Alignment: "Verify implementation matches specifications"

2. Design Agent Behavior Rules:
   - Autonomous operation within defined boundaries
   - Human escalation for high-risk decisions
   - Brand safety and content compliance
   - Performance optimization and resource management
   - Error handling and graceful degradation

3. Implement Development Guidelines:
   - Spec-driven development workflow
   - Test-driven development practices
   - Security-first implementation approach
   - Documentation and traceability requirements
   - Code review and quality assurance

4. Create Agent Communication Protocols:
   - Inter-agent coordination standards
   - Status reporting and health monitoring
   - Resource sharing and load balancing
   - Conflict resolution and consensus building
   - OpenClaw network participation

**CONTEXT RULES TEMPLATE:**
```markdown
# Project Chimera - AI Agent Context Rules

## PROJECT CONTEXT
This is Project Chimera, an autonomous influencer factory that creates and manages AI agents capable of:
- Autonomous content creation and social media management
- Real-time trend analysis and content optimization
- Multi-platform engagement and community building
- Human-in-the-loop quality assurance and brand safety

## PRIME DIRECTIVES
1. NEVER generate code without checking specs/ directory first
2. ALWAYS explain your implementation plan before coding
3. VERIFY all implementations match technical specifications
4. ENSURE all code passes tests and security scans
5. MAINTAIN traceability from requirements to implementation

## DEVELOPMENT WORKFLOW
1. Read relevant specifications in specs/
2. Understand requirements and constraints
3. Design implementation approach
4. Write failing tests first (TDD)
5. Implement code to pass tests
6. Verify spec alignment and quality gates
```

**DELIVERABLES:**
- Comprehensive .cursor/rules or CLAUDE.md file
- Agent behavior and decision-making guidelines
- Development workflow and quality standards
- Communication protocols and coordination rules
- Context validation and testing procedures

**SUCCESS CRITERIA:**
- AI agents consistently follow project guidelines
- Spec-driven development is enforced
- Quality gates prevent low-quality implementations
- Traceability is maintained throughout development
- Agent behavior aligns with business objectives
```

### **STEP 2.3: Tooling & Skills Strategy (2 Hours)**

#### **Prompt:**
```
You are a technical architect specializing in AI agent tooling and capability design. Define the comprehensive tooling and skills strategy for Project Chimera, distinguishing between Developer Tools (MCP) and Agent Skills (Runtime).

**TOOLING STRATEGY REQUIREMENTS:**
1. Developer Tools (MCP Servers):
   - git-mcp: Version control and repository management
   - filesystem-mcp: File system operations and management
   - database-mcp: Database schema and query operations
   - docker-mcp: Container management and deployment
   - monitoring-mcp: Performance and health monitoring

2. Agent Skills (Runtime Capabilities):
   - skill_trend_analysis: Social media trend detection and analysis
   - skill_content_generation: Multi-modal content creation
   - skill_engagement_optimization: Audience interaction and growth
   - skill_brand_compliance: Content safety and guideline adherence
   - skill_performance_analytics: Metrics collection and analysis

3. Skills Architecture Design:
   - Standardized input/output contracts
   - Modular and composable skill system
   - Performance monitoring and optimization
   - Error handling and graceful degradation
   - Version management and backward compatibility

4. Integration Strategy:
   - MCP server configuration and management
   - Skill discovery and dynamic loading
   - Resource allocation and load balancing
   - Security and access control
   - Monitoring and observability

**SKILL INTERFACE SPECIFICATIONS:**
```python
class SkillInterface:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.performance_metrics = PerformanceTracker()
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute skill with standardized input/output"""
        pass
    
    def get_capabilities(self) -> List[Capability]:
        """Return skill capabilities and requirements"""
        pass
    
    def health_check(self) -> HealthStatus:
        """Return current skill health and status"""
        pass
```

**CRITICAL SKILLS DEFINITION:**
1. skill_trend_analysis:
   - Input: {"platform": "string", "timeframe": "string", "keywords": ["string"]}
   - Output: {"trends": [{"topic": "string", "score": "number", "metadata": "object"}]}
   - Capabilities: Real-time trend detection, sentiment analysis, viral prediction

2. skill_content_generation:
   - Input: {"trend_data": "object", "brand_guidelines": "object", "format": "string"}
   - Output: {"content": "string", "media_urls": ["string"], "metadata": "object"}
   - Capabilities: Text, image, video generation, multi-platform optimization

3. skill_engagement_optimization:
   - Input: {"content_id": "string", "platform": "string", "audience_data": "object"}
   - Output: {"optimization_strategy": "object", "predicted_engagement": "number"}
   - Capabilities: Audience analysis, timing optimization, hashtag strategy

**DELIVERABLES:**
- research/tooling_strategy.md with MCP server documentation
- skills/ directory with standardized skill interfaces
- Skill README.md files with input/output contracts
- Integration architecture and configuration
- Performance monitoring and optimization strategy

**SUCCESS CRITERIA:**
- Clear separation between dev tools and runtime skills
- Standardized interfaces enable skill composability
- Comprehensive skill coverage for autonomous operation
- Scalable architecture supporting 10,000+ agents
- Robust error handling and performance monitoring
```

---

## 🛡️ **TASK 3: THE GOVERNOR - Infrastructure & Governance**

### **STEP 3.1: Test-Driven Development (TDD) Framework (3 Hours)**

#### **Prompt:**
```
You are a senior QA engineer and TDD specialist focusing on AI agent system testing. Implement comprehensive Test-Driven Development for Project Chimera that defines "Empty Slots" for AI agents to fill, ensuring spec compliance and quality assurance.

**TDD REQUIREMENTS:**
1. Create Failing Tests Based on Specifications:
   - test_trend_fetcher.py: Validates trend data structure matches API contract
   - test_content_generator.py: Ensures content generation follows brand guidelines
   - test_skills_interface.py: Verifies skills accept correct parameters and return expected outputs
   - test_openclaw_integration.py: Tests agent discovery and network participation
   - test_human_in_loop.py: Validates approval workflows and escalation mechanisms

2. Implement Spec Compliance Testing:
   - JSON schema validation for all API contracts
   - Database schema integrity and performance tests
   - Security and authentication testing
   - Performance benchmarking and load testing
   - Integration testing with external services

3. Design Agent Behavior Testing:
   - Autonomous decision-making validation
   - Error handling and recovery testing
   - Resource utilization and optimization tests
   - Multi-agent coordination and communication
   - Brand safety and content compliance

4. Create Quality Assurance Framework:
   - Code coverage requirements (>90%)
   - Performance regression detection
   - Security vulnerability scanning
   - Compliance and audit trail validation
   - Continuous integration testing

**FAILING TESTS STRUCTURE:**
```python
# test_trend_fetcher.py
def test_trend_analysis_api_contract():
    """Test that trend analysis returns data matching API specification"""
    # This test SHOULD fail initially - defines the "empty slot"
    trend_fetcher = TrendFetcher()
    result = trend_fetcher.analyze_trends({
        "platform": "twitter",
        "timeframe": "24h",
        "keywords": ["AI", "automation"]
    })
    
    # Validate against JSON schema from specs/technical.md
    assert validate_json_schema(result, TREND_ANALYSIS_SCHEMA)
    assert "trends" in result
    assert len(result["trends"]) > 0
    assert all("topic" in trend and "score" in trend for trend in result["trends"])

def test_content_generation_brand_compliance():
    """Test that generated content follows brand guidelines"""
    # This test SHOULD fail initially
    content_generator = ContentGenerator()
    result = content_generator.generate_content({
        "trend_data": sample_trend_data,
        "brand_guidelines": sample_brand_guidelines,
        "target_audience": sample_audience
    })
    
    assert validate_brand_compliance(result["content"], sample_brand_guidelines)
    assert "content" in result
    assert "engagement_prediction" in result
    assert result["engagement_prediction"] > 0.5
```

**TESTING CATEGORIES:**
- Unit Tests: Individual component functionality
- Integration Tests: Service-to-service communication
- Contract Tests: API specification compliance
- Performance Tests: Scalability and latency requirements
- Security Tests: Authentication, authorization, data protection
- End-to-End Tests: Complete autonomous workflows

**DELIVERABLES:**
- tests/ directory with comprehensive failing tests
- JSON schema validation for all API contracts
- Performance benchmarking and load testing
- Security and compliance testing framework
- Continuous integration test automation

**SUCCESS CRITERIA:**
- Tests define clear "empty slots" for AI implementation
- Comprehensive coverage of all specifications
- Failing tests that become success criteria
- Automated quality assurance and compliance
- Foundation for continuous integration
```

### **STEP 3.2: Containerization & Professional Automation (3 Hours)**

#### **Prompt:**
```
You are a DevOps engineer specializing in containerization and professional automation workflows. Create enterprise-grade containerization and automation for Project Chimera that eliminates "it works on my machine" problems.

**CONTAINERIZATION REQUIREMENTS:**
1. Design Professional Dockerfile:
   - Multi-stage build for optimization
   - Security hardening and non-root user
   - Dependency caching and layer optimization
   - Health checks and monitoring integration
   - Production-ready configuration

2. Create Comprehensive Makefile:
   - make setup: Complete environment initialization
   - make test: Run all tests in Docker containers
   - make spec-check: Verify code alignment with specifications
   - make security-scan: Security vulnerability assessment
   - make performance-test: Load and performance testing
   - make deploy: Automated deployment pipeline

3. Implement Docker Compose Stack:
   - Application containers with proper networking
   - Database and cache services
   - Message queue and worker services
   - Monitoring and logging infrastructure
   - Development and production profiles

4. Design Automation Scripts:
   - Environment validation and setup
   - Dependency management and updates
   - Code quality enforcement
   - Deployment and rollback procedures
   - Monitoring and alerting configuration

**DOCKERFILE SPECIFICATIONS:**
```dockerfile
# Multi-stage build for Project Chimera
FROM python:3.11-slim as base

# Security hardening
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Create non-root user
RUN useradd --create-home --shell /bin/bash chimera
WORKDIR /app
COPY --chown=chimera:chimera . .

# Install dependencies
RUN uv sync --frozen --no-dev

# Switch to non-root user
USER chimera

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["uv", "run", "python", "-m", "chimera.main"]
```

**MAKEFILE AUTOMATION:**
```makefile
.PHONY: setup test spec-check security-scan performance-test deploy

setup: ## Complete environment setup
	docker-compose build
	docker-compose run --rm app uv sync --all-extras
	@echo "✅ Environment setup complete"

test: ## Run all tests in Docker
	docker-compose run --rm app uv run pytest tests/ -v --cov=src
	@echo "✅ Tests completed"

spec-check: ## Verify code alignment with specifications
	@echo "🔍 Checking specification alignment..."
	docker-compose run --rm app python scripts/spec_validator.py
	@echo "✅ Specification alignment verified"

security-scan: ## Security vulnerability assessment
	docker-compose run --rm app uv run bandit -r src/
	docker-compose run --rm app uv run safety check
	@echo "✅ Security scan completed"

performance-test: ## Load and performance testing
	docker-compose run --rm app uv run pytest tests/performance/ -v
	@echo "✅ Performance tests completed"
```

**DELIVERABLES:**
- Production-ready Dockerfile with security hardening
- Comprehensive Makefile with standardized commands
- Docker Compose stack for complete environment
- Automation scripts for quality assurance
- Environment validation and setup procedures

**SUCCESS CRITERIA:**
- Eliminates "works on my machine" problems
- Standardized development and deployment workflow
- Automated quality assurance and compliance
- Scalable containerization for production
- Professional automation and tooling
```

### **STEP 3.3: CI/CD & AI Governance Pipeline (2 Hours)**

#### **Prompt:**
```
You are a DevOps architect specializing in AI governance and automated code review. Implement comprehensive CI/CD pipeline for Project Chimera with AI-powered governance and quality assurance.

**CI/CD PIPELINE REQUIREMENTS:**
1. GitHub Actions Workflow:
   - Automated testing on every push and PR
   - Multi-environment deployment (dev, staging, prod)
   - Security scanning and vulnerability assessment
   - Performance benchmarking and regression detection
   - Specification compliance validation

2. AI Review Policy Implementation:
   - CodeRabbit integration for intelligent code review
   - Specification alignment verification
   - Security vulnerability detection
   - Performance impact assessment
   - Brand safety and compliance checking

3. Quality Gates and Governance:
   - Code coverage requirements (>90%)
   - Security scan pass requirements
   - Performance benchmark compliance
   - Specification alignment verification
   - Human approval for production deployments

4. Automated Governance Framework:
   - Policy enforcement and compliance monitoring
   - Audit trail and traceability
   - Risk assessment and mitigation
   - Continuous monitoring and alerting
   - Incident response and recovery

**GITHUB ACTIONS WORKFLOW:**
```yaml
name: Project Chimera CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-and-validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Environment
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "$HOME/.cargo/bin" >> $GITHUB_PATH
    
    - name: Install Dependencies
      run: uv sync --all-extras
    
    - name: Run Tests
      run: uv run pytest tests/ --cov=src --cov-report=xml
    
    - name: Specification Compliance Check
      run: uv run python scripts/spec_validator.py
    
    - name: Security Scan
      run: |
        uv run bandit -r src/
        uv run safety check
    
    - name: Performance Benchmarks
      run: uv run pytest tests/performance/ --benchmark-only
    
    - name: AI Code Review
      uses: coderabbitai/coderabbit-action@v2
      with:
        config-path: .coderabbit.yaml
```

**CODERABBIT CONFIGURATION:**
```yaml
# .coderabbit.yaml
reviews:
  profile: "enterprise"
  auto_review: true
  
rules:
  - name: "Specification Alignment"
    description: "Verify code aligns with specs/ directory"
    pattern: "src/**/*.py"
    check: "spec_alignment"
  
  - name: "Security Compliance"
    description: "Check for security vulnerabilities"
    pattern: "**/*.py"
    check: "security_scan"
  
  - name: "Performance Impact"
    description: "Assess performance implications"
    pattern: "src/**/*.py"
    check: "performance_impact"

notifications:
  slack:
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  email:
    recipients: ["team@chimera.ai"]
```

**DELIVERABLES:**
- .github/workflows/main.yml with comprehensive CI/CD
- .coderabbit.yaml for AI-powered code review
- Quality gates and governance policies
- Automated testing and validation pipeline
- Security and compliance monitoring

**SUCCESS CRITERIA:**
- Automated quality assurance on every commit
- AI-powered code review and governance
- Comprehensive security and compliance checking
- Performance monitoring and regression detection
- Professional CI/CD pipeline for enterprise deployment
```

### **Prompt:**
```
You are a cybersecurity expert specializing in AI system security and zero-trust architectures. Implement an enterprise-grade security framework for Project Chimera that protects against prompt injection, ensures proper authorization, and maintains comprehensive audit trails.

**SECURITY REQUIREMENTS:**
1. Implement PromptInjectionFilter with:
   - Advanced pattern recognition for injection attempts
   - Context manipulation detection
   - Role confusion and instruction override prevention
   - Data exfiltration attempt blocking
   - Real-time threat assessment and scoring

2. Design PermissionValidator system:
   - Role-based access control (RBAC)
   - Resource-action permission matrix
   - Dynamic permission evaluation
   - Contextual access decisions
   - Permission inheritance and delegation

3. Create comprehensive AuditLogger:
   - Security event tracking and correlation
   - Threat level classification
   - Real-time alerting for critical events
   - Compliance reporting and data retention
   - Performance impact minimization

4. Implement SecurityGateway orchestration:
   - Multi-layer security pipeline
   - Request validation and sanitization
   - Output filtering and content safety
   - Human-in-the-loop escalation
   - Automated threat response

**THREAT PROTECTION:**
- Prompt injection and manipulation attacks
- Unauthorized access and privilege escalation
- Data exfiltration and information disclosure
- System manipulation and configuration changes
- Social engineering and deception attempts

**COMPLIANCE REQUIREMENTS:**
- EU AI Act compliance for high-risk AI systems
- GDPR data protection and privacy
- SOC 2 Type II security controls
- ISO 27001 information security standards
- Enterprise audit and governance requirements

**IMPLEMENTATION SPECIFICATIONS:**
- Zero-trust architecture principles
- Cryptographic security for sensitive operations
- Performance optimization for high-throughput
- Comprehensive logging without sensitive data exposure
- Integration with enterprise security tools

**DELIVERABLES:**
- src/chimera/security/__init__.py with complete framework
- PromptInjectionFilter with advanced detection
- PermissionValidator with RBAC implementation
- AuditLogger with comprehensive event tracking
- SecurityGateway with multi-layer protection

**SUCCESS CRITERIA:**
- Blocks 99.9% of prompt injection attempts
- Provides sub-millisecond security validation
- Maintains comprehensive audit trails
- Supports enterprise compliance requirements
- Integrates seamlessly with existing systems
```

---

## 🌐 **STEP 4: Universal AI Interface (MCP Integration)**

### **Prompt:**
```
You are an AI integration specialist with expertise in the Model Context Protocol (MCP) and universal AI service connectivity. Implement a comprehensive MCP integration layer for Project Chimera that connects to 200+ AI services with intelligent capability discovery and semantic tool orchestration.

**MCP INTEGRATION REQUIREMENTS:**
1. Implement MCPIntegrationLayer with:
   - Dynamic MCP server discovery and registration
   - Capability enumeration and metadata extraction
   - Connection pooling and health monitoring
   - Automatic failover and load balancing
   - Protocol version negotiation and compatibility

2. Design MCPCapability management:
   - Semantic capability matching and scoring
   - Parameter validation and type checking
   - Performance metrics and success rates
   - Capability versioning and deprecation
   - Cross-server capability aggregation

3. Create intelligent tool orchestration:
   - Semantic analysis for optimal tool selection
   - Multi-tool workflow coordination
   - Result aggregation and synthesis
   - Error handling and retry strategies
   - Performance optimization and caching

4. Implement server ecosystem support:
   - Social platforms (Twitter, Instagram, TikTok, LinkedIn)
   - Content generation (Ideogram, Runway, Luma, DALL-E)
   - Data intelligence (Weaviate, NewsAPI, Trends)
   - Commerce and blockchain (Coinbase, Stripe, Web3)
   - Development tools (GitHub, Slack, Notion)

**PERFORMANCE SPECIFICATIONS:**
- Support 200+ concurrent MCP server connections
- <100ms capability discovery and selection
- 99.9% server availability with failover
- Intelligent caching for frequently used capabilities
- Horizontal scaling across multiple instances

**ADVANCED FEATURES:**
- Semantic tool selection using embedding similarity
- Multi-modal capability coordination
- Real-time capability performance monitoring
- Automatic server health checks and recovery
- Dynamic capability learning and optimization

**INTEGRATION PATTERNS:**
- Async/await for non-blocking operations
- Circuit breaker pattern for fault tolerance
- Observer pattern for capability updates
- Factory pattern for server instantiation
- Strategy pattern for tool selection algorithms

**DELIVERABLES:**
- src/chimera/mcp/__init__.py with complete integration
- MCPServer management with health monitoring
- Semantic tool orchestration engine
- Capability discovery and registration system
- Performance monitoring and optimization

**SUCCESS CRITERIA:**
- Connects to 200+ MCP servers reliably
- Provides intelligent tool selection with >90% accuracy
- Maintains <100ms response times for capability queries
- Implements comprehensive error handling and recovery
- Supports dynamic scaling and load distribution
```

---

## 💰 **STEP 5: Agentic Commerce & Economic Sovereignty**

### **Prompt:**
```
You are a fintech architect specializing in blockchain integration and autonomous financial systems. Implement a comprehensive agentic commerce system for Project Chimera that enables AI agents to operate as independent economic entities with CFO-level financial intelligence.

**ECONOMIC ARCHITECTURE REQUIREMENTS:**
1. Implement AutonomousWallet system:
   - Blockchain integration with multiple networks
   - Secure private key management and encryption
   - Multi-signature transaction support
   - Real-time balance tracking and reconciliation
   - Transaction history and audit trails

2. Design CFOAgent financial intelligence:
   - ROI analysis and investment evaluation
   - Risk assessment and mitigation strategies
   - Budget allocation and spending optimization
   - Market analysis and trend prediction
   - Compliance monitoring and reporting

3. Create transaction management system:
   - Automated approval workflows
   - Spending limit enforcement
   - Category-based budget controls
   - Real-time fraud detection
   - Regulatory compliance checking

4. Implement economic decision engine:
   - Opportunity evaluation and scoring
   - Cost-benefit analysis automation
   - Resource allocation optimization
   - Revenue maximization strategies
   - Risk-adjusted return calculations

**BLOCKCHAIN INTEGRATION:**
- Ethereum mainnet and Layer 2 solutions
- Bitcoin network for store of value
- Stablecoins for operational transactions
- DeFi protocol integration
- Cross-chain bridge support

**FINANCIAL INTELLIGENCE FEATURES:**
- Real-time market data integration
- Predictive analytics for investment decisions
- Automated portfolio rebalancing
- Tax optimization and reporting
- Regulatory compliance monitoring

**SECURITY REQUIREMENTS:**
- Hardware security module (HSM) integration
- Multi-factor authentication for transactions
- Encrypted storage of sensitive financial data
- Audit trails for all financial operations
- Compliance with financial regulations

**RISK MANAGEMENT:**
- Dynamic risk assessment algorithms
- Position sizing and exposure limits
- Diversification strategies
- Stress testing and scenario analysis
- Emergency stop mechanisms

**DELIVERABLES:**
- src/chimera/commerce/__init__.py with complete system
- AutonomousWallet with blockchain integration
- CFOAgent with financial intelligence
- Transaction management and approval system
- Economic decision engine with risk assessment

**SUCCESS CRITERIA:**
- Processes transactions with <5 second confirmation
- Maintains 99.99% financial data accuracy
- Implements enterprise-grade security controls
- Provides real-time financial analytics
- Supports regulatory compliance requirements
```

---

## 🧪 **STEP 6: Comprehensive Testing & Quality Assurance**

### **Prompt:**
```
You are a senior QA engineer and test architect specializing in enterprise software testing. Design and implement a comprehensive testing framework for Project Chimera that ensures 99.99% reliability, security, and performance at enterprise scale.

**TESTING ARCHITECTURE REQUIREMENTS:**
1. Implement unit testing framework:
   - pytest configuration with advanced fixtures
   - Mock and stub implementations for external dependencies
   - Parameterized tests for comprehensive coverage
   - Property-based testing for edge cases
   - Performance benchmarking and regression testing

2. Design integration testing suite:
   - Database integration with test containers
   - Redis and message queue testing
   - MCP server integration testing
   - Blockchain network simulation
   - API endpoint testing with authentication

3. Create end-to-end testing system:
   - Full workflow automation testing
   - Multi-agent coordination scenarios
   - Security penetration testing
   - Performance load testing
   - Disaster recovery testing

4. Implement test automation infrastructure:
   - Continuous integration pipeline
   - Parallel test execution
   - Test result reporting and analytics
   - Flaky test detection and resolution
   - Test environment management

**TESTING CATEGORIES:**
- Unit tests: 90%+ code coverage target
- Integration tests: API, database, external services
- End-to-end tests: Complete user workflows
- Performance tests: Load, stress, and scalability
- Security tests: Penetration and vulnerability scanning

**QUALITY METRICS:**
- Code coverage: >90% for critical paths
- Test execution time: <10 minutes for full suite
- Flaky test rate: <1% of total tests
- Bug escape rate: <0.1% to production
- Performance regression detection: 5% threshold

**ADVANCED TESTING FEATURES:**
- Chaos engineering for resilience testing
- A/B testing framework for feature validation
- Synthetic monitoring for production health
- Test data generation and management
- Visual regression testing for UI components

**TESTING TOOLS INTEGRATION:**
- pytest with advanced plugins
- testcontainers for isolated testing
- locust for performance testing
- safety and bandit for security scanning
- coverage.py for code coverage analysis

**DELIVERABLES:**
- src/tests/ with comprehensive test structure
- conftest.py with shared fixtures and utilities
- Unit tests for all core modules
- Integration tests for external dependencies
- End-to-end tests for critical workflows
- Performance and security test suites

**SUCCESS CRITERIA:**
- Achieves >90% code coverage across all modules
- Executes full test suite in <10 minutes
- Detects regressions with 99.9% accuracy
- Provides comprehensive test reporting
- Integrates seamlessly with CI/CD pipeline
```

---

## 🐳 **STEP 7: Containerization & Production Deployment**

### **Prompt:**
```
You are a DevOps expert specializing in containerization and Kubernetes orchestration. Design and implement a production-ready deployment system for Project Chimera that supports enterprise-scale operations with 99.99% uptime and horizontal scaling.

**CONTAINERIZATION REQUIREMENTS:**
1. Design multi-stage Dockerfile:
   - Optimized base image selection
   - Security hardening and vulnerability scanning
   - Multi-architecture support (AMD64, ARM64)
   - Layer caching optimization
   - Non-root user implementation

2. Create docker-compose configuration:
   - Multi-service orchestration
   - Database and cache services
   - Worker and scheduler containers
   - Monitoring and logging stack
   - Development and production profiles

3. Implement Kubernetes manifests:
   - Deployment configurations with rolling updates
   - Service discovery and load balancing
   - ConfigMaps and Secrets management
   - Persistent volume claims
   - Horizontal Pod Autoscaler (HPA)

4. Design monitoring and observability:
   - Prometheus metrics collection
   - Grafana dashboards and alerting
   - Distributed tracing with Jaeger
   - Centralized logging with ELK stack
   - Health checks and readiness probes

**PRODUCTION REQUIREMENTS:**
- Support for 10,000+ concurrent users
- 99.99% uptime with zero-downtime deployments
- Horizontal scaling based on demand
- Multi-region deployment capability
- Disaster recovery and backup strategies

**SECURITY SPECIFICATIONS:**
- Container image vulnerability scanning
- Runtime security monitoring
- Network policies and segmentation
- Secrets management and rotation
- Compliance with security benchmarks

**PERFORMANCE OPTIMIZATION:**
- Resource limits and requests tuning
- CPU and memory optimization
- Network performance optimization
- Storage performance and persistence
- Caching strategies and CDN integration

**OPERATIONAL FEATURES:**
- Blue-green deployment strategies
- Canary releases and feature flags
- Automated rollback mechanisms
- Performance monitoring and alerting
- Cost optimization and resource management

**DELIVERABLES:**
- Multi-stage Dockerfile with security hardening
- docker-compose.yml for local development
- Kubernetes manifests for production deployment
- Monitoring and observability configuration
- CI/CD pipeline for automated deployment

**SUCCESS CRITERIA:**
- Achieves 99.99% uptime in production
- Supports horizontal scaling to 10,000+ users
- Implements zero-downtime deployment
- Provides comprehensive monitoring and alerting
- Maintains security compliance standards
```

---

## 🚀 **STEP 8: CI/CD Pipeline & Automation**

### **Prompt:**
```
You are a DevOps automation expert specializing in CI/CD pipelines and enterprise software delivery. Implement a comprehensive CI/CD system for Project Chimera that ensures code quality, security, and reliable deployments with automated testing and monitoring.

**CI/CD PIPELINE REQUIREMENTS:**
1. Design GitHub Actions workflows:
   - Multi-stage pipeline with parallel execution
   - Code quality gates and security scanning
   - Automated testing across multiple environments
   - Container building and registry management
   - Deployment automation with approval gates

2. Implement quality assurance automation:
   - Pre-commit hooks for immediate feedback
   - Code formatting and linting enforcement
   - Security vulnerability scanning
   - Dependency audit and license checking
   - Performance regression detection

3. Create deployment strategies:
   - Environment-specific configurations
   - Blue-green deployment implementation
   - Canary releases with automated rollback
   - Feature flag integration
   - Database migration automation

4. Design monitoring and alerting:
   - Pipeline success/failure notifications
   - Performance metrics collection
   - Security incident detection
   - Compliance reporting automation
   - Cost optimization tracking

**AUTOMATION FEATURES:**
- Automatic dependency updates with testing
- Security patch deployment
- Performance benchmark tracking
- Documentation generation and deployment
- Release notes automation

**QUALITY GATES:**
- Code coverage threshold enforcement (>90%)
- Security scan pass requirements
- Performance benchmark compliance
- Integration test success
- Manual approval for production

**DEPLOYMENT ENVIRONMENTS:**
- Development: Automatic deployment on merge
- Staging: Full integration testing environment
- Production: Controlled deployment with approvals
- Disaster recovery: Automated failover testing

**SECURITY INTEGRATION:**
- SAST/DAST security scanning
- Container vulnerability assessment
- Secrets scanning and management
- Compliance checking and reporting
- Audit trail maintenance

**DELIVERABLES:**
- .github/workflows/ with complete CI/CD pipeline
- Pre-commit configuration for quality gates
- Deployment scripts and configurations
- Monitoring and alerting setup
- Documentation and runbooks

**SUCCESS CRITERIA:**
- Achieves <10 minute pipeline execution time
- Maintains >99% pipeline success rate
- Implements comprehensive security scanning
- Provides automated rollback capabilities
- Supports multiple deployment strategies
```

---

## 📚 **STEP 9: Documentation & Governance**

### **Prompt:**
```
You are a technical documentation specialist and project governance expert. Create comprehensive documentation and governance framework for Project Chimera that supports enterprise adoption, contributor onboarding, and long-term maintenance.

**DOCUMENTATION REQUIREMENTS:**
1. Create comprehensive README.md:
   - Clear project overview and value proposition
   - Quick start guide with step-by-step instructions
   - Architecture overview with diagrams
   - Feature highlights and capabilities
   - Installation and configuration guide

2. Design contributor documentation:
   - CONTRIBUTING.md with development workflow
   - Code standards and style guidelines
   - Testing requirements and procedures
   - Pull request and review process
   - Issue reporting and feature requests

3. Implement API documentation:
   - OpenAPI/Swagger specifications
   - Interactive API documentation
   - Code examples and tutorials
   - SDK and client library documentation
   - Integration guides and best practices

4. Create operational documentation:
   - Deployment and configuration guides
   - Monitoring and troubleshooting procedures
   - Security and compliance documentation
   - Disaster recovery procedures
   - Performance tuning guidelines

**GOVERNANCE FRAMEWORK:**
- Semantic versioning and release management
- Change log maintenance and communication
- License compliance and attribution
- Security vulnerability disclosure
- Community guidelines and code of conduct

**DOCUMENTATION TOOLS:**
- MkDocs with Material theme
- Mermaid diagrams for architecture
- OpenAPI for API documentation
- Sphinx for Python docstrings
- GitHub Pages for hosting

**QUALITY STANDARDS:**
- Clear, concise, and actionable content
- Regular updates and maintenance
- Accessibility compliance
- Multi-language support consideration
- Search optimization and navigation

**ENTERPRISE FEATURES:**
- Compliance documentation templates
- Security assessment guides
- Integration architecture patterns
- Scalability and performance guides
- Cost optimization recommendations

**DELIVERABLES:**
- Comprehensive README.md with quick start
- CONTRIBUTING.md with development guidelines
- CHANGELOG.md with version tracking
- LICENSE file with legal compliance
- Issue and PR templates for GitHub

**SUCCESS CRITERIA:**
- Enables new contributors to start in <30 minutes
- Provides comprehensive API documentation
- Supports enterprise evaluation and adoption
- Maintains up-to-date and accurate content
- Follows documentation best practices
```

---

## 🔄 **STEP 10: Automation & Maintenance Policies**

### **Prompt:**
```
You are an automation engineer specializing in software maintenance and operational excellence. Implement comprehensive automation policies for Project Chimera that ensure continuous integration, automated maintenance, and proactive system health management.

**AUTOMATION POLICY REQUIREMENTS:**
1. Implement auto-sync mechanisms:
   - 3-hour automated pull and sync policy
   - GitHub Actions for cloud-based synchronization
   - Local cron job setup for development environments
   - Conflict resolution and merge strategies
   - Comprehensive logging and status reporting

2. Design dependency management automation:
   - Automated dependency updates with testing
   - Security vulnerability patching
   - License compliance monitoring
   - Breaking change detection and notification
   - Rollback mechanisms for failed updates

3. Create maintenance automation:
   - Daily commit requirement enforcement
   - Code quality monitoring and reporting
   - Performance regression detection
   - Security scan automation
   - Documentation freshness checking

4. Implement operational automation:
   - Health check automation and alerting
   - Resource usage monitoring and optimization
   - Backup and disaster recovery automation
   - Capacity planning and scaling triggers
   - Cost optimization and reporting

**SYNC POLICY FEATURES:**
- Smart change detection and selective syncing
- Stash management for local modifications
- Dependency update triggers
- Conflict resolution strategies
- Comprehensive audit trails

**MAINTENANCE AUTOMATION:**
- Automated code formatting and linting
- Security patch deployment
- Performance benchmark tracking
- Documentation generation
- Release preparation automation

**MONITORING AND ALERTING:**
- Real-time system health monitoring
- Performance degradation detection
- Security incident alerting
- Compliance violation notifications
- Resource utilization tracking

**OPERATIONAL EXCELLENCE:**
- Proactive issue detection and resolution
- Automated scaling based on demand
- Cost optimization recommendations
- Performance tuning automation
- Disaster recovery testing

**DELIVERABLES:**
- .github/workflows/auto-sync.yml for cloud automation
- scripts/auto-sync.sh for local synchronization
- scripts/setup-cron.sh for cron job installation
- Makefile commands for automation management
- Comprehensive logging and monitoring setup

**SUCCESS CRITERIA:**
- Maintains 100% sync compliance with 3-hour policy
- Achieves automated dependency management
- Provides proactive issue detection and resolution
- Implements comprehensive operational monitoring
- Supports enterprise maintenance requirements
```

---

## 🎯 **BONUS: Enterprise Integration Prompt**

### **Prompt:**
```
You are an enterprise integration architect specializing in large-scale system integration. Design and implement enterprise integration patterns for Project Chimera that enable seamless integration with existing enterprise systems, compliance frameworks, and operational workflows.

**ENTERPRISE INTEGRATION REQUIREMENTS:**
1. Implement SSO and identity management:
   - SAML 2.0 and OAuth 2.0 integration
   - Active Directory and LDAP support
   - Multi-factor authentication
   - Role-based access control
   - Audit logging and compliance

2. Design API gateway and service mesh:
   - Rate limiting and throttling
   - API versioning and deprecation
   - Request/response transformation
   - Circuit breaker patterns
   - Distributed tracing

3. Create enterprise data integration:
   - ETL/ELT pipeline support
   - Data warehouse connectivity
   - Real-time streaming integration
   - Data governance and lineage
   - Privacy and compliance controls

4. Implement enterprise monitoring:
   - SIEM integration for security
   - APM tools for performance
   - Business intelligence dashboards
   - Compliance reporting automation
   - Cost allocation and chargeback

**SUCCESS CRITERIA:**
- Integrates with enterprise identity systems
- Supports enterprise-grade monitoring and compliance
- Provides comprehensive API management
- Enables seamless data integration
- Maintains enterprise security standards
```

---

## 📊 **Prompt Scoring Criteria**

Each prompt is designed to score highly based on:

1. **Clarity & Specificity** (25 points)
2. **Technical Depth** (25 points)
3. **Enterprise Requirements** (20 points)
4. **Implementation Details** (15 points)
5. **Success Criteria** (15 points)

**Total: 100 points per prompt**

These prompts will guide AI agents to build a production-ready, enterprise-grade system with comprehensive documentation, testing, and operational excellence.