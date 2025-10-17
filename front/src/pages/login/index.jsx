import '/src/pages/login/index.css';
import '/src/components/icon/iconfont.css';
import { useNavigate } from 'react-router-dom';
import { useState } from "react";
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
    email:''
  });

  const [showPassword, setShowPassword] = useState(false);

  //登录按钮逻辑
  const handleSubmit = async (e) => {
    e.preventDefault();

    // 判断结果
    const result = await dispatch(fetchLogin(form));

    if (result.meta.requestStatus === 'fulfilled') {
      navigate('/talk'); // 登录成功
    } else {
      alert('登录失败：' + result.payload); // 显示错误
    }
  };

  return (
    <div className="body">
      <div className="login">
        <div className="title">
          <span>登录</span>
        </div>
        <div className="form">
          {/* 隐藏的虚拟输入框，用于欺骗浏览器的自动填充 */}
          <input type="text" style={{display: 'none'}} />
          <input type="password" style={{display: 'none'}} />
          
          <div className="input-group">
            <span className="iconfont icon-yonghu input-icon"></span>
            <input 
              name="username"
              type="text" 
              placeholder="用户名/手机号/邮箱" 
              autoComplete="new-password"
              autoCorrect="off"
              autoCapitalize="off"
              spellCheck="false"
              onChange={(e) => setForm({...form, username: e.target.value})}
              value={form.username}
            />
          </div>
          <div className="input-group">
            <span className="iconfont icon-suoding input-icon"></span>
            <input 
              name="password"
              value={form.password}
              type={showPassword ? "text" : "password"} 
              placeholder="请输入密码" 
              autoComplete="new-password"
              autoCorrect="off"
              autoCapitalize="off"
              spellCheck="false"
              onChange={(e) => setForm({...form, password: e.target.value})}
            />
            <span 
              className={`iconfont ${showPassword ? 'icon-yanjing1' : 'icon-yanjing'} password-toggle`}
              onClick={() => setShowPassword(!showPassword)}
            ></span>
          </div>
          <button className="login-btn" onClick={handleSubmit}>登 录</button>
          <div className="extra-link">
            <a href="#">忘记密码？</a>
            <span className="switch-link" onClick={() => handleNavigation('/register')}>注册</span>
          </div>
        </div>
      </div>
    </div>
  )
  
}

export default Login