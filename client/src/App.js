// import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Home from "./pages/Home";
import Browse from "./pages/Browse";
import Search from "./pages/Search";
import Notifications from "./pages/Notifications";

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

  return (
    <Router>
      <Header />
      <div className="main-view">
        {/* <NavMenu /> */}
        <div className="content-section">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/browse" element={<Browse />} />
            <Route path="/search" element={<Search query={"Microsoft"}/>} />
            <Route path="/notifications" element={<Notifications/>} />
          </Routes>
        </div>

      </div>
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
