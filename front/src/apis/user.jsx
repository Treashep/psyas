import { request } from "../utils";

// 1.登录请求
export function loginAPI(formData){
  return request({
    url: '/api/auth/login',
    method: 'POST',
    data: formData
  })
}

export function registerAPI(formData){
  return request({
    url: '/api/auth/register',
    method: 'POST',
    data: formData
  })
}