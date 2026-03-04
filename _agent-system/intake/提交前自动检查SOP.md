---
tags: [系统, 输入处理, Git, 质量门槛]
status: active
created: 2026-03-04
updated: 2026-03-04
---

# 提交前自动检查 SOP

目标：在 `git commit` 前自动拦截不合规输入任务，确保“先结构化再分派、产品文件必回写产品卡”真正执行。

## 一次性安装

1. 启用仓库 hooks 路径：
   - `git config core.hooksPath .githooks`
2. 确认可执行权限：
   - `chmod +x .githooks/pre-commit _agent-system/scripts/precommit_validate_intake.py`

## 每次提交时自动检查

`pre-commit` 会自动执行：
- 脚本：`_agent-system/scripts/precommit_validate_intake.py`
- 触发范围：仅检查**本次暂存区**中有变更的 `_agent-system/tasks/*.md`

## 拦截规则

当任务文件同时满足 `input_type` 存在且 `status: done`，执行以下校验：

1. 必须有 `structured_output` 字段，且是有效 `[[链接]]`
2. `structured_output` 指向文件必须存在
3. 结构化文件必须包含：
   - `parse_status` in `complete|partial`
   - `source_file`
4. 若识别为产品文件（`is_product_file: true` 或源文件名命中产品关键词）：
   - 必须提供 `product_card_paths`
   - 目标产品卡必须存在
   - 产品卡 frontmatter 必须包含：
     - `official_name`
     - `category`
     - `status`
     - `tags`

## 失败处理

提交被拦截时，先按报错逐项补齐：

1. 修正文档字段
2. 重新 `git add` 相关文件
3. 再次 `git commit`

## 维护说明

- 如果规则变更，优先更新：
  - `_agent-system/intake/输入处理SOP.md`
  - `_agent-system/templates/输入任务-PDF解析模板.md`
  - `_agent-system/templates/输入任务-结构化输出模板.md`
  - `_agent-system/scripts/precommit_validate_intake.py`
