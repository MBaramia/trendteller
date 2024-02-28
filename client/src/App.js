// import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
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
import { useState } from "react";

function App() {
  // const [data, setData] = useState([{}]);

  // useEffect(() => {
  //   fetch("/members")
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setData(data);
  //       console.log(data);
  //     });
  // }, []);

  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const logInUser = () => {
    setIsLoggedIn(true);
  }

  const logOutUser = () => {
    setIsLoggedIn(false);
  }

  return (
    <Router>
      { isLoggedIn ? (
        <>
          <Header />
          <div className="main-view">
            <NavMenu logOutUser={logOutUser} />
            <main>
              <div className="content-section">
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/browse" element={<Browse />} />
                  <Route path="/search/:query" element={<Search />} />
                  <Route path="/notifications" element={<Notifications/>} />
                  <Route path="/company/:companyID" element={<Company />} />
                  <Route path="/article/:articleID/:companyID" element={<Article />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="/tutorial" element={<Tutorial />} />
                </Routes>
              </div>
            </main>
          </div>
        </>
      ) : (
        <Login logInUser={logInUser} />
      )};
    </Router>
  
    // <div>
    //   <h1>The Title</h1>
    //   {typeof data.members === "undefined" ? (
    //     <p>"Loading..."</p>
    //   ) : (
    //     <p>{data.members}</p>
    //   )}
    // </div>
  );
}

export default App;
