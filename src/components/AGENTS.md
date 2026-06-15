# src/components/

**Parent:** `../AGENTS.md`

## OVERVIEW

79 个 Astro/Svelte 组件，按功能角色组织。

## STRUCTURE

```
src/components/
├── analytics/   # 3 统计追踪组件
├── comment/     # 5 评论组件 (Twikoo, Giscus, Artalk)
├── common/      # 12 通用基础组件
├── controls/    # 5 交互控制组件 (深色模式、搜索等)
├── features/   # 10 功能特性组件 (主题、动态壁纸)
├── layout/     # 11 布局结构组件
├── misc/       # 6 杂项组件
├── pages/      # 9 页面级组件
└── widget/     # 18 侧边栏小部件
```

## WHERE TO LOOK

| Task | Subdir | Key Files |
|------|--------|-----------|
| 侧边栏部件 | `widget/` | Profile, Categories, Tags, Calendar, SiteStats |
| 评论系统 | `comment/` | Twikoo, Giscus, Artalk |
| 页面布局 | `layout/` | Header, Footer, Sidebar, Card |
| 交互控件 | `controls/` | Search, LightDarkSwitch, BackToTop |

## CONVENTIONS

- 交互组件使用 `.svelte` (响应式)
- 静态组件使用 `.astro`
- 组件名: PascalCase
- 部件组件需在 `widgetConfig` 中注册

## ANTI-PATTERNS

- ⚠️ Svelte 组件禁止使用 `ref:` 语法
- ⚠️ 避免在组件中直接读取 siteConfig，使用 props 传递