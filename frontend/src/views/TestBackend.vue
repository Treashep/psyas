<template>
  <div class="test-backend">
    <h2>前后端连接测试</h2>

    <!-- 测试 1：基础连接 -->
    <div class="test-item">
      <button @click="testHello">测试 GET 接口</button>
      <p v-if="helloMsg">{{ helloMsg }}</p>
    </div>

    <!-- 测试 2：查询用户 -->
    <div class="test-item">
      <input v-model="username" placeholder="输入用户名" />
      <button @click="testGetUser">查询用户</button>
      <p v-if="userData">{{ userData }}</p>
    </div>

    <!-- 测试 3：创建用户 -->
    <div class="test-item">
      <input v-model="newUser.username" placeholder="新用户名" />
      <input v-model="newUser.email" placeholder="新用户邮箱" />
      <button @click="testCreateUser">创建用户</button>
      <p v-if="createMsg">{{ createMsg }}</p>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request';

export default {
  data() {
    return {
      helloMsg: '',
      username: '默认用户',
      userData: '',
      newUser: { username: '', email: '' },
      createMsg: ''
    };
  },
  methods: {
    async testHello() {
      const res = await request.get('/test/hello');
      this.helloMsg = res.message;
    },
    async testGetUser() {
      const res = await request.get('/test/user', {
        params: { username: this.username }
      });
      this.userData = JSON.stringify(res.data);
    },
    async testCreateUser() {
      if (!this.newUser.username || !this.newUser.email) {
        this.createMsg = '请填写完整信息';
        return;
      }
      const res = await request.post('/test/user', this.newUser);
      this.createMsg = res.message;
      this.newUser = { username: '', email: '' }; // 清空输入
    }
  }
};
</script>

<style scoped>
.test-backend { padding: 20px; }
.test-item { margin: 20px 0; }
button { margin: 5px; }
</style>