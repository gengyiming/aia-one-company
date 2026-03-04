---
task_id: TASK-YYYYMMDD-PDF-001
input_type: pdf
from_agent: ceo
to_agent: data_analytics
cc_agents: [business_dev]
status: todo
priority: high
created: 2026-03-03
due: 2026-03-04
source_file: "[[路径/文件.pdf]]"
deliverable: "[[_agent-system/intake/parsed/PDF-解析结果-YYYYMMDD]]"
structured_output: "[[_agent-system/intake/parsed/输入结构化-YYYYMMDD-XXX]]"
full_content_output: "[[_agent-system/intake/parsed/PDF-full-YYYYMMDD-xxx]]"
document_logic_type: policy | product | contract | report | presentation | mixed
is_product_file: false
product_card_paths: []
review_score: ""
review_notes: ""
memory_updated: false
tags: [任务, 输入处理, PDF]
---

# PDF 输入任务

## 业务目标
- 这份 PDF 要支持什么决策或动作？

## 解析要求
- [ ] 先识别文档逻辑类型并选择解析策略（`[[_agent-system/intake/PDF结构化解析策略库]]`）
- [ ] 再生成结构化 Markdown（使用 `[[_agent-system/templates/输入任务-结构化输出模板]]`）
- [ ] 生成全量覆盖 Markdown（逐页全文，覆盖原 PDF 全部页面）
- [ ] 正文按 PDF 原文逻辑展开（不套固定章节）
- [ ] 每个关键结论提供页码证据
- [ ] 若是产品文件，已更新对应产品卡并校验 Dataview 字段

## 下游分派计划
- [ ] 发 `business_dev`：销售/方案任务
- [ ] 发 `customer_service`：服务/理赔任务
- [ ] 发 `content_marketing`：内容提炼任务
- [ ] 发 `data_analytics`：数据入库任务

## 执行记录

### 2026-03-03
- 任务创建

## 复盘（任务完成后由 CEO 填写）

- review_score: high | medium | low
- review_notes:
- [ ] memory_updated = true（已回写 CEO 记忆）
