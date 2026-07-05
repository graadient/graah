import en from './locales/en.json'
import sv from './locales/sv.json'
import type { HistoryContent } from './types'

export const defaultLocale = 'en'

export const supportedLocales = ['en', 'sv'] as const

export type Locale = (typeof supportedLocales)[number]

export interface LocaleOption {
    locale: Locale
    flag: string
    label: string
    htmlLang: string
    ariaLabel: string
}

const localeStorageKey = 'graah-locale'

export const localeOptions: readonly LocaleOption[] = [
    {
        locale: 'sv',
        flag: '🇸🇪',
        label: 'Sverige',
        htmlLang: 'sv',
        ariaLabel: 'Byt till svenska',
    },
    {
        locale: 'en',
        flag: '🇬🇧',
        label: 'English',
        htmlLang: 'en',
        ariaLabel: 'Switch to English',
    },
]

const historyByLocale: Record<Locale, HistoryContent> = {
    en: en as HistoryContent,
    sv: sv as HistoryContent,
}

export function isLocale(value: string): value is Locale {
    return supportedLocales.some((locale) => locale === value)
}

export function normalizeLocale(value: string): Locale | null {
    const primaryLanguage = value.toLowerCase().split('-')[0]
    return isLocale(primaryLanguage) ? primaryLanguage : null
}

function getNavigatorLanguages(): readonly string[] {
    if (!('navigator' in globalThis)) {
        return []
    }

    if (globalThis.navigator.languages.length > 0) {
        return globalThis.navigator.languages
    }

    return [globalThis.navigator.language]
}

export function detectLocale(
    languages: readonly string[] = getNavigatorLanguages()
): Locale {
    for (const language of languages) {
        const locale = normalizeLocale(language)

        if (locale) {
            return locale
        }
    }

    return defaultLocale
}

export function getLocaleOption(locale: Locale): LocaleOption {
    return (
        localeOptions.find((option) => option.locale === locale) ??
        localeOptions[0]
    )
}

export function readStoredLocale(): Locale | null {
    if (!('localStorage' in globalThis)) {
        return null
    }

    try {
        const storedLocale = globalThis.localStorage.getItem(localeStorageKey)
        return storedLocale ? normalizeLocale(storedLocale) : null
    } catch {
        return null
    }
}

export function storeLocale(locale: Locale): void {
    if (!('localStorage' in globalThis)) {
        return
    }

    try {
        globalThis.localStorage.setItem(localeStorageKey, locale)
    } catch {
        // Browsers can reject storage in private or locked-down contexts.
    }
}

export function resolveInitialLocale(): Locale {
    return readStoredLocale() ?? detectLocale()
}

export function getHistoryContent(
    locale: Locale = defaultLocale
): HistoryContent {
    return historyByLocale[locale]
}
