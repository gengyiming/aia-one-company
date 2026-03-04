---
tags: [系统, 知识管理, SOP, 自动回写]
status: active
created: 2026-03-04
updated: 2026-03-04
---

# 知识答复自动回写 SOP

目标：用户提出知识性问题时，回答后在同一轮自动把结论沉淀到资料库对应位置。

## 触发条件（满足其一即触发）

- 产品、客户画像、销售策略、流程、数据、管理方法等知识问答
- “为什么/怎么做/适合谁/如何比较/有哪些风险”这类可复用问题
- 对现有知识库内容进行补充、纠错、澄清

## 默认规则

- 默认开启自动回写，不需要用户额外提醒。
- 仅当用户明确说“这次不要写入资料库”时跳过。
- 回写与答复必须在同一轮完成。

## 回写位置路由

1. 产品与客户策略：
- 主文件：`02-business-dev/knowledge/`
- 产品卡：`02-business-dev/knowledge/product-cards/`

2. 招募与团队培养：
- `01-recruitment/`（手册、Pipeline、scripts、templates、cases）

3. 客户服务与保单维护：
- `03-customer-service/`（clients、scripts、calendar）

4. 内容营销方法：
- `04-content-marketing/`（营销手册、topics、templates、library）

5. 指标与分析方法：
- `05-data-analytics/`（tracking、业绩仪表盘、数据管理手册）

6. 经营与组织管理：
- `00-ceo/`（公司全景、季度OKR、周复盘、决策日志、团队管理总控面板）

## 执行动作

1. 先给用户可执行答案（简洁、合规）。
2. 判断“更新现有文件”还是“新建专题笔记”。
3. 写入结构化内容：
- 结论
- 适用人群/场景
- 不适用边界或风险提醒
- 关键问题清单（如适用）
- 参考来源与核对日期（如适用）
4. 若来源是产品文件（尤其 PDF），必须回写对应产品卡：
- 路径：`02-business-dev/knowledge/product-cards/`
- 不存在则先新建，再补充索引与 `[[双向链接]]`
- 校验 Dataview 字段：`official_name` / `category` / `status` / `tags`
5. 补充 `[[双向链接]]`，确保可从相关页面找到。
6. 更新 frontmatter 中 `updated` 日期。
7. 回写完成后按 `[[_agent-system/intake/Git同步SOP]]` 标记本轮是否命中同步触发条件。

## 质量标准

- 不只记录结论，还要记录适用边界与合规提醒。
- 同类问题优先沉淀到同一位置，避免重复散落。
- Dataview 依赖字段（如 tags/status/category/source_url）不得破坏。
