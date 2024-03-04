import CompanyListRow from "./CompanyListRow";
import "./CompanyListView.css";
import Loading from "./Loading";

function CompanyListView({ hasLoaded, title, data, idToFollowing, toggleFollowing }) {

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
            {hasLoaded ? <>
              {data.map((company) => (
                <CompanyListRow
                  key={company.id} 
                  company={company} 
                  following={idToFollowing[company.id]} 
                  toggleFollowing={toggleFollowing}
                />
              ))}
            </>:<>
            <Loading />
            </>}
          </div>  
        </div>
      </div>
    </>
  );
}

export default CompanyListView;
