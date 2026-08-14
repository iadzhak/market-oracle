import {useRef, useState} from 'react';
import './TarotCard.css';
import flipSound from '../assets/flip.mp3'

interface TarotCardProps {
    card: { id: number; name: string; meaning: string };
    selected: boolean;
    onSelect: (id: number) => void;
}

export default function TarotCard({ card, selected, onSelect }: TarotCardProps) {
    const [isFlipped, setIsFlipped] = useState(false);
    const [isAnimating, setIsAnimating] = useState(false);

    const audioRef = useRef(new Audio(flipSound));

    const handleClick = (e: React.MouseEvent) => {
        e.stopPropagation();
        if (isAnimating && !selected) return;

        if (selected) {
            onSelect(card.id);
            return;
        }

        // Воспроизводим звук
        audioRef.current.currentTime = 0;
        audioRef.current.play().catch(e => console.warn('Звук не воспроизведён:', e));

        setIsAnimating(true);
        setIsFlipped(false);

        setTimeout(() => {
            setIsFlipped(true);
            setIsAnimating(false);
            onSelect(card.id);
        }, 2000);
    };

    return (
        <>
            <div
                className={`tarot-card ${isAnimating ? 'animating' : ''} ${isFlipped ? 'flipped' : ''} ${selected ? 'selected' : ''}`}
                onClick={handleClick}
            >
                <div className="card-inner">
                    <div className="card-front">
                        <span>{card.name}</span>
                    </div>
                    <div className="card-back">
                        <h3>{card.name}</h3>
                        <p>{card.meaning}</p>
                    </div>
                </div>
            </div>

            {selected && (
                <div className="card-overlay" onClick={() => onSelect(card.id)}>
                    <div className="card-large">
                        <div className="card-inner">
                            <div className="card-front-large">
                                <span>{card.name}</span>
                            </div>
                            <div className="card-back-large">
                                <h2>{card.name}</h2>
                                <p>{card.meaning}</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
