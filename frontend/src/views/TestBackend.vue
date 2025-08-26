<template>
  <div class="test-page">
    <h2>后端接口测试页面</h2>

    <!-- 测试接口1：基础连接 -->
    <div class="test-item">
      <button @click="handleTestHello">测试接口1：基础连接（/api/test/hello）</button>
      <div v-if="helloResult" class="result-box">
        <p>接口1返回结果：</p>
        <pre>{{ JSON.stringify(helloResult, null, 2) }}</pre>
      </div>
    </div>

    <!-- 测试接口2：用户数据处理 -->
    <div class="test-item">
      <button @click="handleTestCreateUser">测试接口2：用户数据处理（/api/test/users）</button>
      <div v-if="userResult" class="result-box">
        <p>接口2返回结果：</p>
        <pre>{{ JSON.stringify(userResult, null, 2) }}</pre>
      </div>
    </div>

    <!-- 测试接口3：问候语生成 -->
    <div class="test-item">
      <input
        v-model="userName"
        placeholder="请输入姓名（可选）"
        class="name-input"
      >
      <button @click="handleTestGreet">测试接口3：问候语生成（/api/test/greet）</button>
      <div v-if="greetResult" class="result-box">
        <p>接口3返回结果：</p>
        <pre>{{ JSON.stringify(greetResult, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
// 导入接口调用方法
import { testHello, testCreateUser, testGreet } from '@/api/testApi'

// 存储接口返回结果
const helloResult = ref(null)
const userResult = ref(null)
const greetResult = ref(null)
// 存储输入的姓名（用于接口3）
const userName = ref('')

// 处理接口1调用
const handleTestHello = async () => {
  try {
    const res = await testHello()
    helloResult.value = res // 展示结果（拦截器已处理，res 直接是后端返回的 data）
    console.log('接口1调用成功：', res)
  } catch (err) {
    console.error('接口1调用失败：', err)
  }
}

// 处理接口2调用
const handleTestCreateUser = async () => {
  try {
    // 准备测试数据
    const data = { name: '前端测试用户', age: 25 }
    const res = await testCreateUser(data)
    userResult.value = res
    console.log('接口2调用成功：', res)
  } catch (err) {
    console.error('接口2调用失败：', err)
  }
}

// 处理接口3调用
const handleTestGreet = async () => {
  try {
    const res = await testGreet(userName.value) // 传入输入的姓名（可为空）
    greetResult.value = res
    console.log('接口3调用成功：', res)
  } catch (err) {
    console.error('接口3调用失败：', err)
  }
}
</script>

<style scoped>
.test-page {
  padding: 20px;
}

.test-item {
  margin: 20px 0;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 4px;
}

button {
  padding: 8px 16px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

button:hover {
  background: #359e75;
}

.name-input {
  padding: 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 10px;
}

.result-box {
  margin-top: 10px;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 4px;
}

pre {
  white-space: pre-wrap; /* 自动换行 */
  word-wrap: break-word;
  color: #333;
}
</style>
