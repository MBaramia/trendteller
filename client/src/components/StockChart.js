import './StockChart.css';
import { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ReactComponent as SmileyGood } from "../images/smiley_good_green.svg";
import { ReactComponent as SmileyNeutral} from "../images/smiley_neutral_grey.svg";
import { ReactComponent as SmileyBad } from "../images/smiley_bad_red.svg";
const fetched = {
    0: {
        "2024-02-27 19:55:00": {
            "1. open": "185.0800",
            "2. high": "185.0900",
            "3. low": "184.7400",
            "4. close": "185.0900",
            "5. volume": "84"
        },
        "2024-02-27 19:30:00": {
            "1. open": "185.0900",
            "2. high": "185.0900",
            "3. low": "185.0000",
            "4. close": "185.0000",
            "5. volume": "51"
        },
        "2024-02-27 19:25:00": {
            "1. open": "185.0000",
            "2. high": "185.0000",
            "3. low": "185.0000",
            "4. close": "185.0000",
            "5. volume": "10"
        },
        "2024-02-27 19:20:00": {
            "1. open": "184.9600",
            "2. high": "185.0000",
            "3. low": "184.6000",
            "4. close": "184.6000",
            "5. volume": "202"
        },
        "2024-02-27 19:00:00": {
            "1. open": "184.8700",
            "2. high": "185.0800",
            "3. low": "184.6000",
            "4. close": "184.6400",
            "5. volume": "553513"
        },
        "2024-02-27 18:50:00": {
            "1. open": "185.0900",
            "2. high": "185.0900",
            "3. low": "185.0900",
            "4. close": "185.0900",
            "5. volume": "40"
        },
        "2024-02-27 18:40:00": {
            "1. open": "184.8700",
            "2. high": "185.0900",
            "3. low": "184.8700",
            "4. close": "185.0900",
            "5. volume": "18"
        },
        "2024-02-27 18:35:00": {
            "1. open": "185.0900",
            "2. high": "185.0900",
            "3. low": "185.0900",
            "4. close": "185.0900",
            "5. volume": "29"
        },
        "2024-02-27 18:30:00": {
            "1. open": "184.8700",
            "2. high": "185.0000",
            "3. low": "184.8700",
            "4. close": "185.0000",
            "5. volume": "553490"
        },
        "2024-02-27 18:25:00": {
            "1. open": "185.0900",
            "2. high": "185.0900",
            "3. low": "185.0900",
            "4. close": "185.0900",
            "5. volume": "2"
        },
        "2024-02-27 18:20:00": {
            "1. open": "185.0100",
            "2. high": "185.1000",
            "3. low": "185.0000",
            "4. close": "185.1000",
            "5. volume": "45"
        },
        "2024-02-27 18:10:00": {
            "1. open": "185.0000",
            "2. high": "185.0000",
            "3. low": "185.0000",
            "4. close": "185.0000",
            "5. volume": "1"
        },
        "2024-02-27 18:05:00": {
            "1. open": "185.0000",
            "2. high": "185.0000",
            "3. low": "185.0000",
            "4. close": "185.0000",
            "5. volume": "1"
        },
        "2024-02-27 18:00:00": {
            "1. open": "185.0000",
            "2. high": "185.0000",
            "3. low": "185.0000",
            "4. close": "185.0000",
            "5. volume": "1"
        },
        "2024-02-27 17:55:00": {
            "1. open": "184.0000",
            "2. high": "185.0000",
            "3. low": "184.0000",
            "4. close": "185.0000",
            "5. volume": "111"
        },
        "2024-02-27 17:45:00": {
            "1. open": "183.4600",
            "2. high": "183.4600",
            "3. low": "183.0700",
            "4. close": "183.0700",
            "5. volume": "7"
        },
        "2024-02-27 17:40:00": {
            "1. open": "184.9400",
            "2. high": "184.9400",
            "3. low": "183.4410",
            "4. close": "183.6500",
            "5. volume": "124"
        },
        "2024-02-27 17:35:00": {
            "1. open": "183.6100",
            "2. high": "185.0000",
            "3. low": "183.1200",
            "4. close": "185.0000",
            "5. volume": "18"
        },
        "2024-02-27 17:30:00": {
            "1. open": "184.9000",
            "2. high": "184.9000",
            "3. low": "183.5590",
            "4. close": "183.7110",
            "5. volume": "105"
        },
        "2024-02-27 17:25:00": {
            "1. open": "184.9200",
            "2. high": "185.0000",
            "3. low": "184.9200",
            "4. close": "184.9200",
            "5. volume": "9"
        },
        "2024-02-27 17:15:00": {
            "1. open": "185.0000",
            "2. high": "185.0000",
            "3. low": "184.9200",
            "4. close": "185.0000",
            "5. volume": "211"
        },
        "2024-02-27 17:10:00": {
            "1. open": "184.9200",
            "2. high": "185.0000",
            "3. low": "184.8700",
            "4. close": "185.0000",
            "5. volume": "10951"
        } 
    }, 1: {
        "2024-02-28": {
            "1. open": "184.6300",
            "2. high": "185.3700",
            "3. low": "183.5500",
            "4. close": "185.3000",
            "5. volume": "3216345"
        },
        "2024-02-27": {
            "1. open": "184.1600",
            "2. high": "185.1300",
            "3. low": "182.6200",
            "4. close": "184.8700",
            "5. volume": "3641378"
        },
        "2024-02-26": {
            "1. open": "185.6000",
            "2. high": "186.1250",
            "3. low": "184.0600",
            "4. close": "184.1300",
            "5. volume": "4620815"
        },
        "2024-02-23": {
            "1. open": "184.9000",
            "2. high": "186.4550",
            "3. low": "184.5700",
            "4. close": "185.7200",
            "5. volume": "3433800"
        },
        "2024-02-22": {
            "1. open": "182.4500",
            "2. high": "184.5500",
            "3. low": "181.9300",
            "4. close": "184.2100",
            "5. volume": "5078398"
        },
        "2024-02-21": {
            "1. open": "182.5600",
            "2. high": "183.0300",
            "3. low": "178.7500",
            "4. close": "179.7000",
            "5. volume": "4728473"
        },
        "2024-02-20": {
            "1. open": "187.6400",
            "2. high": "188.7700",
            "3. low": "183.0600",
            "4. close": "183.4400",
            "5. volume": "4247181"
        },
        "2024-02-16": {
            "1. open": "186.6300",
            "2. high": "188.9500",
            "3. low": "185.9452",
            "4. close": "187.6400",
            "5. volume": "4842840"
        },
        "2024-02-15": {
            "1. open": "183.6200",
            "2. high": "186.9800",
            "3. low": "183.6200",
            "4. close": "186.8700",
            "5. volume": "4714301"
        },
        "2024-02-14": {
            "1. open": "185.0000",
            "2. high": "185.0000",
            "3. low": "182.2600",
            "4. close": "183.5700",
            "5. volume": "3173391"
        },
        "2024-02-13": {
            "1. open": "184.2800",
            "2. high": "184.7700",
            "3. low": "182.3600",
            "4. close": "183.7000",
            "5. volume": "4290453"
        },
        "2024-02-12": {
            "1. open": "185.9000",
            "2. high": "186.4800",
            "3. low": "184.0300",
            "4. close": "186.1600",
            "5. volume": "4724021"
        },
        "2024-02-09": {
            "1. open": "184.4400",
            "2. high": "187.1800",
            "3. low": "183.8500",
            "4. close": "186.3400",
            "5. volume": "5064641"
        },
        "2024-02-08": {
            "1. open": "182.6300",
            "2. high": "184.5500",
            "3. low": "181.4900",
            "4. close": "184.3600",
            "5. volume": "5161185"
        },
        "2024-02-07": {
            "1. open": "183.3400",
            "2. high": "184.0200",
            "3. low": "182.6250",
            "4. close": "183.7400",
            "5. volume": "4841188"
        },
        "2024-02-06": {
            "1. open": "183.5500",
            "2. high": "184.6800",
            "3. low": "183.0400",
            "4. close": "183.4100",
            "5. volume": "3338196"
        },
        "2024-02-05": {
            "1. open": "185.5100",
            "2. high": "185.7800",
            "3. low": "183.2550",
            "4. close": "183.4200",
            "5. volume": "4379602"
        },
        "2024-02-02": {
            "1. open": "187.1000",
            "2. high": "187.3900",
            "3. low": "185.6150",
            "4. close": "185.7900",
            "5. volume": "4055411"
        },
        "2024-02-01": {
            "1. open": "183.6300",
            "2. high": "187.5100",
            "3. low": "182.7100",
            "4. close": "186.9000",
            "5. volume": "4669444"
        },
        "2024-01-31": {
            "1. open": "187.0500",
            "2. high": "187.6500",
            "3. low": "183.1400",
            "4. close": "183.6600",
            "5. volume": "8876055"
        },
        "2024-01-30": {
            "1. open": "187.7100",
            "2. high": "188.6500",
            "3. low": "186.7700",
            "4. close": "187.8700",
            "5. volume": "4575058"
        },
        "2024-01-29": {
            "1. open": "187.4600",
            "2. high": "189.4600",
            "3. low": "186.0500",
            "4. close": "187.1400",
            "5. volume": "6107908"
        },
        "2024-01-26": {
            "1. open": "191.3100",
            "2. high": "192.3896",
            "3. low": "186.1600",
            "4. close": "187.4200",
            "5. volume": "9895941"
        },
        "2024-01-25": {
            "1. open": "184.9600",
            "2. high": "196.9000",
            "3. low": "184.8300",
            "4. close": "190.4300",
            "5. volume": "29596239"
        },
        "2024-01-24": {
            "1. open": "174.7600",
            "2. high": "174.8600",
            "3. low": "172.9000",
            "4. close": "173.9300",
            "5. volume": "7831157"
        },
        "2024-01-23": {
            "1. open": "172.9000",
            "2. high": "174.0200",
            "3. low": "172.4800",
            "4. close": "173.9400",
            "5. volume": "3983461"
        },
        "2024-01-22": {
            "1. open": "172.8200",
            "2. high": "174.4500",
            "3. low": "172.4000",
            "4. close": "172.8300",
            "5. volume": "4925964"
        },
        "2024-01-19": {
            "1. open": "170.5900",
            "2. high": "171.5791",
            "3. low": "169.1800",
            "4. close": "171.4800",
            "5. volume": "6929079"
        },
        "2024-01-18": {
            "1. open": "166.4900",
            "2. high": "166.9900",
            "3. low": "165.0400",
            "4. close": "166.8400",
            "5. volume": "3776990"
        },
        "2024-01-17": {
            "1. open": "166.7900",
            "2. high": "167.8200",
            "3. low": "165.4950",
            "4. close": "166.0800",
            "5. volume": "4288604"
        },
        "2024-01-16": {
            "1. open": "165.8000",
            "2. high": "167.2500",
            "3. low": "165.3400",
            "4. close": "166.9600",
            "5. volume": "4869635"
        },
        "2024-01-12": {
            "1. open": "162.9700",
            "2. high": "165.9800",
            "3. low": "162.3550",
            "4. close": "165.8000",
            "5. volume": "4958261"
        },
        "2024-01-11": {
            "1. open": "161.0200",
            "2. high": "162.2300",
            "3. low": "160.2900",
            "4. close": "162.1600",
            "5. volume": "3778395"
        },
        "2024-01-10": {
            "1. open": "160.2800",
            "2. high": "161.3400",
            "3. low": "159.7400",
            "4. close": "161.2300",
            "5. volume": "2967852"
        }
    }, 2: {
        "2024-02-27": {
            "1. open": "185.6000",
            "2. high": "186.1250",
            "3. low": "182.6200",
            "4. close": "184.8700",
            "5. volume": "8262193"
        },
        "2024-02-23": {
            "1. open": "187.6400",
            "2. high": "188.7700",
            "3. low": "178.7500",
            "4. close": "185.7200",
            "5. volume": "17487852"
        },
        "2024-02-16": {
            "1. open": "185.9000",
            "2. high": "188.9500",
            "3. low": "182.2600",
            "4. close": "187.6400",
            "5. volume": "21745006"
        },
        "2024-02-09": {
            "1. open": "185.5100",
            "2. high": "187.1800",
            "3. low": "181.4900",
            "4. close": "186.3400",
            "5. volume": "22784812"
        },
        "2024-02-02": {
            "1. open": "187.4600",
            "2. high": "189.4600",
            "3. low": "182.7100",
            "4. close": "185.7900",
            "5. volume": "28283876"
        },
        "2024-01-26": {
            "1. open": "172.8200",
            "2. high": "196.9000",
            "3. low": "172.4000",
            "4. close": "187.4200",
            "5. volume": "56232762"
        },
        "2024-01-19": {
            "1. open": "165.8000",
            "2. high": "171.5791",
            "3. low": "165.0400",
            "4. close": "171.4800",
            "5. volume": "19864308"
        },
        "2024-01-12": {
            "1. open": "158.6900",
            "2. high": "165.9800",
            "3. low": "157.8850",
            "4. close": "165.8000",
            "5. volume": "17643392"
        },
        "2024-01-05": {
            "1. open": "162.8300",
            "2. high": "163.2900",
            "3. low": "158.6700",
            "4. close": "159.1600",
            "5. volume": "14822074"
        },
        "2023-12-29": {
            "1. open": "162.2300",
            "2. high": "164.1800",
            "3. low": "162.0500",
            "4. close": "163.5500",
            "5. volume": "9376537"
        },
        "2023-12-22": {
            "1. open": "162.2300",
            "2. high": "163.3300",
            "3. low": "159.5300",
            "4. close": "162.1400",
            "5. volume": "17686398"
        },
        "2023-12-15": {
            "1. open": "162.6800",
            "2. high": "166.3400",
            "3. low": "160.1490",
            "4. close": "162.2300",
            "5. volume": "33504550"
        },
        "2023-12-08": {
            "1. open": "160.2900",
            "2. high": "162.7900",
            "3. low": "159.9700",
            "4. close": "161.9600",
            "5. volume": "21918957"
        },
        "2023-12-01": {
            "1. open": "154.9900",
            "2. high": "160.5900",
            "3. low": "154.7500",
            "4. close": "160.5500",
            "5. volume": "21900644"
        },
        "2023-11-24": {
            "1. open": "152.5100",
            "2. high": "155.7050",
            "3. low": "152.3500",
            "4. close": "155.1800",
            "5. volume": "11362696"
        },
        "2023-11-17": {
            "1. open": "148.4600",
            "2. high": "153.5000",
            "3. low": "147.3500",
            "4. close": "152.8900",
            "5. volume": "19547595"
        },
        "2023-11-10": {
            "1. open": "147.8900",
            "2. high": "149.6800",
            "3. low": "145.2800",
            "4. close": "149.0200",
            "5. volume": "18357944"
        },
        "2023-11-03": {
            "1. open": "143.1900",
            "2. high": "148.4450",
            "3. low": "142.5800",
            "4. close": "147.9000",
            "5. volume": "22959464"
        },
        "2023-10-27": {
            "1. open": "136.6300",
            "2. high": "144.7000",
            "3. low": "135.8700",
            "4. close": "142.5200",
            "5. volume": "30227448"
        },
        "2023-10-20": {
            "1. open": "139.2800",
            "2. high": "140.6200",
            "3. low": "136.3100",
            "4. close": "137.1600",
            "5. volume": "21044049"
        },
        "2023-10-13": {
            "1. open": "142.3000",
            "2. high": "143.4150",
            "3. low": "138.2700",
            "4. close": "138.4600",
            "5. volume": "16386334"
        },
        "2023-10-06": {
            "1. open": "140.0400",
            "2. high": "142.9400",
            "3. low": "139.8600",
            "4. close": "142.0300",
            "5. volume": "15932918"
        },
        "2023-09-29": {
            "1. open": "146.5700",
            "2. high": "147.4300",
            "3. low": "139.6100",
            "4. close": "140.3000",
            "5. volume": "23445425"
        },
        "2023-09-22": {
            "1. open": "145.7700",
            "2. high": "151.9299",
            "3. low": "144.6600",
            "4. close": "146.9100",
            "5. volume": "23597168"
        },
        "2023-09-15": {
            "1. open": "148.5700",
            "2. high": "148.7800",
            "3. low": "145.5300",
            "4. close": "145.9900",
            "5. volume": "19316647"
        },
        "2023-09-08": {
            "1. open": "147.9100",
            "2. high": "149.0000",
            "3. low": "147.1200",
            "4. close": "147.6800",
            "5. volume": "13719451"
        },
        "2023-09-01": {
            "1. open": "145.4100",
            "2. high": "148.1000",
            "3. low": "145.2100",
            "4. close": "147.9400",
            "5. volume": "15198607"
        }
    }, 3: {
        "2024-02-27": {
            "1. open": "183.6300",
            "2. high": "188.9500",
            "3. low": "178.7500",
            "4. close": "184.8700",
            "5. volume": "79004718"
        },
        "2024-01-31": {
            "1. open": "162.8300",
            "2. high": "196.9000",
            "3. low": "157.8850",
            "4. close": "183.6600",
            "5. volume": "128121557"
        },
        "2023-12-29": {
            "1. open": "158.4100",
            "2. high": "166.3400",
            "3. low": "158.0000",
            "4. close": "163.5500",
            "5. volume": "87358302"
        },
        "2023-11-30": {
            "1. open": "145.0000",
            "2. high": "158.6000",
            "3. low": "144.4500",
            "4. close": "158.5600",
            "5. volume": "78460252"
        },
        "2023-10-31": {
            "1. open": "140.0400",
            "2. high": "144.7600",
            "3. low": "135.8700",
            "4. close": "144.6400",
            "5. volume": "94386980"
        },
        "2023-09-29": {
            "1. open": "147.2600",
            "2. high": "151.9299",
            "3. low": "139.6100",
            "4. close": "140.3000",
            "5. volume": "82806487"
        },
        "2023-08-31": {
            "1. open": "144.2500",
            "2. high": "147.7275",
            "3. low": "139.7600",
            "4. close": "146.8300",
            "5. volume": "84274205"
        },
        "2023-07-31": {
            "1. open": "133.4200",
            "2. high": "144.6050",
            "3. low": "131.5500",
            "4. close": "144.1800",
            "5. volume": "85778938"
        },
        "2023-06-30": {
            "1. open": "128.4400",
            "2. high": "139.4690",
            "3. low": "127.7800",
            "4. close": "133.8100",
            "5. volume": "100722016"
        },
        "2023-05-31": {
            "1. open": "126.3500",
            "2. high": "130.0699",
            "3. low": "120.5500",
            "4. close": "128.5900",
            "5. volume": "95710890"
        },
        "2023-04-28": {
            "1. open": "130.9700",
            "2. high": "132.6100",
            "3. low": "124.5600",
            "4. close": "126.4100",
            "5. volume": "83664114"
        },
        "2023-03-31": {
            "1. open": "128.9000",
            "2. high": "131.4800",
            "3. low": "121.7100",
            "4. close": "131.0900",
            "5. volume": "138093084"
        },
        "2023-02-28": {
            "1. open": "134.4900",
            "2. high": "137.3900",
            "3. low": "128.8600",
            "4. close": "129.3000",
            "5. volume": "76080679"
        },
        "2023-01-31": {
            "1. open": "141.1000",
            "2. high": "147.1800",
            "3. low": "132.9800",
            "4. close": "134.7300",
            "5. volume": "105576019"
        },
        "2022-12-30": {
            "1. open": "149.9800",
            "2. high": "153.2100",
            "3. low": "137.1950",
            "4. close": "140.8900",
            "5. volume": "86426226"
        },
        "2022-11-30": {
            "1. open": "138.2500",
            "2. high": "150.4600",
            "3. low": "133.9700",
            "4. close": "148.9000",
            "5. volume": "93620235"
        },
        "2022-10-31": {
            "1. open": "120.1600",
            "2. high": "138.8615",
            "3. low": "115.5450",
            "4. close": "138.2900",
            "5. volume": "113480787"
        },
        "2022-09-30": {
            "1. open": "128.4000",
            "2. high": "130.9900",
            "3. low": "118.6100",
            "4. close": "118.8100",
            "5. volume": "87256958"
        },
        "2022-08-31": {
            "1. open": "130.7500",
            "2. high": "139.3400",
            "3. low": "128.4000",
            "4. close": "128.4500",
            "5. volume": "77392342"
        },
        "2022-07-29": {
            "1. open": "141.0000",
            "2. high": "141.8700",
            "3. low": "125.1300",
            "4. close": "130.7900",
            "5. volume": "129801061"
        },
        "2022-06-30": {
            "1. open": "139.6700",
            "2. high": "144.7300",
            "3. low": "132.8500",
            "4. close": "141.1900",
            "5. volume": "105815743"
        },
        "2022-05-31": {
            "1. open": "133.0000",
            "2. high": "139.8300",
            "3. low": "125.8000",
            "4. close": "138.8400",
            "5. volume": "113207659"
        },
        "2022-04-29": {
            "1. open": "129.6600",
            "2. high": "141.8800",
            "3. low": "124.9100",
            "4. close": "132.2100",
            "5. volume": "107525264"
        },
        "2022-03-31": {
            "1. open": "122.6700",
            "2. high": "133.0800",
            "3. low": "120.7000",
            "4. close": "130.0200",
            "5. volume": "96447210"
        }
    }
};

function StockChart({ company }) {

    const [timeScale, setTimeScale] = useState(0);

    const timeScaleToInfo = [
        {name: "1D", count: 100, type: 0},         //1D (intraday)
        {name: "1W", count: 7, type: 1},           //1W (daily)
        {name: "1M", count: 30, type: 1},          //1M (daily)
        {name: "3M", count: 30, type: 1},          //3M (daily)
        {name: "6M", count: 30, type: 1},          //6M (daily)
        {name: "1Y", count: 52, type: 2},          //1Y (weekly)
        {name: "2Y", count: 104, type: 2},         //2Y (weekly)
        {name: "MAX", count: Infinity, type: 3}    //MAX (monthly)
    ];

    // use companyID to fetch data
    const produceAllData = () => {
        let allData = [];
        for (let i=0; i<4; i++) {
            const keys = Object.keys(fetched[i]);
            let dataArray = [];

            for (const key of keys) {
                dataArray.push({date: key, close: parseFloat(fetched[i][key]["4. close"])});
            }
            allData.push(dataArray);
        }

        return allData;
    }
    const allChartData = produceAllData();
    console.log(allChartData);

    const produceToolTipData = () => {
        let allData = [];
        for (let i=0; i<4; i++) {
            const keys = Object.keys(fetched[i]);
            let dateToInfo = {};

            for (const key of keys) {
                dateToInfo[key] = {
                    open: (fetched[i][key]["1. open"]),
                    high: (fetched[i][key]["2. high"]),
                    low: (fetched[i][key]["3. low"]),
                    close: (fetched[i][key]["4. close"]),
                    volume: (fetched[i][key]["5. volume"])
                }
            }
            allData.push(dateToInfo);
        }

        return allData;
    }
    const allToolTipData = produceToolTipData();
    console.log(allToolTipData);

    const mainData = {
        open: "145.4100",  
        high: "148.1000", 
        low: "145.2100", 
        price: "147.9400", 
        volume: "15198607"
    }

    const changes = [
        "+18.32 (0.49%)", "+12.04 (6.38%)", "-1.87 (-0.92%)", "+181.25 (922.39%)",
        "+18.32 (0.49%)", "+12.04 (6.38%)", "-1.87 (-0.92%)", "+181.25 (922.39%)"
    ];

    // fetched data now stored in allData

    // const chartData = [
    //     { date: '2023-01-01', price: 100 },
    //     { date: '2023-01-02', price: 105 },
    //     { date: '2023-01-03', price: 110 },
    //     { date: '2023-01-04', price: 108 },
    //     { date: '2023-01-05', price: 112 },
    //     { date: '2023-01-06', price: 115 },
    // ];

    const getChartData = () => {
        const data = allChartData[timeScaleToInfo[timeScale].type];
        return data.slice(0, Math.min(data.length, timeScaleToInfo[timeScale].count)).reverse();
    }
    const chartData = getChartData();

    function CustomTooltip({ payload, label, active }) {
        if (active) {
            const data = allToolTipData[timeScaleToInfo[timeScale].type][label];
            return (
                <div className="custom-tooltip">
                    <p className='tooltip-title'>{label}</p>
                    <div className="tooltip-text">
                        <div className='tooltip-left'>
                            <p>{`Open:`}</p>
                            <p>{`High:`}</p>
                            <p>{`Low:`}</p>
                            <p>{`Close:`}</p>
                            <p>{`Volume:`}</p>
                        </div>
                        <div className='tooltip-right'>
                            <p>{`£${data.open}`}</p>
                            <p>{`£${data.high}`}</p>
                            <p>{`£${data.low}`}</p>
                            <p>{`£${data.close}`}</p>
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
                        <p>£{mainData.open}</p>
                        <p>£{mainData.high}</p>
                        <p>£{mainData.low}</p>
                       
                    </div>
                </div>
                <div>
                    <div className='left-side'>
                        <p>Price:</p>
                        <p>Change:</p>
                        <p>Volume:</p>
                    </div>
                    <div className='right-side'>
                        <p>£{mainData.price}</p>
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
                            <linearGradient id="colour" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor='#10588f' stopOpacity={0.5} />
                                <stop offset="75%" stopColor='#10588f' stopOpacity={0.1} />
                            </linearGradient>
                        </defs>


                        <CartesianGrid opacity={0.5}/>
                        <XAxis dataKey="date" />
                        <YAxis tickFormatter={(num)=>`£${num.toFixed(2)}`} />
                        <Tooltip content={<CustomTooltip />} />
                        {/* <Legend /> */}
                        <Area type="monotone" dataKey="close" stroke="#0d1f2d" fill="url(#colour)"  activeDot={{ r: 8 }} />
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
        </>
    );
}

export default StockChart;