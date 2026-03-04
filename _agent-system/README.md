---
tags: [系统, 多Agent, 协作]
status: active
created: 2026-03-03
---

# 多 Agent 协作系统

把每个部门视作一个独立 Agent，通过统一任务单进行协作。

## Agent 注册表

| agent_id | 部门 | 目录 | 主要输入 | 主要输出 |
|---|---|---|---|---|
| ceo | CEO/COO | `00-ceo/` | 各部门周报、关键指标 | OKR、决策、跨部门任务 |
| recruitment | 招募 | `01-recruitment/` | 候选人线索、岗位画像 | 候选人推进结果、增员计划 |
| business_dev | 业务拓展 | `02-business-dev/` | 客户画像、产品信息 | 方案建议、成交推进计划 |
| customer_service | 客户服务 | `03-customer-service/` | 客户保单信息、服务记录 | 续保/检视/理赔进度 |
| content_marketing | 内容营销 | `04-content-marketing/` | 品牌定位、选题、业务反馈 | 内容日历、内容资产、线索输入 |
| data_analytics | 数据分析 | `05-data-analytics/` | 活动量、收入、成交数据 | 仪表盘、周报、策略建议 |

## 协作协议

1. 发起方创建任务单：`_agent-system/tasks/TASK-YYYYMMDD-XXX.md`
2. 接收方更新 `status` 为 `in_progress` 并在「执行记录」追加进展
3. 完成后填写 `deliverable`（必须是 Obsidian 双向链接）并改为 `done`
4. 回传给发起方，发起方验收后可归档
5. 跨部门任务（`from_agent != ceo` 且有 `cc_agents`）必须将 `ceo` 纳入 `cc_agents`

状态流转：`todo -> in_progress -> review -> done`（可选 `blocked`）

## 新输入迭代流程（PDF/客户信息）

统一先进入 Intake，再进入部门协作：

1. 在 `[[_agent-system/intake/输入处理SOP]]` 选择输入类型流程
2. 用模板创建 Intake 任务（PDF、客户信息或其他格式）
3. 先产出结构化 Markdown（写入 `_agent-system/intake/parsed/`，再分派）
4. 再按目标分派给对应部门 Agent
5. 在 `[[_agent-system/inbox]]` 跟踪所有后续任务状态

推荐模板：
- `[[_agent-system/templates/输入任务-PDF解析模板]]`
- `[[_agent-system/templates/输入任务-客户信息模板]]`
- `[[_agent-system/templates/输入任务-结构化输出模板]]`

任务治理SOP：
- `[[_agent-system/intake/任务分派预检SOP]]`
- `[[_agent-system/intake/任务复盘SOP]]`
- `[[_agent-system/intake/记忆维护SOP]]`

## 知识答复自动回写

用户提出知识性问题时，默认“先答复、同轮回写”：

1. 按问题类型路由到对应部门知识库
2. 更新现有文档或新建专题笔记
3. 补充 `[[双向链接]]` 与 `updated` 日期

执行细则：`[[_agent-system/intake/知识答复自动回写SOP]]`

## 使用入口

- 总看板：`[[_agent-system/inbox]]`
- 模板：`[[_agent-system/templates/任务单模板]]`
- 任务目录：`_agent-system/tasks/`

## 提交前自动检查

为确保“先结构化再分派、产品文件回写产品卡”落地，启用 pre-commit 检查：

1. 安装：`[[_agent-system/intake/提交前自动检查SOP]]`
2. 核心脚本：`_agent-system/scripts/precommit_validate_intake.py`
