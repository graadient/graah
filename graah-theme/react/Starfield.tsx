import type { CSSProperties } from 'react'
import { useMemo } from 'react'

export interface StarfieldProps {
    /** Number of stars. Default 170. */
    count?: number
    /** Same seed, same sky. Default 7 (the graah.se sky). */
    seed?: number
    /** Every nth star twinkles. Default 9. */
    twinkleEvery?: number
    className?: string
    style?: CSSProperties
}

function seeded(seed: number): () => number {
    let state = seed
    return () => {
        state = (state * 16_807) % 2_147_483_647
        return state / 2_147_483_647
    }
}

/**
 * The night sky: small glacier-white stars, a few twinkling (needs
 * graah.css for the .graah-twinkle animation). Fills its positioned parent.
 */
export function Starfield({
    count = 170,
    seed = 7,
    twinkleEvery = 9,
    className,
    style,
}: StarfieldProps) {
    const stars = useMemo(() => {
        const random = seeded(seed)
        return Array.from({ length: count }, (_, index) => ({
            cx: random() * 1200,
            cy: random() * 520,
            r: random() * 1.1 + 0.2,
            opacity: random() * 0.6 + 0.15,
            twinkle: index % twinkleEvery === 0,
            delay: random() * 6,
        }))
    }, [count, seed, twinkleEvery])

    return (
        <svg
            aria-hidden="true"
            className={className}
            preserveAspectRatio="xMidYMid slice"
            style={{
                position: 'absolute',
                inset: 0,
                width: '100%',
                height: '100%',
                ...style,
            }}
            viewBox="0 0 1200 700"
        >
            {stars.map((star) => (
                <circle
                    className={star.twinkle ? 'graah-twinkle' : undefined}
                    cx={star.cx}
                    cy={star.cy}
                    fill="#DCE6EE"
                    key={`${star.cx}-${star.cy}`}
                    opacity={star.opacity}
                    r={star.r}
                    style={
                        star.twinkle
                            ? { animationDelay: `${star.delay}s` }
                            : undefined
                    }
                />
            ))}
        </svg>
    )
}
