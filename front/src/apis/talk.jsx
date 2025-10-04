import { request } from "../utils";

// 1.发送消息给AI助手
export function sendChatMessageAPI(message) {
  return request({
    url: '/api/conversation/chat',
    method: 'POST',
    data: { message } // 只传 message 字段
  });
}

// 2.获取对话历史
export function getConversationHistoryAPI(limit = 10) {
  return request({
    url: '/api/conversation/history',
    method: 'GET',
    params: { limit } // 使用 params 传递查询参数
  });
}

// 3.检查对话服务状态（无需认证）
export function getConversationStatusAPI() {
  return request({
    url: '/api/conversation/status',
    method: 'GET'
  });
}