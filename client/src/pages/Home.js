import CompanyListView from '../components/CompanyListView';
import NewsListView from '../components/NewsListView';
import RecommendedCompanyView from '../components/RecommendedCompanyView';
// import './Home.css'

function Home() {
  
  return (
    <>
    <div id='home-pg'>
      <CompanyListView title={"Followed Companies"} />
      <RecommendedCompanyView title={"Recommended For You"} />
      <NewsListView title={"News"} />
    </div>
    </>
  );
}
  
export default Home;