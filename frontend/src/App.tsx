import { useState } from 'react';
import TarotCard from "./components/TarotCard.tsx";
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
    const [selectedId, setSelectedId] = useState<number | null>(null);

    const handleSelect = (id: number) => {
        setSelectedId(prev => prev === id ? null : id);
    };

    return (
        <div className="app">
            <h1>🔮 Выбери свою карту крипты</h1>
            <div className={`deck ${selectedId !== null ? 'dimmed' : ''}`}>
                {deck.map((card) => (
                    <TarotCard
                        key={card.id}
                        card={card}
                        selected={selectedId === card.id}
                        onSelect={handleSelect}
                    />
                ))}
            </div>
        </div>
    );
}

export default App;
