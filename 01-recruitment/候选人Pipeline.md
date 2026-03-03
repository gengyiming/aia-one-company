---
tags: [招募, Pipeline]
created: 2026-03-03
updated: 2026-03-03
---

# 候选人 Pipeline

## Pipeline 总览

```dataview
TABLE status AS "状态", source AS "来源", next_action AS "下一步", created AS "添加日期"
FROM "01-recruitment/cases"
WHERE contains(tags, "候选人")
SORT created DESC
```

## 阶段说明

| 阶段 | 说明 | 目标 |
|------|------|------|
| 新线索 | 刚识别的潜在候选人 | 初次接触 |
| 已接触 | 已初步沟通，了解意向 | 邀请参加Career Talk |
| Career Talk | 已参加说明会 | 安排面试 |
| 面试中 | 正在面试评估 | 发出offer |
| 已发Offer | 已邀请加入 | 辅助考牌入职 |
| 考牌中 | 正在准备/报考IIQE | 通过考试 |
| 已入职 | 已正式加入团队 | 30-60-90天培训 |
| 暂缓 | 时机未到，保持联系 | 定期follow up |
| 已拒绝 | 明确拒绝 | 存档，未来再看 |

## 手动追踪表

| 候选人 | 状态 | 来源 | 背景 | 下一步 | 日期 |
|--------|------|------|------|--------|------|
| （示例）李小姐 | 已接触 | LinkedIn | 银行客户经理5年 | 邀请Career Talk | 2026-03-10 |

---

## 本月重点

> 每月更新

-
