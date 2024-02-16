import './Login.css'

function Login() {

  const error = "Error message";
  // const error = "";
  
  return (
    <>
    <div id='login-pg'>
      <div className='login-box'>
        <h1>Log In</h1>
        <p className='login-error'>{error}</p>
        <input type='text' placeholder='Email'/>
        <input type='password' placeholder='Password'/>
        <button>Log In</button>
        <p>New? <a href='/'>Sign up</a></p>
      </div>
    </div>
    </>
  );
}
  
  export default Login;