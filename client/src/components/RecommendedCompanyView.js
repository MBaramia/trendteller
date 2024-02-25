import "./RecommendedCompanyView.css";
import RecommendedCompanyItem from "./RecommendedCompanyItem";

function RecommendedCompanyView({ title }) {
  // view will also take company data as a parameter
  const data = [
    {
      id: 15,
      name: "Oracle",
      code: "ORCL",
      price: "82.49",
      change: "+9.3%",
      perception: 0,
      following: true,
    },
    {
      id: 7,
      name: "PayPal",
      code: "PYPL",
      price: "220.61",
      change: "-14.9%",
      perception: 2,
      following: true,
    },
    {
      id: 9,
      name: "Adobe",
      code: "ADBE",
      price: "632.24",
      change: "+21.3%",
      perception: 1,
      following: false,
    }
  ];

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
