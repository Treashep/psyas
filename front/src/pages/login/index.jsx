import Bar from "../../components/bar"
import '/src/pages/login/index.css';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
      username: '',
      password: ''
    });
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  const handleNavigation = (path) => {
    navigate(path);
  };
  const handleLogin = () => {
  const { username, password } = formData;
  if (!username || !password) {
     alert('请输入完整信息！');
    return;
  }
  // 这里发送请求到后端验证
  // 例如使用 fetch 或 axios
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
        <div className="login">
          <div className="title">
            <span className="active" onClick={() => handleNavigation('/login')}>登录</span>
            <span className="divider">|</span>
            <span onClick={() => handleNavigation('/register')}>注册</span>
          </div>
          <div className="form">
            <div className="input-group">
              <input 
                name="username"
                value={formData.username}
                type="text" 
                placeholder="用户名/手机号/邮箱" 
                autoComplete="off"
                onChange={handleInputChange}
              />
            </div>
            <div className="input-group">
              <input 
                name="password"
                value={formData.password}
                type="password" 
                placeholder="请输入密码" 
                autoComplete="off"
                onChange={handleInputChange}
              />
            </div>
            <div className="remember">
              <label>
                <input type="checkbox" />
                <span>记住密码</span>
              </label>
              <a href="#" className="forget">忘记密码？</a>
            </div>
            <button className="login-btn" onClick={handleLogin}>登 录</button>
            <div className="extra-link">
              <a href="#">意见反馈</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
  
}

export default Login