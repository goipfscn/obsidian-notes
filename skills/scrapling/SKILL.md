# Scrapling - 爬虫工具

> 来源: @akokoi1 Twitter 推荐
> GitHub: https://github.com/akokoi1/scrapling

## 安装

```bash
pip install scrapling --break-system-packages
```

## 常用命令

### 基本爬取
```bash
scrapling extract "https://example.com"
```

### 提取特定内容 (CSS选择器)
```bash
scrapling extract "https://example.com" --selector "h1.title"
```

### 提取特定内容 (XPath)
```bash
scrapling extract "https://example.com" --xpath "//div[@class='content']"
```

### JSON提取
```bash
scrapling extract "https://api.example.com/data" --json
```

### 使用Playwright
```bash
scrapling extract "https://example.com" --fetcher playwright
```

## 高级用法

### 浏览器指纹伪装
自动处理 Cloudflare Turnstile 等验证

### 并发爬取
```bash
scrapling extract "https://example.com" --fetcher async
```

### 保存到文件
```bash
scrapling extract "https://example.com" -o output.html
```

## Fetcher选项

| Fetcher | 说明 |
|---------|------|
| curl | 快速静态页面 |
| httpx | 支持JavaScript |
| playwright | 完整浏览器渲染 |
| selenium | Selenium支持 |

## 示例

```bash
# 提取文章标题
scrapling extract "https://news.example.com/article/123" --selector "h1"

# 提取所有链接
scrapling extract "https://example.com" --selector "a::attr(href)"

# 提取JSON数据
scrapling extract "https://api.example.com/users" --json

# 使用Playwright处理动态内容
scrapling extract "https://example.com SPA" --fetcher playwright
```

## 更新日志

- 2026-03-03: 创建skill，基于@akokoi1推荐
