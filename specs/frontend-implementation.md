# Frontend Implementation Specification

## Agent Implementation Directive
This document provides EXACT specifications for frontend implementation. Every screen, component, field, and API mapping is defined. No guessing required.

---

## Screen 1: Dashboard (`/dashboard`)

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│ Header: Logo | Navigation | User Menu                       │
├─────────────────────────────────────────────────────────────┤
│ Metrics Bar (4 cards)                                       │
├─────────────────────────────────────────────────────────────┤
│ Left (8 cols)              │ Right (4 cols)                 │
│ Agent Status Grid          │ Trend Feed                     │
│                            │ Security Events                │
└─────────────────────────────────────────────────────────────┘
```

### Component: MetricsCard
**File:** `components/dashboard/MetricsCard.tsx`

```typescript
interface MetricsCardProps {
  title: string;
  value: number | string;
  change: number;  // percentage
  icon: ReactNode;
  color: 'green' | 'blue' | 'yellow' | 'red';
}

// API Mapping
GET /api/metrics → {
  activeAgents: number,
  tasksInProgress: number,
  budgetRemaining: number,
  systemHealth: 'healthy' | 'warning' | 'critical'
}

// Accessibility
- aria-label={`${title}: ${value}`}
- role="region"
- tabIndex={0}
```

### Component: AgentStatusGrid
**File:** `components/agents/AgentStatusGrid.tsx`

```typescript
interface AgentGridProps {
  agents: Agent[];
}

interface Agent {
  id: string;
  name: string;
  status: 'idle' | 'busy' | 'error' | 'offline';
  currentTask?: string;
}

// API Mapping
GET /api/agents → Agent[]
WebSocket: ws://api/agents/status → { agentId, status, task }

// Visual Mapping
status === 'idle' → green circle
status === 'busy' → blue circle (pulsing)
status === 'error' → red circle
status === 'offline' → gray circle

// Accessibility
- Each agent: role="button", aria-label="Agent {name}, status {status}"
- Grid: role="grid", aria-label="Agent status overview"
- Keyboard: Arrow keys navigate, Enter opens detail
```

---

## Screen 2: Agent Detail Modal

### Trigger
Click any agent in AgentStatusGrid

### Component: AgentDetailModal
**File:** `components/agents/AgentDetailModal.tsx`

```typescript
interface AgentDetail {
  id: string;
  name: string;
  role: 'planner' | 'worker' | 'judge';
  status: 'idle' | 'busy' | 'error' | 'offline';
  currentTask: {
    id: string;
    description: string;
    startedAt: string;
    progress: number;  // 0-100
  } | null;
  metrics: {
    tasksCompleted: number;
    successRate: number;  // 0-1
    avgResponseTime: number;  // milliseconds
  };
  logs: Array<{
    timestamp: string;
    level: 'info' | 'warn' | 'error';
    message: string;
  }>;
}

// API Mapping
GET /api/agents/{id} → AgentDetail
POST /api/agents/{id}/start → { success: boolean }
POST /api/agents/{id}/stop → { success: boolean }

// Fields
- Agent Name: <h2>, editable=false
- Status Badge: color-coded, real-time via WebSocket
- Current Task: <p>, shows description or "Idle"
- Progress Bar: <progress value={progress} max={100}>
- Metrics Grid: 3 cards (completed, success rate, avg time)
- Logs Table: scrollable, max 100 entries
- Actions: Start/Stop buttons (disabled based on status)

// Accessibility
- Modal: role="dialog", aria-modal="true"
- Close: aria-label="Close agent details"
- Start button: aria-label="Start agent {name}", disabled when busy
- Stop button: aria-label="Stop agent {name}", disabled when idle
- Logs: role="log", aria-live="polite"
```

---

## Screen 3: Trends Page (`/trends`)

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│ Header + Search Bar                                         │
├─────────────────────────────────────────────────────────────┤
│ Filters: Platform | Sentiment | Velocity                    │
├─────────────────────────────────────────────────────────────┤
│ Trend Cards (grid, 3 per row)                              │
└─────────────────────────────────────────────────────────────┘
```

### Component: TrendCard
**File:** `components/trends/TrendCard.tsx`

```typescript
interface Trend {
  id: string;
  topic: string;
  volume: number;
  sentiment: number;  // -1.0 to 1.0
  velocity: number;   // 0.0+
  platforms: Array<'twitter' | 'tiktok' | 'google_trends'>;
  status: 'analyzing' | 'approved' | 'rejected' | 'content_created';
  contentBrief?: {
    id: string;
    script: string;
    visualPrompts: string[];
  };
}

// API Mapping
GET /api/trends?platform={p}&minSentiment={s}&minVelocity={v} → Trend[]
POST /api/trends/analyze → { keywords: string[] } → { jobId: string }
GET /api/trends/{id}/brief → ContentBrief

// Field Mappings
- Topic: <h3>{trend.topic}</h3>
- Volume: <span>{trend.volume.toLocaleString()} mentions</span>
- Sentiment: <SentimentBar value={sentiment} /> (red -1, yellow 0, green 1)
- Velocity: <span>{velocity.toFixed(1)}x rising</span>
- Platforms: <PlatformBadges platforms={platforms} />
- Status: <StatusBadge status={status} />
- Action Button: "View Brief" (if contentBrief exists) or "Create Content"

// Accessibility
- Card: role="article", aria-label="Trend: {topic}"
- Sentiment bar: role="progressbar", aria-valuenow={sentiment}, aria-valuemin={-1}, aria-valuemax={1}
- Action button: aria-label="Create content for {topic}"
```

### Component: TrendFilters
**File:** `components/trends/TrendFilters.tsx`

```typescript
interface FilterState {
  platforms: string[];
  minSentiment: number;
  minVelocity: number;
}

// Field Mappings
- Platform checkboxes: twitter, tiktok, google_trends
  → onChange: updateFilters({ platforms: [...selected] })
- Sentiment slider: -1.0 to 1.0, step 0.1
  → onChange: updateFilters({ minSentiment: value })
- Velocity slider: 0.0 to 5.0, step 0.1
  → onChange: updateFilters({ minVelocity: value })

// Accessibility
- Fieldset: <fieldset><legend>Filter Trends</legend>
- Checkboxes: aria-label="Filter by {platform}"
- Sliders: aria-label="Minimum {metric}", aria-valuetext="{value}"
```

---

## Screen 4: Commerce Dashboard (`/commerce`)

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│ Budget Overview Card                                        │
├─────────────────────────────────────────────────────────────┤
│ Left (6 cols)              │ Right (6 cols)                 │
│ Transaction History        │ Category Breakdown Chart       │
└─────────────────────────────────────────────────────────────┘
```

### Component: BudgetOverview
**File:** `components/commerce/BudgetOverview.tsx`

```typescript
interface BudgetMetrics {
  dailyLimit: number;
  spent: number;
  remaining: number;
  utilizationPercent: number;
}

// API Mapping
GET /api/commerce/budget → BudgetMetrics

// Field Mappings
- Daily Limit: <span>${dailyLimit.toFixed(2)}</span>
- Spent: <span className="text-red-600">${spent.toFixed(2)}</span>
- Remaining: <span className="text-green-600">${remaining.toFixed(2)}</span>
- Progress Bar: <progress value={spent} max={dailyLimit}>
- Utilization: <span>{utilizationPercent.toFixed(1)}%</span>

// Accessibility
- Section: role="region", aria-label="Budget overview"
- Progress: aria-label="Budget utilization", aria-valuenow={spent}, aria-valuemax={dailyLimit}
```

### Component: TransactionTable
**File:** `components/commerce/TransactionTable.tsx`

```typescript
interface Transaction {
  id: string;
  timestamp: string;
  agentId: string;
  amount: number;
  recipient: string;
  purpose: string;
  status: 'pending' | 'approved' | 'rejected' | 'executed';
  approvedBy?: string;
}

// API Mapping
GET /api/commerce/transactions?limit={n}&offset={o} → Transaction[]
POST /api/commerce/transactions/{id}/approve → { success: boolean }

// Table Columns
1. Timestamp: format(timestamp, 'MMM dd, HH:mm')
2. Agent: agentId (link to agent detail)
3. Amount: $amount.toFixed(2)
4. Purpose: purpose (truncate at 50 chars)
5. Status: <StatusBadge status={status} />
6. Actions: Approve button (if pending)

// Accessibility
- Table: role="table", aria-label="Transaction history"
- Headers: <th scope="col">
- Rows: <tr role="row">
- Approve button: aria-label="Approve transaction {id}"
```

---

## Screen 5: Security Monitor (`/security`)

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│ Threat Level Indicator + Stats                             │
├─────────────────────────────────────────────────────────────┤
│ Security Event Feed (real-time)                            │
└─────────────────────────────────────────────────────────────┘
```

### Component: ThreatIndicator
**File:** `components/security/ThreatIndicator.tsx`

```typescript
interface SecurityStatus {
  threatLevel: 'low' | 'medium' | 'high' | 'critical';
  eventsLast24h: number;
  blockedRequests: number;
  activeAlerts: number;
}

// API Mapping
GET /api/security/status → SecurityStatus
WebSocket: ws://api/security/events → SecurityEvent

// Visual Mapping
threatLevel === 'low' → green indicator
threatLevel === 'medium' → yellow indicator
threatLevel === 'high' → orange indicator
threatLevel === 'critical' → red indicator (pulsing)

// Accessibility
- Indicator: role="status", aria-live="polite"
- Level: aria-label="Current threat level: {threatLevel}"
```

### Component: SecurityEventFeed
**File:** `components/security/SecurityEventFeed.tsx`

```typescript
interface SecurityEvent {
  id: string;
  timestamp: string;
  type: 'injection' | 'permission' | 'rate_limit' | 'kill_switch';
  severity: 'low' | 'medium' | 'high' | 'critical';
  agentId: string;
  details: string;
  blocked: boolean;
}

// API Mapping
GET /api/security/events?limit={n} → SecurityEvent[]
WebSocket: ws://api/security/events → SecurityEvent (real-time)

// Event Card Fields
- Timestamp: format(timestamp, 'HH:mm:ss')
- Type Badge: color-coded by type
- Severity Badge: color-coded by severity
- Agent: agentId (link)
- Details: details (expandable)
- Status: "Blocked" (red) or "Allowed" (green)

// Accessibility
- Feed: role="log", aria-live="polite", aria-atomic="false"
- Event: role="article", aria-label="{severity} {type} event at {time}"
- Auto-scroll: aria-relevant="additions"
```

---

## API Endpoints Reference

### Base URL
```
Development: http://localhost:8000/api
Production: https://api.chimera.ai/api
```

### Authentication
```typescript
// All requests require JWT token
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

### Endpoints

#### Metrics
```
GET /api/metrics
Response: {
  activeAgents: number,
  tasksInProgress: number,
  budgetRemaining: number,
  systemHealth: 'healthy' | 'warning' | 'critical'
}
```

#### Agents
```
GET /api/agents
Response: Agent[]

GET /api/agents/{id}
Response: AgentDetail

POST /api/agents/{id}/start
Response: { success: boolean, message?: string }

POST /api/agents/{id}/stop
Response: { success: boolean, message?: string }
```

#### Trends
```
GET /api/trends?platform={p}&minSentiment={s}&minVelocity={v}
Response: Trend[]

POST /api/trends/analyze
Body: { keywords: string[] }
Response: { jobId: string }

GET /api/trends/{id}/brief
Response: ContentBrief
```

#### Commerce
```
GET /api/commerce/budget
Response: BudgetMetrics

GET /api/commerce/transactions?limit={n}&offset={o}
Response: Transaction[]

POST /api/commerce/transactions/{id}/approve
Response: { success: boolean, message?: string }
```

#### Security
```
GET /api/security/status
Response: SecurityStatus

GET /api/security/events?limit={n}
Response: SecurityEvent[]
```

### WebSocket Events
```
ws://api/agents/status
→ { agentId: string, status: string, task?: string }

ws://api/security/events
→ SecurityEvent

ws://api/trends/new
→ Trend
```

---

## Styling System

### Colors (Tailwind)
```typescript
// Status colors
idle: 'bg-green-500'
busy: 'bg-blue-500'
error: 'bg-red-500'
offline: 'bg-gray-400'

// Severity colors
low: 'bg-blue-100 text-blue-800'
medium: 'bg-yellow-100 text-yellow-800'
high: 'bg-orange-100 text-orange-800'
critical: 'bg-red-100 text-red-800'

// Sentiment colors
negative: 'bg-red-500'
neutral: 'bg-yellow-500'
positive: 'bg-green-500'
```

### Typography
```typescript
// Headings
h1: 'text-3xl font-bold'
h2: 'text-2xl font-semibold'
h3: 'text-xl font-medium'

// Body
body: 'text-base'
small: 'text-sm'
tiny: 'text-xs'
```

---

## Accessibility Requirements

### WCAG 2.1 Level AA Compliance

#### Keyboard Navigation
- All interactive elements: `tabIndex={0}`
- Modal traps: Focus management with `react-focus-lock`
- Skip links: "Skip to main content"

#### Screen Readers
- Semantic HTML: `<main>`, `<nav>`, `<article>`
- ARIA labels: All buttons, inputs, regions
- Live regions: `aria-live="polite"` for updates

#### Color Contrast
- Text: Minimum 4.5:1 ratio
- Large text: Minimum 3:1 ratio
- Interactive elements: 3:1 ratio

#### Focus Indicators
- Visible focus: `focus:ring-2 focus:ring-blue-500`
- Never remove: `outline: none` forbidden

---

## Error Handling

### API Errors
```typescript
try {
  const response = await fetch('/api/endpoint');
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  const data = await response.json();
} catch (error) {
  // Show toast notification
  toast.error('Failed to load data. Please try again.');
  // Log to monitoring
  logger.error('API error', { endpoint, error });
}
```

### WebSocket Reconnection
```typescript
const ws = new WebSocket(url);
ws.onclose = () => {
  // Exponential backoff
  setTimeout(() => reconnect(), Math.min(1000 * 2 ** retries, 30000));
};
```

---

## Testing Requirements

### Unit Tests
```typescript
// Test each component
describe('AgentStatusGrid', () => {
  it('renders all agents', () => {
    render(<AgentStatusGrid agents={mockAgents} />);
    expect(screen.getAllByRole('button')).toHaveLength(mockAgents.length);
  });
  
  it('shows correct status colors', () => {
    render(<AgentStatusGrid agents={[idleAgent]} />);
    expect(screen.getByLabelText(/idle/i)).toHaveClass('bg-green-500');
  });
});
```

### Accessibility Tests
```typescript
import { axe } from 'jest-axe';

it('has no accessibility violations', async () => {
  const { container } = render(<Dashboard />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

---

**Implementation Priority:**
1. Dashboard (core metrics + agent grid)
2. Agent detail modal
3. Trends page
4. Commerce dashboard
5. Security monitor

**Estimated Effort:** 2-3 weeks for full implementation

