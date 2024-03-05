import { useEffect, useState } from "react";
import "./Profile.css";
import { processUpdate, getUserData } from "../Auth";
import Loading from "../components/Loading";

function Profile() {

  const [hasLoaded, setHasLoaded] = useState(false);

  let [email, setEmail] = useState("");
  let [password, setPassword] = useState("");
  let [errors, setErrors] = useState([]);
  let [update, setUpdate] = useState("");

  useEffect(() => {
    getUserData().then((result) => {
      setEmail(result.data.username);
      setHasLoaded(true);
    });
  }, []);

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const isUsernameValid = () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setErrors(["Email is not of correct form"]);
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
    setUpdate("");
    console.log(errors); 
    if (isUsernameValid() && isPasswordValid()) {
      // console.log("submit");
      submitChanges();
    }
  };

  const submitChanges = async () => {
    const update = await processUpdate(email, password);
    if (update.status) {
      console.log(update.data);
      if (update.data.success) {
        setErrors([]);
        setUpdate(update.data.message);
      } else {
        setErrors([update.data.message]);
      }
    } else {
      console.log(update.data);
    }
  };

  return (
    <>
      <div id="profile-pg">
        <div className="form-area narrow-content">
          <h2>Profile</h2>
          {hasLoaded ?<>
            <div className="errors">
            {errors.map((error, index) => (
              <p key={index} className="login-error">
                {error}
              </p>
            ))}
            </div>
            <div className="update">
              <p>{update}</p>
            </div>
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
              <button onClick={validateInput}>Submit</button>
            </span>
          </>:<>
            <Loading />
          </>}
        </div>
      </div>
    </>
  );
}

export default Profile;
