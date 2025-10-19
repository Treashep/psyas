import { fetchRegister } from "../../store/modules/user";
import '/src/pages/register/index.css';
import '/src/components/icon/iconfont.css';
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
const Register = ()=>{
    const navigate = useNavigate();
    const dispatch = useDispatch();

    //跳转逻辑
    const handleNavigation = (path) => {
      navigate(path);
    };

    const [form, setForm] = useState({
      username: '',
      password: ''
    });

    const [showPassword, setShowPassword] = useState(false);

    const handleSubmit = async (e) => {
      e.preventDefault();

      // 等待注册结果
      const result = await dispatch(fetchRegister(form));

      if (result.meta.requestStatus === 'fulfilled') {
        // 注册成功，跳转到登录页
        alert('注册成功，请登录');
        navigate('/'); // 跳转到登录页
      } else {
        // 注册失败，提示错误
        alert('注册失败：' + result.payload); // result.payload 是错误信息
      }
    };

  return (
    <div className="register-body">
      <div className="register">
        <div className="title">
          <span>注册</span>
        </div>
        <div className="form">
          {/* 隐藏的虚拟输入框，用于欺骗浏览器的自动填充 */}
          <input type="text" style={{display: 'none'}} />
          <input type="password" style={{display: 'none'}} />
          
          <div className="input-group">
            <span className="iconfont icon-yonghu input-icon"></span>
            <input 
              name="user-input"
              type="text" 
              placeholder="用户名" 
              autoComplete="new-password"
              autoCorrect="off"
              autoCapitalize="off"
              spellCheck="false"
              value={form.username}
              onChange={(e) => setForm({...form, username: e.target.value})}
            />
          </div>
          <div className="input-group">
            <span className="iconfont icon-suoding input-icon"></span>
            <input 
              name="pass-input"
              type={showPassword ? "text" : "password"} 
              placeholder="密码" 
              autoComplete="new-password"
              autoCorrect="off"
              autoCapitalize="off"
              spellCheck="false"
              value={form.password}
              onChange={(e) => setForm({...form, password: e.target.value})}
            />
            <span 
              className={`iconfont ${showPassword ? 'icon-yanjing1' : 'icon-yanjing'} password-toggle`}
              onClick={() => setShowPassword(!showPassword)}
            ></span>
          </div>
          <button className="register-btn" onClick={handleSubmit}>注 册</button>
          <div className="extra-link">
            <a href="#">忘记密码？</a>
            <span className="switch-link" onClick={() => handleNavigation('/')}>登录</span>
          </div>
        </div>
      </div>
    </div>
  )
  
}

export default Register