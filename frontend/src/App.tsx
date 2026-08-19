import TarotCard from "./components/TarotCard.tsx";
import AlertCard from "./components/AlertCard.tsx";
import './App.css';
import {useEffect, useState} from "react";
import {tokensUrl} from "./api.ts";


function App() {
    const [data, setData] = useState([])
    useEffect(()=>{
        fetch(tokensUrl).then(res=>res.json()).then(res=>setData(res))
    }, [])

    return (
        <div className="app">
            <h1>🔮 Крипто Оракул</h1>
            <div className="deck">
                <AlertCard  />
                {data.map((token) => (
                    <TarotCard key={token} token={token} />
                ))}
            </div>
        </div>
    );
}

export default App;
