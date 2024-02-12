import { useEffect, useState } from "react";
import axios from "axios";

import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from "recharts";

import { basic_url } from "@/stack/stack";

interface DataItem {
    date:string,
    open:number,
    high:number,
    low:number
}


const GoldPriceChart = () => {

    const [ minPrice, setMinPrice ] = useState<number>(0);
    const [ maxPrice, setMaxPrice ] = useState<number>(10000);
    const [ period, setPeriod ] = useState<number>(30);
    const [ pData, setPData ] = useState<DataItem[]>([{date:'2024-01-01',open:0,high:0,low:0}]);

    useEffect(() => {
        axios.get(`${basic_url}goldprices/chart/${period}`).then((res) => {
            console.log(typeof res.data.highest_price);
            setPData(res.data.prices);  
            setMinPrice(res.data.highest_price + 100);
            setMaxPrice(res.data.lowest_price - 100);
            
        }).catch(() => {
            console.log("Price Get Error");
        })
    }, [period])

    return(
        <>
            <ResponsiveContainer width="100%" height="100%">
                <LineChart
                    width={500}
                    height={300}
                    data={pData}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date"/>
                    <YAxis domain={[minPrice, maxPrice ]}/>
                    <Tooltip />
                    <Legend />
                    <Line
                        type="monotone"
                        dataKey="open_price"
                        stroke="#a8323e"
                        dot={false}
                    />
                    <Line
                        type="monotone"
                        dataKey="high_price"
                        stroke="#3296a8"
                        dot={false}
                    />
                    <Line
                        type="monotone"
                        dataKey="low_price"
                        stroke="#82ca9d"
                        dot={false}
                    />
                </LineChart>
            </ResponsiveContainer>
            <div className="mx-auto flex w-[80%] md:w-[50%] items-center justify-between mt-10">
                {
                    period === 30 ? <button className="bg-[#1d4354] text-[white] px-5 py-3" onClick={() => setPeriod(30)}>1 Month</button>
                        : <button className="bg-[#6597ad] text-[white] px-5 py-3" onClick={() => setPeriod(30)}>1 Month</button>
                }
                {
                    period === 90 ? <button className="bg-[#1d4354] text-[white] px-5 py-3" onClick={() => setPeriod(90)}>3 Month</button>
                        : <button className="bg-[#6597ad] text-[white] px-5 py-3" onClick={() => setPeriod(90)}>3 Month</button>
                }
                {
                    period === 365 ?  <button className="bg-[#1d4354] text-[white] px-5 py-3" onClick={() => setPeriod(365)}>1 Year</button>
                        :  <button className="bg-[#6597ad] text-[white] px-5 py-3" onClick={() => setPeriod(365)}>1 Year</button>
                }
            </div>
        </>
    )
}

export default GoldPriceChart;