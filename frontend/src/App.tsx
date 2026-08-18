import TarotCard from "./components/TarotCard.tsx";
import AlertCard from "./components/AlertCard.tsx";
import './App.css';

const deck = [
    { id: 1, name: 'BTC', meaning: 'Завтра вырастет', direction: 'up', confidence: 96, risk: 2, args: 'Позитивные новости / Восходящий тренд', sources: 'SMA20, 1H таймфрейм / Новости криптовалюты' },
    { id: 2, name: 'ETH', meaning: 'Завтра упадет', direction: 'down', confidence: 96, risk: 2, args: 'Позитивные новости / Восходящий тренд', sources: 'SMA20, 1H таймфрейм / Новости криптовалюты' },
    { id: 3, name: 'SOL', meaning: 'Завтра вырастет', direction: 'up', confidence: 96, risk: 2, args: 'Позитивные новости / Восходящий тренд', sources: 'SMA20, 1H таймфрейм / Новости криптовалюты' },
    { id: 4, name: 'BNB', meaning: 'Завтра упадет', direction: 'down', confidence: 96, risk: 2, args: 'Позитивные новости / Восходящий тренд', sources: 'SMA20, 1H таймфрейм / Новости криптовалюты' },
    { id: 5, name: 'XRP', meaning: 'Завтра вырастет', direction: 'up', confidence: 96, risk: 2, args: 'Позитивные новости / Восходящий тренд', sources: 'SMA20, 1H таймфрейм / Новости криптовалюты' },
    { id: 6, name: 'ADA', meaning: 'Завтра упадет', direction: 'down', confidence: 96, risk: 2, args: 'Позитивные новости / Восходящий тренд', sources: 'SMA20, 1H таймфрейм / Новости криптовалюты' },
    { id: 7, name: 'DOGE', meaning: 'Завтра вырастет', direction: 'up', confidence: 96, risk: 2, args: 'Позитивные новости / Восходящий тренд', sources: 'SMA20, 1H таймфрейм / Новости криптовалюты' },
    { id: 8, name: 'AVAX', meaning: 'Завтра упадет', direction: 'down', confidence: 96, risk: 2, args: 'Позитивные новости / Восходящий тренд', sources: 'SMA20, 1H таймфрейм / Новости криптовалюты' },
    { id: 9, name: 'DOT', meaning: 'Завтра вырастет', direction: 'up', confidence: 96, risk: 2, args: 'Позитивные новости / Восходящий тренд', sources: 'SMA20, 1H таймфрейм / Новости криптовалюты' },
];

function App() {
    return (
        <div className="app">
            <h1>🔮 Крипто Оракул</h1>
            <div className="deck">
                <AlertCard  />
                {deck.map((card) => (
                    <TarotCard key={card.id} card={card} />
                ))}
            </div>
        </div>
    );
}

export default App;
