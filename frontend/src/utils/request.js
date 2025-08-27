// src/utils/request.js
import axios from 'axios'

// 1. 创建 axios 实例，配置基础路径（后端接口的根地址）
const service = axios.create({
  baseURL: 'http://localhost:5000',  // 从前端环境变量读取后端地址
  timeout: 5000  // 请求超时时间（5秒）
})

// 2. 请求拦截器（发送请求前做处理，如加 Token）
service.interceptors.request.use(
  config => {
    // 示例：如果有登录 Token，添加到请求头
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    // 请求错误时的处理（如打印日志）
    console.error('请求拦截器错误：', error)
    return Promise.reject(error)
  }
)

// 3. 响应拦截器（接收后端响应后做处理，如统一错误提示）
service.interceptors.response.use(
  response => {
    // 只返回响应体中的 data（忽略状态码等元数据，简化使用）
    return response.data
  },
  error => {
    // 统一处理错误（如 401 未登录、500 服务器错误）
    console.error('响应拦截器错误：', error)
    // 示例：401 时跳转到登录页
    if (error.response?.status === 401) {
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// 4. 导出封装好的 axios 实例，供其他组件使用
export default service