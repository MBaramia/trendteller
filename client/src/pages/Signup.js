import "./Login.css";
import { processLogin, processRegister } from "../Auth";
import { useEffect, useState } from "react";

function Signup({ logInUser }) {
  let [username, setUsername] = useState("");
  let [password, setPassword] = useState("");
  let [errors, setErrors] = useState([]);

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const isUsernameValid = () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(username)) {
      setErrors(["Username must be an email"]);
      return false;
    } 
    return true;
  };

  const isPasswordValid = () => {
    if (password.length < 5) {
      setErrors(["Password must be longer than 5 characters"]);
      return false;
    } else if (password.length > 20) {
      setErrors(["Password must be shorter than 20 characters"]);
      return false;
    }
    return true;
  };

  const validateInput = async () => {
    console.log(errors); 
    if (isUsernameValid() && isPasswordValid()) {
        // console.log("submit");
        submitChanges();
    }
  };

  const submitChanges = async () => {
    console.log(`${username} | ${password}`);
    const register = await processRegister(username, password);
    if (register.status) {
      logInUser();
    } else {
      console.log(register.data);
      setErrors([register.data.message]);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      validateInput();
    }
  };

  return (
    <>
      <div id="login-pg">
        <div className="login-box">
          <h1>Sign up</h1>
          <div className="errors">
            {errors.map((error, index) => (
              <p key={index} className="login-error">
                {error}
              </p>
            ))}
          </div>
          <input
            value={username}
            onChange={handleUsernameChange}
            onKeyDown={handleKeyDown}
            type="text"
            placeholder="Email"
          />
          <input
            value={password}
            onChange={handlePasswordChange}
            onKeyDown={handleKeyDown}
            type="password"
            placeholder="Password"
          />
          <div className="btn-container">
            <button onClick={validateInput}>Sign Up</button>
          </div>
          <p>
            Already have an account? <a href="/singup">Log In</a>
          </p>
        </div>
      </div>
    </>
  );
}

export default Signup;
