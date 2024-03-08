import './StockChart.css';
import { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ReactComponent as SmileyGood } from "../images/smiley_good_green.svg";
import { ReactComponent as SmileyNeutral} from "../images/smiley_neutral_grey.svg";
import { ReactComponent as SmileyBad } from "../images/smiley_bad_red.svg";
import { getStockData, getPredictedStockData, getMainStockData, getStockChanges, getStockDates, getPredictedStockDates } from '../Auth';
import Loading from './Loading';

function StockChart({ company }) {

    const [timeScale, setTimeScale] = useState(0);
    const [stockData, setStockData] = useState(null);
    const [mainData, setMainData] = useState({});
    const [changes, setChanges] = useState([]);
    const [dates, setDates] = useState(null);
    const [predictedDates, setPredictedDates] = useState(null);
    const [hasLoaded, setHasLoaded] = useState(false);

    const [normalChartData, setNormalChartData] = useState([[],[],[],[]]);
    const [predictedChartData, setPredictedChartData] = useState([[],[],[],[]]);

    useEffect(() => {
        getStockData(company.id)
          .then((result) => {
            setStockData(result.data);
            return getMainStockData(company.id);
          }).then((result) => {
            setMainData(result.data);
            return getStockChanges(company.id);
          }).then((result) => {
            setChanges(result.data.data);
            return getStockDates(company.id);
          }).then((result) => {
            setDates(result.data);
            return getPredictedStockDates(company.id);
          }).then((result) => {
            setPredictedDates(result.data);
          });
    }, []);

    useEffect(() => {
        if (dates !== null && predictedDates !== null && stockData !== null) {
            setHasLoaded(true);
            setNormalChartData(produceNormalChartData());
            setPredictedChartData(producePredictedChartData());
        }
    }, [dates, predictedDates, stockData]);

    const timeScaleToInfo = [
        {name: "1D", count: 100, type: 0},         //1D (intraday)
        {name: "1W", count: 7, type: 1},           //1W (daily)
        {name: "1M", count: 30, type: 1},          //1M (daily)
        {name: "3M", count: 61, type: 1},          //3M (daily)
        {name: "6M", count: 90, type: 1},          //6M (daily)
        {name: "1Y", count: 52, type: 2},          //1Y (weekly)
        {name: "2Y", count: 104, type: 2},         //2Y (weekly)
        {name: "MAX", count: Infinity, type: 3}    //MAX (monthly)
    ];

    const produceNormalChartData = () => {
        let allData = [];
        for (let i=0; i<4; i++) {
            let dataArray = [];
            const keys = dates[i];
            
            for (const key of keys) {
                dataArray.push({date: key, close: parseFloat(stockData[i][key].close)});
            }
            dataArray[0] = {
                date: dataArray[0].date, 
                close: dataArray[0].close, 
                prediction: dataArray[0].close
            };

            allData.push(dataArray);
        }

        return allData;
    }

    const producePredictedChartData = () => {
        let allData = [];
        for (let i=0; i<4; i++) {
            let dataArray = [];

            const predKeys = predictedDates[i];

            for (const key of predKeys) {
                dataArray.push({date: key, prediction: parseFloat(stockData[i][key].close)});
            }

            allData.push(dataArray);
        }

        return allData;
    }

    const getChartData = () => {
        let normal = normalChartData[timeScaleToInfo[timeScale].type];
        normal = normal.slice(0, Math.min(normal.length, timeScaleToInfo[timeScale].count)).reverse();

        const predicted = predictedChartData[timeScaleToInfo[timeScale].type].reverse();
        return normal.concat(predicted);
    }
    const chartData = getChartData();

    function CustomTooltip({ payload, label, active }) {
        if (active) {
            const data = stockData[timeScaleToInfo[timeScale].type][label];

            return (
                <div className="custom-tooltip">
                    <p className='tooltip-title'>{label + (data.isPrediction ? " (predicted)" : "")}</p>
                    <div className="tooltip-text">
                        <div className='tooltip-left'>
                            <p>{`Open:`}</p>
                            <p>{`High:`}</p>
                            <p>{`Low:`}</p>
                            <p>{`Close:`}</p>
                            <p>{`Volume:`}</p>
                        </div>
                        <div className='tooltip-right'>
                            <p>{`$${data.open}`}</p>
                            <p>{`$${data.high}`}</p>
                            <p>{`$${data.low}`}</p>
                            <p>{`$${data.close}`}</p>
                            <p>{`${data.volume}`}</p>
                        </div>
                    </div>
                </div>
            );
        }
      
        return null;
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
        {hasLoaded ? <>
        <div id='company-info'>
            <div className='info-left'>
                <div className='left-title'>
                    <h1>{company.code}</h1>
                    {perceptionToSmiley(company.perception)}
                </div>
              <h3>{company.name}</h3>
            </div>
            <div className='info-right'>
                <div>
                    <div className='left-side'>
                        <p>Open:</p>
                        <p>High:</p>
                        <p>Low:</p>
                        
                    </div>
                    <div className='right-side'>
                        <p>${mainData.open}</p>
                        <p>${mainData.high}</p>
                        <p>${mainData.low}</p>
                       
                    </div>
                </div>
                <div>
                    <div className='left-side'>
                        <p>Price:</p>
                        <p>Change:</p>
                        <p>Volume:</p>
                    </div>
                    <div className='right-side'>
                        <p>${mainData.price}</p>
                        <p>{changes[timeScale]}</p>
                        <p>{mainData.volume}</p>
                    </div>
                </div>
              
            </div>
        </div>
        <div id='stock-chart'>
            <div className='chart-area'>
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart width={100} height={50} data={chartData} margin={{ top: 5, right: 50, left: 10, bottom: 5 }}>
                        <defs>
                            <linearGradient id="close-colour" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor='#10588f' stopOpacity={0.5} />
                                <stop offset="75%" stopColor='#10588f' stopOpacity={0.1} />
                            </linearGradient>
                            <linearGradient id="pred-colour" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor='#40494f' stopOpacity={0.5} />
                                <stop offset="75%" stopColor='#40494f' stopOpacity={0.1} />
                            </linearGradient>
                        </defs>


                        <CartesianGrid opacity={0.5}/>
                        <XAxis dataKey="date" />
                        <YAxis tickFormatter={(num)=>`$${num.toFixed(2)}`} /> 
                        <Tooltip content={<CustomTooltip />} />
                        {/* <Legend /> */}
                        <Area type="monotone" dataKey="close" stroke="#0d1f2d" fill="url(#close-colour)"  activeDot={{ r: 8 }} />
                        <Area type="monotone" dataKey="prediction" strokeDasharray="5 5" stroke="#000000" fill="url(#pred-colour)"  activeDot={{ r: 8 }} />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
            <div className='btn-area'>
                {timeScaleToInfo.map((info, index) => (
                    <div key={index} className='btn-container'>
                        <button
                            style={timeScale === index ? {backgroundColor: "var(--neutral)"} : {}}
                            key={index}
                            onClick={()=>{setTimeScale(index)}}>
                                {info.name}
                        </button>
                    </div>
                ))}
            </div>
        </div>
        </>:<>
        <Loading />
        </>}
        </>
    );
}

export default StockChart;
