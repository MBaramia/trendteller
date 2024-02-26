import "./CompanyListView.css";
import { ReactComponent as HeartFill } from "../images/heart_filled.svg";
import { ReactComponent as HeartEmpty } from "../images/heart_empty.svg";
import { useState } from "react";


function CompanyListRow({ company, toggleFollowing }) {
  let [isFollowing, setIsFollowing] = useState(company.following);

  const goToCompanyPage = () => {
    window.location.href = `/company/${company.id}`;
  }

  const toggleCompanyFollow = (e) => {
    toggleFollowing(company.id);
    setIsFollowing(!isFollowing);
    e.stopPropagation();
  }

  const perceptionToComponent = (p) => {
    if (p === 2) {
      return <p style={{ color: "var(--positive)" }}>Good</p>;
    } else if (p === 1) {
      return <p style={{ color: "var(--neutral)" }}>Neutral</p>;
    } else {
      return <p style={{ color: "var(--negative)" }}>Bad</p>;
    }
  };

  const followingToComponent = (f) => {
    if (f) {
      return <HeartFill onClick={toggleCompanyFollow} />
    } else {
      return <HeartEmpty onClick={toggleCompanyFollow} />
    }
  }

  return (
    <>
      <div onClick={goToCompanyPage} className="list-row">
        <p>{company.name} ({company.code})</p>
        <p>£{company.price}</p>
        <p>{company.change}</p>
        <>{perceptionToComponent(company.perception)}</>
        <p className="heart">{followingToComponent(isFollowing)}</p>
      </div>
    </>
  );
}

export default CompanyListRow;
