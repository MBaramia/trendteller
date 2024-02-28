import './Login.css'

function Login({ logInUser }) {
  const errors = ["Error Message 1", "Error Message 2"];
  // const error = "";
  
  return (
    <>
    <div id='login-pg'>
      <div className='login-box'>
        <h1>Log In</h1>
        <div className='errors'>
          {errors.map((error, index) => (
            <p key={index} className='login-error'>{error}</p>
          ))}
        </div>
        <input type='text' placeholder='Email'/>
        <input type='password' placeholder='Password'/>
        <div className='btn-container'>
          <button>Log In</button>
        </div>
        <p>New? <a href='/'>Sign up</a></p>
      </div>
    </div>
    </>
  );
}
  
export default Login;