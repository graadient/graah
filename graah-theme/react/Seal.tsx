import type { SVGProps } from 'react'
import { useId } from 'react'

import { ARMS_MARKUP, SEAL_ARMS_TRANSFORM, SEAL_RING_PATH } from './geometry'

export interface SealProps
    extends Omit<
        SVGProps<SVGSVGElement>,
        'children' | 'dangerouslySetInnerHTML'
    > {
    /** Width and height in px (or any CSS length). Default 160. */
    size?: number | string
    /** wax: oxblood seal with brass (default). ink: one colour, lines only. */
    variant?: 'wax' | 'ink'
    /** Metal / ink colour. Default brass; for ink, defaults to currentColor. */
    color?: string
    /** Accessible name. Pass '' if decorative. */
    title?: string
}

/**
 * The Graah seal: the arms in brass, ringed by runes reading
 * ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ (Graah · Søllested). The runes are outlines, so no
 * font is needed. Use at 64px and up; below that, use <Arms> alone.
 */
export function Seal({
    size = 160,
    variant = 'wax',
    color,
    title = 'The Graah seal',
    ...rest
}: SealProps) {
    const uid = `graah-seal-${useId().replace(/[^a-zA-Z0-9]/g, '')}`
    const metal = color ?? (variant === 'ink' ? 'currentColor' : '#C9A15E')
    const arms = ARMS_MARKUP.mono
        .replaceAll('__UID__', uid)
        .replaceAll('__COLOR__', metal.replace(/["<>]/g, ''))
        .replace('stroke-width="3.2"', 'stroke-width="4"')
    const a11y =
        title === '' ? { 'aria-hidden': true as const } : { role: 'img' }

    return (
        <svg
            height={size}
            viewBox="0 0 200 200"
            width={size}
            xmlns="http://www.w3.org/2000/svg"
            {...a11y}
            {...rest}
        >
            <title>{title}</title>
            {variant === 'wax' ? (
                <>
                    <circle cx="100" cy="100" fill="#6E1414" r="97" />
                    <circle
                        cx="100"
                        cy="100"
                        fill="none"
                        r="92"
                        stroke="#9A2A2A"
                        strokeWidth="2"
                    />
                </>
            ) : (
                <>
                    <circle
                        cx="100"
                        cy="100"
                        fill="none"
                        r="96"
                        stroke={metal}
                        strokeWidth="2.4"
                    />
                    <circle
                        cx="100"
                        cy="100"
                        fill="none"
                        r="88"
                        stroke={metal}
                        strokeWidth="0.8"
                    />
                </>
            )}
            <circle
                cx="100"
                cy="100"
                fill="none"
                r="60"
                stroke={metal}
                strokeWidth="1"
            />
            <path d={SEAL_RING_PATH} fill={metal} />
            <g
                dangerouslySetInnerHTML={{ __html: arms }}
                transform={SEAL_ARMS_TRANSFORM}
            />
        </svg>
    )
}
