# Agent Rule-Intent Specification

## Purpose
This document defines the behavioral rules and intent patterns that govern autonomous agent decision-making in Project Chimera.

## Rule Categories

### 1. Financial Rules (CFO Agent)

#### Budget Enforcement
```yaml
rule: daily_budget_limit
intent: Prevent runaway spending
threshold: $50.00
action: REJECT transaction if exceeds limit
priority: CRITICAL
```

#### ROI Threshold
```yaml
rule: minimum_roi_hurdle
intent: Ensure profitable investments
threshold: 1.5x (150% return)
action: REJECT if projected ROI < 1.5
priority: HIGH
```

#### Risk Assessment
```yaml
rule: risk_score_limit
intent: Avoid high-risk transactions
threshold: 0.8
action: REJECT if risk_score >= 0.8
priority: HIGH
```

### 2. Content Quality Rules (Judge Agent)

#### Quality Score
```yaml
rule: minimum_quality_score
intent: Maintain content standards
threshold: 0.8
action: REJECT content if quality < 0.8
priority: HIGH
```

#### Sentiment Boundaries
```yaml
rule: sentiment_range
intent: Ensure positive content
range: [-1.0, 1.0]
minimum: 0.3
action: REJECT if sentiment < 0.3
priority: MEDIUM
```

### 3. Security Rules (SecurityGateway)

#### Prompt Injection Detection
```yaml
rule: block_injection_attempts
intent: Prevent prompt manipulation
patterns: 12+ attack vectors
action: BLOCK and LOG
priority: CRITICAL
```

#### Permission Validation
```yaml
rule: rbac_enforcement
intent: Enforce role-based access
method: Permission validator
action: DENY if no permission
priority: CRITICAL
```

### 4. Governance Rules (Kill Switch)

#### Low Confidence Halt
```yaml
rule: confidence_threshold
intent: Stop on uncertainty
threshold: 0.5
action: EMERGENCY_HALT
priority: CRITICAL
```

#### Market Crash Protection
```yaml
rule: volatility_limit
intent: Protect during market crashes
threshold: 50% volatility
action: EMERGENCY_HALT
priority: CRITICAL
```

### 5. Trend Analysis Rules (Scout Agent)

#### Velocity Threshold
```yaml
rule: minimum_rising_velocity
intent: Focus on trending topics
threshold: 0.5
action: FILTER OUT if velocity < 0.5
priority: MEDIUM
```

#### Volume Threshold
```yaml
rule: minimum_volume
intent: Ensure significant trends
threshold: 1000 mentions
action: FILTER OUT if volume < 1000
priority: MEDIUM
```

## Intent Patterns

### Economic Intent
```
IF opportunity.projected_roi > 1.5
AND opportunity.cost <= daily_budget_remaining
AND opportunity.risk_score < 0.8
THEN approve_transaction()
ELSE reject_with_reason()
```

### Content Creation Intent
```
IF trend.rising_velocity > 0.5
AND trend.sentiment_score > 0.3
AND trend.volume > 1000
THEN create_content_brief()
ELSE skip_trend()
```

### Security Intent
```
IF input.contains_injection_pattern()
OR input.exceeds_rate_limit()
OR user.lacks_permission()
THEN block_request()
AND log_security_event()
ELSE allow_request()
```

### Quality Assurance Intent
```
IF content.quality_score >= 0.8
AND content.meets_guidelines()
AND content.passes_safety_check()
THEN approve_for_publishing()
ELSE request_revision()
```

## Rule Hierarchy

```
CRITICAL (Cannot be overridden)
├── Security rules
├── Kill switch rules
└── Budget hard limits

HIGH (Requires approval to override)
├── ROI thresholds
├── Quality standards
└── Risk limits

MEDIUM (Can be adjusted)
├── Trend filters
├── Content preferences
└── Performance targets

LOW (Configurable)
├── Logging levels
├── Retry attempts
└── Timeout values
```

## Rule Enforcement

### Validation Order
1. Security validation (CRITICAL)
2. Permission check (CRITICAL)
3. Budget validation (CRITICAL)
4. Kill switch check (CRITICAL)
5. ROI validation (HIGH)
6. Quality validation (HIGH)
7. Trend filtering (MEDIUM)

### Override Protocol
```python
def can_override_rule(rule, agent, justification):
    if rule.priority == "CRITICAL":
        return False  # Never override
    
    if rule.priority == "HIGH":
        return requires_human_approval(justification)
    
    if rule.priority == "MEDIUM":
        return agent.has_permission("override_medium_rules")
    
    return True
```

## Monitoring & Compliance

### Rule Violation Tracking
```yaml
metric: rule_violations_total
labels: [rule_name, agent_id, severity]
alert: violations > 10 in 1 hour
```

### Compliance Reporting
```yaml
report: daily_compliance_report
includes:
  - Total rule evaluations
  - Violations by category
  - Override requests
  - Security incidents
```

## Rule Updates

### Version Control
- All rule changes tracked in git
- Requires PR approval
- Automated testing before deployment

### Rollback Procedure
```bash
# Revert to previous rule version
git revert <commit-hash>
# Deploy immediately
make deploy-rules
```

## Examples

### Example 1: Transaction Approval
```python
# Input
transaction = {
    "amount": 45.00,
    "projected_roi": 2.0,
    "risk_score": 0.6
}

# Rule Evaluation
daily_budget_check: PASS (45 < 50)
roi_threshold_check: PASS (2.0 > 1.5)
risk_limit_check: PASS (0.6 < 0.8)

# Result: APPROVED
```

### Example 2: Content Rejection
```python
# Input
content = {
    "quality_score": 0.7,
    "sentiment": 0.85
}

# Rule Evaluation
quality_check: FAIL (0.7 < 0.8)
sentiment_check: PASS (0.85 > 0.3)

# Result: REJECTED (quality too low)
```

### Example 3: Emergency Halt
```python
# Input
market_data = {
    "volatility": 65.0,
    "confidence": 0.4
}

# Rule Evaluation
volatility_check: FAIL (65 > 50)
confidence_check: FAIL (0.4 < 0.5)

# Result: EMERGENCY_HALT triggered
```

## Integration Points

### With Skills
```python
from chimera.rules import RuleEngine

class TrendAnalyzer(ChimeraSkill):
    def __init__(self):
        self.rules = RuleEngine.load("trend_analysis_rules")
    
    async def execute(self, params):
        if not self.rules.validate(params):
            raise RuleViolation(self.rules.get_violations())
        # ... proceed with execution
```

### With Security
```python
from chimera.rules import SecurityRules

gateway = SecurityGateway(rules=SecurityRules.load())
result = await gateway.validate_request(request)
```

### With Commerce
```python
from chimera.rules import FinancialRules

cfo = CFOAgent(rules=FinancialRules.load())
approval = await cfo.review_transaction(transaction)
```

---

**Version:** 1.0.0
**Last Updated:** 2024
**Owner:** Governance Team
**Review Cycle:** Monthly
