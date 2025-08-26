import axios from 'axios';
const request = axios.create({
  // 基础路径，从环境变量获取，这样在开发、测试、生产环境可以灵活配置
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 5000, // 设置请求超时时间为 5 秒
  headers: {
    'Content-Type': 'application/json' // 默认请求头，适用于大多数 JSON 数据交互场景
  }
});
export default request;