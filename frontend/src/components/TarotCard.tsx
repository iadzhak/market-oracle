import React, {useRef, useState} from 'react';
import './TarotCard.css';
import flipSound from '../assets/flip.mp3'

export default function TarotCard({ card }) {
    const [isFlipped, setIsFlipped] = useState(false);
    const [isAnimating, setIsAnimating] = useState(false);

    const audioRef = useRef(new Audio(flipSound));

    const handleClick = () => {
        if (isAnimating) return;

        // Воспроизводим звук
        audioRef.current.currentTime = 0; // перезапуск с начала
        audioRef.current.play().catch(e => console.warn('Звук не воспроизведён:', e));

        setIsAnimating(true);
        setIsFlipped(false); // сначала сбрасываем, чтобы анимация сработала

        // Завершаем анимацию через ~2 секунды
        setTimeout(() => {
            setIsFlipped(true);
            setIsAnimating(false);
        }, 2000);
    };

    return (
        <div
            className={`tarot-card ${isAnimating ? 'animating' : ''} ${isFlipped ? 'flipped' : ''}`}
            onClick={handleClick}
        >
            <div className="card-inner">
                <div className="card-front">
                    <span>❓</span>
                </div>
                <div className="card-back">
                    <h3>{card.name}</h3>
                    <p>{card.meaning}</p>
                </div>
            </div>
        </div>
    );
}
