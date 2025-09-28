import Bar from "../../components/bar"
import { fetchRegister } from "../../store/modules/user";
import '/src/pages/login/index.css';
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
      password: '',
      email:'',
      remember: false
    });

    const handleSubmit = async (e) => {
      e.preventDefault();

      // 保存“记住密码”
      if (form.remember) {
        localStorage.setItem('login_remember', JSON.stringify({
          username: form.username,
          password: form.password
        }));
      } else {
        localStorage.removeItem('login_remember');
      }

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
            <span onClick={() => handleNavigation('/')}>登录</span>
            <span className="divider">|</span>
            <span className="active" onClick={() => handleNavigation('/register')}>注册</span>
          </div>
          <div className="form">
            <div className="input-group">
              <input
                name="password"
                type="text" 
                placeholder="用户名/手机号/邮箱" 
                autoComplete="off"
                onChange={(e) => setForm({...form, username: e.target.value})}
                value={form.username}
              />
            </div>
            <div className="input-group">
              <input
                type="password" 
                placeholder="请输入密码" 
                autoComplete="off"
                value={form.password}
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
            </div>
          </div>
        </div>
      </div>
    </div>
  )
  
}

export default Register