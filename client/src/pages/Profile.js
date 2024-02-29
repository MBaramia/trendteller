import { useEffect, useState } from "react";
import "./Profile.css";
import { processUpdate, getUserData } from "../Auth";

function Profile() {
  const userData = { email: "myemail@gmail.com" };

  let [email, setEmail] = useState(userData.email);
  let [password, setPassword] = useState("");

  useEffect(() => {
    getUserData().then((result) => {
      setEmail(result.data.username);
    });
  });

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const validatePassword = () => {
    return true;
  };

  const submitChanges = async () => {
    if (validatePassword()) {
      console.log(`${email} | ${password}`);
      const update = await processUpdate(email, password);
      if (update.status) {
        console.log(update.data);
      } else {
        console.log(update.data);
      }
    }
  };

  return (
    <>
      <div id="profile-pg">
        <div className="form-area narrow-content">
          <h2>Profile</h2>
          <input
            type="text"
            id="email"
            placeholder="New Email"
            value={email}
            onChange={handleEmailChange}
          />
          <input
            type="password"
            id="password"
            placeholder="New Password"
            value={password}
            onChange={handlePasswordChange}
          />
          <span className="btn-container">
            <button onClick={submitChanges}>Submit</button>
          </span>
        </div>
      </div>
    </>
  );
}

export default Profile;
