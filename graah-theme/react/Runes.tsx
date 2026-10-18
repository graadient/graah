import type { HTMLAttributes } from 'react'

import { RUNES } from './geometry'

export interface RunesProps extends HTMLAttributes<HTMLSpanElement> {
    /** Accessible name. Pass '' if decorative. */
    label?: string
}

/**
 * ᚴᚱᛅᛅᚼ, GRAAH in Younger Futhark, glowing in brass (needs graah.css).
 * Only ever the whole name: never use a single rune, and never ᚼ alone,
 * as a symbol or logo.
 */
export function Runes({
    label = 'Graah, in runes',
    className,
    ...rest
}: RunesProps) {
    const a11y =
        label === ''
            ? { 'aria-hidden': true as const }
            : { role: 'img', 'aria-label': label }

    return (
        <span
            className={className ? `graah-runes ${className}` : 'graah-runes'}
            {...a11y}
            {...rest}
        >
            {RUNES}
        </span>
    )
}
