import { useState } from "react";
import "./SearchBar.css";
import { ReactComponent as Cross } from "../images/close_icon.svg";


function SearchBar() {
  let [query, setQuery] = useState("");

  const handleChange = (e) => {
    setQuery(e.target.value);
  }

  const focusOnInput = () => {
    document.getElementById("search-input").focus();
  }

  const emptyQuery = () => {
    setQuery("");
    focusOnInput();
  }

  const submitSearch = (e) => {
    if (e.key === "Enter") {
      window.location.href=`/search/${query}`;
    }
  }

  return (
    <>
    <span id="search-bar">
      <input value={query} onChange={handleChange} onKeyDown={submitSearch} id="search-input" type="text" placeholder="Search" />
      {(query!=="") && <div className="search-btn"><Cross onClick={emptyQuery} /></div>}
    </span>
    </>
  );
}

export default SearchBar;