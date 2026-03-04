---
tags: [系统, 任务治理, 复盘]
status: active
created: 2026-03-04
updated: 2026-03-04
---

# 任务复盘 SOP

目标：任务完成后把经验沉淀到 CEO 记忆系统，形成闭环。

## 触发条件

- 任务状态拟从 `review` 或 `in_progress` 变为 `done`
- 或用户要求“复盘此任务”

## 执行步骤

### 1. 验收检查
- [ ] `deliverable` 可访问且满足交付标准
- [ ] 执行记录完整，关键决策可追溯

### 2. 用户反馈采集
- [ ] 记录 `review_score`（high/medium/low）
- [ ] 记录 `review_notes`

### 3. 经验提炼
- [ ] 识别成功做法
- [ ] 识别返工/阻塞原因
- [ ] 形成下一次分派规则

### 4. 记忆回写
- [ ] 更新 `[[00-ceo/ceo-memory/分派经验]]`
- [ ] 更新 `[[00-ceo/ceo-memory/反馈记录]]`
- [ ] 任务单中 `memory_updated: true`

### 5. 关闭
- [ ] 任务 `status: done`
- [ ] 在执行记录中写入复盘结论

### 6. Git 同步
- [ ] 执行 `[[_agent-system/intake/Git同步SOP]]`
- [ ] 若命中 must-sync，完成 commit + push
