const zh = {
  // Header
  "app.title": "情侣出行决策助手",
  "app.subtitle": "查附近商场 · 结合品牌偏好推荐 · 运行在 EdgeOne Makers",

  // Empty state
  "empty.title": "情侣出行决策助手",
  "empty.hint": "告诉我你在哪、想找什么样的商场（比如「既有倍轻松又有西厅村屋」），我会用地图检索附近商场，按距离和偏好帮你推荐，并列出需要你手动确认的事项。",
  "empty.features": "高德地图 · 会话记忆 · Agent Tools",

  // Chat input
  "chat.placeholder": "说说你的位置和偏好…  ⏎ 发送 · Shift+⏎ 换行",
  "chat.hint": "由 OpenAI Agents SDK + EdgeOne Makers 驱动",

  // Preset questions
  "preset.1": "我在红莲南路地铁站附近，想找既有倍轻松又有西厅村屋的近一点的商场，帮我推荐。",
  "preset.2": "我在静安大悦城附近，帮我找附近适合情侣约会的商场，并列出我需要手动确认的事项。",

  // Tool indicators
  "tool.geocode": "地点解析",
  "tool.nearby": "附近商场",
  "tool.keyword": "关键词搜索",
  "tool.distance": "距离计算",
  "tool.weather": "天气查询",

  // Status & errors
  "status.error": "⚠️ 请求失败，请检查后端服务是否启动。",
  "status.stopped": "⏹ *已停止生成*",
  "status.backendError": "⚠️ 后端中断请求失败，服务端可能仍在运行。",

  // Debug panel
  "debug.title": "传输流",
  "debug.events": "事件",
  "debug.clear": "清除",
  "debug.empty": "等待 SSE 事件...",
  "debug.emptyHint": "发送消息后，所有原始后端数据将在此处显示。",

  // Conversation sidebar
  "sidebar.label": "会话列表",
  "sidebar.title": "会话",
  "sidebar.newChat": "新建聊天",
  "sidebar.loading": "正在加载会话...",
  "sidebar.loadMore": "加载更多",
  "sidebar.loadingMore": "加载中...",
  "sidebar.emptyTitle": "暂无会话",
  "sidebar.emptyHint": "点击「新建聊天」开始第一段对话。",
  "sidebar.delete": "删除会话",
  "sidebar.deleteConfirm": "确定要永久删除这个会话吗？此操作不可恢复。",

  // Aria labels (button hover/screen-reader)
  "aria.send": "发送",
  "aria.clearHistory": "清除历史",
  "aria.stopGeneration": "停止生成",

  // Language toggle
  "lang.switch": "English",

  // ─── Floating bottom-right action badges ─────────────────────────────
  "floatingLink.deploy": "一键部署",
  "floatingLink.github": "GitHub",
} as const;

export default zh;
