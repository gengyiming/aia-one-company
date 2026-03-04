---
tags: [CEO, 战略, 系统架构, 改进方案]
status: 进行中
created: 2026-03-04
updated: 2026-03-04
---

# 系统改进方案：CEO 单一入口 + 记忆闭环 + 任务分派治理

> 目标：用户只与 CEO Agent 对话 → CEO 越用越懂用户 → CEO 精准分派 → 部门执行 → 结果回传 → 反哺记忆

---

## A. 当前结构梳理（As-Is）

### A1. 架构总览

```
用户 ──可直接进入──┬── 根目录 CLAUDE.md（COO 角色）
                  ├── 00-ceo/CLAUDE.md（CEO 助理角色）
                  ├── 01-recruitment/CLAUDE.md
                  ├── 02-business-dev/CLAUDE.md
                  ├── 03-customer-service/CLAUDE.md
                  ├── 04-content-marketing/CLAUDE.md
                  └── 05-data-analytics/CLAUDE.md
```

**当前交互方式**：用户 `cd` 到哪个目录，就激活哪个部门 Agent。没有强制单一入口。

### A2. 已建成机制

| 机制 | 文件 | 成熟度 | 说明 |
|------|------|--------|------|
| 多Agent协作协议 | `_agent-system/README.md` | ★★★☆ | 有完整任务流转：todo→done，有模板 |
| Intake SOP | `_agent-system/intake/输入处理SOP.md` | ★★★☆ | PDF/客户信息标准化流程清晰 |
| 知识自动回写 | `_agent-system/intake/知识答复自动回写SOP.md` | ★★★★ | 触发条件+路由+质量标准完整 |
| 任务看板 | `_agent-system/inbox.md` | ★★★☆ | Dataview 多维度看板已搭建 |
| 产品知识库 | `02-business-dev/knowledge/` | ★★★★★ | 100+ 产品卡，5大分类 |
| CEO 总控面板 | `00-ceo/团队管理总控面板.md` | ★★★☆ | 快速入口+Dataview看板已搭建 |
| OKR/复盘/决策 | `00-ceo/` | ★☆☆☆ | 全部空模板，无实际数据 |

### A3. 已有实际任务（7笔）

```
TASK-20260303-001  营销→业务 线索交付          status: todo
TASK-20260303-101  CEO→业务 投资移民筛查清单    status: done ✓
TASK-20260303-102  CEO→营销 投资移民解读栏目    status: done ✓
TASK-20260303-103  CEO→数据 投资移民线索追踪    status: done ✓
TASK-20260303-PDF-001 CEO→数据 计划规则PDF      status: done ✓
TASK-20260303-PDF-002 CEO→数据 完整指南PDF      status: done ✓
TASK-20260304-PDF-003 CEO→数据 环宇盈活PDF      status: done ✓
```

---

## B. 关键问题诊断（按严重度排序）

### B1. 🔴 严重｜无 CEO 单一入口的硬性治理

**现状**：根目录 CLAUDE.md 写的是"用户 cd 进入对应部门目录后自动切换"，意味着用户可以绕过 CEO 直接与任何部门对话。

**后果**：
- 部门 Agent 接到的指令没有经过 CEO 上下文过滤，可能与全局优先级冲突
- 任务不经 `_agent-system/tasks/` 留痕，无法追溯和复盘
- CEO 记忆系统无法捕获用户与部门的直接对话内容

### B2. 🔴 严重｜CEO 没有结构化记忆系统

**现状**：`00-ceo/CLAUDE.md` 定义了 CEO 管理哪些文件，但没有"用户画像/偏好/决策风格"的持久记忆机制。

**后果**：
- 每次新会话，CEO Agent 从零开始理解用户
- 无法积累"用户说过不想做XXX""用户偏好YYY风格"等关键偏好
- "越用越懂"无从实现

### B3. 🟡 中等｜任务分派缺少质量标准与预检

**现状**：任务单模板有 `from_agent`/`to_agent`/`deliverable`，但没有分派前的"预检清单"（该不该派？派给谁？输入够不够？）。

**后果**：
- 可能出现无效任务（信息不全就派出）
- 可能派错部门（例如需要客服配合的任务只派了业务）
- 没有"CEO 审批"环节，缺乏治理

### B4. 🟡 中等｜任务完成后无结构化复盘反馈

**现状**：任务 `done` 后就结束，没有"从这次任务中学到什么→回写 CEO 记忆"的闭环。

**后果**：
- 同样的分派错误可能反复出现
- 用户偏好（比如"这个任务做得好，以后都这样做"）无处沉淀
- OKR/周复盘与任务系统断裂（全是空模板）

### B5. 🟢 轻微｜部门间直接协作缺少 CEO 可见性

**现状**：`TASK-20260303-001` 是 `content_marketing → business_dev`，CEO 不在 `from_agent` 中。

**后果**：
- CEO 看板能看到，但没有主动通知/审批机制
- 部门间自行建任务若不通知 CEO，可能产生优先级冲突

### B6. 🟢 轻微｜OKR/周复盘/决策日志全空

**现状**：三个文件均为空模板。

**后果**：
- CEO Agent 做决策时无历史数据参考
- 周复盘和目标进度追踪形同虚设

---

## C. 目标架构（To-Be）

### C1. 分层架构图

```
                        ┌─────────────────────┐
                        │       用  户         │
                        └────────┬────────────┘
                                 │ 唯一入口
                                 ▼
                 ┌───────────────────────────────┐
                 │         CEO Agent              │
                 │  ┌───────────────────────┐     │
                 │  │   用户记忆系统         │     │
                 │  │  (偏好/风格/约束/历史) │     │
                 │  └───────────────────────┘     │
                 │  ┌───────────────────────┐     │
                 │  │   任务路由引擎         │     │
                 │  │  (预检→分派→跟踪→复盘) │     │
                 │  └───────────────────────┘     │
                 └──┬────┬────┬────┬────┬────────┘
                    │    │    │    │    │
          ┌────────┐│┌───┐│┌───┐│┌───┐│┌───────┐
          │招募    │││业务│││客服│││营销│││数据   │
          │Agent   │││Agent│││Agent│││Agent│││Agent  │
          └───┬────┘│└─┬─┘│└─┬─┘│└─┬─┘│└──┬────┘
              │      │  │   │  │   │  │   │  │
              └──────┴──┴───┴──┴───┴──┴───┴──┘
                         │
                    ┌────▼─────┐
                    │ 执行结果  │
                    │ 回传CEO   │
                    │ → 更新记忆 │
                    └──────────┘
```

### C2. 核心流转（单次交互）

```
用户输入
  │
  ▼
CEO Agent 接收
  │
  ├─ 1. 读取 [[00-ceo/ceo-memory/用户画像.md]]  ← 了解用户
  ├─ 2. 意图识别（知识问答 / 任务指令 / 闲聊 / 复盘）
  │
  ├─ 若「知识问答」→ CEO 直接回答 + 自动回写
  ├─ 若「闲聊/确认」→ CEO 直接回答
  │
  ├─ 若「任务指令」→ 进入分派流程：
  │   ├─ a. 预检：输入是否完整？优先级如何？
  │   ├─ b. 路由：匹配最佳部门（可多部门协作）
  │   ├─ c. 生成任务单 → _agent-system/tasks/
  │   ├─ d. 向用户确认分派摘要
  │   └─ e. 触发部门执行
  │
  └─ 若「复盘/报告」→ 汇总各部门数据 → 写入周复盘/OKR

部门完成 → 回传 CEO → CEO 验收
  │
  ├─ 更新任务状态
  ├─ 提取经验 → 更新用户画像/决策偏好
  └─ 通知用户结果
```

### C3. CEO 记忆系统架构

```
00-ceo/ceo-memory/
├── 用户画像.md            ← 持续更新的用户理解
├── 决策偏好.md            ← 用户的决策风格与约束
├── 分派经验.md            ← 哪类任务怎么分效果最好
└── 反馈记录.md            ← 用户对交付结果的满意度记录
```

---

## D. 可执行改进方案

### Phase 1: 基础治理（0-7 天）

#### D1.1 建立 CEO 单一入口治理规则

**动作**：修改根目录 `CLAUDE.md`

**具体改动**：

在 `## 如何切换部门` 部分替换为：

```markdown
## CEO 单一入口（核心治理规则）

**硬规则：用户的所有输入必须先经过 CEO Agent 处理。**

1. 用户始终在根目录或 `00-ceo/` 与 CEO Agent 对话。
2. CEO Agent 负责意图识别、记忆更新、任务分派。
3. 部门 Agent 仅通过任务单 `_agent-system/tasks/` 接收工作。
4. 用户不直接 `cd` 进部门目录操作（除非 CEO 明确建议）。

当 CEO 需要调用部门能力时：
- 读取部门 CLAUDE.md 了解其职责边界
- 读取部门知识库获取专业内容
- 通过任务单正式分派需要执行的工作
```

#### D1.2 创建 CEO 记忆目录与初始文件

**动作**：创建 `00-ceo/ceo-memory/` 目录及 4 个文件

**文件 1：`00-ceo/ceo-memory/用户画像.md`**

```yaml
---
tags: [CEO, 记忆, 用户画像]
status: active
created: 2026-03-04
updated: 2026-03-04
version: 1
---
```

```markdown
# 用户画像

> CEO Agent 持续维护。每次对话后自动更新。

## 基本信息
- 角色：AIA Hong Kong 理财顾问
- 团队阶段：（待确认）
- MDRT 状态：（待确认）

## 工作偏好
<!-- 格式：- [偏好描述] (来源: YYYY-MM-DD 对话/任务) -->

## 沟通风格
<!-- 格式：- [观察] (来源: YYYY-MM-DD) -->

## 约束与红线
<!-- 格式：- [约束描述] (来源: YYYY-MM-DD) -->

## 当前关注重点
<!-- 格式：- [重点] (来源: YYYY-MM-DD) — 有效期至 YYYY-MM-DD -->

## 更新日志
<!-- 格式：### YYYY-MM-DD — 新增/修改了什么 -->
```

**文件 2：`00-ceo/ceo-memory/决策偏好.md`**

```yaml
---
tags: [CEO, 记忆, 决策偏好]
status: active
created: 2026-03-04
updated: 2026-03-04
version: 1
---
```

```markdown
# 决策偏好

> 记录用户做决策时的规律性模式，帮助 CEO Agent 更精准地建议和分派。

## 风险偏好
<!-- 保守/中等/积极？有无具体表述？ -->

## 时间偏好
<!-- 喜欢快速行动还是谨慎评估？对deadline的态度？ -->

## 信息偏好
<!-- 喜欢详细报告还是一页摘要？偏好数据还是叙事？ -->

## 审批偏好
<!-- 哪些事需要过问？哪些可以自动执行？ -->

## 已确认的决策规则
<!-- 格式：- 规则描述 (来源: YYYY-MM-DD，决策场景) -->

## 更新日志
```

**文件 3：`00-ceo/ceo-memory/分派经验.md`**

```yaml
---
tags: [CEO, 记忆, 分派, 复盘]
status: active
created: 2026-03-04
updated: 2026-03-04
version: 1
---
```

```markdown
# 分派经验库

> 从每次任务复盘中提炼的分派规律。帮助 CEO Agent 做更好的任务路由。

## 分派规则（已验证）

<!-- 格式：
### 场景：[任务类型]
- 最佳分派：[to_agent]
- 需 cc：[cc_agents]
- 关键输入：[必须提供什么]
- 注意事项：[踩过的坑]
- 来源：[task_id] (YYYY-MM-DD)
-->

## 常见失败模式
<!-- 格式：- [失败描述] → 改进措施 (来源: task_id) -->

## 更新日志
```

**文件 4：`00-ceo/ceo-memory/反馈记录.md`**

```yaml
---
tags: [CEO, 记忆, 反馈, 满意度]
status: active
created: 2026-03-04
updated: 2026-03-04
version: 1
---
```

```markdown
# 用户反馈记录

> 记录用户对 Agent 交付结果的反馈，用于改进服务质量。

## 反馈汇总

<!-- 格式：
### YYYY-MM-DD — [task_id 或 对话主题]
- 满意度：高/中/低
- 具体反馈：[用户原话或总结]
- 改进动作：[基于反馈做了什么调整]
- 已回写：[更新了哪个记忆文件]
-->
```

#### D1.3 在 CEO CLAUDE.md 中增加记忆读写指令

**动作**：修改 `00-ceo/CLAUDE.md`，在 `## 工作指令` 后新增：

```markdown
## CEO 记忆系统（每次对话必执行）

### 对话开始时
1. 读取 `[[00-ceo/ceo-memory/用户画像]]` — 了解用户当前状态
2. 读取 `[[00-ceo/ceo-memory/决策偏好]]` — 校准沟通和建议风格

### 对话过程中
- 捕捉用户新偏好、约束、反馈 → 标记为待更新
- 用户表达满意/不满 → 立即记录到 `[[00-ceo/ceo-memory/反馈记录]]`

### 对话结束前
- 把本次捕捉的新信息更新到对应记忆文件
- 更新 frontmatter 中 `updated` 和 `version`（version +1）
- 若有分派经验 → 更新 `[[00-ceo/ceo-memory/分派经验]]`
```

#### D1.4 填充 OKR 首版数据

**动作**：与用户一次对话完成 `季度OKR.md` 的首次填充。

**CEO Agent 应主动询问**：
- Q1 FYP 目标金额
- Case Count 目标
- MDRT/COT/TOT 目标
- 增员目标人数
- 续保率底线
- 内容发布频率目标

---

### Phase 2: 分派治理 + 闭环（8-30 天）

#### D2.1 新增任务分派预检 SOP

**动作**：创建 `_agent-system/intake/任务分派预检SOP.md`

```yaml
---
tags: [系统, SOP, 任务分派, 预检]
status: active
created: 2026-03-04
---
```

```markdown
# 任务分派预检 SOP

> CEO Agent 在创建任务单之前必须过这个清单。

## 预检清单（全部通过才可创建任务单）

### 1. 必要性检查
- [ ] 这个任务是否对当前 OKR 有直接贡献？
- [ ] 是否已有类似任务在进行中？（查 `[[_agent-system/inbox]]`）
- [ ] 是否可以 CEO 直接回答而不需要分派？

### 2. 输入完整性
- [ ] 背景信息是否足够部门 Agent 独立执行？
- [ ] 参考资料是否已转为 `[[双向链接]]`？
- [ ] 如有依赖任务，其状态是否为 `done`？

### 3. 路由判断
- [ ] 主执行部门是否明确？（查 `[[_agent-system/README]]` Agent注册表）
- [ ] 是否需要 cc 其他部门？
- [ ] 是否参考 `[[00-ceo/ceo-memory/分派经验]]` 中的已验证规则？

### 4. 验收标准
- [ ] 交付标准是否可量化/可检查？
- [ ] 截止日期是否合理？
- [ ] deliverable 格式是否为 `[[双向链接]]`？

### 5. 用户确认
- [ ] 已向用户展示分派摘要（任务、部门、截止日、交付物）
- [ ] 用户确认或调整后再创建任务单
```

#### D2.2 修改任务单模板——增加复盘字段

**动作**：修改 `_agent-system/templates/任务单模板.md`

在 frontmatter 中新增字段：

```yaml
review_score: ""         # 用户满意度: high/medium/low
review_notes: ""         # 用户反馈摘要
memory_updated: false    # 是否已回写CEO记忆
```

在正文末尾新增：

```markdown
## 复盘（任务完成后由 CEO Agent 填写）

### 用户满意度
- 评分：high / medium / low
- 用户反馈：

### 经验提炼
- 分派是否合理？
- 交付质量如何？
- 下次可改进的点：

### 记忆回写
- [ ] 已更新 `[[00-ceo/ceo-memory/分派经验]]`
- [ ] 已更新 `[[00-ceo/ceo-memory/用户画像]]`（如有新发现）
- [ ] 已更新 `[[00-ceo/ceo-memory/反馈记录]]`
```

#### D2.3 新增任务复盘 SOP

**动作**：创建 `_agent-system/intake/任务复盘SOP.md`

```markdown
---
tags: [系统, SOP, 复盘, 闭环]
status: active
created: 2026-03-04
---

# 任务复盘 SOP

> 每个任务 `status: done` 后，CEO Agent 必须执行此流程。

## 触发条件
- 任务 `status` 变为 `done`
- 或用户主动说"复盘/回顾 TASK-XXX"

## 执行步骤

### 1. 验收检查
- 逐条核对任务单中的「交付标准」
- 打开 `deliverable` 链接确认内容存在且完整
- 若不达标 → status 改回 `in_progress`，在执行记录中写明缺什么

### 2. 用户反馈采集
- 向用户简报任务结果（一句话 + 交付物链接）
- 询问满意度（high/medium/low）
- 记录用户的具体反馈

### 3. 经验提炼
- 分派路由是否最优？（对比 `[[00-ceo/ceo-memory/分派经验]]`）
- 输入资料是否充足？有无信息缺口导致返工？
- 交付时效是否合理？

### 4. 记忆回写
- 更新 `[[00-ceo/ceo-memory/分派经验]]`：新增或修正分派规则
- 更新 `[[00-ceo/ceo-memory/用户画像]]`：若发现新偏好/约束
- 更新 `[[00-ceo/ceo-memory/反馈记录]]`：记录本次反馈
- 在任务单中勾选「记忆回写」checklist

### 5. 关闭
- 任务单 `review_score` / `review_notes` / `memory_updated` 填写完毕
- 若满意度为 `low`，自动创建改进任务
```

#### D2.4 建立周复盘自动化流程

**动作**：在 `00-ceo/CLAUDE.md` 的「周复盘」指令中增加：

```markdown
### 「周复盘」（增强版）
1. 汇总本周所有 `status: done` 的任务（从 `_agent-system/tasks/` 读取）
2. 汇总用户反馈记录（从 `[[00-ceo/ceo-memory/反馈记录]]` 读取本周条目）
3. 读取 `[[05-data-analytics/业绩仪表盘]]` 获取数据
4. 撰写结构化复盘追加到 `周复盘.md`：
   - 本周完成任务清单（含满意度）
   - 各部门亮点
   - 发现的问题与改进措施
   - 记忆系统本周更新摘要
   - 下周优先级排序
5. 更新 `季度OKR.md` 对应周的进度
```

#### D2.5 部门间协作审批机制

**动作**：修改 `_agent-system/README.md`，在「协作协议」部分新增：

```markdown
## 部门间协作规则（新增）

1. 部门间直接创建的任务，`cc_agents` 必须包含 `ceo`。
2. CEO Agent 在看到 cc 的任务时，判断是否需要介入或调整优先级。
3. 任何任务的 `priority: high` 必须经 CEO Agent 确认。
4. 部门间协作任务完成后，同样走复盘 SOP。
```

---

### Phase 3: 智能化 + 深度记忆（31-90 天）

#### D3.1 CEO 记忆版本化与定期整理

**动作**：创建 `_agent-system/intake/记忆维护SOP.md`

```markdown
---
tags: [系统, SOP, 记忆, 维护]
status: active
created: 2026-03-04
---

# CEO 记忆维护 SOP

## 每周维护（周复盘时顺带执行）
1. 审查 `用户画像.md` — 移除过时信息，标注信息新鲜度
2. 审查 `分派经验.md` — 合并重复规则，删除过时条目
3. 检查 `当前关注重点` — 过期项标记为历史
4. `version` 字段 +1，`updated` 更新

## 每月深度整理
1. 统计本月反馈分布（high/medium/low 占比）
2. 提炼本月 Top3 用户偏好变化
3. 从分派经验中归纳"部门能力矩阵"更新
4. 在 `决策偏好.md` 中新增或修正规则
5. 生成一段"本月 CEO 对用户的理解更新摘要"追加到 `用户画像.md`

## 季度回顾
1. 将季度记忆摘要归档到 `00-ceo/ceo-memory/archive/YYYY-QX-摘要.md`
2. 精简主文件，只保留当前有效信息
3. 对照 OKR 结果，验证记忆系统是否帮助了更好的决策
```

#### D3.2 智能意图路由规则

**动作**：在 `00-ceo/CLAUDE.md` 新增路由决策树

```markdown
## 意图识别与路由决策树

用户输入 →

### 类型1: 知识问答
关键词：为什么/怎么做/什么是/如何比较/有哪些
→ CEO 直接回答 + 知识回写 SOP
→ 若涉及专业深度超出CEO范围 → 读取对应部门knowledge目录辅助回答

### 类型2: 任务指令
关键词：帮我做/创建/分析/整理/跟进/生成
→ 走分派预检 SOP → 创建任务单 → 分派

### 类型3: 信息查询
关键词：目前/进度/状态/有多少
→ CEO 读取相关文件直接回答（看板/Pipeline/OKR/记忆文件）

### 类型4: 复盘与决策
关键词：复盘/总结/回顾/决定/选择
→ 走复盘流程或决策分析流程

### 类型5: 闲聊与确认
→ CEO 直接回应，捕捉可能的隐含偏好
```

#### D3.3 部门能力矩阵（辅助路由）

**动作**：创建 `_agent-system/部门能力矩阵.md`

```markdown
---
tags: [系统, 路由, Agent能力]
status: active
created: 2026-03-04
---

# 部门能力矩阵

> CEO Agent 分派任务时查阅此矩阵，确定最佳执行方。

| 任务类型 | 主执行 | 协作 | 典型交付物 |
|----------|--------|------|-----------|
| 客户需求分析 | business_dev | customer_service | 方案建议书 |
| 产品方案设计 | business_dev | — | 产品组合+卖点话术 |
| 客户跟进策略 | business_dev | customer_service, data_analytics | 跟进计划+Pipeline更新 |
| 新客户建档 | customer_service | business_dev, data_analytics | 客户档案+Pipeline条目 |
| 续保/理赔服务 | customer_service | — | 服务记录+待办更新 |
| 年度保单检视 | customer_service | business_dev | 检视报告+加保建议 |
| 内容创作 | content_marketing | business_dev | 内容稿件 |
| 选题策划 | content_marketing | data_analytics | 内容日历更新 |
| 线索交付 | content_marketing | business_dev | Pipeline新线索 |
| 业绩数据分析 | data_analytics | — | 仪表盘/报表 |
| MDRT进度追踪 | data_analytics | — | 差距分析+行动建议 |
| 活动量分析 | data_analytics | — | 活动量报表+改进建议 |
| 候选人评估 | recruitment | — | 评估报告 |
| Career Talk策划 | recruitment | content_marketing | 策划方案 |
| 新人培训计划 | recruitment | — | 30-60-90天计划 |
| PDF文件解析 | data_analytics | （按内容路由） | 结构化解析结果 |
| 投资移民咨询 | business_dev | customer_service, data_analytics | 资格筛查+方案 |
```

#### D3.4 增强 Claude Code Memory 与 CEO 记忆的同步

**动作**：在 `/Users/gengyiming/.claude/projects/...memory/MEMORY.md` 中增加：

```markdown
## CEO 记忆系统关键路径
- 用户画像: 00-ceo/ceo-memory/用户画像.md
- 决策偏好: 00-ceo/ceo-memory/决策偏好.md
- 分派经验: 00-ceo/ceo-memory/分派经验.md
- 反馈记录: 00-ceo/ceo-memory/反馈记录.md
- 每次对话开始时应读取用户画像和决策偏好
```

---

## E. 关键机制设计

### E1. CEO 记忆系统

```
触发 → 来源 → 写入目标 → 格式

对话中发现偏好    → 用户发言      → 用户画像.md    → "- [偏好] (来源: 日期)"
用户做出选择      → 决策过程      → 决策偏好.md    → "- 规则描述 (场景)"
任务完成复盘      → 任务单review  → 分派经验.md    → 场景/分派/注意事项
用户表达满意/不满 → 用户反馈      → 反馈记录.md    → 日期/任务/满意度/改进
周复盘整理        → 全周汇总      → 用户画像.md    → "当前关注重点"更新
月度整理          → 月度统计      → 决策偏好.md    → 规则合并精简
```

**版本控制**：每个记忆文件 frontmatter 中有 `version` 字段，每次更新 +1。`updated` 记录最后更新日期。

**冲突处理**：新信息与旧记忆矛盾时，保留两条并标注 `[待确认]`，下次对话时向用户求证。

### E2. 任务分发规则

```
用户输入 "帮我做XXX"
      │
      ▼
  CEO 意图识别
      │
      ▼
  读取分派经验 → 有匹配规则？
      │                │
     是               否
      │                │
      ▼                ▼
  套用已验证规则    查部门能力矩阵
      │                │
      └────┬───────────┘
           ▼
      分派预检 SOP（5项全过）
           │
           ▼
      向用户展示分派摘要
           │
      用户确认？──否→ 调整后重新展示
           │
          是
           ▼
      创建任务单 → 写入 _agent-system/tasks/
           │
           ▼
      部门执行 → 更新执行记录
           │
           ▼
      status: done → CEO 复盘 SOP
           │
           ▼
      回写记忆 → 关闭任务
```

### E3. 反馈闭环

| 环节 | 触发 | 动作 | 沉淀位置 |
|------|------|------|----------|
| 即时反馈 | 用户说"不错/不行/改改" | 立即记录 | 反馈记录.md |
| 任务复盘 | 任务 done | 走复盘 SOP | 任务单+分派经验+反馈记录 |
| 周复盘 | 每周五或用户发起 | 汇总全周 | 周复盘.md + 用户画像.md |
| 月度整理 | 每月最后一周 | 精简合并 | 全部记忆文件 |
| 季度归档 | 季度结束 | 归档+精简 | archive/ + OKR |

### E4. 升级机制

| 等级 | 条件 | 处理方式 |
|------|------|----------|
| L0 正常 | 任务在 due 前完成，满意度 high | 正常关闭 |
| L1 关注 | 任务接近 due 未完成 | CEO 主动提醒用户，询问是否调整 |
| L2 预警 | 任务 blocked 超过2天 | CEO 诊断阻塞原因，提出解决方案 |
| L3 升级 | 满意度连续2次 low | CEO 触发系统改进任务，检查根因 |
| L4 系统级 | 用户明确说"系统不好用" | 暂停执行，全面复盘架构，输出改进方案 |

---

## F. KPI 与看板

### F1. 可量化指标（12项）

| # | 指标 | 计算方式 | 目标值 | 数据来源 |
|---|------|----------|--------|----------|
| 1 | CEO 入口使用率 | 通过CEO分派的任务数 / 总任务数 | 100% | `_agent-system/tasks/` 中 `from_agent` 字段 |
| 2 | 任务完成率 | `done` 任务数 / 总任务数 | ≥85% | inbox Dataview |
| 3 | 任务准时率 | 在 `due` 前完成的比例 | ≥80% | `done` 日期 vs `due` |
| 4 | 用户满意度均值 | high=3 / medium=2 / low=1 的加权平均 | ≥2.5 | `review_score` 字段 |
| 5 | 记忆更新频率 | 记忆文件 `version` 增长 / 周 | ≥3次/周 | 记忆文件 frontmatter |
| 6 | 知识回写率 | 实际回写次数 / 知识问答次数 | ≥90% | 知识文件 `updated` 变化 |
| 7 | 分派预检通过率 | 首次预检通过 / 总分派次数 | ≥70%（逐步提升） | CEO 分派日志 |
| 8 | 任务返工率 | 从 done 退回 in_progress 的次数 / 总完成数 | ≤10% | 任务执行记录 |
| 9 | 周复盘完成率 | 实际写入周数 / 计划周数 | 100% | `周复盘.md` 条目计数 |
| 10 | OKR 进度更新率 | 有进度记录的周数 / 总周数 | ≥80% | `季度OKR.md` 周进度 |
| 11 | 阻塞任务平均处理时长 | blocked → 解除的平均天数 | ≤2天 | 任务执行记录时间戳 |
| 12 | 部门间协作 CEO 可见率 | cc 含 ceo 的跨部门任务 / 总跨部门任务 | 100% | `cc_agents` 字段 |

### F2. 看板增强

**动作**：在 `00-ceo/团队管理总控面板.md` 新增以下 Dataview 查询：

```markdown
## CEO 记忆系统健康度

记忆文件最近更新：

| 文件 | 最后更新 | 版本 |
|------|----------|------|
| [[00-ceo/ceo-memory/用户画像]] | 查看frontmatter | 查看version |
| [[00-ceo/ceo-memory/决策偏好]] | 查看frontmatter | 查看version |
| [[00-ceo/ceo-memory/分派经验]] | 查看frontmatter | 查看version |
| [[00-ceo/ceo-memory/反馈记录]] | 查看frontmatter | 查看version |

## 本周任务满意度

```dataview
TABLE review_score as "满意度", review_notes as "反馈"
FROM "_agent-system/tasks"
WHERE status = "done" AND review_score != ""
SORT file.mtime desc
LIMIT 10
```

## 分派来源统计

```dataview
TABLE length(rows) as "任务数"
FROM "_agent-system/tasks"
GROUP BY from_agent
SORT length(rows) desc
```
```

---

## G. 风险与防错

| # | 风险 | 严重度 | 防错措施 |
|---|------|--------|----------|
| 1 | 用户绕过 CEO 直接进部门目录 | 高 | CLAUDE.md 硬规则 + 部门 CLAUDE.md 加提醒"你是否从 CEO 分派而来？如否，请回到根目录" |
| 2 | CEO 记忆写入错误信息（幻觉） | 高 | 每条记忆标注来源日期，有矛盾标`[待确认]`，周维护时逐条审查 |
| 3 | 记忆文件膨胀失控 | 中 | 月度整理 SOP + 季度归档。主文件控制在 200 行内 |
| 4 | 任务分派全部堆给单一部门 | 中 | 看板增加"按部门未完成任务数"视图，CEO 分派时检查负载 |
| 5 | 用户反馈采集影响对话流畅度 | 中 | 反馈非必选，CEO 根据语境判断是否询问；隐性反馈（如"不错"）直接记录 |
| 6 | 复盘 SOP 变成形式主义 | 中 | 满意度为 `low` 的任务强制创建改进任务；季度统计满意度趋势 |
| 7 | 部门 CLAUDE.md 与 CEO 路由规则冲突 | 低 | 部门 CLAUDE.md 加注"任务优先以 CEO 分派的任务单为准" |
| 8 | 新增文件打破 Dataview 查询 | 低 | 所有新文件必须有标准 frontmatter（通过模板强制）；看板用字段名匹配而非路径硬编码 |
| 9 | Claude Code memory 与 Vault 记忆不同步 | 低 | 两者定位不同：Claude Code memory 存跨项目偏好，Vault 存业务知识。在 MEMORY.md 中注明路径指引 |
| 10 | 过度流程化导致简单问题也走任务单 | 中 | 意图路由决策树中明确区分"CEO直接回答"和"需要分派"的边界 |

---

## H. 给 CEO 的审阅清单

### Phase 1（0-7 天）— 基础治理

- [ ] **确认**：同意"所有输入只与 CEO Agent 沟通"作为硬规则
- [ ] **确认**：同意创建 `00-ceo/ceo-memory/` 目录及 4 个记忆文件
- [ ] **确认**：同意修改根目录 `CLAUDE.md`，去掉"cd进部门自动切换"，改为 CEO 单一入口
- [ ] **确认**：同意修改 `00-ceo/CLAUDE.md`，增加记忆读写指令
- [ ] **行动**：与 CEO Agent 完成 `季度OKR.md` 首次填充（提供实际目标数字）
- [ ] **行动**：与 CEO Agent 完成 `用户画像.md` 首次填充（基本信息、工作偏好）

### Phase 2（8-30 天）— 分派闭环

- [ ] **确认**：同意新增 `任务分派预检SOP.md`
- [ ] **确认**：同意修改任务单模板，增加复盘字段（review_score/review_notes/memory_updated）
- [ ] **确认**：同意新增 `任务复盘SOP.md`
- [ ] **确认**：同意在 `_agent-system/README.md` 中新增"部门间协作 CEO 必须 cc"规则
- [ ] **确认**：同意增强 `周复盘` 流程（自动汇总任务+反馈+数据）
- [ ] **行动**：完成首次周复盘（验证流程可行性）
- [ ] **行动**：完成至少 3 个任务的完整复盘闭环

### Phase 3（31-90 天）— 智能化

- [ ] **确认**：同意创建 `记忆维护SOP.md`（周/月/季度整理节奏）
- [ ] **确认**：同意创建 `部门能力矩阵.md`（辅助 CEO 路由）
- [ ] **确认**：同意在 CEO CLAUDE.md 中增加意图识别决策树
- [ ] **确认**：同意在各部门 CLAUDE.md 中增加"任务应来自 CEO 分派"的提醒
- [ ] **行动**：完成首次月度记忆整理
- [ ] **行动**：完成首次季度记忆归档+OKR回顾

### 持续验证

- [ ] 每周检查：CEO 入口使用率是否 100%
- [ ] 每周检查：记忆文件 version 是否有增长
- [ ] 每月检查：用户满意度均值是否 ≥ 2.5
- [ ] 每季检查：任务返工率是否 ≤ 10%

---

## I. Git 版本管理与自动同步 GitHub

> 目标：Vault 的每次有效变更都以 Git 提交留痕，在恰当时机自动推送至 GitHub 远端，实现"本地知识库 ↔ 远端仓库"的持续同步。

---

### I1. 同步触发规则

#### I1.1 必须同步（Must-Sync）

以下场景完成后 **必须立即执行 commit + push**：

| # | 触发场景 | 理由 |
|---|----------|------|
| M1 | 任务单 `status` 变为 `done` 且复盘完成 | 任务闭环是核心资产，必须持久化 |
| M2 | CEO 记忆文件更新（`ceo-memory/` 下任何文件 `version` +1） | 记忆是不可重建的累积资产，丢失代价极高 |
| M3 | 新 SOP / 模板文件创建或重大修改 | 系统规则变更影响全局，必须版本化 |
| M4 | `CLAUDE.md`（根目录或任何部门）被修改 | Agent 行为定义变更必须可追溯可回滚 |
| M5 | 周复盘 / 季度 OKR 更新写入 | 经营数据是决策依据，不可仅存本地 |

#### I1.2 建议同步（Should-Sync）

以下场景 **建议在当次会话结束前合并提交一次**：

| # | 触发场景 | 理由 |
|---|----------|------|
| S1 | 知识回写（产品卡新增/更新、话术更新等） | 知识资产有价值但非紧急，批量提交即可 |
| S2 | 会话中累计变更 ≥ 5 个文件 | 变更量达到阈值，降低丢失风险 |
| S3 | 用户主动说"今天先到这里"或明确结束会话 | 会话结束是天然同步点 |

#### I1.3 禁止同步（Must-Not-Sync）

| # | 场景 | 理由 |
|---|------|------|
| N1 | 文件正在编辑中途（frontmatter 未闭合、内容不完整） | 半成品提交污染历史，增加回滚复杂度 |
| N2 | 含敏感信息的临时文件（客户真实姓名/身份证/手机号等未脱敏内容） | 推送到远端即泄露，违反数据合规 |
| N3 | `.obsidian/` 目录的频繁自动变更（workspace、插件缓存等） | 属于本地 IDE 状态，不是知识资产，会造成大量噪声提交 |

> **兜底规则**：如果不确定是否该同步，默认归入 S2（会话结束前提交），不要跳过。

---

### I2. 分支策略与提交规范

#### I2.1 分支策略

```
master              ← 唯一长期分支，始终保持可用状态
  │
  ├── session/YYYY-MM-DD-主题   ← 大型变更时可选使用（如系统架构调整）
  │         │
  │         └── 完成后 squash merge 回 master
  │
  └── 日常变更直接提交 master   ← 单人操作，小步提交，保持简单
```

**分支规则**：

1. **默认在 `master` 直接提交**。单人项目无需为每个小变更建分支，过度分支反而增加管理负担。
2. **以下情况必须建 session 分支**：
   - 一次变更涉及 ≥ 10 个文件（如批量产品卡导入）
   - 系统架构级调整（如修改多个 CLAUDE.md + SOP）
   - 任何实验性变更（不确定是否保留）
3. **分支命名**：`session/YYYY-MM-DD-简要描述`（例：`session/2026-03-04-git同步机制`）
4. **分支生命周期**：创建后 7 天内必须合并或删除，不允许长期悬挂。

#### I2.2 提交信息规范

采用简化版 Conventional Commits，中文描述：

```
<type>(<scope>): <简要描述>

[可选正文：变更详情、关联任务ID]

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

**type 枚举**：

| type | 适用场景 | 示例 |
|------|----------|------|
| `feat` | 新增内容/功能 | `feat(knowledge): 新增环宇盈活产品卡` |
| `update` | 更新已有内容 | `update(ceo-memory): 更新用户画像v3` |
| `task` | 任务相关变更 | `task(TASK-20260303-101): 完成投资移民筛查清单` |
| `sop` | SOP/模板/系统文件 | `sop(agent-system): 新增任务分派预检SOP` |
| `fix` | 修正错误内容 | `fix(knowledge): 修正活然人生保费表错误` |
| `chore` | 杂项（.gitignore、目录整理等） | `chore: 更新.gitignore排除.obsidian缓存` |

**scope 使用部门缩写或模块名**：
`ceo` / `recruitment` / `business-dev` / `customer-service` / `content-marketing` / `data-analytics` / `agent-system` / `knowledge`

**提交粒度原则**：
- 一个任务一个提交（不要把多个不相关任务混在一个 commit）
- 记忆文件更新可以和触发它的任务合并为一个提交
- 知识回写可以批量提交（同一会话中的多次回写合为一个 commit）

#### I2.3 PR 策略

即便单人操作，**session 分支合并回 master 时必须走 PR**：

1. **PR 标题**：与分支描述一致，简明扼要
2. **PR 正文**：
   - 变更摘要（bullet points）
   - 关联任务 ID（如有）
   - 影响范围（哪些部门/SOP 受影响）
3. **合并方式**：统一用 **Squash Merge**，保持 master 历史线性清晰
4. **合并后**：自动删除 session 分支
5. **日常直接提交 master 的变更**：不需要 PR，但提交信息必须符合规范

---

### I3. 自动化执行流程

#### I3.1 同步执行四步流程

```
Pre-Check（预检）
    │
    ├─ 1. git status 检查工作区状态
    ├─ 2. 确认无 N1/N2/N3 禁止同步的文件被暂存
    ├─ 3. 检查 .gitignore 是否覆盖敏感路径
    ├─ 4. 若有未追踪文件，判断是否应纳入版本管理
    │
    ▼
Commit（提交）
    │
    ├─ 1. 按变更类型分组暂存（git add 指定文件，不用 git add -A）
    ├─ 2. 生成符合规范的提交信息
    ├─ 3. 执行 git commit
    ├─ 4. 验证 commit 成功（检查 git log 最新条目）
    │
    ▼
Push（推送）
    │
    ├─ 1. git pull --rebase origin master（先拉取远端变更，避免冲突）
    ├─ 2. 若 rebase 有冲突 → 进入冲突处理流程（见 I3.2）
    ├─ 3. git push origin master（或当前分支）
    ├─ 4. 若 push 失败 → 进入失败处理流程（见 I3.2）
    │
    ▼
Verify（验证）
    │
    ├─ 1. git status 确认工作区干净
    ├─ 2. git log --oneline -3 确认提交已在远端
    ├─ 3. 若为 session 分支 PR 合并 → 确认 PR 状态为 merged
    └─ 4. 向用户简报同步结果（一行摘要）
```

#### I3.2 失败处理与安全回滚策略

**核心原则：绝不使用破坏性命令**。禁止 `git reset --hard`、`git push --force`、`git clean -f`、`git checkout .`。

| 失败场景 | 处理方式 |
|----------|----------|
| **Pre-Check 发现敏感文件** | 将该文件路径加入 `.gitignore`，从暂存区移除（`git rm --cached`），通知用户 |
| **Commit 失败（hook 报错）** | 查看 hook 报错信息，修正问题后重新暂存、创建新提交（不用 `--amend`） |
| **Pull rebase 冲突** | 1. `git rebase --abort` 回到 rebase 前状态；2. 改用 `git pull --no-rebase`（merge 方式）；3. 手动解决冲突文件后提交 |
| **Push 被拒绝（远端有新提交）** | 重新 `git pull --rebase` → 若仍冲突走上一条流程 |
| **Push 网络失败** | 等待 30 秒后重试一次；若仍失败，通知用户"本次提交已保存在本地，远端同步待网络恢复后手动执行 `git push`" |
| **提交后发现内容错误** | 用 `git revert <commit-hash>` 创建反转提交（保留历史，不破坏记录），然后修正内容重新提交 |

**回滚决策树**：

```
发现提交有误
    │
    ├─ 尚未 push → git revert HEAD 创建反转提交（安全）
    │
    └─ 已 push → git revert <hash> + git push（远端也安全回滚）
    
    ✗ 禁止：git reset --hard / git push --force / git checkout .
```

---

### I4. 必要的文件配置

#### I4.1 `.gitignore` 补充

确保根目录 `.gitignore` 包含以下规则：

```gitignore
# Obsidian 本地状态（不属于知识资产）
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache/
.obsidian/plugins/*/data.json

# 敏感信息
**/客户原始数据/
**/*身份证*
**/*护照*
**/*银行*
*.secret
.env

# 系统临时文件
.DS_Store
Thumbs.db
*.tmp
```

#### I4.2 新增 SOP 文件

| 操作 | 文件路径 | 说明 |
|------|----------|------|
| **新建** | `_agent-system/intake/Git同步SOP.md` | 本章核心流程的可执行版本，含 Pre-Check/Commit/Push/Verify 四步检查清单 |
| **新建** | `_agent-system/templates/Git提交信息模板.md` | type/scope/描述的快速参考卡片 |

#### I4.3 现有文档修改

| 操作 | 文件路径 | 修改内容 |
|------|----------|----------|
| **修改** | `CLAUDE.md`（根目录） | `## 文件管理规则` 后新增 `## Git 同步规则`，引用 `[[_agent-system/intake/Git同步SOP]]`，列出 M1-M5 必须同步触发点 |
| **修改** | `00-ceo/CLAUDE.md` | `## CEO 记忆系统` 的「对话结束前」步骤中追加："执行 Git 同步预检，若命中触发规则则 commit + push" |
| **修改** | `_agent-system/README.md` | 「协作协议」部分新增：任务 `status: done` 且复盘完成后，CEO Agent 触发 Git 同步 |
| **修改** | `_agent-system/intake/任务复盘SOP.md` | 步骤 5「关闭」之后新增步骤 6「Git 同步」：复盘关闭后自动走 Git 同步四步流程 |
| **修改** | `_agent-system/intake/知识答复自动回写SOP.md` | 回写完成后追加：标记为"待同步"，在会话结束前随 S1 规则批量提交 |
| **修改** | `00-ceo/团队管理总控面板.md` | 新增「Git 同步健康度」看板区块（见 I5 KPI 数据源） |

#### I4.4 文件变更总览（追加到现有附录）

| 操作 | 文件路径 | Phase |
|------|----------|-------|
| **修改** | `.gitignore` | P1 |
| **新建** | `_agent-system/intake/Git同步SOP.md` | P1 |
| **新建** | `_agent-system/templates/Git提交信息模板.md` | P1 |
| **修改** | `CLAUDE.md`（根目录） | P1 |
| **修改** | `00-ceo/CLAUDE.md` | P1 |
| **修改** | `_agent-system/README.md` | P2 |
| **修改** | `_agent-system/intake/任务复盘SOP.md` | P2 |
| **修改** | `_agent-system/intake/知识答复自动回写SOP.md` | P2 |
| **修改** | `00-ceo/团队管理总控面板.md` | P2 |

---

### I5. Git 同步质量 KPI

| # | 指标 | 计算方式 | 目标值 | 数据来源 |
|---|------|----------|--------|----------|
| G1 | **必须同步执行率** | 命中 M1-M5 后实际完成 commit+push 的次数 / 应同步次数 | 100% | `git log` 与任务单 `done` 时间戳交叉比对 |
| G2 | **提交信息规范率** | 符合 `type(scope): 描述` 格式的提交数 / 总提交数 | ≥ 95% | `git log --oneline` 格式校验 |
| G3 | **敏感信息泄露次数** | 含客户真实姓名/身份证/手机号的提交被推送到远端的次数 | 0 | Pre-Check 拦截记录 + 定期 `git log -p` 抽检 |
| G4 | **同步失败修复时长** | push 失败到成功推送的平均间隔 | ≤ 5 分钟 | 失败日志时间戳 |
| G5 | **破坏性命令使用次数** | `reset --hard` / `push --force` / `clean -f` / `checkout .` 的执行次数 | 0 | `git reflog` 审计 |
| G6 | **每周提交频率** | 每周 commit 数量 | ≥ 10 次/活跃周 | `git shortlog --since="1 week ago"` |
| G7 | **提交粒度合理率** | 单个 commit 变更文件数 ≤ 10 的比例 | ≥ 90% | `git log --stat` 统计 |

#### 看板增强（追加到 `00-ceo/团队管理总控面板.md`）

```markdown
## Git 同步健康度

最近 10 次提交：

| 时间 | 提交信息 | 变更文件数 |
|------|----------|-----------|
<!-- 由 CEO Agent 每次同步后更新 -->

本周同步统计：
- 总提交数：__
- 必须同步命中/执行：__ / __
- 提交信息规范率：__%
- 敏感信息拦截：__ 次
- 破坏性命令使用：__ 次
```

---

### I6. 给 CEO 的审阅清单（Git 同步部分）

#### Phase 1（随基础治理一同落地）

- [ ] **确认**：同意 M1-M5 必须同步规则和 N1-N3 禁止同步规则
- [ ] **确认**：同意日常变更直接提交 master、大型变更走 session 分支的策略
- [ ] **确认**：同意提交信息使用 `type(scope): 描述` 规范
- [ ] **行动**：补全 `.gitignore`（排除 Obsidian 缓存和敏感路径）
- [ ] **行动**：创建 `_agent-system/intake/Git同步SOP.md`
- [ ] **行动**：在根目录 `CLAUDE.md` 中增加 Git 同步规则引用

#### Phase 2（随分派闭环一同落地）

- [ ] **确认**：同意任务复盘 SOP 末尾追加 Git 同步步骤
- [ ] **确认**：同意知识回写后标记"待同步"、会话结束批量提交
- [ ] **行动**：在总控面板增加 Git 同步健康度看板
- [ ] **行动**：完成首周 Git KPI 采集，验证指标可操作性

#### 持续验证

- [ ] 每周检查：必须同步执行率是否 100%
- [ ] 每周检查：提交信息规范率是否 ≥ 95%
- [ ] 每月检查：敏感信息泄露次数是否为 0
- [ ] 每月检查：破坏性命令使用次数是否为 0
## J. 统一输入先结构化 Markdown 再分派（全格式适用）

### 1. 硬规则

| # | 规则 | 说明 |
|---|------|------|
| J-1 | **先结构化，再分派** | 任何外部输入（PDF、图片、语音、网页、邮件）必须先转为标准 Markdown，写入 `_agent-system/intake/parsed/` 后才可流转到部门 |
| J-2 | **原件留档** | 原始文件存入 `_agent-system/intake/raw/`，Markdown 文件通过 `source_file` 字段反向链接原件 |
| J-3 | **单次解析，多次引用** | 同一输入只解析一次；后续部门通过 `[[双向链接]]` 引用结构化结果，禁止重复解析 |
| J-4 | **解析失败不静默** | 无法完整解析时，必须在文件中标注 `parse_status: partial`，并列出缺失字段，通知 CEO 人工补录 |

### 2. 标准字段（Frontmatter）

```yaml
---
source_type: pdf | image | voice | webpage | email | manual
source_file: "[[_agent-system/intake/raw/原始文件名]]"
parse_status: complete | partial | failed
parsed_by: agent_id
parsed_date: YYYY-MM-DD
dispatch_to: [business_dev, customer_service]
tags: [输入处理, 结构化]
---
```

### 3. 执行流程

```
外部输入
  │
  ▼
① 存原件 → intake/raw/
  │
  ▼
② 识别格式 → 调用对应解析能力
  │  PDF → 文本提取 + 表格识别
  │  图片 → OCR + 结构化
  │  语音 → 转录 + 摘要
  │  网页 → 抓取 + 清洗
  │  邮件/手动 → 直接结构化
  │
  ▼
③ 填充标准字段 → 生成 Markdown 写入 intake/parsed/
  │
  ▼
④ 质检：核对必填字段完整性
  │  ├─ complete → 设 parse_status: complete
  │  └─ 有缺失 → 设 parse_status: partial，列出缺失项
  │
  ▼
⑤ 分派：根据内容类型自动设置 dispatch_to
  │  ├─ 产品资料 → 02-business-dev/knowledge/
  │  ├─ 客户信息 → 02-business-dev/ 或 03-customer-service/
  │  ├─ 营销素材 → 04-content-marketing/
  │  └─ 业绩数据 → 05-data-analytics/
  │
  ▼
⑥ 创建任务单 → _agent-system/tasks/，通知目标部门
```

### 4. 产品文件专项规则

- **产品文件（尤其PDF）**解析后，必须更新对应产品卡：`02-business-dev/knowledge/product-cards/`。
- 若产品卡不存在，先新建产品卡，再写入本次结构化结果中的关键信息。
- 产品卡回写后必须可被 Dataview 检索（至少保证 `official_name`、`category`、`status`、`tags` 字段完整）。
- 若涉及新产品或更名，需同步更新产品索引文档并补 `[[双向链接]]`。

### 5. 失败兜底

| 场景 | 处理方式 |
|------|----------|
| 解析完全失败 | `parse_status: failed`，写入错误原因和原件链接，并通知 CEO |
| 部分字段缺失 | `parse_status: partial`，缺失字段标记 `⚠️ 待补录`，先分派可执行部分 |
| 产品无法匹配现有卡片 | 新建临时卡并标记 `待核名`，在索引中登记待确认项 |
| 口径冲突（官网 vs 文件） | 结构化文件内并列记录冲突口径，标注证据来源和核对日期，任务状态设为 `blocked` 待CEO裁决 |

### 6. 需修改文件清单

| 文件路径 | 改动内容 |
|----------|----------|
| `_agent-system/intake/输入处理SOP.md` | 新增“全格式先结构化Markdown”强制流程与质量门槛 |
| `_agent-system/templates/输入任务-PDF解析模板.md` | 增加结构化输出链接字段 |
| `_agent-system/templates/输入任务-客户信息模板.md` | 增加结构化输出链接字段 |
| `_agent-system/templates/输入任务-结构化输出模板.md` | 新增统一结构化输出模板 |
| `_agent-system/scripts/precommit_validate_intake.py` | 新增提交前自动拦截脚本（校验结构化输出与产品卡回写） |
| `.githooks/pre-commit` | 新增 Git pre-commit hook，自动执行校验脚本 |
| `_agent-system/intake/提交前自动检查SOP.md` | 新增安装与失败处理SOP |
| `CLAUDE.md`（根目录） | 在“新输入进入系统”补充“先结构化再分派”硬规则 |
| `02-business-dev/CLAUDE.md` | 增加“产品文件必须回写产品卡”责任 |
## 附录：文件变更总览

| 操作 | 文件路径 | Phase |
|------|----------|-------|
| **修改** | `CLAUDE.md`（根目录） | P1 |
| **修改** | `00-ceo/CLAUDE.md` | P1+P3 |
| **新建** | `00-ceo/ceo-memory/用户画像.md` | P1 |
| **新建** | `00-ceo/ceo-memory/决策偏好.md` | P1 |
| **新建** | `00-ceo/ceo-memory/分派经验.md` | P1 |
| **新建** | `00-ceo/ceo-memory/反馈记录.md` | P1 |
| **填充** | `00-ceo/季度OKR.md` | P1 |
| **新建** | `_agent-system/intake/任务分派预检SOP.md` | P2 |
| **新建** | `_agent-system/intake/任务复盘SOP.md` | P2 |
| **修改** | `_agent-system/templates/任务单模板.md` | P2 |
| **修改** | `_agent-system/README.md` | P2 |
| **修改** | `00-ceo/团队管理总控面板.md` | P2 |
| **新建** | `_agent-system/intake/记忆维护SOP.md` | P3 |
| **新建** | `_agent-system/部门能力矩阵.md` | P3 |
| **修改** | 各部门 `CLAUDE.md`（增加 CEO 分派提醒） | P3 |
| **修改** | `.gitignore` | P1 |
| **新建** | `_agent-system/intake/Git同步SOP.md` | P1 |
| **新建** | `_agent-system/templates/Git提交信息模板.md` | P1 |
| **修改** | `_agent-system/intake/知识答复自动回写SOP.md`（加入会话结束批量同步标记） | P2 |
| **修改** | `_agent-system/intake/输入处理SOP.md`（全格式先结构化再分派） | P1 |
| **修改** | `_agent-system/templates/输入任务-PDF解析模板.md`（增加 structured_output） | P1 |
| **修改** | `_agent-system/templates/输入任务-客户信息模板.md`（增加 structured_output） | P1 |
| **新建** | `_agent-system/templates/输入任务-结构化输出模板.md` | P1 |
| **修改** | `02-business-dev/CLAUDE.md`（产品文件强制回写产品卡） | P1 |
| **新建** | `_agent-system/scripts/precommit_validate_intake.py` | P1 |
| **新建** | `.githooks/pre-commit` | P1 |
| **新建** | `_agent-system/intake/提交前自动检查SOP.md` | P1 |
