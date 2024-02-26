import "./NewsListView.css";
import { ReactComponent as SmileyGood } from "../images/smiley_good_green.svg";
import { ReactComponent as SmileyNeutral} from "../images/smiley_neutral_grey.svg";
import { ReactComponent as SmileyBad } from "../images/smiley_bad_red.svg";

function NewsListItem({ article }) {

  const goToCompanyPage = () => {
    window.location.href = `/company/${article.companyID}`;
  }

  const goToArticlePage = () => {
    window.location.href = `/article/${article.id}/${article.companyID}`;
  }

  const perceptionToSmiley = (p) => {
    if (p === 2) {
      return <SmileyGood className="smiley" />;
    } else if (p === 1) {
      return <SmileyNeutral className="smiley" />;
    } else {
      return <SmileyBad className="smiley" />;
    }
  }

  return (
    <>
      <div className="list-item">
        <div onClick={goToCompanyPage} className="item-left">
          <p>{article.companyCode}</p>
        </div>
        <div onClick={goToArticlePage} className="item-main">
          <div className="item-text">
            <div className="text-top">
              <p>{article.title}</p>
            </div>
            <div className="text-bottom">
              <p>{article.source}</p>
              <p>{article.date}</p>
            </div>                
          </div>
          <div className="item-right">
            <>{perceptionToSmiley(article.perception)}</>
          </div>
        </div>
      </div>
    </>
  );
}

export default NewsListItem;
