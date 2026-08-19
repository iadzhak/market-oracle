import {useRef, useState} from 'react';
import './TarotCard.css';
import flipSound from '../assets/flip.mp3';
import {forecastUrl} from "../api.ts";
import arrowUp from '../assets/up.png';
import arrowDown from '../assets/down.png'
import arrowUnknown from '../assets/unknown.png'


function get_icon(token: string) {
    return `https://cryptoicon.io/wp-content/uploads/cc-assets/SVG/Light/${token.toUpperCase()}.svg`
}

function get_arrow(target: number | undefined) {
    if (target == 1) return arrowUp;
    if (target == 0) return arrowDown;
    return arrowUnknown;
}

function get_contributions(t: number | undefined, contr: number[] | undefined) {
    if (!contr) return;
    const [ma, p] = contr
    let reasons = ''
    if (t == 1) {
        if (ma > 0) reasons += 'Восходящий тренд по часовому графику.\n'
        if (p > 0) reasons += 'Новости позитивные.\n'
    }
    if (t == 0) {
        if (ma < 0) reasons += 'Нисходящий тренд по часовому графику.\n'
        if (p < 0) reasons += 'Новости не позитивные.\n'
    }
    return reasons || 'Противоречивые данные, но чутье мне подсказывает что будет так.';
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

type ResponseProps = {
    forecast: TarotCardProps;
    error_raito: number;
    contributions: number[];
}

export default function TarotCard({ token }: {token: string}) {
    const [isAnimating, setIsAnimating] = useState(false);
    const [isRevealed, setIsRevealed] = useState(false);
    const [isOverlayVisible, setIsOverlayVisible] = useState(false);
    const audioRef = useRef(new Audio(flipSound));
    const [info, setInfo] = useState<ResponseProps>();

    const handleClick = () => {

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
                            <img src={get_icon(token)} alt={`${token} icon`} width="50" height="50" />
                            <br />
                            <span>{token}</span>
                        </div>
                        <div className="card-back">
                            <img src={get_arrow(info?.forecast?.target)} alt={`forecast direction`} width="50" height="50" />
                            <br />
                            <span>{token}</span>
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
                                    <p className="forecast-main">
                                        {info?.forecast?.target == 1 && 'Вырастет через сутки'}
                                        {info?.forecast?.target == 0 && 'Упадет через сутки'}
                                    </p>
                                    <p>Уверен на {info?.forecast?.confidence && Math.trunc(info?.forecast.confidence * 100)} %</p>
                                    <p className="errors">В среднем ошибаюсь в {info?.error_raito && Math.trunc(info?.error_raito * 100)}% случаев</p>
                                    <br />
                                    <p>{get_contributions(info?.forecast?.target, info?.contributions)}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
