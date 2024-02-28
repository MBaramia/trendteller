import "./RecommendedCompanyView.css";
import RecommendedCompanyItem from "./RecommendedCompanyItem";

function RecommendedCompanyView({ title, data, idToFollowing, toggleFollowing }) {

  return (
    <>
      <div className="recommended-company-view">
        <h2>{title}</h2>
        <div className="grid-section">
          {data.map((company) => (
            <RecommendedCompanyItem key={company.id} company={company} following={idToFollowing[company.id]} toggleFollowing={toggleFollowing} />
          ))}
        </div>
      </div>
    </>
  );
}

export default RecommendedCompanyView;
