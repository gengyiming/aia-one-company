---
tags: [系统, 知识管理, SOP, 生命周期]
status: active
created: 2026-03-04
updated: 2026-03-04
---

# 知识生命周期 SOP

目标：确保知识库不只是持续"写入"，还能自动检测过期、触发复核、归档清理，保持知识的新鲜度和可信度。

## 知识新鲜度分级

| 状态 | 条件 | 标识 | 处理 |
|------|------|------|------|
| **新鲜** | `updated` 在 90 天内 | 正常使用 | 无需操作 |
| **待复核** | `updated` 在 90-180 天前 | `#待复核` | 下次使用时先验证准确性 |
| **过期** | `updated` 超过 180 天 | `#过期` | 必须复核后才能引用 |

## 过期检测规则

### 自动检测（周复盘时执行）

每周复盘时，CEO Agent 执行以下 Dataview 查询，列出待复核和过期文件：

```dataview
TABLE file.folder AS "部门", updated AS "最近更新",
  choice(
    date(today) - updated > dur(180 days), "⚠️ 过期",
    choice(date(today) - updated > dur(90 days), "🔶 待复核", "✅ 新鲜")
  ) AS "状态"
FROM "01-recruitment" OR "02-business-dev/knowledge" OR "03-customer-service/scripts" OR "04-content-marketing/topics" OR "_resources"
WHERE updated AND (date(today) - updated > dur(90 days))
SORT updated ASC
```

### 高优先复核触发

以下类型文件超期时优先复核：
1. **产品卡**（`02-business-dev/knowledge/product-cards/`）— 产品条款可能已更新
2. **合规提醒**（`_resources/合规提醒.md`）— 监管要求可能变化
3. **官方文件结构化输出**（`_agent-system/intake/parsed/`）— 官方政策可能修订
4. **客户服务 SOP**（`03-customer-service/scripts/`）— 流程可能已优化

## 复核流程

1. CEO Agent 在周复盘中发现待复核/过期文件
2. 创建复核任务（`_agent-system/tasks/TASK-YYYYMMDD-REVIEW-XXX.md`）
3. 分派给对应部门 Agent
4. 部门 Agent 验证内容是否仍然准确：
   - 准确 → 更新 `updated` 日期，标记为已复核
   - 需修订 → 更新内容 + `updated` 日期
   - 已废弃 → 添加 `status: archived`，在文件顶部标注废弃原因
5. 复核完成后任务标记为 `done`

## 复核后标记规范

在文件 frontmatter 中增加：
```yaml
last_reviewed: 2026-03-04
review_result: confirmed | revised | archived
review_notes: "内容仍然准确" 或 "已更新XX部分"
```

## 归档策略

### 知识文件归档
- `status: archived` 的文件保留在原位置，但从 Dataview 查询中排除
- 排除方式：在 Dataview 查询中添加 `WHERE status != "archived"`

### 结构化输入归档（`_agent-system/intake/parsed/`）
- 当前阶段（文件 <50 个）：保持平铺在 `parsed/` 目录
- 中期阶段（文件 50-200 个）：按年月建子目录 `parsed/YYYY-MM/`
- 长期阶段（文件 >200 个）：已完成分派且超过 6 个月的文件归入 `parsed/archive/`

### 案例文件归档
- 案例文件不归档（永久保留，作为知识资产）
- 但超过 1 年未更新的案例可标记 `#历史案例`

## 在周复盘中的嵌入

在 `[[00-ceo/周复盘]]` 的每周复盘模板中，增加以下检查项：

```markdown
### 知识健康检查
- [ ] 查看知识地图中的过期文件数量
- [ ] 对高优先过期文件创建复核任务
- [ ] 确认上周复核任务是否已完成
```

## 与现有 SOP 的关系

- 本 SOP 是 `[[_agent-system/intake/知识答复自动回写SOP]]` 的下游：回写负责"写入"，本 SOP 负责"维护"
- 复核任务使用标准任务协议：`[[_agent-system/README]]`
- 归档状态的文件仍可通过 `[[_resources/知识地图]]` 查看

---

相关入口：
- [[_resources/知识地图]]
- [[_agent-system/intake/知识答复自动回写SOP]]
- [[00-ceo/周复盘]]
