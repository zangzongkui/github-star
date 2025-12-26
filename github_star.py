# -*- coding: utf-8 -*-
"""
GitHub 自动点 Star 脚本
使用 DrissionPage 自动化浏览器操作，给指定的 GitHub 项目点 Star
"""

# 导入 DrissionPage 的 ChromiumPage 类
from DrissionPage import ChromiumPage
# 导入 ChromiumOptions 用于配置浏览器
from DrissionPage import ChromiumOptions
# 导入时间模块
import time


def is_element_visible(element) -> bool:
    """
    检查元素是否可见

    参数:
        element: DrissionPage 的元素对象

    返回:
        bool: 元素是否可见
    """
    # 如果元素不存在，返回 False
    if not element:
        return False

    try:
        # 获取元素的尺寸
        size = element.rect.size
        # 如果宽度和高度都大于 0，则认为元素可见
        return size[0] > 0 and size[1] > 0
    except Exception:
        # 如果获取尺寸失败，返回 False
        return False


def find_star_button(page):
    """
    查找 Star 相关按钮

    参数:
        page: DrissionPage 的页面对象

    返回:
        tuple: (按钮元素, 是否已 starred)
        如果没找到返回 (None, None)
    """
    # 获取页面上所有按钮
    buttons = page.eles('tag:button')

    # 遍历所有按钮
    for btn in buttons:
        try:
            # 检查元素是否可见
            if not is_element_visible(btn):
                continue

            # 获取按钮的 aria-label 属性
            aria_label = btn.attr('aria-label') or ''
            # 转换为小写进行比较
            aria_label_lower = aria_label.lower()

            # 检查是否是已 starred 的按钮（Unstar 按钮）
            # aria-label 格式: "Starred, click to unstar this repository (17895)"
            if 'unstar' in aria_label_lower or 'starred,' in aria_label_lower:
                return (btn, True)

            # 检查是否是未 star 的按钮（Star 按钮）
            # aria-label 格式: "Star this repository (17895)"
            if 'star this repository' in aria_label_lower:
                return (btn, False)

        except Exception:
            # 忽略获取属性失败的按钮
            continue

    # 没有找到按钮
    return (None, None)


def star_repo_with_existing_browser(repo_url: str, port: int = 9222) -> str:
    """
    使用已打开的浏览器给仓库点 Star（接管已有浏览器）

    参数:
        repo_url: GitHub 仓库的 URL
        port: 浏览器调试端口，默认 9222

    返回:
        str: 操作结果状态
            - 'already_starred': 已经是 starred 状态
            - 'star_success': 成功点击 star
            - 'star_failed': 点击 star 失败
            - 'button_not_found': 未找到按钮
            - 'not_logged_in': 用户未登录 GitHub

    使用前需要以调试模式启动 Chrome:
    chrome.exe --remote-debugging-port=9222
    """
    # 创建浏览器配置对象
    co = ChromiumOptions()
    # 设置连接已有浏览器的地址和端口
    co.set_address(f'127.0.0.1:{port}')
    # 创建浏览器页面对象（接管已有浏览器）
    page = ChromiumPage(co)

    # 导航到目标仓库页面
    print(f'正在打开: {repo_url}')
    page.get(repo_url)

    # 等待页面加载完成
    time.sleep(3)

    # 打印当前页面 URL 用于调试
    print(f'当前页面: {page.url}')

    # 检查是否被重定向到登录页面
    current_url = page.url.lower()
    if 'login' in current_url or 'signin' in current_url:
        print('错误: 用户未登录 GitHub！')
        return 'not_logged_in'

    # 查找 Star 按钮
    button, is_starred = find_star_button(page)

    # 如果找到按钮
    if button is not None:
        if is_starred:
            # 已经是 starred 状态
            aria_label = button.attr('aria-label') or 'Starred'
            print(f'该仓库已是 Starred 状态: {aria_label}')
            return 'already_starred'
        else:
            # 未 star，执行点击操作
            print('正在点击 Star 按钮...')
            button.click()

            # 等待按钮状态变化
            time.sleep(2)

            # 验证是否成功 - 再次查找按钮状态
            new_button, new_is_starred = find_star_button(page)

            if new_button and new_is_starred:
                aria_label = new_button.attr('aria-label') or 'Starred'
                print(f'Star 成功！当前状态: {aria_label}')
                return 'star_success'
            else:
                print('Star 操作可能未成功，请检查是否已登录 GitHub')
                return 'star_failed'

    # 未找到按钮，检查是否未登录
    print('未找到 Star 按钮，请检查是否已登录 GitHub')
    return 'button_not_found'


def main():
    """
    主函数
    """
    # 目标仓库 URL
    # repo_url = 'https://github.com/anthropics/anthropic-cookbook'
    repo_url = 'https://github.com/ChromeDevTools/chrome-devtools-mcp'

    # 接管已打开的浏览器（需要先以调试模式启动 Chrome）
    # chrome.exe --remote-debugging-port=9222
    print('=' * 50)
    print('接管已有浏览器并点 Star')
    print('=' * 50)
    result = star_repo_with_existing_browser(repo_url, port=9222)
    print(f'操作结果: {result}')


# 程序入口
if __name__ == '__main__':
    # 运行主函数
    main()
