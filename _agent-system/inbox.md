---
tags: [看板, Agent协作, Dataview]
status: active
created: 2026-03-03
---

# Agent 收件箱与协作看板

## 全部未完成任务

```dataview
TABLE task_id as "任务ID", from_agent as "发起", to_agent as "接收", priority as "优先级", due as "截止", status as "状态", deliverable as "交付"
FROM "_agent-system/tasks"
WHERE status != "done"
SORT due asc
```

## 新输入任务（PDF/客户信息）

```dataview
TABLE task_id as "任务ID", input_type as "输入类型", to_agent as "当前负责人", due as "截止", status as "状态", source_file as "来源PDF", source_note as "来源笔记"
FROM "_agent-system/tasks"
WHERE input_type = "pdf" OR input_type = "customer_info"
SORT due asc
```

## 按部门查看

### 招募部

```dataview
TABLE task_id, from_agent, priority, due, status
FROM "_agent-system/tasks"
WHERE to_agent = "recruitment" AND status != "done"
SORT due asc
```

### 业务拓展部

```dataview
TABLE task_id, from_agent, priority, due, status
FROM "_agent-system/tasks"
WHERE to_agent = "business_dev" AND status != "done"
SORT due asc
```

### 客户服务部

```dataview
TABLE task_id, from_agent, priority, due, status
FROM "_agent-system/tasks"
WHERE to_agent = "customer_service" AND status != "done"
SORT due asc
```

### 内容营销部

```dataview
TABLE task_id, from_agent, priority, due, status
FROM "_agent-system/tasks"
WHERE to_agent = "content_marketing" AND status != "done"
SORT due asc
```

### 数据分析部

```dataview
TABLE task_id, from_agent, priority, due, status
FROM "_agent-system/tasks"
WHERE to_agent = "data_analytics" AND status != "done"
SORT due asc
```
