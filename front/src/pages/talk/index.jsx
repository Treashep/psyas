import React, { useState, useRef, useEffect } from "react";
import Bar from "../../components/bar";
import { sendChatMessageAPI, getConversationHistoryAPI } from "../../apis/talk";
import "./index.css";

const Talk = () => {
    const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([]); // 聊天消息列表
  const [loading, setLoading] = useState(false);
  const [historyList, setHistoryList] = useState([]); // 历史会话列表
  const [currentSessionId, setCurrentSessionId] = useState(null); // 当前会话 ID
  const [showInitialText, setShowInitialText] = useState(true); // 是否显示引导语
  const chatWindowRef = useRef(null);

  // 👉 获取历史对话列表
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await getConversationHistoryAPI(10);
        if (res.conversations && Array.isArray(res.conversations)) {
          setHistoryList(res.conversations);
        } else {
          setHistoryList([]);
        }
      } catch (error) {
        console.error("获取历史对话失败:", error);
        setHistoryList([]);
      }
    };

    fetchHistory();
  }, []);

  // 👉 自动滚动到底部
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  // 👉 发送消息（支持 session_id）
  const handleSend = async () => {
    const trimmed = inputValue.trim();
    if (!trimmed || loading) return;

    // 隐藏引导文字
    setShowInitialText(false);

    // 添加用户消息
    const userMsg = { id: Date.now(), type: "user", text: trimmed };
    setMessages((prev) => [...prev, userMsg]);
    setInputValue("");
    setLoading(true);

    try {
      // 发送消息，带上 session_id（如果是新对话，后端会返回新的 session_id）
      const response = await sendChatMessageAPI({
        message: trimmed,
        session_id: currentSessionId, // 可能为 null
      });

      // 如果是新对话，保存后端返回的 session_id
      if (response.session_id && !currentSessionId) {
        setCurrentSessionId(response.session_id);
      }

      const aiMsg = {
        id: Date.now() + 1,
        type: "ai",
        text:
          response.assistant_response || "我暂时无法回答，请换一种方式提问。",
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (error) {
      console.error("API 请求失败:", error);
      const errorMsg = {
        id: Date.now() + 1,
        type: "ai",
        text: "网络连接失败，请稍后重试。",
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  // 👉 回车发送
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  // 👉 点击历史条目（未来可扩展：加载该会话内容）
  const handleLoadHistory = (session) => {
    // 临时：仅切换当前会话 ID，清空消息（后续应加载真实消息）
    setCurrentSessionId(session.session_id);
    setMessages([]);
    setShowInitialText(false);
  };

  // 👉 格式化时间显示
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString("zh-CN", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    }).replace(/\//g, "-");
  };

  return (
    <div className="body">
      <Bar />

      {/* 左侧历史对话栏 */}
      <div className="history-box">
        <div className="history-title">历史对话</div>
        <div className="history-empty">
          {historyList.length > 0 ? (
            historyList.map((session) => (
              <div
                key={session.session_id}
                className={`history-item ${
                  currentSessionId === session.session_id ? "active" : ""
                }`}
                onClick={() => handleLoadHistory(session)}
              >
                <span className="history-time">
                  {formatTime(session.created_at)}
                </span>
                <span className="history-desc">
                  {session.title || "未命名对话"}
                </span>
              </div>
            ))
          ) : (
            <div className="history-empty">暂无历史对话</div>
          )}
        </div>
      </div>

      {/* 右侧内容区域 */}
      <div className="right-content">
        {/* 对话内容区域 */}
        <div className="chat-area">
          <div className="chat-window" ref={chatWindowRef}>
            <div className="chat-text">
              {/* === 初始引导文字：普通段落，无气泡 === */}
              {showInitialText && (
                <div className="initial-intro-text">
                  <p>
                    心理分析最初由西格蒙德·弗洛伊德创立，是一种深入探索人类潜意识、情感冲突与人格结构的心理学方法。它认为，许多我们表面无法理解的情绪、行为与人际关系模式，其实源于童年经历、未被觉察的欲望、压抑的情感与内在冲突。
                  </p>
                  <p>
                    心理分析不仅关注"你做了什么"，更关注"你为什么这么做"。它试图揭示那些隐藏在意识之下的心理动力。
                  </p>
                  <p>
                    通过自由联想、梦境解析、移情分析等方法，心理分析帮助个体将潜意识中的内容带入意识层面，从而实现理解、整合与转化。
                  </p>
                  <p>
                    今天的心理分析已融合了荣格的分析心理学、客体关系理论、依恋理论等多元视角，更加注重个体成长、自我实现与关系修复。它不再局限于"治疗疾病"，而是成为促进自我认知、提升心理弹性、实现内在自由的重要途径。
                  </p>
                  <p>
                    在"心理分析助手"中，我们以人本主义与整合心理视角为基础，结合认知行为、正念与心理动力学理念，设计出温和而深刻的互动体验。你将逐步构建属于你自己的"内心地图"，走向更真实、更自由的自我。
                  </p>
                </div>
              )}

              {/* === 正式聊天记录：用户发送后出现，带气泡样式 === */}
              {!showInitialText && (
                <div className="actual-messages">
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`message-bubble ${msg.type}-bubble`}
                    >
                      <p>{msg.text}</p>
                    </div>
                  ))}

                  {/* 加载中提示 */}
                  {loading && (
                    <div className="message-bubble ai-bubble">
                      <p><em>思考中...</em></p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* 底部输入框 */}
        <div className="input-area">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="请输入您的问题..."
            className="input-box"
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={loading}
          >
            {loading ? "发送中..." : "发送"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Talk;