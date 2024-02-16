import './Login.css'

function Login() {
  
    return (
      <>
      <div id='login-pg'>
        <div className='login-box'>
          <h1>Log in</h1>
          <input type='text' placeholder='username'/>
          <input type='password' placeholder='password'/>
          <button>Submit</button>
        </div>
      </div>
      </>
    );
  }
  
  export default Login;