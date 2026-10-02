## Context

从 `event-storming.md`、`event-modeling.md` 和 `specs/**/*.md` 中已批准的故事总结架构上下文。

## Goals / Non-Goals

- Goals：
- Non-goals：

## Messaging and Platform Decisions

### Broker / Runtime
- 选择的 broker/runtime：
- 理由：
- 考虑的替代方案：

### Subject/Topic Naming
- 命名约定：
- 版本控制策略：
- 所有权约定：

### Payload and Schema Format
- 消息编码格式：
- Schema 格式和演化规则：
- 兼容性期望：

### Delivery Semantics and Reliability
- At-most-once / at-least-once / exactly-once 期望：
- 重试和死信策略：
- 幂等性策略：

## Security Decisions

- 身份验证方法：
- 授权模型：
- 敏感数据处理：
- 传输安全和密钥管理：

## Operations and Observability

- 监控和告警：
- 跟踪/关联策略：
- 容量/性能考虑：

## Risks / Trade-offs

- [Risk] <description>
  - Mitigation：

## Handoff to AsyncAPI

列出编写 `asyncapi.yaml` 所需的具体输入：
- Channels/subjects
- Messages 和 schemas
- Bindings/protocol 详情
- 安全方案