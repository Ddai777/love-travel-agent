const en = {
  // Header
  "app.title": "Couple Travel Decision Assistant",
  "app.subtitle": "Find nearby malls · Recommend by brand preference · Powered by EdgeOne Makers",

  // Empty state
  "empty.title": "Couple Travel Decision Assistant",
  "empty.hint": "Tell me where you are and what kind of mall you want (e.g. one with both '倍轻松' and '西厅村屋'). I'll search nearby malls on the map, recommend by distance and preference, and list what you need to confirm manually.",
  "empty.features": "AMap · Session Memory · Agent Tools",

  // Chat input
  "chat.placeholder": "Tell me your location and preferences...  ⏎ Send · Shift+⏎ Newline",
  "chat.hint": "Powered by OpenAI Agents SDK + EdgeOne Makers",

  // Preset questions
  "preset.1": "I'm near Honglian South Rd subway station. Find a nearby mall that has both '倍轻松' and '西厅村屋'.",
  "preset.2": "I'm near Jing'an Joy City. Recommend malls nearby that are good for a couple's date, and list what I need to confirm manually.",

  // Tool indicators
  "tool.geocode": "Geocode",
  "tool.nearby": "Nearby malls",
  "tool.keyword": "Keyword search",
  "tool.distance": "Distance",
  "tool.weather": "Weather",

  // Status & errors
  "status.error": "Request failed. Please check if the backend service is running.",
  "status.stopped": "⏹ *Generation stopped*",
  "status.backendError": "Backend abort request failed. The server may still be running.",

  // Debug panel
  "debug.title": "Trace",
  "debug.events": "events",
  "debug.clear": "Clear",
  "debug.empty": "Waiting for SSE events...",
  "debug.emptyHint": "After sending a message, all raw backend data will be displayed here.",

  // Conversation sidebar
  "sidebar.label": "Conversation list",
  "sidebar.title": "Chats",
  "sidebar.newChat": "New chat",
  "sidebar.loading": "Loading conversations...",
  "sidebar.loadMore": "Load more",
  "sidebar.loadingMore": "Loading...",
  "sidebar.emptyTitle": "No conversations yet",
  "sidebar.emptyHint": "Click \"New chat\" to start your first conversation.",
  "sidebar.delete": "Delete conversation",
  "sidebar.deleteConfirm": "Permanently delete this conversation? This cannot be undone.",

  // Aria labels (button hover/screen-reader)
  "aria.send": "Send",
  "aria.clearHistory": "Clear history",
  "aria.stopGeneration": "Stop generation",

  // Language toggle
  "lang.switch": "中文",

  // ─── Floating bottom-right action badges ─────────────────────────────
  "floatingLink.deploy": "Deploy",
  "floatingLink.github": "GitHub",
} as const;

export default en;
