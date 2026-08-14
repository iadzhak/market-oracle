import './App.css'
import TarotCard from "./components/TarotCard.tsx";

const deck = [
  { id: 1, name: 'The Fool', meaning: 'Новые начинания, свобода' },
  { id: 2, name: 'The Magician', meaning: 'Сила, творчество, воля' },
  { id: 3, name: 'The High Priestess', meaning: 'Интуиция, тайны' },
];

function App() {

  return (
      <div className="app">
        <h1>Выбери свою карту судьбы 🔮</h1>
        <div className="deck">
          {deck.map((card) => (
              <TarotCard key={card.id} card={card}/>
          ))}
        </div>
      </div>
  );
}

export default App
