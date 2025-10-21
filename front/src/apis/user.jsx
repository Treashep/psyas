import { request } from "../utils";

// 1.登录请求
export function loginAPI(formData){
  return request({
    url: '/api/auth/login',
    method: 'POST',
    data: formData
  })
}

// 2. 注册请求
export function registerAPI(formData){
  return request({
    url: '/api/auth/register',
    method: 'POST',
    data: formData
  })
}

// 4. 获取当前用户信息
export function getMeAPI() {
  return request({
    url: '/api/auth/me',
    method: 'GET'
  });
}

// 5. 刷新 Token
export function refreshAPI(refreshToken) {
  return request({
    url: '/api/auth/refresh',
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${refreshToken}`
    }
  });
}