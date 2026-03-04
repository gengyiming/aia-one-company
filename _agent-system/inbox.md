---
tags: [系统, 任务看板, Dataview]
status: active
created: 2026-03-04
updated: 2026-03-04
---

# 任务总看板（Inbox）

> 用途：所有部门任务的统一查看入口。按状态、优先级、部门筛选。

## 紧急待办（高优先 + 未完成）

```dataview
TABLE task_id as "任务ID", from_agent as "发起", to_agent as "接收", due as "截止", status as "状态", deliverable as "交付"
FROM "_agent-system/tasks"
WHERE status != "done" AND priority = "high"
SORT due asc
```

## 进行中

```dataview
TABLE task_id as "任务ID", from_agent as "发起", to_agent as "接收", priority as "优先级", due as "截止", deliverable as "交付"
FROM "_agent-system/tasks"
WHERE status = "in_progress"
SORT due asc
```

## 待处理

```dataview
TABLE task_id as "任务ID", from_agent as "发起", to_agent as "接收", priority as "优先级", due as "截止"
FROM "_agent-system/tasks"
WHERE status = "todo"
SORT priority desc, due asc
```

## 阻塞中

```dataview
TABLE task_id as "任务ID", from_agent as "发起", to_agent as "接收", priority as "优先级", due as "截止"
FROM "_agent-system/tasks"
WHERE status = "blocked"
SORT due asc
```

## 待验收

```dataview
TABLE task_id as "任务ID", from_agent as "发起", to_agent as "接收", priority as "优先级", deliverable as "交付"
FROM "_agent-system/tasks"
WHERE status = "review"
SORT due asc
```

## 按部门分布

```dataview
TABLE length(rows) as "未完成任务数"
FROM "_agent-system/tasks"
WHERE status != "done"
GROUP BY to_agent
SORT length(rows) desc
```

## 最近完成（近 7 天）

```dataview
TABLE task_id as "任务ID", from_agent as "发起", to_agent as "接收", review_score as "满意度", deliverable as "交付"
FROM "_agent-system/tasks"
WHERE status = "done"
SORT file.mtime desc
LIMIT 10
```

---

相关入口：
- [[00-ceo/团队管理总控面板]]
- [[_agent-system/README]]
- [[_agent-system/intake/任务分派预检SOP]]
