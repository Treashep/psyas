// 导入封装好的 axios 实例（带拦截器）
import request from '@/utils/request'

// 测试接口1：基础连接测试（GET）
export const testHello = () => {
  return request({
    url: '/test/hello', // 实际请求地址：baseURL + /test/hello（baseURL 是 /api，对应后端 /api/test/hello）
    method: 'GET'
  })
}

// 测试接口2：用户数据处理（POST）
export const testCreateUser = (userData) => {
  return request({
    url: '/test/users',
    method: 'POST',
    data: userData // 传入用户数据（{ name: 'xxx', age: xxx }）
  })
}

// 测试接口3：问候语生成（GET，带URL参数）
export const testGreet = (name) => {
  return request({
    url: '/test/greet',
    method: 'GET',
    params: { name } // URL参数：?name=xxx（如果name为空，后端会用默认值）
  })
}
