import '/src/pages/login/index.css';
import { useNavigate } from 'react-router-dom';
import { useState,useEffect } from "react";
import { fetchLogin } from "../../store/modules/user";
import { useDispatch } from "react-redux";

const Login = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  //跳转逻辑
  const handleNavigation = (path) => {
    navigate(path);
  };

  const [form, setForm] = useState({
    username: '',
    password: '',
    email:'',
    remember: false
  });

  //登录按钮逻辑
  const handleSubmit = async (e) => {
    e.preventDefault();

    // 保存"记住密码"
    if (form.remember) {
      localStorage.setItem('login_remember', JSON.stringify({
        username: form.username,
        password: form.password
      }));
    } else {
      localStorage.removeItem('login_remember');
    }

    // ✅ 现在可以判断结果了
    const result = await dispatch(fetchLogin(form));

    if (result.meta.requestStatus === 'fulfilled') {
      navigate('/talk'); // 登录成功
    } else {
      alert('登录失败：' + result.payload); // 显示错误
    }
  };

    // 初始化：读取"记住的密码"
  useEffect(() => {
    const saved = localStorage.getItem('login_remember');
    if (saved) {
      const { username, password } = JSON.parse(saved);
      setForm(prev => ({ ...prev, username, password, remember: true }));
    }
  }, []);

  return (
    <div className="body">
      <div className="right">
        <div className="login">
          <div className="title">
            <span className="active">登录</span>
          </div>
          <div className="form">
            <div className="input-group">
              <input 
                name="username"
                type="text" 
                placeholder="用户名/手机号/邮箱" 
                autoComplete="off"
                onChange={(e) => setForm({...form, username: e.target.value})}
                value={form.username}
              />
            </div>
            <div className="input-group">
              <input 
                name="password"
                value={form.password}
                type="password" 
                placeholder="请输入密码" 
                autoComplete="off"
                onChange={(e) => setForm({...form, password: e.target.value})}
              />
            </div>
            <div className="remember">
              <label>
                <input
                 type="checkbox" 
                 checked={form.remember}
                 onChange={(e) => setForm({...form, remember: e.target.checked})}
                />
                <span>记住密码</span>
              </label>
              <a href="#" className="forget">忘记密码？</a>
            </div>
            <button className="login-btn" onClick={handleSubmit}>登 录</button>
            <div className="extra-link">
              <a href="#">意见反馈</a>
              <span className="switch-link" onClick={() => handleNavigation('/register')}>注册</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
  
}

export default Login