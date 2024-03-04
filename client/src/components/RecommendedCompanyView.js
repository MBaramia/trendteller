import "./RecommendedCompanyView.css";
import RecommendedCompanyItem from "./RecommendedCompanyItem";
import Loading from "./Loading";

function RecommendedCompanyView({ hasLoaded, title, data, idToFollowing, toggleFollowing }) {

  return (
    <>
      <div className="recommended-company-view">
        <h2>{title}</h2>
        <div className="grid-section">
          {hasLoaded ? <>
          {data.map((company) => (
            <RecommendedCompanyItem key={company.id} company={company} following={idToFollowing[company.id]} toggleFollowing={toggleFollowing} />
          ))}
          </>:<>
          <Loading />
          </>}
        </div>
      </div>
    </>
  );
}

export default RecommendedCompanyView;
