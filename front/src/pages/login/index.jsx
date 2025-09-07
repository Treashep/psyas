import Bar from "../bar"
import '/src/pages/login/index.css';
const Login = ()=>{
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
      <div className="right">22</div>
    </div>
  )
  
}

export default Login