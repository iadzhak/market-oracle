import TarotCard from "./components/TarotCard.tsx";
import AlertCard from "./components/AlertCard.tsx";
import './App.css';

const deck = [
    { id: 1, name: 'BTC', meaning: 'Завтра вырастет 📈' },
    { id: 2, name: 'ETH', meaning: 'Завтра упадет 📉' },
    { id: 3, name: 'SOL', meaning: 'Завтра вырастет 📈' },
    { id: 4, name: 'BNB', meaning: 'Завтра упадет 📉' },
    { id: 5, name: 'XRP', meaning: 'Завтра вырастет 📈' },
    { id: 6, name: 'ADA', meaning: 'Завтра упадет 📉' },
    { id: 7, name: 'DOGE', meaning: 'Завтра вырастет 📈' },
    { id: 8, name: 'AVAX', meaning: 'Завтра упадет 📉' },
    { id: 9, name: 'DOT', meaning: 'Завтра вырастет 📈' },
];

function App() {
    return (
        <div className="app">
            <h1>🔮 Крипто Оракул</h1>
            <div className="deck">
                <AlertCard card={{
                    id: 0,
                    name: '⚠️ Предупреждение ⚠️',
                    meaning: 'Cервис носит демонстрационный характер. Не является финансовой рекомендацией, не гарантирует доходность и не предназначен для проведения реальных финансовых операций.'
                }} />
                {deck.map((card) => (
                    <TarotCard key={card.id} card={card} />
                ))}
            </div>
        </div>
    );
}

export default App;
