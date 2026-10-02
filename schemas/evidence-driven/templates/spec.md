# Delta for <Capability>

<!-- 新能力的 delta 以 ## Purpose 开头（≥50 字符）；既有能力不要加 Purpose -->
<!-- 注意：## 级 delta 标题必须保持英文原文，CLI 依赖它们解析归档 -->
<!-- Requirement/Scenario 前缀必须保持英文；名称可以用中文 -->
<!-- 场景必须恰好 4 个 #；THEN 必须可机械断言 -->
<!-- P0/P1：每个需求至少 1 个快乐路径场景 + 1 个失败/边界场景 -->

## Purpose

<!-- 新能力专用：这个能力是干什么的，1-2 句 -->

## ADDED Requirements

### Requirement: <需求名称>
系统 SHALL <可观测的规范行为>。

#### Scenario: <快乐路径场景名>
- **GIVEN** <前置状态>
- **WHEN** <触发动作>
- **THEN** <可断言的结果：一个值/状态/错误>

#### Scenario: <失败或边界场景名>
- **GIVEN** <异常前置状态>
- **WHEN** <触发动作>
- **THEN** <可断言的错误行为>

## MODIFIED Requirements

<!-- 必须粘贴完整需求块再修改；只贴部分会在归档时丢失细节 -->

## REMOVED Requirements

### Requirement: <被移除的需求名称>
**Reason**: <为什么移除>
**Migration**: <用户/调用方如何迁移>

## RENAMED Requirements

<!-- FROM: <旧名称> / TO: <新名称>，仅改名时使用 -->
