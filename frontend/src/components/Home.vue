<template>
  <div>
    <nav class="navbar">
      <div class="navbar-title">心理分析助手</div>
      <ul class="navbar-links">
        <input type="text" class="search-input" placeholder="搜索...">
        <li><a href="#">登录</a></li>
        <li><a href="#">注册</a></li>
        <li><a href="#">首页</a></li>
        <li><a href="#">心理测试</a></li>
        <li><a href="#">专家咨询</a></li>
        <li><a href="#">关于我们</a></li>
      </ul>
    </nav>
    <div class="main-content">
      <h2>欢迎来到心理分析助手</h2>
      <p>
        在快节奏的现代生活中，情绪波动、压力困扰、人际关系难题时常悄然影响着我们的幸福感与生活质量。<br>
        你是否也曾感到迷茫、焦虑，或在夜深人静时渴望一个倾听与理解的声音？<br>
        心理分析助手，是一个致力于帮助每个人更好地认识自己、理解情绪、释放压力的在线心理支持平台。我们结合现代心理学理论与前沿科技，打造一个安全、私密、非评判的数字空间，陪伴你开启一段深入内心的旅程。<br>
        在这里，你无需面对面对面咨询的压力，也不必担心被误解。通过智能引导式问答、情绪记录工具、个性化解析报告与心理知识科普，我们帮助你：<br><br>
        觉察情绪模式：识别日常情绪背后的心理动因<br>
        理解行为根源：探索习惯、反应与思维模式的深层原因<br>
        获得自我洞察：从心理学视角解读你的内心世界<br>
        学习心理知识：掌握实用的心理调适技巧与成长方法<br><br>
        我们不是替代专业心理咨询的工具，而是你心理成长路上的启蒙者、陪伴者与引导者。无论你是想提升自我认知、改善人际关系，还是缓解轻度情绪困扰，心理分析助手都愿成为你心灵旅程中的一盏温柔灯火。
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 95%;
  height: 60px;
  background: #1b62b2;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  z-index: 1000;
  padding: 0 40px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.navbar-title {
  font-size: 22px;
  font-weight: bold;
  margin-right: 60px;
}
.navbar-links {
  list-style: none;
  display: flex;
  margin-left: auto;
  margin-right: 20px;
  padding: 0;
}
.navbar-links li {
  margin-left: 30px;
}
.navbar-links a {
  color: #fff;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.2s;
}
.navbar-links a:hover {
  color: #ffd700;
}
.navbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
.search-input {
  padding: 6px 12px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 15px;
}
.login-btn,
.register-btn {
  padding: 6px 16px;
  border: none;
  border-radius: 4px;
  background: #fff;
  color: #1b62b2;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.login-btn:hover,
.register-btn:hover {
  background: #ffd700;
  color: #1b62b2;
}
.main-content {
  margin-top: 80px;
  text-align: center;
  padding: 40px 20px;
}
.main-content h1 {
  font-size: 32px;
  margin-bottom: 20px;
}
.main-content p {
  font-size: 16px;
  color: #333;
  line-height: 1.8;
  text-align: left;
}
</style>
