import {useState} from 'react';
import './TarotCard.css';

interface TarotCardProps {
    card: { id: number; name: string; meaning: string };
}

export default function AlertCard({ card }: TarotCardProps) {
    const [isAnimating, setIsAnimating] = useState(false);
    const [isRevealed, setIsRevealed] = useState(false);
    const [isOverlayVisible, setIsOverlayVisible] = useState(false);

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

        setIsAnimating(true);

        // Завершаем анимацию
        setTimeout(() => {
            setIsAnimating(false);
            setIsRevealed(true);
            setIsOverlayVisible(true);
        }, 100);
    };

    const handleOverlayClick = () => {
        setIsOverlayVisible(false);
    };

    return (
        <>
            <div
                className={`tarot-card flipped`}
                onClick={handleClick}
            >
                <div className="card-inner">
                    <div className="card-spin-wrapper">
                        <div className="card-front">
                            <span>{card.name}</span>
                        </div>
                        <div className="card-back">
                            <h3>⚠️ Предупреждение</h3>
                            <p></p>
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
