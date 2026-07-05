import en from './locales/en.json'
import type { HistoryContent } from './types'

export const defaultLocale = 'en'

export const supportedLocales = [defaultLocale] as const

export type Locale = (typeof supportedLocales)[number]

const historyByLocale: Record<Locale, HistoryContent> = {
    en: en as HistoryContent,
}

export function isLocale(value: string): value is Locale {
    return supportedLocales.some((locale) => locale === value)
}

export function getHistoryContent(
    locale: Locale = defaultLocale
): HistoryContent {
    return historyByLocale[locale]
}
