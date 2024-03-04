import Loading from "./Loading";
import "./SummaryTextView.css";

function SummaryTextView({ hasLoaded, title, text }) {

  return (
    <>
      <div className="summary-text-view narrow-content">
        <h2>{title}</h2>
        {hasLoaded ? <>
          <div className="text-content">
            <p>{text}</p>
          </div>
        </>: <>
          <Loading />
        </>
        }
      </div>
    </>
  );
}

export default SummaryTextView;
