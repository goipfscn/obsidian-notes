# Scrapling 爬虫工具

> 绕过Cloudflare的反爬虫工具

## 安装

```bash
pip install scrapling --break-system-packages
```

## 基本用法

### 静态页面
```bash
scrapling extract "https://example.com" -o output.html
```

### 动态页面 (JavaScript渲染)
```bash
scrapling extract fetch "https://example.com" -o output.html
```

### 等待加载
```bash
scrapling extract fetch "https://example.com" -o output.html --wait 3000
```

## 选项

| 选项 | 说明 |
|------|------|
| `--headless` | 无头模式（默认） |
| `--no-headless` | 显示浏览器 |
| `--wait` | 等待毫秒数 |
| `-s, --css-selector` | CSS选择器 |
| `--real-chrome` | 使用真实Chrome |

## 示例

### 绕过Cloudflare
```bash
scrapling extract stealthy-fetch "https://polymarketanalytics.com/traders" -o output.html
```

### 等待页面加载
```bash
scrapling extract fetch "https://example.com" page.html --wait 5000
```

### 使用真实Chrome
```bash
scrapling extract fetch "https://example.com" page.html --real-chrome
```

## 反爬虫绕过

Scrapling使用以下技术绕过反爬虫：

1. **Stealth模式** - 模拟真实浏览器
2. **Cloudflare绕过** - 自动处理验证
3. **User-Agent轮换** - 避免被识别

## 更新日志

- 2026-03-04: 创建skill
