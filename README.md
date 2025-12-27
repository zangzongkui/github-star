# GitHub 自动点 Star 脚本

使用 DrissionPage 自动化浏览器操作，给指定的 GitHub 项目点 Star。

## 功能特性

- 自动给指定的 GitHub 仓库点 Star
- 支持接管已打开的 Chrome 浏览器
- 自动检测仓库是否已被 Star
- 支持登录状态检测

## 依赖安装

```bash
pip install -r requirements.txt
```

## 使用前准备

### 1. 确保已安装 Chrome 浏览器

### 2. 以调试模式启动 Chrome 浏览器

**Windows:**
```bash
chrome.exe --remote-debugging-port=9222
```

**macOS:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

**Linux:**
```bash
google-chrome --remote-debugging-port=9222
```

### 3. 在浏览器中登录 GitHub 账号

## 使用方法

### 方式一: 直接运行脚本

修改 `main()` 函数中的 `repo_url` 变量，然后运行:

```bash
python github_star.py
```

### 方式二: 作为模块导入

```python
from github_star import star_repo_with_existing_browser

# 给单个仓库点 Star
result = star_repo_with_existing_browser('https://github.com/owner/repo')
print(result)
```

### 批量点 Star 示例

```python
from github_star import star_repo_with_existing_browser

repos = [
    'https://github.com/anthropics/anthropic-cookbook',
    'https://github.com/anthropics/courses',
]

for repo in repos:
    result = star_repo_with_existing_browser(repo)
    print(f'{repo}: {result}')
```

## 返回值说明

| 返回值 | 说明 |
|--------|------|
| `already_starred` | 仓库已经是 Star 状态，无需操作 |
| `star_success` | 成功给仓库点 Star |
| `star_failed` | 点击 Star 按钮后验证失败 |
| `button_not_found` | 未找到 Star 按钮（可能页面未加载完成） |
| `not_logged_in` | 用户未登录 GitHub |

## 函数参数

### `star_repo_with_existing_browser(repo_url, port=9222)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `repo_url` | str | 必填 | GitHub 仓库的 URL |
| `port` | int | 9222 | Chrome 浏览器调试端口 |

## 注意事项

- 请确保 Chrome 浏览器以调试模式启动
- 请确保已在浏览器中登录 GitHub 账号
- 默认调试端口为 9222，可通过 `port` 参数修改
- 脚本会等待页面加载，请保持网络畅通

## 许可证

MIT License
