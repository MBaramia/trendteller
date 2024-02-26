import "./SummaryTextView.css";

function SummaryTextView({ title, text }) {

  return (
    <>
      <div className="summary-text-view narrow-content">
        <h2>{title}</h2>
        <div className="text-content">
          <p>{text}</p>
        </div>
      </div>
    </>
  );
}

export default SummaryTextView;
