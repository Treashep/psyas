import Bar from "../../components/bar"
import '/src/pages/login/index.css';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();

  const handleNavigation = (path) => {
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
        <div className="login">
          <div className="title">
            <span className="active" onClick={() => handleNavigation('/login')}>登录</span>
            <span className="divider">|</span>
            <span onClick={() => handleNavigation('/register')}>注册</span>
          </div>
          <div className="form">
            <div className="input-group">
              <input 
                type="text" 
                placeholder="用户名/手机号/邮箱" 
                autoComplete="off"
              />
            </div>
            <div className="input-group">
              <input 
                type="password" 
                placeholder="请输入密码" 
                autoComplete="off"
              />
            </div>
            <div className="remember">
              <label>
                <input type="checkbox" />
                <span>记住密码</span>
              </label>
              <a href="#" className="forget">忘记密码？</a>
            </div>
            <button className="login-btn">登 录</button>
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