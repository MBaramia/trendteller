// import React, { useState, useEffect } from "react";
// import Login from './pages/Login';
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CompanyListView from "./components/CompanyListView";
import Header from "./components/Header";
import RecommendedCompanies from "./components/RecommendedCompanies";

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
      <div className="content-section">
        <Routes>
          <Route path="/" element={<CompanyListView title={"Companies"} />} />
        </Routes>
        <RecommendedCompanies title={"Recommended Companies"}/>
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
