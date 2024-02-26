import { useState } from 'react';
import './Profile.css'

function Profile() {
  const userData = {email: "myemail@gmail.com"}

  let [email, setEmail] = useState(userData.email);
  let [password, setPassword] = useState("");

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  }

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  }

  const validatePassword = () => {
    return true;
  }

  const submitChanges = () => {
    if (validatePassword()) {
      console.log(`${email} | ${password}`);
    }
  }

  return (
    <>
    <div id='profile-pg'>
      <div className='form-area narrow-content'>
          <h2>Profile</h2>
          <input type='text' id="email" placeholder='New Email' value={email} onChange={handleEmailChange} />
          <input type='password' id="password" placeholder='New Password' value={password} onChange={handlePasswordChange} />
          <span className='btn-container'>
            <button onClick={submitChanges}>Submit</button>
          </span>
      </div>
    </div>
    </>
  );
}
  
export default Profile;