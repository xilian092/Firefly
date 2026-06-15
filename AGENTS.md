# PROJECT KNOWLEDGE BASE

**Generated:** 2026-03-10
**Commit:** 20f613be
**Branch:** master

## OVERVIEW

Astro 5.17.3 静态博客主题模板 (Firefly)，基于 fuwari 二次开发。支持 TypeScript + Svelte 5 + Tailwind CSS 4，配备双侧边栏、文章网格/瀑布流布局、Pagefind 全文搜索、多语言 i18n。

## STRUCTURE

```
{root}/
├── src/
│   ├── components/    # 79 Astro/Svelte 组件 (widget/layout/page/comment)
│   ├── config/        # 24 个配置模块 (*.ts)
│   ├── pages/         # 14 页面路由
│   ├── utils/         # 14 工具函数
│   ├── plugins/       # 9 Markdown/Rehype 插件
│   ├── layouts/       # 2 布局组件
│   ├── i18n/          # 5 语言文件
│   ├── styles/       # 13 样式文件 (CSS/Stylus)
│   ├── types/        # 类型定义
│   ├── content/      # Markdown/MDX 内容集合
│   └── constants/    # 常量定义
├── public/           # 静态资源 (图片/字体/PIO模型)
├── scripts/          # 构建脚本
└── astro.config.mjs  # Astro 主配置
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| 新增页面 | `src/pages/` | `.astro` 文件，文件即路由 |
| 修改配置 | `src/config/` | 24 个模块化配置 |
| 添加组件 | `src/components/` | 按类型选择子目录 |
| Markdown 扩展 | `src/plugins/` | 自定义 remark/rehype 插件 |
| i18n | `src/i18n/languages/` | 语言文件 + `i18nKey.ts` |
| 样式修改 | `src/styles/` | CSS + Stylus + Tailwind |

## CODE MAP

| Symbol | Type | Location | Role |
|--------|------|----------|------|
| `Layout.astro` | Layout | `src/layouts/` | 根布局，主题初始化 |
| `MainGridLayout.astro` | Layout | `src/layouts/` | 双栏网格布局 |
| `siteConfig` | Config | `src/config/siteConfig.ts` | 核心站点配置 |
| `content` | Collection | `src/content.config.ts` | 内容集合定义 |

## CONVENTIONS

- **TypeScript**: 使用严格模式，启用 `noImplicitAny`
- **格式化**: Biome (tab 缩进, 双引号)
- **组件**: `.astro` 用于静态, `.svelte` 用于交互
- **配置**: 模块化到 `src/config/*.ts`，统一从 `index.ts` 导出
- **样式**: Tailwind CSS 4 (Vite 插件) + Stylus + 纯 CSS 混用

## ANTI-PATTERNS (THIS PROJECT)

- ⚠️ 禁止在 Svelte 组件中使用 `ref:`
- ⚠️ 避免直接在 Layout 中嵌入业务逻辑
- ⚠️ 配置文件修改后需同步到类型定义 (`src/types/config.ts`)

## UNIQUE STYLES

- **双侧边栏**: 通过 `sidebarConfig.ts` 控制左右侧边栏
- **Swup 页面切换**: SPA 风格过渡动画
- **Content Collections**: 使用 Zod schema 验证 frontmatter
- **动态壁纸**: `backgroundWallpaper.ts` 支持多种模式
- **PIO/Live2D**: 看板娘模型集成

## COMMANDS

```bash
pnpm dev          # 开发服务器 localhost:4321
pnpm build        # 构建并生成搜索索引
pnpm preview      # 预览构建产物
pnpm check        # Astro 类型检查
pnpm format       # Biome 格式化
pnpm lint         # Biome 代码检查
pnpm new-post     # 创建新文章
```

## NOTES

- 需 Node.js ≥ 22, pnpm ≥ 9
- 构建时自动清理 console.log (esbuild drop)
- Pagefind 搜索索引在构建后生成