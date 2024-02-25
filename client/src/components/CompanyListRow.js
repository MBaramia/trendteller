import "./CompanyListView.css";
import { ReactComponent as HeartFill } from "../images/heart_filled.svg";
import { ReactComponent as HeartEmpty } from "../images/heart_empty.svg";


function CompanyListRow({ company }) {

  const toggleCompanyFollow = () => {
    // company.follow = !company.follow;
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
      return <HeartFill />
    } else {
      return <HeartEmpty />
    }
  }

  return (
    <>
      <div className="list-row">
        <p>{company.name} ({company.code})</p>
        <p>£{company.price}</p>
        <p>{company.change}</p>
        <>{perceptionToComponent(company.perception)}</>
        <p className="heart" onClick={toggleCompanyFollow}>{followingToComponent(company.following)}</p>
      </div>
    </>
  );
}

export default CompanyListRow;
