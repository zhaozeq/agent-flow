# Event Modeling

将 event-storming 输出转换为明确的行为流。

对每个场景使用以下泳道顺序：
`Trigger -> Command -> Event -> Read Model`

## Scenario Overview
- 场景：
- 业务目标：
- 来自 `event-storming.md` 的源引用：

## Swim Lanes

### Trigger
- 人类/系统触发器：
- 输入信号：

### Command
- 命令名称：
- 目标聚合/上下文：
- 验证规则：

### Event
- 事件名称：
- 事件有效负载摘要：
- 排序/幂等性备注：

### Read Model
- 投影或物化视图：
- 消费者：
- 启用的查询/用例：

## Mermaid Flow
```mermaid
flowchart LR
  T[Trigger] --> C[Command]
  C --> E[Event]
  E --> R[Read Model]

  classDef actor fill:#F7DC6F,stroke:#B7950B,color:#1C1C1C
  classDef command fill:#85C1E9,stroke:#2471A3,color:#1C1C1C
  classDef event fill:#F5B041,stroke:#AF601A,color:#1C1C1C
  classDef policy fill:#D7BDE2,stroke:#884EA0,color:#1C1C1C
  classDef readModel fill:#82E0AA,stroke:#1E8449,color:#1C1C1C

  class T actor
  class C command
  class E event
  class R readModel
```

## Timeline / Swimlane Diagram
```mermaid
flowchart LR
  subgraph TriggerLane[Trigger]
    T1[Trigger]
  end
  subgraph CommandLane[Command]
    C1[Command]
  end
  subgraph EventLane[Event]
    E1[Event]
  end
  subgraph ReadModelLane[Read Model]
    R1[Read Model]
  end

  T1 --> C1
  C1 --> E1
  E1 --> R1

  classDef actor fill:#F7DC6F,stroke:#B7950B,color:#1C1C1C
  classDef command fill:#85C1E9,stroke:#2471A3,color:#1C1C1C
  classDef event fill:#F5B041,stroke:#AF601A,color:#1C1C1C
  classDef policy fill:#D7BDE2,stroke:#884EA0,color:#1C1C1C
  classDef readModel fill:#82E0AA,stroke:#1E8449,color:#1C1C1C

  class T1 actor
  class C1 command
  class E1 event
  class R1 readModel
```

## Derivation Notes for Downstream Artifacts
- Specs 输入（用户故事和验收标准）：
- Design 输入（broker、subject 命名、有效负载格式、安全性）：
- AsyncAPI 输入（channels、messages、bindings、schemas）：