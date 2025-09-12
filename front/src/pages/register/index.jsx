import Bar from "../../components/bar"
import './index.css';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: ''
  });
  const [rememberPassword, setRememberPassword] = useState(false);

  // 组件加载时检查localStorage
  useEffect(() => {
    const savedData = localStorage.getItem('registerData');
    if (savedData) {
      const parsedData = JSON.parse(savedData); //json化账户信息
      setFormData(parsedData); // 进入页面填充信息
      setRememberPassword(true); // 自动勾选
    }
  }, []);

  // 处理输入变化
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // 处理记住密码变化
  const handleRememberChange = (e) => {
    const isChecked = e.target.checked;
    setRememberPassword(isChecked);
    
    if (isChecked) {
      localStorage.setItem('registerData', JSON.stringify(formData));
    }
  };

  const handleNavigation = (path) => {
    if (path === '/login' && formData) {
      // 检查是否有空值
      if (!formData.username || !formData.password || !formData.confirmPassword) {
        alert('请填写完整信息！');
        return;
      }
      // 检查两次密码是否一致
      if (formData.password !== formData.confirmPassword) {
        alert('两次输入的密码不一致！');
        return;
      }
    }
    navigate(path);
  };

  return (
    <div className="body">
      <Bar />
      <div className="left">
        <p>
          那些知道为了什么而活的人几乎可以承受任何磨难；
        </p>
        <p>
          谁懂得了为什么生活，谁就能承受任何一种生活。
        </p>
        <p className="people">
          ————尼采
        </p>
      </div>
      <div className="right">
        <div className="register">
          <div className="title">
            <span onClick={() => handleNavigation('/login')}>登录</span>
            <span className="divider">|</span>
            <span className="active" onClick={() => handleNavigation('/register')}>注册</span>
          </div>
          <div className="form">
            <div className="input-group">
              <input 
                type="text" 
                placeholder="用户名/手机号/邮箱" 
                autoComplete="new-password"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
              />
            </div>
            <div className="input-group">
              <input 
                type="password" 
                placeholder="请输入密码" 
                autoComplete="new-password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
              />
            </div>
            <div className="input-group">
              <input 
                type="password"
                autoComplete="new-password"
                placeholder="请再次输入密码" 
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
              />
            </div>
            <div className="remember">
              <label>
                <input 
                  type="checkbox"
                  checked={rememberPassword}
                  onChange={handleRememberChange}
                />
                <span>记住密码</span>
              </label>
            </div>
            <button 
              className="register-btn" 
              onClick={() => {
                if (rememberPassword) {
                  localStorage.setItem('registerData', JSON.stringify(formData));
                }
                handleNavigation('/login')
              }}
            >
              注 册
            </button>
            <div className="extra-link">
              <a href="#">意见反馈</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
  
}

export default Register