import {useRef, useState} from 'react';
import './TarotCard.css';
import flipSound from '../assets/flip.mp3'

interface TarotCardProps {
    card: { id: number; name: string; meaning: string };
}

function get_icon(token: string) {
    return `https://cryptoicon.io/wp-content/uploads/cc-assets/SVG/Light/${token.toUpperCase()}.svg`
}

export default function TarotCard({ card }: TarotCardProps) {
    const [isAnimating, setIsAnimating] = useState(false);
    const [isRevealed, setIsRevealed] = useState(false);
    const [isOverlayVisible, setIsOverlayVisible] = useState(false);
    const audioRef = useRef(new Audio(flipSound));

    const handleClick = (e: React.MouseEvent) => {
        e.stopPropagation();

        if (isOverlayVisible) {
            return;
        }

        // Если уже открыта — просто показываем оверлей снова
        if (isRevealed && !isAnimating) {
            setIsOverlayVisible(true);
            return;
        }

        if (isAnimating) return;

        // Воспроизводим звук
        audioRef.current.currentTime = 0;
        audioRef.current.play().catch(e => console.warn('Звук не воспроизведён:', e));

        setIsAnimating(true);

        // Завершаем анимацию
        setTimeout(() => {
            setIsAnimating(false);
            setIsRevealed(true);
            setIsOverlayVisible(true);
        }, 1000);
    };

    const handleOverlayClick = () => {
        setIsOverlayVisible(false);
    };

    return (
        <>
            <div
                className={`tarot-card ${isAnimating ? 'animating' : ''} ${isRevealed ? 'flipped' : ''}`}
                onClick={handleClick}
            >
                <div className="card-inner">
                    <div className="card-spin-wrapper">
                        <div className="card-front">
                            <img src={get_icon(card.name)} width="50" height="50" />
                            <br />
                            <span>{card.name}</span>
                        </div>
                        <div className="card-back">
                            <h3>{card.name}</h3>
                            <p>{card.meaning}</p>
                        </div>
                    </div>
                </div>
            </div>

            {isOverlayVisible && (
                <div className="card-overlay" onClick={handleOverlayClick}>
                    <div className="card-large">
                        <div className="card-inner">
                            <div className="card-spin-wrapper">
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
                </div>
            )}
        </>
    );
}
