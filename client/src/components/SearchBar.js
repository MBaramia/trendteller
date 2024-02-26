import { useState } from "react";
import "./SearchBar.css";
import { ReactComponent as MagnifyingGlass } from "../images/smiley_good_green.svg";
import { ReactComponent as Cross } from "../images/smiley_bad_red.svg";


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
      <div className="search-btn">
        {query==="" ? <MagnifyingGlass onClick={focusOnInput} /> : <Cross onClick={emptyQuery} />}
      </div>
    </span>
    </>
  );
}

export default SearchBar;