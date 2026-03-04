---
tags: [业务, 产品, Dataview]
status: active
created: 2026-03-03
updated: 2026-03-03
---

# 产品快速筛选（Dataview）

数据来源：`*/02-business-dev/knowledge/product-cards/`（自动适配主 Vault/子 Vault）

## 全部在售产品卡

```dataview
TABLE official_name as "产品", category as "类别", source_url as "官网链接", tags as "标签"
FROM ""
WHERE contains(file.path, "02-business-dev/knowledge/product-cards/") AND status = "active"
SORT category asc, official_name asc
```

## 医疗

```dataview
TABLE official_name as "产品", category as "类别", source_url as "官网链接"
FROM ""
WHERE contains(file.path, "02-business-dev/knowledge/product-cards/") AND contains(tags, "医疗")
SORT official_name asc
```

## 健康其他（未归入医疗/危疾/意外）

```dataview
TABLE official_name as "产品", source_url as "官网链接", tags as "标签"
FROM ""
WHERE contains(file.path, "02-business-dev/knowledge/product-cards/")
  AND contains(tags, "健康")
  AND !contains(tags, "医疗")
  AND !contains(tags, "危疾")
  AND !contains(tags, "意外")
SORT official_name asc
```

## 危疾

```dataview
TABLE official_name as "产品", source_url as "官网链接"
FROM ""
WHERE contains(file.path, "02-business-dev/knowledge/product-cards/") AND contains(tags, "危疾")
SORT official_name asc
```

## 人寿

```dataview
TABLE official_name as "产品", source_url as "官网链接"
FROM ""
WHERE contains(file.path, "02-business-dev/knowledge/product-cards/") AND contains(tags, "人寿")
SORT official_name asc
```

## 储蓄 / 退休

```dataview
TABLE official_name as "产品", tags as "标签", source_url as "官网链接"
FROM ""
WHERE contains(file.path, "02-business-dev/knowledge/product-cards/") AND (contains(tags, "储蓄") OR contains(tags, "退休"))
SORT official_name asc
```

## 团险 / MPF / ORSO

```dataview
TABLE official_name as "产品", category as "类别", source_url as "官网链接"
FROM ""
WHERE contains(file.path, "02-business-dev/knowledge/product-cards/") AND (contains(tags, "团险") OR contains(tags, "MPF") OR contains(tags, "ORSO"))
SORT category asc, official_name asc
```

## 投资

```dataview
TABLE official_name as "产品", source_url as "官网链接"
FROM ""
WHERE contains(file.path, "02-business-dev/knowledge/product-cards/") AND contains(tags, "投资")
SORT official_name asc
```

## 一般保险

```dataview
TABLE official_name as "产品", source_url as "官网链接"
FROM ""
WHERE contains(file.path, "02-business-dev/knowledge/product-cards/") AND contains(tags, "一般保险")
SORT official_name asc
```
