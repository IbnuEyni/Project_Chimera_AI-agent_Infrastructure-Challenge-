# Frontend Architecture Specification

## Overview
Project Chimera frontend provides real-time monitoring, control, and visualization for the autonomous agent swarm.

## Technology Stack

### Core Framework
- **React 18+** with TypeScript
- **Next.js 14** for SSR and routing
- **TailwindCSS** for styling
- **shadcn/ui** for component library

### State Management
- **Zustand** for global state
- **React Query** for server state
- **WebSocket** for real-time updates

### Visualization
- **Recharts** for metrics dashboards
- **D3.js** for agent network graphs
- **React Flow** for workflow visualization

## Application Structure

```
frontend/
├── app/
│   ├── dashboard/          # Main dashboard
│   ├── agents/             # Agent management
│   ├── trends/             # Trend monitoring
│   ├── commerce/           # Financial overview
│   ├── security/           # Security events
│   └── settings/           # Configuration
├── components/
│   ├── ui/                 # shadcn components
│   ├── charts/             # Chart components
│   ├── agents/             # Agent-specific
│   └── shared/             # Shared components
├── lib/
│   ├── api/                # API client
│   ├── websocket/          # WebSocket client
│   └── utils/              # Utilities
└── types/                  # TypeScript types
```

## Key Features

### 1. Real-Time Dashboard

#### Metrics Display
```typescript
interface DashboardMetrics {
  activeAgents: number;
  tasksInProgress: number;
  trendsAnalyzed: number;
  budgetRemaining: number;
  systemHealth: 'healthy' | 'warning' | 'critical';
}
```

#### Components
- Agent status grid (10x10 for 100 agents)
- Real-time task queue
- Budget utilization chart
- Security event feed
- Performance metrics

### 2. Agent Management

#### Agent Card
```typescript
interface AgentCard {
  id: string;
  name: string;
  role: 'planner' | 'worker' | 'judge';
  status: 'idle' | 'busy' | 'error';
  currentTask?: string;
  metrics: {
    tasksCompleted: number;
    successRate: number;
    avgResponseTime: number;
  };
}
```

#### Features
- Start/stop agents
- View agent logs
- Assign tasks manually
- Monitor performance
- Configure agent parameters

### 3. Trend Monitoring

#### Trend Card
```typescript
interface TrendCard {
  id: string;
  topic: string;
  volume: number;
  sentiment: number;
  velocity: number;
  platforms: string[];
  status: 'analyzing' | 'approved' | 'rejected';
  contentBrief?: ContentBrief;
}
```

#### Visualization
- Trend timeline
- Sentiment heatmap
- Platform distribution
- Velocity graph
- Content pipeline status

### 4. Commerce Dashboard

#### Financial Overview
```typescript
interface FinancialMetrics {
  dailyBudget: number;
  spent: number;
  remaining: number;
  transactions: Transaction[];
  roi: {
    projected: number;
    actual: number;
  };
  categorySpending: Record<string, number>;
}
```

#### Features
- Budget utilization gauge
- Transaction history
- ROI tracking
- Category breakdown
- Approval queue

### 5. Security Monitor

#### Security Events
```typescript
interface SecurityEvent {
  id: string;
  timestamp: Date;
  type: 'injection' | 'permission' | 'rate_limit';
  severity: 'low' | 'medium' | 'high' | 'critical';
  agentId: string;
  details: string;
  blocked: boolean;
}
```

#### Features
- Real-time event stream
- Threat level indicator
- Blocked requests log
- Security metrics
- Alert configuration

## API Integration

### REST API Client
```typescript
// lib/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const agentsApi = {
  list: () => apiClient.get('/agents'),
  get: (id: string) => apiClient.get(`/agents/${id}`),
  start: (id: string) => apiClient.post(`/agents/${id}/start`),
  stop: (id: string) => apiClient.post(`/agents/${id}/stop`),
};

export const trendsApi = {
  list: () => apiClient.get('/trends'),
  analyze: (keywords: string[]) => apiClient.post('/trends/analyze', { keywords }),
};

export const commerceApi = {
  getMetrics: () => apiClient.get('/commerce/metrics'),
  getTransactions: () => apiClient.get('/commerce/transactions'),
  approveTransaction: (id: string) => apiClient.post(`/commerce/transactions/${id}/approve`),
};
```

### WebSocket Client
```typescript
// lib/websocket/client.ts
import { io, Socket } from 'socket.io-client';

class WebSocketClient {
  private socket: Socket;

  connect() {
    this.socket = io(process.env.NEXT_PUBLIC_WS_URL);
    
    this.socket.on('agent:status', (data) => {
      // Update agent status in real-time
    });
    
    this.socket.on('trend:new', (data) => {
      // Show new trend notification
    });
    
    this.socket.on('security:event', (data) => {
      // Alert on security event
    });
  }

  disconnect() {
    this.socket.disconnect();
  }
}

export const wsClient = new WebSocketClient();
```

## State Management

### Global Store
```typescript
// lib/store/useStore.ts
import { create } from 'zustand';

interface ChimeraStore {
  agents: Agent[];
  trends: Trend[];
  metrics: DashboardMetrics;
  securityEvents: SecurityEvent[];
  
  setAgents: (agents: Agent[]) => void;
  updateAgent: (id: string, updates: Partial<Agent>) => void;
  addTrend: (trend: Trend) => void;
  addSecurityEvent: (event: SecurityEvent) => void;
}

export const useStore = create<ChimeraStore>((set) => ({
  agents: [],
  trends: [],
  metrics: {} as DashboardMetrics,
  securityEvents: [],
  
  setAgents: (agents) => set({ agents }),
  updateAgent: (id, updates) => set((state) => ({
    agents: state.agents.map(a => a.id === id ? { ...a, ...updates } : a)
  })),
  addTrend: (trend) => set((state) => ({
    trends: [trend, ...state.trends]
  })),
  addSecurityEvent: (event) => set((state) => ({
    securityEvents: [event, ...state.securityEvents].slice(0, 100)
  })),
}));
```

## Component Examples

### Dashboard Page
```typescript
// app/dashboard/page.tsx
'use client';

import { useQuery } from '@tanstack/react-query';
import { MetricsGrid } from '@/components/dashboard/MetricsGrid';
import { AgentStatusGrid } from '@/components/agents/AgentStatusGrid';
import { TrendFeed } from '@/components/trends/TrendFeed';
import { SecurityFeed } from '@/components/security/SecurityFeed';

export default function DashboardPage() {
  const { data: metrics } = useQuery({
    queryKey: ['metrics'],
    queryFn: () => fetch('/api/metrics').then(r => r.json()),
    refetchInterval: 5000, // Refresh every 5 seconds
  });

  return (
    <div className="grid grid-cols-12 gap-4 p-6">
      <div className="col-span-12">
        <MetricsGrid metrics={metrics} />
      </div>
      
      <div className="col-span-8">
        <AgentStatusGrid />
      </div>
      
      <div className="col-span-4">
        <TrendFeed />
        <SecurityFeed />
      </div>
    </div>
  );
}
```

### Agent Status Grid
```typescript
// components/agents/AgentStatusGrid.tsx
import { useStore } from '@/lib/store/useStore';
import { AgentCard } from './AgentCard';

export function AgentStatusGrid() {
  const agents = useStore((state) => state.agents);

  return (
    <div className="grid grid-cols-10 gap-2">
      {agents.map((agent) => (
        <AgentCard key={agent.id} agent={agent} />
      ))}
    </div>
  );
}
```

## Deployment

### Build Configuration
```javascript
// next.config.js
module.exports = {
  output: 'standalone',
  env: {
    NEXT_PUBLIC_API_URL: process.env.API_URL,
    NEXT_PUBLIC_WS_URL: process.env.WS_URL,
  },
};
```

### Docker
```dockerfile
FROM node:20-alpine AS base

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

COPY --from=base /app/.next/standalone ./
COPY --from=base /app/public ./public
COPY --from=base /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
```

## Performance Targets

- **Initial Load**: <2 seconds
- **Time to Interactive**: <3 seconds
- **WebSocket Latency**: <100ms
- **Chart Render**: <16ms (60fps)
- **Bundle Size**: <500KB (gzipped)

## Accessibility

- WCAG 2.1 Level AA compliance
- Keyboard navigation
- Screen reader support
- High contrast mode
- Reduced motion support

## Security

- CSP headers
- XSS protection
- CSRF tokens
- Secure WebSocket (WSS)
- JWT authentication

---

**Status:** Architecture Defined
**Implementation:** Pending
**Priority:** HIGH
