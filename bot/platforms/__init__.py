# -*- coding: utf-8 -*-
"""
===================================
平台适配器模块
===================================

包含各平台的 Webhook 处理和消息解析逻辑。

支持两种接入模式：
1. Webhook 模式：需要公网 IP，配置回调 URL
2. Stream 模式：无需公网 IP，通过 WebSocket 长连接（钉钉、飞书支持）
"""

from bot.platforms.base import BotPlatform

# 所有可用平台（Webhook 模式）
ALL_PLATFORMS = {
    'dingtalk': DingtalkPlatform,
}

__all__ = [
    'BotPlatform',
    'ALL_PLATFORMS',
]
