import React, { useState, useRef, useEffect } from "react";
import { sendChatMessageAPI, getConversationHistoryAPI } from "../../apis/talk";
import { useSelector, useDispatch } from "react-redux";
import { fetchUserInfo } from "../../store/modules/user";
import styles from "./index.module.css";
import { Helmet } from 'react-helmet-async';

const Talk = () => {
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([]); // 聊天消息列表
  const [loading, setLoading] = useState(false);
  const [historyList, setHistoryList] = useState([]); // 历史会话列表
  const [currentSessionId, setCurrentSessionId] = useState(null); // 当前会话 ID
  const [showInitialText, setShowInitialText] = useState(true); // 是否显示引导语
  const [hasSentMessage, setHasSentMessage] = useState(false); // 是否已发送消息
  const chatWindowRef = useRef(null);
  const [managementVisible, setManagementVisible] = useState(false);
  
  // 获取用户信息
  const dispatch = useDispatch();
  const { username, userId, isLoggedIn } = useSelector(state => state.user);

  // 获取历史对话列表
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await getConversationHistoryAPI(10, userId);
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

    // 如果已登录但没有用户信息，则获取用户信息
    if (isLoggedIn && !username) {
      dispatch(fetchUserInfo());
    }

    // 只有当有用户ID时才获取历史对话
    if (userId) {
      fetchHistory();
    }
  }, [isLoggedIn, username, userId, dispatch]);

  // 自动滚动到底部
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  // 发送消息（支持 session_id）
  const handleSend = async () => {
    const trimmed = inputValue.trim();
    if (!trimmed || loading) return;

    // 隐藏引导文字
    setShowInitialText(false);
    // 标记已发送消息
    setHasSentMessage(true);

    // 添加用户消息
    const userMsg = { id: Date.now(), type: "user", text: trimmed };
    setMessages((prev) => [...prev, userMsg]);
    setInputValue("");
    setLoading(true);

    try {
      // 发送消息，带上 session_id（如果是新对话，后端会返回新的 session_id）和用户ID
      const response = await sendChatMessageAPI({
        message: trimmed,
        session_id: currentSessionId, // 可能为 null
        user_id: userId, // 添加用户ID
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

  // 回车发送
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  // 点击历史条目（未来可扩展：加载该会话内容）
  const handleLoadHistory = (session) => {
    // 临时：仅切换当前会话 ID，清空消息（后续应加载真实消息）
    setCurrentSessionId(session.session_id);
    setMessages([]);
    setShowInitialText(false);
    setHasSentMessage(true);
  };

  // 创建新对话
  const handleNewChat = () => {
    setCurrentSessionId(null); // 重置会话ID
    setMessages([]); // 清空消息
    setShowInitialText(true); // 显示初始引导文字
    setHasSentMessage(false); // 重置发送消息状态
  };

  const handleManagement = () => {
    // 打开管理弹窗
    setManagementVisible(!managementVisible);
  };

  // 格式化时间显示
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
    <>
      {/* SEO优化 - 页面元数据 */}
      <Helmet>
        <title>PSYAS - 专业心理咨询助手 | 在线心理支持与咨询</title>
        <meta name="description" content="PSYAS是您的专业心理咨询助手，提供24/7在线心理支持、情绪疏导和心理健康咨询服务。通过AI技术，为您提供私密、安全、专业的心理辅导体验。" />
        <meta name="keywords" content="心理咨询,心理健康,情绪疏导,心理支持,在线咨询,PSYAS,心理助手,心理辅导" />
        <meta property="og:title" content="PSYAS - 专业心理咨询助手" />
        <meta property="og:description" content="PSYAS是您的专业心理咨询助手，提供24/7在线心理支持与咨询服务" />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary" />
        <meta name="twitter:title" content="PSYAS - 专业心理咨询助手" />
        <meta name="twitter:description" content="PSYAS是您的专业心理咨询助手，提供24/7在线心理支持与咨询服务" />
        <link rel="canonical" href="https://psyas.com/talk" />
        
        {/* 结构化数据 - JSON-LD */}
        <script type="application/ld+json">
          {`
            {
              "@context": "https://schema.org",
              "@type": "WebApplication",
              "name": "PSYAS",
              "alternateName": "专业心理咨询助手",
              "description": "PSYAS是您的专业心理咨询助手，提供24/7在线心理支持、情绪疏导和心理健康咨询服务",
              "url": "https://psyas.com",
              "applicationCategory": "HealthApplication",
              "operatingSystem": "Web",
              "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "CNY"
              },
              "author": {
                "@type": "Organization",
                "name": "PSYAS Team"
              }
            }
          `}
        </script>
      </Helmet>
      
      <div className={styles.talkContainer}>
      {/* 左侧边栏 */}
      <div className={styles.leftSidebar}>
        {/* 新增对话按钮 */}
        <div className={styles.newChatBtn} onClick={handleNewChat}>
          + 新增对话
        </div>
        {/* 历史对话栏 */}
        <div className={styles.historyBox}>
          <div className={styles.historyTitle}>历史对话</div>
          <div className={styles.historyList}>
            {historyList.length > 0 ? (
              historyList.map((session) => (
                <div
                  key={session.session_id}
                  className={`${styles.historyItem} ${
                    currentSessionId === session.session_id ? styles.active : ""
                  }`}
                  onClick={() => handleLoadHistory(session)}
                >
                  <span className={styles.historyTime}>
                    {formatTime(session.created_at)}
                  </span>
                  <span className={styles.historyDesc}>
                    {session.title || "未命名对话"}
                  </span>
                </div>
              ))
            ) : (
              <div className={styles.historyEmpty}>暂无历史对话</div>
            )}
          </div>
          <div className={styles.managementBtn} onClick={handleManagement}>
            管理历史记录
          </div>
        </div>
      </div>

      {/* 右侧内容区域 */}
      <div className={styles.rightContent}>
        {/* SEO优化的品牌标识 */}
        <header className={styles.brandHeader} itemScope itemType="https://schema.org/Organization">
          <h1 className={styles.brandTitle}>
            <span className={styles.brandName} itemProp="name">PSYAS</span>
            <span className={styles.brandTagline} itemProp="description">专业心理咨询助手</span>
          </h1>
          <meta itemProp="url" content="https://psyas.com" />
          <meta itemProp="logo" content="https://psyas.com/logo.png" />
          <link itemProp="sameAs" href="https://twitter.com/psyas" />
          <link itemProp="sameAs" href="https://facebook.com/psyas" />
        </header>
        
        {/* 对话内容区域 */}
        <div className={styles.chatArea}>
          <div className={styles.chatWindow} ref={chatWindowRef}>
            <div className={styles.chatText}>
              {/* === 初始引导文字：普通段落，无气泡 === */}
              {showInitialText && (
                <div className={styles.initialIntroText}>
                  <p>
                    你好，{username || "用户"}，我是你的个人心理咨询助手。
                  </p>
                </div>
              )}

              {/* === 正式聊天记录：用户发送后出现，带气泡样式 === */}
              {!showInitialText && (
                <div className={styles.actualMessages}>
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`${styles.messageBubble} ${styles[msg.type + 'Bubble']}`}
                    >
                      <p>{msg.text}</p>
                    </div>
                  ))}

                  {/* 加载中提示 */}
                  {loading && (
                    <div className={`${styles.messageBubble} ${styles.aiBubble}`}>
                      <p><em>思考中...</em></p>
                    </div>
                  )}
                </div>
              )}
              {/* 底部输入框 */}
              <div className={`${styles.inputArea} ${hasSentMessage ? styles.fixedInputArea : ''}`}>
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="有什么我可以帮到你的？"
                  className={styles.inputBox}
                  disabled={loading}
                />
                <button
                  className={styles.sendBtn}
                  onClick={handleSend}
                  disabled={loading}
                >
                  {loading ? "发送中..." : "发送"}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
    </>
  );
};

export default Talk;