import "./NewsListView.css";
import NewsListItem from "./NewsListItem";

function NewsListView({ title, data }) {
  // view will also take news data as a parameter

  return (
    <>
      <div className="news-list-view">
        <h2>{title}</h2>
        <div className="list-section">
          {data.map((item) => (
            <NewsListItem key={item.id} article={item} />
          ))}
        </div>
      </div>
    </>
  );
}

export default NewsListView;
