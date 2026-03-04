---
tags: [业务, Pipeline]
created: 2026-03-03
updated: 2026-03-04
---

# 客户 Pipeline

> **数据来源**：所有客户档案统一存放在 `[[03-customer-service/clients/_客户总览]]`。
> 本页面通过 Dataview 自动聚合销售视角的数据，不再独立维护客户基本信息。

## Pipeline 总览（自动汇总）

```dataview
TABLE sales_stage AS "销售阶段", category AS "需求类别", next_followup AS "下次跟进", source AS "来源", annual_income_range AS "收入范围"
FROM "03-customer-service/clients"
WHERE file.name != "_客户总览" AND file.name != "_客户档案模板"
WHERE sales_stage != "已成交" AND sales_stage != "已流失"
SORT next_followup ASC
```

## 按阶段分布

```dataview
TABLE length(rows) AS "客户数"
FROM "03-customer-service/clients"
WHERE file.name != "_客户总览" AND file.name != "_客户档案模板"
GROUP BY sales_stage
SORT length(rows) DESC
```

## 阶段说明

| 阶段 | 说明 | 关键动作 |
|------|------|---------|
| 新线索 | 刚获得联系方式 | 初次接触，建立关系 |
| 已接触 | 已初步沟通 | 约定FNA时间 |
| 需求分析中 | 正在做FNA | 完成需求分析，设计方案 |
| 方案呈现 | 已提交方案 | 解答疑问，处理异议 |
| 促成中 | 客户有意向 | 促成签单 |
| 已成交 | 已签单 | 售后服务，转介绍 |
| 已流失 | 暂时不跟进 | 定期保持联系 |

## 本周重点跟进

```dataview
TABLE sales_stage AS "阶段", category AS "需求", next_followup AS "跟进日期"
FROM "03-customer-service/clients"
WHERE file.name != "_客户总览" AND file.name != "_客户档案模板"
WHERE next_followup <= date(today) + dur(7 days) AND next_followup
WHERE sales_stage != "已成交" AND sales_stage != "已流失"
SORT next_followup ASC
```

## 已成交客户

```dataview
TABLE category AS "产品类别", annual_premium AS "年保费", source AS "来源"
FROM "03-customer-service/clients"
WHERE file.name != "_客户总览" AND file.name != "_客户档案模板"
WHERE sales_stage = "已成交"
SORT annual_premium DESC
```

---

**新建客户**：使用统一模板 `[[03-customer-service/clients/_客户档案模板]]`，存放到 `03-customer-service/clients/` 目录。
