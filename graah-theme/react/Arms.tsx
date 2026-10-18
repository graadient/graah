import type { SVGProps } from 'react'
import { useId } from 'react'

import { ARMS_MARKUP, ARMS_TITLE, ARMS_VIEWBOX } from './geometry'

export type ArmsVariant = 'shaded' | 'flat' | 'mono'

export interface ArmsProps
    extends Omit<
        SVGProps<SVGSVGElement>,
        'children' | 'dangerouslySetInnerHTML'
    > {
    /** shaded: screens (default). flat: print, small sizes. mono: one colour. */
    variant?: ArmsVariant
    /** mono only. Defaults to currentColor. */
    color?: string
    /** Accessible name. Pass '' if the arms are decorative. */
    title?: string
}

/**
 * The Graah arms: a faithful trace of the family's original. Never redraw,
 * recolour (other than mono) or rearrange them. Size with height or className;
 * width follows the 156:192 aspect.
 */
export function Arms({
    variant = 'shaded',
    color = 'currentColor',
    title = ARMS_TITLE,
    ...rest
}: ArmsProps) {
    const uid = `graah-arms-${useId().replace(/[^a-zA-Z0-9]/g, '')}`
    const markup = ARMS_MARKUP[variant]
        .replaceAll('__UID__', uid)
        .replaceAll('__COLOR__', color.replace(/["<>]/g, ''))
    const a11y =
        title === ''
            ? { 'aria-hidden': true as const }
            : { role: 'img', 'aria-label': title }

    return (
        <svg
            viewBox={ARMS_VIEWBOX}
            xmlns="http://www.w3.org/2000/svg"
            {...a11y}
            {...rest}
            dangerouslySetInnerHTML={{ __html: markup }}
        />
    )
}
