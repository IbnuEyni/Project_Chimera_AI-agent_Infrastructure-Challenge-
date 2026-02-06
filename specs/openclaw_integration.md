# 🌐 Project Chimera - OpenClaw Network Integration

**Version**: 1.0.0  
**Last Updated**: 2026-02-06  
**Status**: Optional Enhancement

---

## Overview

OpenClaw is a decentralized network for AI agent discovery and coordination using a Distributed Hash Table (DHT). This specification defines how Project Chimera broadcasts its availability, handles service requests, and participates in the OpenClaw ecosystem.

---

## 1. Discovery Protocol

### Heartbeat Broadcasting

Chimera nodes **MUST** publish a "Heartbeat" to the OpenClaw DHT every **60 seconds** to announce availability.

#### Heartbeat Payload

**Endpoint**: `DHT.publish("chimera-alpha-001", payload)`

```json
{
  "node_id": "chimera-alpha-001",
  "version": "1.0.0",
  "timestamp": 1707123456,
  "capabilities": [
    "trend_analysis",
    "video_synthesis",
    "market_prediction",
    "content_generation"
  ],
  "reputation_score": 98.5,
  "endpoint": "wss://chimera-node.api/v1/stream",
  "status": 200,
  "metrics": {
    "active_agents": 9847,
    "available_capacity": 153,
    "avg_response_time_ms": 1850,
    "success_rate": 0.98
  }
}
```

**Field Specifications**:
- `node_id`: Unique identifier for this Chimera instance
- `timestamp`: Unix timestamp (seconds since epoch)
- `capabilities`: Array of service identifiers
- `reputation_score`: 0-100 score based on historical performance
- `endpoint`: WebSocket endpoint for real-time communication
- `status`: HTTP-style status code (see Status Codes section)

**DHT Key**: `chimera:{node_id}:heartbeat`  
**TTL**: 90 seconds (1.5x heartbeat interval for fault tolerance)

---

### Discovery Query

External agents discover Chimera by querying the DHT:

```python
# Query by capability
results = DHT.query(capability="trend_analysis", min_reputation=90)

# Returns:
[
  {
    "node_id": "chimera-alpha-001",
    "reputation_score": 98.5,
    "endpoint": "wss://chimera-node.api/v1/stream",
    "status": 200
  }
]
```

---

## 2. Service Handshake

When an external OpenClaw agent requests a service from Chimera, the following 4-phase handshake occurs:

### Phase 1: Verification

**Request**: External agent sends signed request
```json
{
  "request_id": "uuid",
  "requester_id": "external-agent-xyz",
  "capability": "trend_analysis",
  "parameters": {
    "keywords": ["AI", "Crypto"],
    "timeframe": "24h"
  },
  "signature": "0x1234...abcd",
  "timestamp": 1707123456
}
```

**Action**: Chimera validates request signature against OpenClaw public registry
```python
def verify_request(request):
    public_key = OpenClawRegistry.get_public_key(request.requester_id)
    is_valid = verify_signature(request.signature, public_key, request.payload)
    return is_valid
```

**Response** (if invalid):
```json
{
  "error": "INVALID_SIGNATURE",
  "message": "Request signature verification failed"
}
```

---

### Phase 2: Negotiation

**Action**: Chimera CFO_Agent quotes a price in compute credits

```json
{
  "request_id": "uuid",
  "quote": {
    "price": 50,
    "currency": "compute_credits",
    "estimated_duration_ms": 1850,
    "expires_at": 1707123516
  },
  "escrow_address": "0xabcd...1234",
  "terms": {
    "sla_response_time_ms": 2000,
    "refund_policy": "full_refund_if_sla_breach"
  }
}
```

**Pricing Logic**:
```python
def calculate_price(capability, parameters):
    base_price = CAPABILITY_PRICES[capability]
    complexity_multiplier = estimate_complexity(parameters)
    demand_multiplier = get_current_load() / max_capacity
    return base_price * complexity_multiplier * demand_multiplier
```

---

### Phase 3: Execution

**Trigger**: Upon escrow lock confirmation

```json
{
  "request_id": "uuid",
  "escrow_status": "locked",
  "escrow_tx": "0x9876...5432",
  "locked_amount": 50
}
```

**Action**: Worker_Agent executes task

```python
async def execute_task(request):
    # Assign to appropriate agent
    agent = AgentPool.get_agent(capability=request.capability)
    
    # Execute with timeout
    result = await agent.execute(
        parameters=request.parameters,
        timeout=30000  # 30s
    )
    
    # Validate quality
    if result.quality_score < 0.8:
        raise QualityThresholdError()
    
    return result
```

---

### Phase 4: Settlement

**Action**: Result delivered, payment released

```json
{
  "request_id": "uuid",
  "status": "completed",
  "result": {
    "trends": [
      {
        "topic": "AI Regulation",
        "volume": 15000,
        "sentiment_score": 0.75
      }
    ]
  },
  "execution_time_ms": 1820,
  "quality_score": 0.92,
  "settlement": {
    "escrow_released": true,
    "payment_tx": "0x5555...9999",
    "amount": 50
  }
}
```

**Escrow Release Conditions**:
- Task completed successfully
- Quality score ≥ 0.8
- Response time within SLA
- Result passes validation

**Refund Conditions**:
- SLA breach (response time > 2000ms)
- Quality score < 0.8
- Task failure or timeout

---

## 3. Status Codes

Chimera uses HTTP-style status codes in heartbeat broadcasts:

### 200: Ready / Idle
```json
{
  "status": 200,
  "message": "Ready to accept requests",
  "available_capacity": 153,
  "current_load_percent": 15
}
```
**Meaning**: System healthy, accepting new requests

---

### 429: Swarm Saturation
```json
{
  "status": 429,
  "message": "Too many active tasks",
  "available_capacity": 0,
  "current_load_percent": 100,
  "retry_after_seconds": 120
}
```
**Meaning**: All agents busy, external requests will be queued or rejected

---

### 503: Maintenance / Sleep Mode
```json
{
  "status": 503,
  "message": "System in maintenance mode",
  "estimated_recovery_time": 1707125000,
  "reason": "scheduled_maintenance"
}
```
**Meaning**: System temporarily unavailable, do not send requests

---

### 500: Internal Error
```json
{
  "status": 500,
  "message": "Internal system error",
  "error_code": "DATABASE_UNAVAILABLE"
}
```
**Meaning**: System experiencing issues, avoid sending requests

---

## 4. Implementation Architecture

### Component: OpenClawPublisher

```python
class OpenClawPublisher:
    """Publishes Chimera status to OpenClaw DHT."""
    
    def __init__(self, node_id: str, dht_client: DHTClient):
        self.node_id = node_id
        self.dht = dht_client
        self.heartbeat_interval = 60  # seconds
    
    async def start_heartbeat(self):
        """Start periodic heartbeat broadcasting."""
        while True:
            payload = self.build_heartbeat_payload()
            await self.dht.publish(
                key=f"chimera:{self.node_id}:heartbeat",
                value=payload,
                ttl=90
            )
            await asyncio.sleep(self.heartbeat_interval)
    
    def build_heartbeat_payload(self) -> dict:
        """Build heartbeat payload with current metrics."""
        return {
            "node_id": self.node_id,
            "version": "1.0.0",
            "timestamp": int(time.time()),
            "capabilities": self.get_capabilities(),
            "reputation_score": self.get_reputation_score(),
            "endpoint": self.get_endpoint(),
            "status": self.get_status_code(),
            "metrics": self.get_current_metrics()
        }
    
    def get_status_code(self) -> int:
        """Determine current status code."""
        load = self.get_current_load()
        if load > 0.95:
            return 429  # Swarm saturation
        elif self.is_maintenance_mode():
            return 503  # Maintenance
        elif self.has_critical_error():
            return 500  # Internal error
        else:
            return 200  # Ready
```

---

### Component: ServiceHandshakeHandler

```python
class ServiceHandshakeHandler:
    """Handles 4-phase service handshake with external agents."""
    
    async def handle_request(self, request: ServiceRequest) -> ServiceResponse:
        """Execute 4-phase handshake."""
        
        # Phase 1: Verification
        if not await self.verify_signature(request):
            raise InvalidSignatureError()
        
        # Phase 2: Negotiation
        quote = await self.cfo_agent.generate_quote(
            capability=request.capability,
            parameters=request.parameters
        )
        
        # Wait for escrow lock
        escrow_locked = await self.wait_for_escrow(
            request_id=request.request_id,
            amount=quote.price,
            timeout=30
        )
        
        if not escrow_locked:
            raise EscrowTimeoutError()
        
        # Phase 3: Execution
        result = await self.execute_task(request)
        
        # Phase 4: Settlement
        settlement = await self.settle_payment(
            request_id=request.request_id,
            result=result
        )
        
        return ServiceResponse(
            request_id=request.request_id,
            status="completed",
            result=result,
            settlement=settlement
        )
    
    async def verify_signature(self, request: ServiceRequest) -> bool:
        """Verify request signature against OpenClaw registry."""
        public_key = await OpenClawRegistry.get_public_key(
            agent_id=request.requester_id
        )
        return verify_signature(
            signature=request.signature,
            public_key=public_key,
            payload=request.payload
        )
```

---

## 5. Reputation System

### Reputation Score Calculation

```python
def calculate_reputation_score() -> float:
    """Calculate reputation score (0-100)."""
    metrics = get_historical_metrics()
    
    # Weighted components
    success_rate_score = metrics.success_rate * 40  # 40% weight
    response_time_score = (1 - metrics.avg_response_time / 5000) * 30  # 30% weight
    uptime_score = metrics.uptime_percent * 20  # 20% weight
    customer_satisfaction_score = (metrics.avg_rating / 5) * 10  # 10% weight
    
    total_score = (
        success_rate_score +
        response_time_score +
        uptime_score +
        customer_satisfaction_score
    )
    
    return min(100, max(0, total_score))
```

### Reputation Updates

Reputation score is recalculated every **15 minutes** and published to DHT:

```json
{
  "node_id": "chimera-alpha-001",
  "reputation": {
    "overall_score": 98.5,
    "components": {
      "success_rate": 0.98,
      "avg_response_time_ms": 1850,
      "uptime_percent": 99.9,
      "customer_satisfaction": 4.8
    },
    "tasks_completed": 1000000,
    "last_updated": 1707123456
  }
}
```

---

## 6. Error Handling

### Timeout Handling

If task execution exceeds SLA:
1. Cancel task execution
2. Release escrow to requester (full refund)
3. Log incident for reputation tracking
4. Update status to 500 if repeated failures

### Quality Threshold Failures

If result quality_score < 0.8:
1. Retry task with different agent
2. If retry fails, refund requester
3. Penalize reputation score

### Escrow Failures

If escrow lock fails or times out:
1. Reject request immediately
2. Return 402 Payment Required
3. Do not execute task

---

## 7. Security Considerations

### Threat: Sybil Attack (Fake Reputation)
**Mitigation**: Reputation tied to OpenClaw registry identity, verified by network consensus

### Threat: Request Replay Attack
**Mitigation**: Timestamp validation (reject requests >30s old)

### Threat: Escrow Manipulation
**Mitigation**: Use internal ledger with CFO cryptographic signatures. For external OpenClaw transactions, reference smart contract escrow addresses but settlement is tracked in internal ledger table.

**Note**: The `ledger` table in technical.md tracks all financial decisions internally. When interacting with external OpenClaw agents, smart contract escrow provides payment guarantees, but Chimera's internal accounting remains in the SQL ledger with CFO approval signatures.

### Threat: DDoS via Discovery
**Mitigation**: Rate limit DHT queries (100/min per IP)

---

## 8. Monitoring & Metrics

### Metrics to Track

```python
# OpenClaw-specific metrics
openclaw_heartbeat_success_rate
openclaw_discovery_queries_total
openclaw_service_requests_total{status="completed|failed"}
openclaw_escrow_locks_total
openclaw_reputation_score
openclaw_external_task_duration_seconds
```

### Alerts

- Heartbeat failure (3 consecutive misses)
- Reputation score drop >10 points
- Escrow lock failure rate >5%
- External task error rate >10%

---

## 9. Configuration

### Environment Variables

```bash
# OpenClaw Integration
OPENCLAW_ENABLED=true
OPENCLAW_DHT_BOOTSTRAP_NODES=["dht1.openclaw.network:6881", "dht2.openclaw.network:6881"]
OPENCLAW_NODE_ID=chimera-alpha-001
OPENCLAW_HEARTBEAT_INTERVAL=60
OPENCLAW_ENDPOINT=wss://chimera-node.api/v1/stream

# Pricing
OPENCLAW_BASE_PRICE_TREND_ANALYSIS=50
OPENCLAW_BASE_PRICE_VIDEO_SYNTHESIS=200
OPENCLAW_PRICE_CURRENCY=compute_credits

# Security
OPENCLAW_PRIVATE_KEY=<secret>
OPENCLAW_REGISTRY_URL=https://registry.openclaw.network
```

---

## 10. Testing Strategy

### Unit Tests
- Heartbeat payload generation
- Signature verification
- Price calculation logic
- Reputation score calculation

### Integration Tests
- DHT publish/query operations
- 4-phase handshake flow
- Escrow lock/release
- Timeout handling

### Load Tests
- 1000 concurrent external requests
- Heartbeat under high load
- DHT query performance

---

## Success Metrics

- Heartbeat uptime: >99.9%
- Discovery query response time: <100ms
- Service handshake completion rate: >95%
- Reputation score: >90
- External task success rate: >98%
