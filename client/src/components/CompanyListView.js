import CompanyListRow from "./CompanyListRow";
import "./CompanyListView.css";

function CompanyListView({ title, data }) {
  // view will also take company data as a parameter

  return (
    <>
      <div className="company-list-view">
        <h2>{title}</h2>
        <div className="list-section">
          <div className="list-header">
            <p>Name</p>
            <p>Price</p>
            <p>Change</p>
            <p>Perception</p>
            <p>Following</p>
          </div>
          <div className="list-content">
            {data.map((item) => (
              <CompanyListRow key={item.id} company={item} />
            ))}
          </div>  
        </div>
      </div>
    </>
  );
}

export default CompanyListView;
