---
tags: [系统, Git, 同步]
status: active
created: 2026-03-04
updated: 2026-03-04
---

# Git 同步 SOP

目标：在恰当时机自动同步到 GitHub，保证变更可追溯。

## 触发规则

### Must-Sync
1. 任务 `status: done` 且复盘完成
2. `00-ceo/ceo-memory/` 任一文件更新
3. 新增/修改 SOP 或模板文件
4. 修改任一 `CLAUDE.md`
5. 更新 `00-ceo/周复盘.md` 或 `00-ceo/季度OKR.md`

### Should-Sync
1. 知识回写批量更新
2. 单次会话变更文件数 >= 5
3. 用户结束当次会话

### Must-Not-Sync
1. 文档半成品
2. 含敏感信息未脱敏
3. `.obsidian/` 本地状态噪声文件

## 执行流程

1. Pre-Check
- `git status`
- 运行 pre-commit 校验脚本（提交时自动触发）

2. Commit
- 按主题分组暂存
- 提交信息遵循 `[[_agent-system/templates/Git提交信息模板]]`

3. Push
- `git pull --rebase origin master`
- `git push origin master`

4. Verify
- `git status` 应为干净或仅剩未纳入本次提交的变更
- 记录同步摘要到任务执行记录（如适用）

## 失败处理

- 冲突：先 `git rebase --abort`，再按可控方式合并冲突
- 内容错误：使用 `git revert <hash>` 回滚提交（禁止破坏性命令）
