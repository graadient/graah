import type { CSSProperties, ReactNode } from 'react'

import { AuroraArc } from './AuroraArc'
import { Starfield } from './Starfield'

export interface NightHeroProps {
    children: ReactNode
    /** Optional nav or toolbar pinned to the top of the hero. */
    top?: ReactNode
    className?: string
    style?: CSSProperties
}

/**
 * The Night Smithy start page: sky gradient, starfield and aurora arc, with
 * its children centred above the arc. Typical children:
 * <Arms /> + <h1 className="graah-wordmark">GRAAH</h1> + <Runes />.
 */
export function NightHero({ children, top, className, style }: NightHeroProps) {
    return (
        <header
            className={className ? `graah-sky ${className}` : 'graah-sky'}
            style={{
                position: 'relative',
                isolation: 'isolate',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
                minHeight: 'min(92svh, 860px)',
                borderBottom: '1px solid var(--graah-line)',
                ...style,
            }}
        >
            <Starfield />
            <AuroraArc />
            {top ? (
                <div style={{ position: 'relative', zIndex: 2 }}>{top}</div>
            ) : null}
            <div
                style={{
                    position: 'relative',
                    zIndex: 2,
                    flex: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    textAlign: 'center',
                    padding: '0 20px clamp(140px, 22vw, 300px)',
                }}
            >
                {children}
            </div>
        </header>
    )
}
