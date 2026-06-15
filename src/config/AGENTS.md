# src/config/

**Parent:** `../AGENTS.md`

## OVERVIEW

24 个模块化配置文件，控制博客所有功能特性。

## WHERE TO LOOK

| Config | Purpose |
|--------|---------|
| `siteConfig.ts` | 站点基础 (标题、描述、语言、URL) |
| `sidebarConfig.ts` | 双侧边栏布局配置 |
| `backgroundWallpaper.ts` | 动态壁纸/背景配置 |
| `profileConfig.ts` | 个人资料 (头像、昵称、社交链接) |
| `navBarConfig.ts` | 导航栏配置 |
| `fontConfig.ts` | 字体配置 |
| `pioConfig.ts` | PIO/Live2D 看板娘 |
| `musicConfig.ts` | 背景音乐播放器 |
| `commentConfig.ts` | 评论系统选择与配置 |
| `expressiveCodeConfig.ts` | 代码高亮配置 |

## KEY FILES

```
src/config/
├── index.ts              # 统一导出所有配置
├── siteConfig.ts          # 核心站点配置 (6963 行)
├── sidebarConfig.ts       # 侧边栏配置 (6111 行)
├── backgroundWallpaper.ts # 壁纸配置 (5918 行)
└── *.ts                   # 其他 20+ 配置文件
```

## CONVENTIONS

- 每个功能模块对应独立 `.ts` 文件
- 统一从 `index.ts` 导出: `import { siteConfig } from "@/config"`
- 配置使用 TypeScript 类型定义 (参考 `src/types/config.ts`)
- 修改配置后需同步类型定义

## ANTI-PATTERNS

- ⚠️ 禁止直接修改 `index.ts` 以外的导出方式
- ⚠️ 新增配置需同步更新 `src/types/config.ts`