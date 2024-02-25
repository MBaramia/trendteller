import "./RecommendedCompanyView.css";
import RecommendedCompanyItem from "./RecommendedCompanyItem";

function RecommendedCompanyView({ title, data }) {
  // view will also take company data as a parameter

  return (
    <>
      <div className="recommended-company-view">
        <h2>{title}</h2>
        <div className="grid-section">
          {data.map((item) => (
            <RecommendedCompanyItem key={item.id} company={item} />
          ))}
        </div>
      </div>
    </>
  );
}

export default RecommendedCompanyView;
