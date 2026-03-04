---
tags: [系统, 输入处理, Agent协作]
status: active
created: 2026-03-03
---

# 输入处理 SOP（Intake）

目标：任何新输入（不分格式）都先产出结构化 Markdown，再派发给部门 Agent。

## 硬规则

1. 先结构化，再分派：任何输入必须先写入 `_agent-system/intake/parsed/` 后才能创建下游任务。
2. 原件留档：原始输入统一留在 `_agent-system/intake/raw/`，结构化文件必须回链原件。
3. 单次解析，多次引用：同一输入只解析一次，各部门只引用结构化文件，不重复解析。
4. 产品文件强制回写产品卡：若识别为产品资料（尤其 PDF），必须更新 `02-business-dev/knowledge/product-cards/` 对应产品卡。

## 总流程

1. 识别输入类型：`pdf` / `customer_info` / `image` / `voice` / `webpage` / `other`
2. 识别是否命中专题关键词（见“专题路由规则”）
3. 原件归档到 `_agent-system/intake/raw/`（必要时同时生成文本与预览）
4. 创建 Intake 任务（放到 `_agent-system/tasks/`）
5. 先按模板生成结构化 Markdown：`[[_agent-system/templates/输入任务-结构化输出模板]]`
6. 通过质量门槛后，再创建二级任务分派到部门
7. 在 `[[_agent-system/inbox]]` 跟踪状态并回收交付

## 专题路由规则

命中以下关键词时，默认路由到 CIES 专题：
- `CIES`
- `新资本投资者入境计划`
- `香港新资本投资计划`
- `投资移民`
- `净资产3000万`

执行动作：
1. 结构化文件正文增加“专题归属：`[[_agent-system/topics/香港新资本投资者入境计划-专题总控]]`”
2. Intake 任务 `tags` 必须包含 `投资移民` 或 `CIES`
3. 下游分派优先使用专题既有入口（业务/营销/数据/客服）而非新建散落文档

## PDF 输入流程

1. 用模板：`[[_agent-system/templates/输入任务-PDF解析模板]]`
2. 必做结构化输出（先于任何分派）：
- 文档摘要（目标、结论、行动项）
- 结构化字段（日期、客户名、产品、金额、风险点）
- 页码定位（便于回查）
 - 全量覆盖文件（逐页全文，覆盖原 PDF 所有页面）
3. 若为产品文件，先更新对应产品卡后再分派（见“产品文件专项规则”）。
4. 根据用途分派：
- 销售方案相关 -> `business_dev`
- 保单服务/理赔相关 -> `customer_service`
- 内容提炼 -> `content_marketing`
- 指标统计 -> `data_analytics`

## 客户信息输入流程

1. 用模板：`[[_agent-system/templates/输入任务-客户信息模板]]`
2. 首先更新/创建：
- `[[03-customer-service/clients/_客户总览]]`
- 对应客户档案 `03-customer-service/clients/[客户名].md`
- `[[02-business-dev/客户Pipeline]]`
3. 先生成结构化输入文件，再自动拆分后续任务：
- 需求评估 -> `business_dev`
- 服务待办（检视/续保/理赔）-> `customer_service`
- 跟进节奏与KPI -> `data_analytics`

## 结构化 Markdown 标准

统一输出文件放在 `_agent-system/intake/parsed/`，frontmatter 至少包含：

```yaml
source_type: pdf | customer_info | image | voice | webpage | other
source_file: "[[_agent-system/intake/raw/原始文件]]"
parse_status: complete | partial | failed
parsed_by: ceo
parsed_date: YYYY-MM-DD
dispatch_to: [business_dev]
is_product_file: true | false
product_card_paths: ["[[02-business-dev/knowledge/product-cards/xxx]]"]
full_content_output: "[[_agent-system/intake/parsed/PDF-full-YYYYMMDD-xxx]]"
```

正文至少包含：
- 摘要
- 关键字段
- 待确认项
- 分派建议
- 回写位置
- （可选）产品识别结果

## 产品文件专项规则

1. 输入被识别为产品资料时，必须定位或新建对应产品卡：
- 路径：`02-business-dev/knowledge/product-cards/`
2. 回写后必须保证 Dataview 可检索字段完整：
- `official_name` / `category` / `status` / `tags`
3. 若产品名无法匹配，先建“待核名”临时卡并标注 `blocked`，等待 CEO 确认。
4. 若口径冲突（官网 vs 文件），结构化文件并列记录证据并标记待裁决。

## 质量门槛

- 没有 frontmatter 的输入任务不进入执行
- `deliverable` 必须是 `[[双向链接]]`
- 有信息缺口时状态改为 `blocked`，并列明缺什么
- 未生成结构化 Markdown，不得创建下游分派任务
- 未生成 PDF 全量覆盖文件（逐页全文），不得将 PDF 输入任务标记为 `done`
- 产品文件未回写产品卡，不得标记输入任务为 `done`
