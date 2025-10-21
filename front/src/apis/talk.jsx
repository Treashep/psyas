import { request } from "../utils";

// 1.发送消息给AI助手（支持 session_id）
export function sendChatMessageAPI(data) {
  // data 可以是 { message: "内容", session_id: "xxx" }
  return request({
    url: '/api/conversation/chat',
    method: 'POST',
    data
  });
}

// 2.获取对话历史
export function getConversationHistoryAPI(limit = 10, userId = null) {
  return request({
    url: '/api/conversation/history',
    method: 'GET',
    params: { limit, user_id: userId } // 使用 params 传递查询参数
  });
}

// 3.检查对话服务状态（无需认证）
export function getConversationStatusAPI() {
  return request({
    url: '/api/conversation/status',
    method: 'GET'
  });
}