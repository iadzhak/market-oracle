import {useRef, useState} from 'react';
import './TarotCard.css';
import flipSound from '../assets/flip.mp3';
import {forecastUrl} from "../api.ts";


function get_icon(token: string) {
    return `https://cryptoicon.io/wp-content/uploads/cc-assets/SVG/Light/${token.toUpperCase()}.svg`
}

type TarotCardProps = {
    "last_price": number,
    "token": string,
    "id": number,
    "target": number,
    "actual": number,
    "news_polarity": number,
    "created_at": string,
    "confidence": number,
    "price_ma_ratio": number,
    "news_subjectivity": number,
    "is_trained": boolean
}

export default function TarotCard({ token }: {token: string}) {
    const [isAnimating, setIsAnimating] = useState(false);
    const [isRevealed, setIsRevealed] = useState(false);
    const [isOverlayVisible, setIsOverlayVisible] = useState(false);
    const audioRef = useRef(new Audio(flipSound));
    const [info, setInfo] = useState<TarotCardProps>();

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

        fetch(forecastUrl(token))
            .then(res=>res.json())
            .then(res=>{
                setInfo(res);
                // Завершаем анимацию
                setIsAnimating(false);
                setIsRevealed(true);
                setIsOverlayVisible(true);
            })

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
                            <img src={get_icon(token)} width="50" height="50" />
                            <br />
                            <span>{token}</span>
                        </div>
                        <div className="card-back">
                            <h2>{token}</h2>
                            <span className={`arrow`}>
                                {info?.target == 1 && '📈'}
                                {info?.target == 0 && '📉'}
                            </span>
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
                                    <span>token</span>
                                </div>
                                <div className="card-back-large">
                                    <h2>{token}</h2>
                                    <p className="forecast-main">Завтра вырастет</p>
                                    <p>уверен на {Math.trunc(info?.confidence * 100)} %</p>
                                    <p>В среднем ошибаюсь в 5%</p>
                                    <p>Текущий тренд по SMA20 вверх на часовом графике</p>
                                    <p>Новостной фон хороший</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
