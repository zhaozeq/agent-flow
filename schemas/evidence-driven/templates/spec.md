# Delta for <Capability>

<!-- 新能力必须保留并填写 Purpose（50+ 字符，--strict 强制检查）；既有能力删除本节；删除未使用的操作节及占位内容 -->
<!-- 注意：## 级 delta 标题必须保持英文原文，CLI 依赖它们解析归档 -->
<!-- Requirement/Scenario 前缀必须保持英文；名称可以用中文 -->
<!-- 场景必须恰好 4 个 #；THEN 必须可机械断言 -->
<!-- P0/P1：考虑相关失败/边界场景，不适用时说明理由；REMOVED/RENAMED 不硬凑场景 -->

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

<!-- 仅改名时保留；FROM/TO 必须逐行包含完整 Requirement 标题 -->
- FROM: `### Requirement: <旧名称>`
- TO: `### Requirement: <新名称>`
