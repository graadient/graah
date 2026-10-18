import type { CSSProperties } from 'react'
import { useId } from 'react'

export interface AuroraArcProps {
    className?: string
    style?: CSSProperties
}

const BANDS = [
    ['#3E62B8', 0],
    ['#C9A15E', 15],
    ['#C8283A', 30],
] as const

/**
 * The planet's edge at the bottom of a hero, traced by three hairlines in the
 * colours of the bend: steel, brass, red. Sits at the bottom of its positioned
 * parent; reserve about 26vw (max 330px) of bottom padding for it.
 */
export function AuroraArc({ className, style }: AuroraArcProps) {
    const gradient = `graah-planet-${useId().replace(/[^a-zA-Z0-9]/g, '')}`

    return (
        <svg
            aria-hidden="true"
            className={className}
            preserveAspectRatio="none"
            style={{
                position: 'absolute',
                bottom: 0,
                left: '-4%',
                width: '108%',
                height: 'clamp(140px, 26vw, 330px)',
                zIndex: 1,
                ...style,
            }}
            viewBox="0 0 1200 300"
        >
            <defs>
                <linearGradient id={gradient} x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0" stopColor="#101A33" />
                    <stop offset="1" stopColor="#0B0F1A" />
                </linearGradient>
            </defs>
            <path
                d="M-20 300 Q600 40 1220 300"
                fill="none"
                opacity=".13"
                stroke="#3E62B8"
                strokeWidth="46"
            />
            <path d="M-20 300 Q600 40 1220 300 Z" fill={`url(#${gradient})`} />
            {BANDS.map(([color, offset]) => (
                <path
                    d={`M-20 ${300 + offset} Q600 ${40 + offset} 1220 ${300 + offset}`}
                    fill="none"
                    key={color}
                    stroke={color}
                    strokeWidth="1.2"
                    vectorEffect="non-scaling-stroke"
                />
            ))}
        </svg>
    )
}
