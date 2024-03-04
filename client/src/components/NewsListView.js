import "./NewsListView.css";
import NewsListItem from "./NewsListItem";
import Loading from "./Loading";

function NewsListView({ hasLoaded, title, data }) {
  // view will also take news data as a parameter

  return (
    <>
      <div className="news-list-view narrow-content">
        <h2>{title}</h2>
        <div className="list-section">
          {hasLoaded ? <>
            {data.map((item) => (
                <NewsListItem key={item.id} article={item} />
            ))}
          </>:<>
              <Loading />
          </>}
          
        </div>
      </div>
    </>
  );
}

export default NewsListView;
