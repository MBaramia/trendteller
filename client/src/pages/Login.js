import "./Login.css";
import { processLogin } from "../Auth";
import { useState } from "react";

function Login({ logInUser }) {
  let [username, setUsername] = useState("");
  let [password, setPassword] = useState("");

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const submitChanges = async () => {
    console.log(`${username} | ${password}`);
    const logIn = await processLogin(username, password);
    if (logIn.status) {
      logInUser();
    } else {
      console.log(logIn.data);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      submitChanges();
    }
  };

  const errors = ["Error Message 1", "Error Message 2"];
  // const error = "";

  return (
    <>
      <div id="login-pg">
        <div className="login-box">
          <h1>Log In</h1>
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
            <button onClick={submitChanges}>Log In</button>
          </div>
          <p>
            New? <a href="/">Sign up</a>
          </p>
        </div>
      </div>
    </>
  );
}

export default Login;
