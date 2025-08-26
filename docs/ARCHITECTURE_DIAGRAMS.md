# TradingAgents Architecture Diagrams

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Agent Workflow](#agent-workflow)
4. [Data Flow Architecture](#data-flow-architecture)
5. [State Management](#state-management)
6. [LLM Integration](#llm-integration)
7. [Deployment Architecture](#deployment-architecture)

## System Overview

### High-Level System Architecture

```mermaid
graph TB
    User[User Interface] --> TG[TradingAgentsGraph]
    TG --> AT[Analyst Team]
    TG --> RT[Research Team] 
    TG --> TR[Trader]
    TG --> RM[Risk Management]
    TG --> PM[Portfolio Manager]
    
    AT --> MA[Market Analyst]
    AT --> SA[Social Analyst]
    AT --> NA[News Analyst]
    AT --> FA[Fundamentals Analyst]
    
    RT --> BR[Bull Researcher]
    RT --> BE[Bear Researcher]
    RT --> RMG[Research Manager]
    
    RM --> RA[Risky Analyst]
    RM --> CA[Conservative Analyst]
    RM --> NEU[Neutral Analyst]
    RM --> RJ[Risk Judge]
    
    subgraph "Data Sources"
        YF[Yahoo Finance]
        FH[FinnHub]
        RD[Reddit]
        GN[Google News]
    end
    
    subgraph "LLM Providers"
        OAI[OpenAI]
        ANT[Anthropic]
        GOO[Google]
    end
    
    AT --> YF
    AT --> FH
    AT --> RD
    AT --> GN
    
    TG --> OAI
    TG --> ANT
    TG --> GOO
```

### Trading Decision Pipeline

```mermaid
graph LR
    Start([Start]) --> Data[Data Collection]
    Data --> Analysis[Multi-Agent Analysis]
    Analysis --> Debate[Research Debate]
    Debate --> Trade[Trading Decision]
    Trade --> Risk[Risk Assessment]
    Risk --> Decision{Final Decision}
    Decision -->|Approve| Execute[Execute Trade]
    Decision -->|Reject| Reject[Reject Trade]
    Execute --> End([End])
    Reject --> End
```

## Component Architecture

### Core Framework Components

```mermaid
graph TB
    subgraph "TradingAgents Framework"
        subgraph "Orchestration Layer"
            TG[TradingAgentsGraph]
            GS[GraphSetup]
            CL[ConditionalLogic]
            PR[Propagator]
        end
        
        subgraph "Agent Layer"
            subgraph "Analysts"
                MA[Market Analyst]
                SA[Social Analyst]
                NA[News Analyst]
                FA[Fundamentals Analyst]
            end
            
            subgraph "Research Team"
                BR[Bull Researcher]
                BE[Bear Researcher]
                RM[Research Manager]
            end
            
            subgraph "Trading Team"
                TR[Trader]
            end
            
            subgraph "Risk Management"
                RA[Risky Analyst]
                CA[Conservative Analyst]
                NEU[Neutral Analyst]
                RJ[Risk Judge]
            end
        end
        
        subgraph "Data Layer"
            IF[Interface]
            YU[YFin Utils]
            FU[FinnHub Utils]
            RU[Reddit Utils]
            GU[GoogleNews Utils]
        end
        
        subgraph "State Management"
            AS[AgentState]
            IDS[InvestDebateState]
            RDS[RiskDebateState]
            MEM[Memory Systems]
        end
    end
    
    TG --> GS
    GS --> CL
    GS --> Analysts
    GS --> "Research Team"
    GS --> "Trading Team"
    GS --> "Risk Management"
    
    Analysts --> IF
    IF --> YU
    IF --> FU
    IF --> RU
    IF --> GU
    
    TG --> AS
    "Research Team" --> IDS
    "Risk Management" --> RDS
    Analysts --> MEM
```

### Module Dependencies

```mermaid
graph TD
    Main[main.py] --> TG[tradingagents.graph.trading_graph]
    CLI[cli.main] --> TG
    
    TG --> Agents[tradingagents.agents]
    TG --> Config[tradingagents.default_config]
    TG --> DataFlows[tradingagents.dataflows]
    
    Agents --> Utils[tradingagents.agents.utils]
    Agents --> Analysts[tradingagents.agents.analysts]
    Agents --> Researchers[tradingagents.agents.researchers]
    Agents --> Trader[tradingagents.agents.trader]
    Agents --> Managers[tradingagents.agents.managers]
    Agents --> RiskMgmt[tradingagents.agents.risk_mgmt]
    
    DataFlows --> Interface[tradingagents.dataflows.interface]
    DataFlows --> YFinUtils[tradingagents.dataflows.yfin_utils]
    DataFlows --> FinnHubUtils[tradingagents.dataflows.finnhub_utils]
    DataFlows --> RedditUtils[tradingagents.dataflows.reddit_utils]
    DataFlows --> GoogleNewsUtils[tradingagents.dataflows.googlenews_utils]
    
    Utils --> AgentStates[agent_states.py]
    Utils --> AgentUtils[agent_utils.py]
    Utils --> Memory[memory.py]
```

## Agent Workflow

### Complete Agent Execution Flow

```mermaid
graph TD
    Start([Start Analysis]) --> Init[Initialize State]
    Init --> MA[Market Analyst]
    
    MA --> MATools{Tool Calls?}
    MATools -->|Yes| MAT[Market Tools]
    MATools -->|No| MAC[Clear Messages]
    MAT --> MA
    MAC --> SA[Social Analyst]
    
    SA --> SATools{Tool Calls?}
    SATools -->|Yes| SAT[Social Tools]
    SATools -->|No| SAC[Clear Messages]
    SAT --> SA
    SAC --> NA[News Analyst]
    
    NA --> NATools{Tool Calls?}
    NATools -->|Yes| NAT[News Tools]
    NATools -->|No| NAC[Clear Messages]
    NAT --> NA
    NAC --> FA[Fundamentals Analyst]
    
    FA --> FATools{Tool Calls?}
    FATools -->|Yes| FAT[Fundamentals Tools]
    FATools -->|No| FAC[Clear Messages]
    FAT --> FA
    FAC --> BR[Bull Researcher]
    
    BR --> DebateCheck{Continue Debate?}
    DebateCheck -->|Yes| BE[Bear Researcher]
    DebateCheck -->|No| RMG[Research Manager]
    BE --> DebateCheck
    
    RMG --> TR[Trader]
    TR --> RA[Risky Analyst]
    
    RA --> RiskCheck{Continue Risk Analysis?}
    RiskCheck -->|Yes| CA[Conservative Analyst]
    RiskCheck -->|No| RJ[Risk Judge]
    CA --> RiskCheck2{Continue Risk Analysis?}
    RiskCheck2 -->|Yes| NEU[Neutral Analyst]
    RiskCheck2 -->|No| RJ
    NEU --> RiskCheck
    
    RJ --> End([Final Decision])
```

### Research Debate Flow

```mermaid
graph TD
    Start([Start Debate]) --> Bull[Bull Researcher Turn]
    Bull --> BullUpdate[Update Bull History]
    BullUpdate --> DebateCount{Debate Count < Max?}
    
    DebateCount -->|Yes| Bear[Bear Researcher Turn]
    DebateCount -->|No| Judge[Research Manager Judge]
    
    Bear --> BearUpdate[Update Bear History]
    BearUpdate --> DebateCount2{Debate Count < Max?}
    
    DebateCount2 -->|Yes| Bull
    DebateCount2 -->|No| Judge
    
    Judge --> Decision[Investment Plan]
    Decision --> End([End Debate])
```

### Risk Assessment Flow

```mermaid
graph TD
    Start([Start Risk Assessment]) --> Risky[Risky Analyst Turn]
    Risky --> RiskyUpdate[Update Risky History]
    RiskyUpdate --> RiskCount{Risk Count < Max?}
    
    RiskCount -->|Yes| Safe[Safe Analyst Turn]
    RiskCount -->|No| RiskJudge[Risk Judge]
    
    Safe --> SafeUpdate[Update Safe History]
    SafeUpdate --> RiskCount2{Risk Count < Max?}
    
    RiskCount2 -->|Yes| Neutral[Neutral Analyst Turn]
    RiskCount2 -->|No| RiskJudge
    
    Neutral --> NeutralUpdate[Update Neutral History]
    NeutralUpdate --> RiskCount
    
    RiskJudge --> FinalDecision[Final Trade Decision]
    FinalDecision --> End([End Risk Assessment])
```

## Data Flow Architecture

### Data Source Integration

```mermaid
graph TB
    subgraph "External Data Sources"
        YF[Yahoo Finance API]
        FH[FinnHub API]
        RD[Reddit API]
        GN[Google News API]
        OAI_API[OpenAI API]
    end
    
    subgraph "Data Access Layer"
        IF[Interface Layer]
        YU[YFin Utils]
        FU[FinnHub Utils]
        RU[Reddit Utils]
        GU[GoogleNews Utils]
    end
    
    subgraph "Agent Tools"
        MT[Market Tools]
        ST[Social Tools]
        NT[News Tools]
        FT[Fundamentals Tools]
    end
    
    subgraph "Caching Layer"
        DC[Data Cache]
        LC[Local Cache]
        MC[Memory Cache]
    end
    
    YF --> YU
    FH --> FU
    RD --> RU
    GN --> GU
    OAI_API --> IF
    
    YU --> IF
    FU --> IF
    RU --> IF
    GU --> IF
    
    IF --> MT
    IF --> ST
    IF --> NT
    IF --> FT
    
    IF --> DC
    DC --> LC
    LC --> MC
```

### Data Processing Pipeline

```mermaid
graph LR
    Raw[Raw Data] --> Fetch[Data Fetching]
    Fetch --> Validate[Data Validation]
    Validate --> Transform[Data Transformation]
    Transform --> Cache[Caching]
    Cache --> Analyze[Analysis]
    Analyze --> Report[Report Generation]
    Report --> State[State Update]
```

### Tool Node Architecture

```mermaid
graph TB
    subgraph "Market Tool Node"
        YFOnline[get_YFin_data_online]
        YFOffline[get_YFin_data]
        SSOnline[get_stockstats_indicators_report_online]
        SSOffline[get_stockstats_indicators_report]
    end
    
    subgraph "Social Tool Node"
        SONOnline[get_stock_news_openai]
        RDOffline[get_reddit_stock_info]
    end
    
    subgraph "News Tool Node"
        GNOnline[get_global_news_openai]
        GoogleNews[get_google_news]
        FHNews[get_finnhub_news]
        RDNews[get_reddit_news]
    end
    
    subgraph "Fundamentals Tool Node"
        FOnline[get_fundamentals_openai]
        FHInsider[get_finnhub_company_insider_sentiment]
        FHTransactions[get_finnhub_company_insider_transactions]
        SimFinBalance[get_simfin_balance_sheet]
        SimFinCash[get_simfin_cashflow]
        SimFinIncome[get_simfin_income_stmt]
    end
    
    MA[Market Analyst] --> "Market Tool Node"
    SA[Social Analyst] --> "Social Tool Node"
    NA[News Analyst] --> "News Tool Node"
    FA[Fundamentals Analyst] --> "Fundamentals Tool Node"
```

## State Management

### State Evolution Through Pipeline

```mermaid
graph TD
    InitState[Initial State<br/>company_of_interest<br/>trade_date<br/>messages] --> 
    AnalystState[Analyst State<br/>+ market_report<br/>+ sentiment_report<br/>+ news_report<br/>+ fundamentals_report]
    
    AnalystState --> ResearchState[Research State<br/>+ investment_debate_state<br/>+ investment_plan]
    
    ResearchState --> TraderState[Trader State<br/>+ trader_investment_plan]
    
    TraderState --> RiskState[Risk State<br/>+ risk_debate_state<br/>+ final_trade_decision]
    
    RiskState --> FinalState[Final State<br/>Complete with all reports<br/>and decisions]
```

### State Structure Hierarchy

```mermaid
graph TB
    AgentState[AgentState] --> MessagesState[MessagesState]
    AgentState --> CompanyInfo[company_of_interest<br/>trade_date<br/>sender]
    AgentState --> AnalystReports[market_report<br/>sentiment_report<br/>news_report<br/>fundamentals_report]
    AgentState --> ResearchOutputs[investment_debate_state<br/>investment_plan]
    AgentState --> TradingOutputs[trader_investment_plan]
    AgentState --> RiskOutputs[risk_debate_state<br/>final_trade_decision]
    
    ResearchOutputs --> InvestDebateState[InvestDebateState<br/>bull_history<br/>bear_history<br/>history<br/>current_response<br/>judge_decision<br/>count]
    
    RiskOutputs --> RiskDebateState[RiskDebateState<br/>risky_history<br/>safe_history<br/>neutral_history<br/>history<br/>latest_speaker<br/>current_responses<br/>judge_decision<br/>count]
```

### Memory System Architecture

```mermaid
graph TB
    subgraph "Memory Systems"
        BM[Bull Memory]
        BEM[Bear Memory]
        TM[Trader Memory]
        IJM[Invest Judge Memory]
        RMM[Risk Manager Memory]
    end
    
    subgraph "Memory Operations"
        Store[Store Experience]
        Recall[Recall Similar]
        Learn[Learn Patterns]
    end
    
    BR[Bull Researcher] --> BM
    BE[Bear Researcher] --> BEM
    TR[Trader] --> TM
    RM[Research Manager] --> IJM
    RJ[Risk Judge] --> RMM
    
    BM --> Store
    BEM --> Store
    TM --> Store
    IJM --> Store
    RMM --> Store
    
    Store --> Recall
    Recall --> Learn
```

## LLM Integration

### LLM Provider Architecture

```mermaid
graph TB
    subgraph "LLM Configuration"
        Config[Configuration]
        Provider[Provider Selection]
        Models[Model Selection]
    end
    
    subgraph "LLM Providers"
        OpenAI[OpenAI<br/>GPT-4o, GPT-4o-mini<br/>o1-preview]
        Anthropic[Anthropic<br/>Claude-3-Opus<br/>Claude-3-Haiku]
        Google[Google<br/>Gemini-2.0-flash<br/>Gemini-Pro]
    end
    
    subgraph "LLM Usage Patterns"
        DeepThink[Deep Thinking<br/>Strategic Analysis<br/>o1-preview, Claude-Opus]
        QuickThink[Quick Thinking<br/>Routine Analysis<br/>GPT-4o-mini, Claude-Haiku]
    end
    
    Config --> Provider
    Provider --> OpenAI
    Provider --> Anthropic
    Provider --> Google
    
    OpenAI --> DeepThink
    OpenAI --> QuickThink
    Anthropic --> DeepThink
    Anthropic --> QuickThink
    Google --> DeepThink
    Google --> QuickThink
    
    DeepThink --> RM[Research Manager]
    DeepThink --> RJ[Risk Judge]
    QuickThink --> Analysts[All Analysts]
    QuickThink --> Researchers[Researchers]
    QuickThink --> TR[Trader]
```

### Tool Binding and Execution

```mermaid
graph LR
    Agent[Agent] --> LLM[LLM with Tools]
    LLM --> ToolCall[Tool Call Decision]
    ToolCall --> ToolNode[Tool Node Execution]
    ToolNode --> DataSource[External Data Source]
    DataSource --> Response[Tool Response]
    Response --> LLM
    LLM --> FinalOutput[Final Agent Output]
```

## Deployment Architecture

### Development Deployment

```mermaid
graph TB
    subgraph "Development Environment"
        Dev[Developer Machine]
        IDE[IDE/Editor]
        LocalPython[Python 3.13]
        LocalCache[Local Cache]
    end
    
    subgraph "External Services"
        OpenAI_API[OpenAI API]
        FinnHub_API[FinnHub API]
        Reddit_API[Reddit API]
        GoogleNews_API[Google News API]
    end
    
    Dev --> IDE
    IDE --> LocalPython
    LocalPython --> LocalCache
    LocalPython --> OpenAI_API
    LocalPython --> FinnHub_API
    LocalPython --> Reddit_API
    LocalPython --> GoogleNews_API
```

### Production Deployment

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Container Orchestration"
            K8s[Kubernetes]
            Pods[Application Pods]
            Services[Services]
        end
        
        subgraph "Application Layer"
            API[API Gateway]
            LB[Load Balancer]
            App[TradingAgents App]
        end
        
        subgraph "Data Layer"
            Cache[Redis Cache]
            DB[Database]
            Storage[File Storage]
        end
        
        subgraph "Monitoring"
            Logs[Logging]
            Metrics[Metrics]
            Alerts[Alerting]
        end
    end
    
    subgraph "External Services"
        LLM_APIs[LLM APIs]
        Data_APIs[Data APIs]
    end
    
    K8s --> Pods
    Pods --> Services
    Services --> API
    API --> LB
    LB --> App
    
    App --> Cache
    App --> DB
    App --> Storage
    
    App --> Logs
    App --> Metrics
    Metrics --> Alerts
    
    App --> LLM_APIs
    App --> Data_APIs
```

### Scalability Architecture

```mermaid
graph TB
    subgraph "Horizontal Scaling"
        LB[Load Balancer]
        App1[App Instance 1]
        App2[App Instance 2]
        App3[App Instance N]
    end
    
    subgraph "Data Layer Scaling"
        CacheCluster[Redis Cluster]
        DBCluster[Database Cluster]
        CDN[Content Delivery Network]
    end
    
    subgraph "Service Scaling"
        APIGateway[API Gateway]
        RateLimiter[Rate Limiter]
        CircuitBreaker[Circuit Breaker]
    end
    
    LB --> App1
    LB --> App2
    LB --> App3
    
    App1 --> CacheCluster
    App2 --> CacheCluster
    App3 --> CacheCluster
    
    CacheCluster --> DBCluster
    
    APIGateway --> RateLimiter
    RateLimiter --> CircuitBreaker
    CircuitBreaker --> LB
```

---

These architecture diagrams provide a comprehensive visual understanding of the TradingAgents framework structure, data flows, and deployment patterns. Use these diagrams as reference for development, debugging, and system design discussions.