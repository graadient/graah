import type { CSSProperties, ReactNode } from 'react'
import { useLayoutEffect, useState } from 'react'

import { Button, Card, Chip, Dropdown, Label } from '@heroui/react'

import { Arms, NightHero, Runes, Seal } from '../theme/react'
import type { Locale } from './i18n'
import {
    getHistoryContent,
    getLocaleOption,
    localeOptions,
    resolveInitialLocale,
    storeLocale,
} from './i18n'
import type { Bearer, Chapter, HistoryContent } from './i18n/types'
import { motion, useReducedMotion } from 'framer-motion'
import {
    Anchor,
    ArrowDown,
    ArrowUpRight,
    ChevronDown,
    Flame,
    Radio,
    Snowflake,
} from 'lucide-react'

const bearerIcons = {
    radio: Radio,
    snowflake: Snowflake,
} satisfies Record<Bearer['icon'], typeof Radio>

/** Chapter grounds: the night, a shade deeper, the abyss for the darkest
 * chapters, and the sky for the sea crossing. */
function chapterGround(chapter: Chapter, index: number): string {
    switch (chapter.theme) {
        case 'ink': {
            return 'bg-graah-abyss'
        }
        case 'blue': {
            return 'graah-sky'
        }
        case 'grid':
        case 'mint':
        case 'paper': {
            return index % 2 === 0 ? 'bg-graah-night' : 'bg-[#0D1220]'
        }
        default: {
            return 'bg-graah-night'
        }
    }
}

function Reveal({
    children,
    className,
}: {
    children: ReactNode
    className?: string
}) {
    const reduceMotion = useReducedMotion()
    return (
        <motion.div
            className={className}
            initial={reduceMotion ? false : { opacity: 0, y: 24 }}
            transition={{ duration: 0.7, ease: [0.2, 0.7, 0.2, 1] }}
            viewport={{ once: true, margin: '-80px' }}
            whileInView={{ opacity: 1, y: 0 }}
        >
            {children}
        </motion.div>
    )
}

function LocaleSwitcher({
    content,
    locale,
    onLocaleChange,
}: {
    content: HistoryContent['languageSwitcher']
    locale: Locale
    onLocaleChange: (locale: Locale) => void
}) {
    const active = getLocaleOption(locale)

    return (
        <Dropdown>
            <Dropdown.Trigger>
                <Button
                    aria-label={content.legend}
                    size="sm"
                    variant="tertiary"
                >
                    <span aria-hidden="true">{active.flag}</span>
                    {content.options[locale].label}
                    <ChevronDown aria-hidden="true" size={14} />
                </Button>
            </Dropdown.Trigger>
            <Dropdown.Popover placement="bottom end">
                <Dropdown.Menu
                    aria-label={content.legend}
                    onAction={(key) => {
                        const next = localeOptions.find(
                            (option) => option.locale === key
                        )
                        if (next) {
                            onLocaleChange(next.locale)
                        }
                    }}
                    selectedKeys={[locale]}
                    selectionMode="single"
                >
                    {localeOptions.map((option) => {
                        const copy = content.options[option.locale]
                        return (
                            <Dropdown.Item
                                aria-label={copy.ariaLabel}
                                id={option.locale}
                                key={option.locale}
                                textValue={copy.label}
                            >
                                <Label>
                                    <span aria-hidden="true">
                                        {option.flag}
                                    </span>{' '}
                                    {copy.label}
                                </Label>
                                <Dropdown.ItemIndicator />
                            </Dropdown.Item>
                        )
                    })}
                </Dropdown.Menu>
            </Dropdown.Popover>
        </Dropdown>
    )
}

function ExternalLink({ href, label }: { href: string; label: string }) {
    return (
        <a
            className="graah-link inline-flex items-center gap-1 text-sm"
            href={href}
            rel="noreferrer"
            target="_blank"
        >
            {label}
            <ArrowUpRight aria-hidden="true" className="shrink-0" size={14} />
        </a>
    )
}

function Figure({
    src,
    alt,
    caption,
    className = '',
}: {
    src: string
    alt: string
    caption?: string
    className?: string
}) {
    return (
        <figure
            className={`m-0 border border-graah-line bg-graah-fjord p-2.5 ${className}`}
        >
            <img
                alt={alt}
                className="block h-auto w-full saturate-[.8]"
                loading="lazy"
                src={src}
            />
            {caption ? (
                <figcaption className="px-0.5 pt-2.5 font-graah-mono text-[11px] leading-relaxed tracking-[0.04em] text-graah-smoke">
                    {caption}
                </figcaption>
            ) : null}
        </figure>
    )
}

function ChapterSection({
    chapter,
    index,
    recordHeading,
    sourcesHeading,
}: {
    chapter: Chapter
    index: number
    recordHeading: string
    sourcesHeading: string
}) {
    return (
        <section
            className={`scroll-mt-16 border-t border-graah-line px-5 py-20 sm:px-8 sm:py-28 ${chapterGround(chapter, index)}`}
            id={chapter.id}
        >
            <div className="mx-auto w-full max-w-6xl">
                <Reveal>
                    <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:gap-8">
                        <span
                            aria-hidden="true"
                            className="graah-numeral text-[clamp(84px,14vw,160px)]"
                        >
                            {chapter.numeral}
                        </span>
                        <div className="sm:pb-2">
                            <p className="graah-label m-0">
                                {chapter.years} · {chapter.place}
                            </p>
                            <h2 className="mt-3 mb-0 text-[clamp(38px,5.6vw,68px)] leading-[1.02] break-words hyphens-auto">
                                {chapter.title}
                            </h2>
                        </div>
                    </div>
                    <Chip className="mt-6" color="accent" variant="soft">
                        <span
                            aria-hidden="true"
                            className="mr-1 inline-block size-1.5 rounded-full bg-graah-red"
                        />
                        {chapter.mood.label}
                    </Chip>
                </Reveal>

                <div className="mt-12 grid gap-12 lg:grid-cols-[minmax(0,1.2fr)_minmax(300px,1fr)]">
                    <Reveal>
                        <p className="m-0 font-graah-display text-[clamp(23px,2.4vw,30px)] leading-[1.35] text-graah-rime">
                            {chapter.kicker}.
                        </p>
                        <div className="mt-8 space-y-5 text-[17px] font-light leading-[1.75] text-[#C5D0DC]">
                            {chapter.paragraphs.map((paragraph) => (
                                <p key={paragraph.slice(0, 24)}>{paragraph}</p>
                            ))}
                        </div>
                    </Reveal>

                    <Reveal className="flex flex-col gap-6">
                        {chapter.image ? (
                            <Figure
                                alt={chapter.image.alt}
                                caption={chapter.image.caption}
                                src={chapter.image.src}
                            />
                        ) : null}

                        <div className="graah-panel p-5 sm:p-6">
                            <p className="graah-label m-0">{recordHeading}</p>
                            <ul className="m-0 mt-4 list-none p-0">
                                {chapter.record.map((entry) => (
                                    <li
                                        className="grid grid-cols-[60px_1fr] gap-3 border-t border-graah-line py-2.5 text-[14px] leading-[1.5] font-light text-[#C5D0DC]"
                                        key={entry.year + entry.text}
                                    >
                                        <span className="font-graah-mono text-[13px] text-graah-brass">
                                            {entry.year}
                                        </span>
                                        <span>{entry.text}</span>
                                    </li>
                                ))}
                            </ul>
                            {chapter.sources?.length ? (
                                <div className="mt-3 border-t border-graah-line pt-4">
                                    <p className="graah-label m-0">
                                        {sourcesHeading}
                                    </p>
                                    <ul className="m-0 mt-3 list-none space-y-2 p-0">
                                        {chapter.sources.map((source) => (
                                            <li key={source.label}>
                                                {source.href ? (
                                                    <ExternalLink
                                                        href={source.href}
                                                        label={source.label}
                                                    />
                                                ) : (
                                                    <span className="text-sm text-graah-mist">
                                                        {source.label}
                                                    </span>
                                                )}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            ) : null}
                        </div>

                        {chapter.aside ? (
                            <aside className="rounded-graah-surface border border-graah-brass/45 bg-graah-brass/[0.06] p-5 sm:p-6">
                                <p className="graah-label m-0 flex items-center gap-2">
                                    <Anchor aria-hidden="true" size={14} />
                                    {chapter.aside.title}
                                </p>
                                <p className="mt-3 mb-0 text-[15px] leading-[1.65] text-graah-glacier">
                                    {chapter.aside.text}
                                </p>
                            </aside>
                        ) : null}
                    </Reveal>
                </div>
            </div>
        </section>
    )
}

const emberGround: CSSProperties = {
    background:
        'radial-gradient(90% 75% at 50% 115%, rgba(200, 40, 58, 0.38) 0%, rgba(110, 20, 20, 0.22) 38%, transparent 70%), #080B14',
}

function FireInterstitial({
    content,
}: {
    content: HistoryContent['fireInterstitial']
}) {
    return (
        <section
            className="border-t border-graah-line px-5 py-24 sm:px-8 sm:py-32"
            style={emberGround}
        >
            <Reveal className="mx-auto w-full max-w-6xl">
                <p className="m-0 flex items-center gap-3 font-graah-mono text-xs uppercase tracking-[0.2em] text-[#F0B44C]">
                    <Flame aria-hidden="true" size={16} />
                    {content.label}
                </p>
                <p className="mt-8 mb-0 font-graah-display text-[clamp(52px,10vw,136px)] leading-[0.95] text-graah-rime">
                    {content.titlePrefix}{' '}
                    <span className="text-[#E5484D] [text-shadow:0_0_28px_rgba(240,110,60,0.55),0_0_6px_rgba(240,180,76,0.35)]">
                        {content.titleEmphasis}
                    </span>
                </p>
                <p className="mt-10 mb-0 max-w-2xl text-lg leading-[1.7] font-light text-[#C5D0DC] sm:text-xl">
                    {content.body}
                </p>
                {content.sources?.length ? (
                    <ul className="m-0 mt-8 flex list-none flex-wrap gap-x-6 gap-y-3 p-0">
                        {content.sources.map((source) =>
                            source.href ? (
                                <li key={source.label}>
                                    <ExternalLink
                                        href={source.href}
                                        label={source.label}
                                    />
                                </li>
                            ) : null
                        )}
                    </ul>
                ) : null}
            </Reveal>
        </section>
    )
}

function NameTicker({ nameForms }: { nameForms: string[] }) {
    const sequence = [...nameForms, ...nameForms]
    return (
        <div
            aria-hidden="true"
            className="ticker border-t border-graah-line bg-graah-abyss py-5"
        >
            <div className="ticker-track">
                {sequence.map((form, index) => (
                    <span
                        className="flex items-center gap-8 pr-8 font-graah-display text-[28px] tracking-[0.12em] text-graah-mist sm:text-[34px]"
                        key={`${form}-${index}`}
                    >
                        {form}
                        <span className="text-[18px] text-graah-brass">→</span>
                    </span>
                ))}
            </div>
        </div>
    )
}

function updateMetaTag(selector: string, content: string): void {
    const element = globalThis.document.querySelector<HTMLMetaElement>(selector)
    element?.setAttribute('content', content)
}

export function HistoryPage() {
    const [locale, setLocale] = useState<Locale>(resolveInitialLocale)
    const content = getHistoryContent(locale)
    const firstChapter = content.chapters[0]

    function handleLocaleChange(nextLocale: Locale): void {
        setLocale(nextLocale)
        storeLocale(nextLocale)
    }

    useLayoutEffect(() => {
        const localeOption = getLocaleOption(locale)
        globalThis.document.documentElement.lang = localeOption.htmlLang
        globalThis.document.title = content.meta.htmlTitle
        updateMetaTag('meta[name="description"]', content.meta.description)
        updateMetaTag('meta[property="og:title"]', content.meta.ogTitle)
        updateMetaTag(
            'meta[property="og:description"]',
            content.meta.ogDescription
        )
        return () => {
            globalThis.document.title = content.meta.defaultTitle
        }
    }, [
        content.meta.defaultTitle,
        content.meta.description,
        content.meta.htmlTitle,
        content.meta.ogDescription,
        content.meta.ogTitle,
        locale,
    ])

    return (
        <div className="min-h-screen bg-graah-night text-graah-glacier">
            <header className="fixed inset-x-0 top-0 z-40 border-b border-graah-line bg-graah-night/80 px-5 backdrop-blur-md sm:px-8">
                <nav className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between gap-4">
                    <a
                        className="graah-signature flex items-center gap-3 text-[13px] no-underline"
                        href="#top"
                    >
                        <Arms
                            className="h-7 w-auto"
                            title={content.nav.logoAlt}
                        />
                        {content.nav.brand}
                    </a>
                    <LocaleSwitcher
                        content={content.languageSwitcher}
                        locale={locale}
                        onLocaleChange={handleLocaleChange}
                    />
                </nav>
            </header>

            <main id="top">
                <NightHero style={{ minHeight: 'max(100svh, 640px)' }}>
                    <div className="flex flex-col items-center pt-20">
                        <Arms
                            className="mb-7 h-auto w-[clamp(88px,12vw,150px)] drop-shadow-[0_0_28px_rgba(62,98,184,0.3)]"
                            title={content.nav.logoAlt}
                        />
                        <h1 className="graah-wordmark mt-0 mb-0 text-[clamp(60px,15vw,176px)]">
                            {content.nav.brand}
                        </h1>
                        <Runes className="mt-4 inline-block text-[clamp(16px,2vw,26px)]" />
                        <p className="mt-8 mb-0 font-graah-mono text-[clamp(11px,1.1vw,14px)] uppercase tracking-[0.2em] text-graah-mist">
                            {content.hero.titleLines.join(' ')}
                        </p>
                        <p className="mt-3 mb-0 font-graah-mono text-[clamp(11px,1.1vw,14px)] uppercase tracking-[0.2em] text-graah-brass">
                            {content.hero.startYear} → {content.hero.endYear}
                        </p>
                        <a
                            className="mt-12 inline-flex items-center gap-2 font-graah-mono text-[11px] uppercase tracking-[0.2em] text-graah-smoke no-underline hover:text-graah-glow"
                            href="#intro"
                        >
                            {firstChapter.numeral} · {firstChapter.title}
                            <ArrowDown aria-hidden="true" size={14} />
                        </a>
                    </div>
                </NightHero>

                <section
                    className="scroll-mt-16 px-5 py-24 text-center sm:px-8 sm:py-32"
                    id="intro"
                >
                    <Reveal className="mx-auto max-w-3xl">
                        <p className="graah-label m-0">{content.hero.chip}</p>
                        <p className="mt-8 mb-0 font-graah-display text-[clamp(26px,3.2vw,40px)] leading-[1.3] text-graah-rime">
                            {content.hero.intro}
                        </p>
                        <p className="mt-8 mb-0 font-graah-mono text-[12px] uppercase leading-relaxed tracking-[0.18em] text-graah-brass">
                            {content.hero.introEmphasis}
                        </p>
                    </Reveal>
                    <Reveal className="mx-auto mt-16 max-w-6xl">
                        <dl className="m-0 grid grid-cols-2 overflow-hidden rounded-graah-surface border border-graah-line bg-graah-line gap-px text-left lg:grid-cols-4">
                            {content.chronicleStats.map(({ label, value }) => (
                                <div
                                    className="bg-graah-fjord p-5 sm:p-6"
                                    key={label}
                                >
                                    <dd className="m-0 font-graah-display text-[clamp(40px,5vw,60px)] leading-[0.95] text-graah-glow">
                                        {value}
                                    </dd>
                                    <dt className="mt-3 font-graah-mono text-[11px] uppercase leading-[1.4] tracking-[0.14em] text-graah-smoke">
                                        {label}
                                    </dt>
                                </div>
                            ))}
                        </dl>
                    </Reveal>
                </section>

                <NameTicker nameForms={content.nameForms} />

                {content.chapters.slice(0, 5).map((chapter, index) => (
                    <ChapterSection
                        chapter={chapter}
                        index={index}
                        key={chapter.id}
                        recordHeading={content.chapterRecordHeading}
                        sourcesHeading={content.chapterSourcesHeading}
                    />
                ))}

                <FireInterstitial content={content.fireInterstitial} />

                {content.chapters.slice(5).map((chapter, index) => (
                    <ChapterSection
                        chapter={chapter}
                        index={index + 5}
                        key={chapter.id}
                        recordHeading={content.chapterRecordHeading}
                        sourcesHeading={content.chapterSourcesHeading}
                    />
                ))}

                <section className="border-t border-graah-line bg-graah-abyss px-5 py-20 sm:px-8 sm:py-28">
                    <div className="mx-auto w-full max-w-6xl">
                        <Reveal>
                            <p className="graah-label m-0">
                                {content.bearersSection.eyebrow}
                            </p>
                            <h2 className="mt-3 mb-0 max-w-4xl text-[clamp(38px,5.6vw,68px)] leading-[1.02] break-words hyphens-auto">
                                {content.bearersSection.title}
                            </h2>
                            <p className="mt-5 mb-0 max-w-2xl text-lg leading-[1.65] font-light text-graah-mist">
                                {content.bearersSection.intro}
                            </p>
                        </Reveal>
                        <Reveal className="mt-12">
                            <Figure
                                alt={content.bearersSection.figure.alt}
                                caption={content.bearersSection.figure.caption}
                                src={content.bearersSection.figure.src}
                            />
                        </Reveal>
                        <div className="mt-6 grid gap-6 md:grid-cols-2">
                            {content.bearersSection.bearers.map((bearer) => {
                                const Icon = bearerIcons[bearer.icon]
                                return (
                                    <Reveal key={bearer.name}>
                                        <Card className="h-full p-6">
                                            <Card.Header className="flex flex-row items-start justify-between gap-4">
                                                <div className="flex flex-col gap-2">
                                                    <Card.Description>
                                                        {bearer.years}
                                                    </Card.Description>
                                                    <Card.Title>
                                                        {bearer.name}
                                                    </Card.Title>
                                                </div>
                                                {bearer.img ? (
                                                    <img
                                                        alt={bearer.img.alt}
                                                        className="w-20 shrink-0 border border-graah-line object-cover saturate-[.8]"
                                                        loading="lazy"
                                                        src={bearer.img.src}
                                                    />
                                                ) : (
                                                    <span className="grid size-12 shrink-0 place-items-center rounded-full border border-graah-brass/50 text-graah-brass">
                                                        <Icon
                                                            aria-hidden="true"
                                                            size={20}
                                                        />
                                                    </span>
                                                )}
                                            </Card.Header>
                                            <Card.Content>
                                                <p className="m-0 text-[16px] leading-[1.7] font-light text-[#C5D0DC]">
                                                    {bearer.deed}
                                                </p>
                                            </Card.Content>
                                            {bearer.source?.href ? (
                                                <Card.Footer>
                                                    <ExternalLink
                                                        href={
                                                            bearer.source.href
                                                        }
                                                        label={
                                                            bearer.source.label
                                                        }
                                                    />
                                                </Card.Footer>
                                            ) : null}
                                        </Card>
                                    </Reveal>
                                )
                            })}
                        </div>
                    </div>
                </section>

                <section className="border-t border-graah-line bg-graah-night py-20 sm:py-28">
                    <Reveal className="mx-auto w-full max-w-6xl px-5 sm:px-8">
                        <p className="graah-label m-0">
                            {content.timelineSection.eyebrow}
                        </p>
                        <h2 className="mt-3 mb-0 text-[clamp(38px,5.6vw,68px)] leading-[1.02] break-words hyphens-auto">
                            {content.timelineSection.title}
                        </h2>
                    </Reveal>
                    <div className="mt-12 overflow-x-auto pb-6 [scrollbar-width:thin]">
                        <ol className="relative m-0 flex w-max list-none gap-0 p-0 pr-5 pl-[max(20px,calc((100vw-72rem)/2+2rem))] sm:pr-8">
                            {content.timelineSection.stops.map(
                                (stop, index, stops) => {
                                    const last = index === stops.length - 1
                                    return (
                                        <li
                                            className="relative w-56 shrink-0 pr-6"
                                            key={stop.year + stop.text}
                                        >
                                            <span
                                                aria-hidden="true"
                                                className="absolute top-[5px] right-0 left-0 h-px"
                                                style={{
                                                    background:
                                                        'var(--graah-aurora)',
                                                    backgroundSize: `${stops.length * 100}% 100%`,
                                                    backgroundPosition: `${(index / Math.max(stops.length - 1, 1)) * 100}% 0`,
                                                }}
                                            />
                                            <span
                                                aria-hidden="true"
                                                className={`relative block size-[11px] rounded-full border border-graah-brass ${
                                                    last
                                                        ? 'bg-graah-brass shadow-[0_0_12px_rgba(233,201,138,0.7)]'
                                                        : 'bg-graah-night'
                                                }`}
                                            />
                                            <p className="mt-5 mb-0 font-graah-display text-[30px] leading-none text-graah-rime">
                                                {stop.year}
                                            </p>
                                            <p className="mt-3 mb-0 text-[14px] leading-[1.5] font-light text-graah-mist">
                                                {stop.text}
                                            </p>
                                        </li>
                                    )
                                }
                            )}
                        </ol>
                    </div>
                </section>

                <section className="graah-sky border-t border-graah-line px-5 py-24 text-center sm:px-8 sm:py-32">
                    <Reveal className="mx-auto max-w-4xl">
                        <p className="graah-label m-0">
                            {content.closing.eyebrow}
                        </p>
                        <h2 className="mx-auto mt-5 mb-0 max-w-4xl text-[clamp(40px,6.4vw,84px)] leading-[1.02]">
                            {content.closing.title}
                        </h2>
                        <p className="mx-auto mt-8 mb-0 max-w-2xl text-lg leading-[1.7] font-light text-[#C5D0DC] sm:text-xl">
                            {content.closing.body}
                        </p>
                        <p className="mx-auto mt-12 mb-0 max-w-2xl border-t border-graah-line pt-6 text-[13px] leading-[1.65] text-graah-smoke">
                            {content.closing.note}
                        </p>
                    </Reveal>
                </section>
            </main>

            <hr className="graah-aurora m-0" />
            <footer className="bg-graah-abyss px-5 py-12 sm:px-8">
                <div className="mx-auto flex w-full max-w-6xl flex-wrap items-center gap-8">
                    <Seal size={96} />
                    <div className="flex flex-col gap-3">
                        <span className="graah-signature text-2xl">
                            {content.nav.brand}
                        </span>
                        <Runes className="block text-sm" label="" />
                    </div>
                    <p className="m-0 font-graah-mono text-[11px] uppercase tracking-[0.18em] text-graah-smoke sm:ml-auto">
                        {content.hero.startYear} → {content.hero.endYear}
                    </p>
                </div>
            </footer>
        </div>
    )
}
