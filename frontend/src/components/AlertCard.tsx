import {useState} from 'react';
import './TarotCard.css';
import './AlertCard.css';

const info = {
    name: '⚠️ Предупреждение',
    meaning: `Cервис носит демонстрационный характер.\n    Не является финансовой рекомендацией, не гарантирует доходность и не предназначен для\n    проведения реальных финансовых операций.`
}

export default function AlertCard() {
    const [isOverlayVisible, setIsOverlayVisible] = useState(false);

    return (
        <>
            <div
                className="tarot-card flipped"
                onClick={() => setIsOverlayVisible(true)}
            >
                <div className="card-inner">
                    <div className="card-spin-wrapper">
                        <div className="card-front">
                            <span>{info.name}</span>
                        </div>
                        <div className="card-back">
                            <h3>{info.name}</h3>
                            <p className="alert">{info.meaning}</p>
                        </div>
                    </div>
                </div>
            </div>

            {isOverlayVisible && (
                <div className="card-overlay" onClick={() => setIsOverlayVisible(false)}>
                    <div className="card-large">
                        <div className="card-inner">
                            <div className="card-spin-wrapper">
                                <div className="card-front-large">
                                    <span>{info.name}</span>
                                </div>
                                <div className="card-back-large">
                                    <h3>{info.name}</h3>
                                    <p>{info.meaning}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
