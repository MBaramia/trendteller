// import React, { useState, useEffect } from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Header from "./components/Header";
import Home from "./pages/Home";
import Browse from "./pages/Browse";
import Search from "./pages/Search";
import Notifications from "./pages/Notifications";
import NavMenu from "./components/NavMenu";
import Company from "./pages/Company";
import Article from "./pages/Article";
import Profile from "./pages/Profile";
import Tutorial from "./pages/Tutorial";
import Login from "./pages/Login";
import { useState, useEffect } from "react";
import Signup from "./pages/Signup";
import { processLogin, checkLoggedIn } from "./Auth";
import Loading from "./components/Loading";
import NavButton from "./components/NavButton";

function App() {
  const [navHidden, setNavHidden] = useState(false);
  // const [data, setData] = useState([{}]);

  // useEffect(() => {
  //   fetch("/members")
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setData(data);
  //       console.log(data);
  //     });
  // }, []);

  // console.log(hasLoaded);

  const [hasLoaded, setHasLoaded] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    checkLoggedIn().then((result) => {
      setIsLoggedIn(result);
      setHasLoaded(true);
      console.log(`loaded: ${hasLoaded}`);
      // console.log(result.status);
    });
  });

  const logInUser = () => {
    setIsLoggedIn(true);
  };

  const logOutUser = () => {
    setIsLoggedIn(false);
  };

  return (
    <>
      {hasLoaded ? (
        <>
          {isLoggedIn ? (
            <>
              <Header />
              <div className="main-view">
                <div className={"nav-section" + (navHidden ? " hide" : "")}>
                  <NavMenu logOutUser={logOutUser} />
                  <NavButton navHidden={navHidden} setNavHidden={setNavHidden} />
                </div>
                <main>
                  <div onClick={()=>{setNavHidden(false)}} className="content-section">
                    <Routes>
                      <Route path="/" element={<Home />} />
                      <Route path="/browse" element={<Browse />} />
                      <Route path="/search/:query" element={<Search />} />
                      <Route
                        path="/notifications"
                        element={<Notifications />}
                      />
                      <Route path="/company/:companyID" element={<Company />} />
                      <Route
                        path="/article/:articleID/:companyID"
                        element={<Article />}
                      />
                      <Route path="/profile" element={<Profile />} />
                      <Route path="/tutorial" element={<Tutorial />} />

                      <Route path="/*" element={<Navigate to="/" />} />
                    </Routes>
                  </div>
                </main>
              </div>
            </>
          ) : (
            <Routes>
              <Route
                path="/signup"
                element={<Signup logInUser={logInUser} />}
              />
              <Route path="/" element={<Login logInUser={logInUser} />} />
              <Route path="/*" element={<Navigate to="/" />} />
            </Routes>
          )}
        </>
      ) : (
        <Loading />
      )}
    </>
  );
}

export default App;
