import React from "react";
import Bar from "../../components/bar";
import './index.css';

const Talk = () => {
  return (
    <div className="body">
      <Bar />
      {/* 左侧历史对话栏 */}
      <div className="history-box">
        <div className="history-title">历史对话</div>
        {/* 渲染历史对话列表 */}
        <div className="history-empty">暂无历史对话</div>
      </div>

      {/* 右侧内容区域 */}
      <div className="right-content">
        {/* 对话内容区域 */}
        <div className="chat-area">
          <div className="chat-window">
            <div className="chat-title">
              如你需要，我还可以为你设计：
            </div>
            <div className="chat-text">
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
          </div>
        </div>

        {/* 底部输入框 */}
        <div className="input-area">
          <input 
            type="text"
            placeholder="请输入您的问题..."
            className="input-box"
          />
          <button className="send-btn">
            发送
          </button>
        </div>
      </div>
    </div>
  );
};

export default Talk;