import type { ReactNode } from 'react'
import { useEffect, useState } from 'react'

import { Button, Chip, Link } from '@heroui/react'

import type { Locale } from './i18n'
import {
    getHistoryContent,
    getLocaleOption,
    localeOptions,
    resolveInitialLocale,
    storeLocale,
} from './i18n'
import type { Bearer, Chapter, HistoryContent, Mood } from './i18n/types'
import { motion, useReducedMotion } from 'framer-motion'
import {
    Anchor,
    ArrowDown,
    ArrowUpRight,
    Flame,
    Radio,
    Snowflake,
} from 'lucide-react'

const themeStyles: Record<Chapter['theme'], string> = {
    paper: 'bg-paper text-ink',
    grid: 'bg-paper bg-grid text-ink',
    blue: 'bg-blue text-ink',
    ink: 'bg-ink text-paper',
    mint: 'bg-mint text-ink',
}

const bearerIcons = {
    radio: Radio,
    snowflake: Snowflake,
} satisfies Record<Bearer['icon'], typeof Radio>

function contact(): void {
    globalThis.location.href = 'mailto:hello@graah.se'
}

function LocaleSwitcher({
    locale,
    onLocaleChange,
}: {
    locale: Locale
    onLocaleChange: (locale: Locale) => void
}) {
    return (
        <fieldset className="flex shrink-0 overflow-hidden rounded-md border-2 border-ink bg-paper shadow-hard">
            <legend className="sr-only">Language</legend>
            {localeOptions.map((option) => {
                const selected = option.locale === locale
                return (
                    <button
                        aria-label={option.ariaLabel}
                        aria-pressed={selected}
                        className={`flex h-9 items-center gap-1.5 border-l-2 border-ink px-2.5 font-mono text-xs font-bold uppercase tracking-normal first:border-l-0 sm:px-3 ${
                            selected
                                ? 'bg-ink text-paper'
                                : 'bg-paper text-ink hover:bg-mint'
                        }`}
                        key={option.locale}
                        onClick={() => {
                            onLocaleChange(option.locale)
                        }}
                        type="button"
                    >
                        <span aria-hidden="true">{option.flag}</span>
                        <span
                            className={selected ? 'inline' : 'hidden sm:inline'}
                        >
                            {option.label}
                        </span>
                    </button>
                )
            })}
        </fieldset>
    )
}

function MoodChip({ mood }: { mood: Mood }) {
    return (
        <span
            className={`inline-flex items-center gap-2 border-2 border-ink ${mood.bg} px-3 py-1 font-mono text-xs font-bold uppercase tracking-normal text-ink`}
        >
            <span className="size-2 rounded-full bg-ink" />
            {mood.label}
        </span>
    )
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
            initial={reduceMotion ? false : { opacity: 0, y: 28 }}
            transition={{ duration: 0.55, ease: 'easeOut' }}
            viewport={{ once: true, margin: '-80px' }}
            whileInView={{ opacity: 1, y: 0 }}
        >
            {children}
        </motion.div>
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
    const dark = chapter.theme === 'ink'
    const borderColor = dark ? 'border-paper' : 'border-ink'
    const shadow = dark ? 'shadow-paper' : 'shadow-hard'
    const tilt = index % 2 === 0 ? 'rotate-1' : '-rotate-1'

    return (
        <section
            className={`border-b-2 border-ink px-4 py-16 sm:px-6 sm:py-24 lg:px-8 ${themeStyles[chapter.theme]}`}
            id={chapter.id}
        >
            <div className="mx-auto w-full max-w-7xl">
                <Reveal>
                    <div className="flex flex-wrap items-end justify-between gap-6">
                        <div className="flex items-end gap-5">
                            <span
                                aria-hidden="true"
                                className="font-serif text-7xl font-medium leading-none text-coral sm:text-9xl"
                            >
                                {chapter.numeral}
                            </span>
                            <div className="pb-1">
                                <p className="font-mono text-sm font-bold uppercase tracking-normal">
                                    {chapter.years} · {chapter.place}
                                </p>
                                <h2 className="mt-2 font-display text-4xl font-black uppercase leading-none tracking-normal sm:text-6xl lg:text-7xl">
                                    {chapter.title}
                                </h2>
                            </div>
                        </div>
                        <MoodChip mood={chapter.mood} />
                    </div>
                </Reveal>

                <div className="mt-10 grid gap-10 lg:grid-cols-[minmax(0,0.62fr)_minmax(280px,0.38fr)]">
                    <Reveal>
                        <p
                            className={`font-serif text-2xl italic leading-9 sm:text-3xl sm:leading-11 ${
                                dark ? 'text-blue' : ''
                            }`}
                        >
                            {chapter.kicker}.
                        </p>
                        <div className="mt-6 space-y-5 font-serif text-lg leading-8 sm:text-xl sm:leading-9">
                            {chapter.paragraphs.map((paragraph) => (
                                <p key={paragraph.slice(0, 24)}>{paragraph}</p>
                            ))}
                        </div>
                    </Reveal>
                    <Reveal>
                        {chapter.image ? (
                            <figure
                                className={`mb-6 border-2 ${borderColor} ${shadow} ${
                                    dark ? 'bg-ink' : 'bg-paper'
                                } p-2 ${tilt}`}
                            >
                                <img
                                    alt={chapter.image.alt}
                                    className={`w-full border-2 ${borderColor} object-cover`}
                                    loading="lazy"
                                    src={chapter.image.src}
                                />
                                {chapter.image.caption ? (
                                    <figcaption className="px-1 pb-1 pt-2 font-mono text-xs font-bold uppercase tracking-normal">
                                        {chapter.image.caption}
                                    </figcaption>
                                ) : null}
                            </figure>
                        ) : null}
                        <div
                            className={`border-2 ${borderColor} ${shadow} ${
                                dark ? 'bg-ink' : 'bg-paper'
                            } p-5`}
                        >
                            <p className="font-mono text-xs font-bold uppercase tracking-normal">
                                {recordHeading}
                            </p>
                            <ul className="mt-4 space-y-3">
                                {chapter.record.map((entry) => (
                                    <li
                                        className={`flex gap-4 border-t-2 ${borderColor} pt-3 first:border-t-0 first:pt-0`}
                                        key={entry.year + entry.text}
                                    >
                                        <span className="w-14 shrink-0 font-display text-lg font-black">
                                            {entry.year}
                                        </span>
                                        <span className="text-sm font-semibold leading-6">
                                            {entry.text}
                                        </span>
                                    </li>
                                ))}
                            </ul>
                            {chapter.sources?.length ? (
                                <div
                                    className={`mt-4 border-t-2 ${borderColor} pt-3`}
                                >
                                    <p className="font-mono text-xs font-bold uppercase tracking-normal">
                                        {sourcesHeading}
                                    </p>
                                    <ul className="mt-2 space-y-1.5">
                                        {chapter.sources.map((source) => (
                                            <li key={source.label}>
                                                {source.href ? (
                                                    <a
                                                        className="inline-flex items-center gap-1 text-sm font-bold underline decoration-2 underline-offset-2 hover:decoration-coral"
                                                        href={source.href}
                                                        rel="noreferrer"
                                                        target="_blank"
                                                    >
                                                        {source.label}
                                                        <ArrowUpRight
                                                            aria-hidden="true"
                                                            size={14}
                                                        />
                                                    </a>
                                                ) : (
                                                    <span className="text-sm font-semibold">
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
                            <div
                                className={`mt-4 border-2 ${borderColor} ${shadow} bg-signal p-5 text-ink`}
                            >
                                <p className="flex items-center gap-2 font-mono text-xs font-bold uppercase tracking-normal">
                                    <Anchor aria-hidden="true" size={14} />
                                    {chapter.aside.title}
                                </p>
                                <p className="mt-2 font-serif text-base leading-7">
                                    {chapter.aside.text}
                                </p>
                            </div>
                        ) : null}
                    </Reveal>
                </div>
            </div>
        </section>
    )
}

function FireInterstitial({
    content,
}: {
    content: HistoryContent['fireInterstitial']
}) {
    return (
        <section className="border-b-2 border-ink bg-ink bg-stripes-coral px-4 py-20 text-paper sm:px-6 sm:py-28 lg:px-8">
            <div className="mx-auto w-full max-w-7xl">
                <Reveal>
                    <p className="flex items-center gap-3 font-mono text-sm font-bold uppercase tracking-normal text-coral">
                        <Flame aria-hidden="true" size={18} />
                        {content.label}
                    </p>
                    <p className="mt-6 max-w-6xl font-display text-[clamp(3rem,10vw,8.5rem)] font-black uppercase leading-[0.85] tracking-normal">
                        {content.titlePrefix}{' '}
                        <span className="text-coral">
                            {content.titleEmphasis}
                        </span>
                    </p>
                    <p className="mt-8 max-w-2xl font-serif text-xl italic leading-9 text-paper/85 sm:text-2xl sm:leading-10">
                        {content.body}
                    </p>
                </Reveal>
            </div>
        </section>
    )
}

function NameTicker({ nameForms }: { nameForms: string[] }) {
    const sequence = [...nameForms, ...nameForms]
    return (
        <div
            aria-hidden="true"
            className="ticker border-b-2 border-ink bg-signal py-4"
        >
            <div className="ticker-track">
                {sequence.map((form, index) => (
                    <span
                        className="flex items-center gap-6 pr-6 font-display text-2xl font-black tracking-normal text-ink sm:text-3xl"
                        key={`${form}-${index}`}
                    >
                        {form}
                        <span className="text-coral">→</span>
                    </span>
                ))}
            </div>
        </div>
    )
}

export function HistoryPage() {
    const [locale, setLocale] = useState<Locale>(resolveInitialLocale)
    const content = getHistoryContent(locale)

    function handleLocaleChange(nextLocale: Locale): void {
        setLocale(nextLocale)
        storeLocale(nextLocale)
    }

    useEffect(() => {
        const localeOption = getLocaleOption(locale)
        globalThis.document.documentElement.lang = localeOption.htmlLang
        globalThis.document.title = content.meta.htmlTitle
        return () => {
            globalThis.document.title = content.meta.defaultTitle
        }
    }, [content.meta.defaultTitle, content.meta.htmlTitle, locale])

    return (
        <div className="min-h-screen bg-paper text-ink">
            <header className="fixed inset-x-0 top-0 z-40 border-b-2 border-ink bg-paper/92 backdrop-blur">
                <nav className="mx-auto flex h-16 w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
                    <Link className="flex items-center gap-3 text-ink" href="/">
                        <img
                            alt={content.nav.logoAlt}
                            className="h-11 w-auto"
                            src="/graah-coa.png"
                        />
                        <span className="font-display text-xl font-black tracking-normal">
                            {content.nav.brand}
                        </span>
                    </Link>
                    <LocaleSwitcher
                        locale={locale}
                        onLocaleChange={handleLocaleChange}
                    />
                </nav>
            </header>

            <main>
                <section className="relative isolate overflow-hidden border-b-2 border-ink bg-grid px-4 pb-14 pt-28 sm:px-6 sm:pb-20 sm:pt-36 lg:px-8">
                    <div className="absolute right-[-16rem] top-24 -z-10 h-[70vmin] max-h-[680px] min-h-[320px] w-[70vmin] min-w-[320px] max-w-[680px] -rotate-6 opacity-15 sm:right-[-6rem]">
                        <img
                            alt={content.hero.crestAlt}
                            className="h-full w-full object-contain"
                            src="/graah-crest.svg"
                        />
                    </div>
                    <div className="mx-auto w-full max-w-7xl">
                        <Chip className="mb-6 rounded-md border-2 border-ink bg-coral px-3 font-bold text-ink">
                            {content.hero.chip}
                        </Chip>
                        <h1 className="max-w-6xl font-display text-[clamp(3.2rem,11vw,9.5rem)] font-black uppercase leading-[0.82] tracking-normal">
                            {content.hero.titleLines.map((line) => (
                                <span key={line}>
                                    {line}
                                    <br />
                                </span>
                            ))}
                        </h1>
                        <p className="mt-8 max-w-3xl font-serif text-xl leading-9 sm:text-2xl sm:leading-10">
                            {content.hero.intro}{' '}
                            <em>{content.hero.introEmphasis}</em>
                        </p>
                        <div className="mt-10 flex flex-wrap items-center gap-3">
                            <span className="border-2 border-ink bg-ink px-4 py-2 font-display text-2xl font-black text-paper shadow-hard sm:text-3xl">
                                {content.hero.startYear}
                            </span>
                            <ArrowDown
                                aria-hidden="true"
                                className="-rotate-90"
                                size={26}
                            />
                            <span className="border-2 border-ink bg-mint px-4 py-2 font-display text-2xl font-black text-ink shadow-hard sm:text-3xl">
                                {content.hero.endYear}
                            </span>
                        </div>
                        <div className="mt-12 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                            {content.chronicleStats.map(
                                ({ bg, label, value }) => (
                                    <div
                                        className={`border-2 border-ink ${bg} p-4 text-ink shadow-hard`}
                                        key={label}
                                    >
                                        <p className="font-display text-4xl font-black tracking-normal">
                                            {value}
                                        </p>
                                        <p className="mt-2 text-sm font-bold uppercase leading-6">
                                            {label}
                                        </p>
                                    </div>
                                )
                            )}
                        </div>
                    </div>
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

                <section className="border-b-2 border-ink bg-ink py-16 text-paper sm:py-24">
                    <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
                        <Reveal>
                            <p className="font-mono text-sm font-bold uppercase tracking-normal text-blue">
                                {content.bearersSection.eyebrow}
                            </p>
                            <h2 className="mt-2 max-w-4xl font-display text-4xl font-black uppercase tracking-normal sm:text-6xl">
                                {content.bearersSection.title}
                            </h2>
                            <p className="mt-4 max-w-2xl font-serif text-lg italic leading-8 text-paper/80">
                                {content.bearersSection.intro}
                            </p>
                        </Reveal>
                        <Reveal>
                            <figure className="mt-10 -rotate-1 border-2 border-paper bg-paper p-2 text-ink shadow-paper">
                                <img
                                    alt={content.bearersSection.figure.alt}
                                    className="w-full border-2 border-ink object-cover"
                                    loading="lazy"
                                    src={content.bearersSection.figure.src}
                                />
                                <figcaption className="px-1 pb-1 pt-2 font-mono text-xs font-bold uppercase tracking-normal">
                                    {content.bearersSection.figure.caption}
                                </figcaption>
                            </figure>
                        </Reveal>
                        <div className="mt-6 grid gap-4 md:grid-cols-2">
                            {content.bearersSection.bearers.map((bearer) => {
                                const Icon = bearerIcons[bearer.icon]
                                return (
                                    <Reveal key={bearer.name}>
                                        <div className="h-full border-2 border-paper bg-paper p-6 text-ink shadow-paper">
                                            <div className="flex items-center justify-between">
                                                <span className="font-mono text-sm font-bold uppercase tracking-normal">
                                                    {bearer.years}
                                                </span>
                                                {bearer.img ? (
                                                    <img
                                                        alt={bearer.img.alt}
                                                        className="w-20 border-2 border-ink object-cover"
                                                        loading="lazy"
                                                        src={bearer.img.src}
                                                    />
                                                ) : (
                                                    <span className="grid size-11 place-items-center border-2 border-ink bg-blue">
                                                        <Icon
                                                            aria-hidden="true"
                                                            size={22}
                                                            strokeWidth={2.4}
                                                        />
                                                    </span>
                                                )}
                                            </div>
                                            <h3 className="mt-5 font-display text-2xl font-black leading-8 tracking-normal">
                                                {bearer.name}
                                            </h3>
                                            <p className="mt-3 font-serif text-base leading-7">
                                                {bearer.deed}
                                            </p>
                                            {bearer.source?.href ? (
                                                <a
                                                    className="mt-4 inline-flex items-center gap-1 text-sm font-bold underline decoration-2 underline-offset-2 hover:decoration-coral"
                                                    href={bearer.source.href}
                                                    rel="noreferrer"
                                                    target="_blank"
                                                >
                                                    {bearer.source.label}
                                                    <ArrowUpRight
                                                        aria-hidden="true"
                                                        size={14}
                                                    />
                                                </a>
                                            ) : null}
                                        </div>
                                    </Reveal>
                                )
                            })}
                        </div>
                    </div>
                </section>

                <section className="border-b-2 border-ink bg-paper py-16 sm:py-20">
                    <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
                        <Reveal>
                            <p className="font-mono text-sm font-bold uppercase tracking-normal">
                                {content.timelineSection.eyebrow}
                            </p>
                            <h2 className="mt-2 font-display text-4xl font-black uppercase tracking-normal sm:text-6xl">
                                {content.timelineSection.title}
                            </h2>
                        </Reveal>
                    </div>
                    <div className="mt-8 overflow-x-auto pb-6">
                        <div className="mx-auto flex w-max gap-4 px-4 sm:px-6 lg:px-8">
                            {content.timelineSection.stops.map((stop) => (
                                <div
                                    className="w-52 shrink-0 border-2 border-ink bg-paper p-4 shadow-hard"
                                    key={stop.year + stop.text}
                                >
                                    <p className="font-display text-3xl font-black">
                                        {stop.year}
                                    </p>
                                    <p className="mt-2 text-sm font-semibold leading-6">
                                        {stop.text}
                                    </p>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>

                <section className="bg-coral px-4 py-16 text-ink sm:px-6 sm:py-24 lg:px-8">
                    <div className="mx-auto w-full max-w-7xl">
                        <Reveal>
                            <p className="font-mono text-sm font-bold uppercase tracking-normal">
                                {content.closing.eyebrow}
                            </p>
                            <h2 className="mt-3 max-w-6xl font-display text-[clamp(2.6rem,7.5vw,6.5rem)] font-black uppercase leading-[0.88] tracking-normal">
                                {content.closing.title}
                            </h2>
                            <p className="mt-8 max-w-3xl font-serif text-xl leading-9">
                                {content.closing.body}
                            </p>
                            <div className="mt-10 flex flex-wrap gap-3">
                                <Button
                                    className="h-12 rounded-md border-2 border-ink bg-ink px-5 font-bold text-paper shadow-hard"
                                    onPress={contact}
                                    variant="primary"
                                >
                                    {content.closing.cta}
                                    <ArrowUpRight
                                        aria-hidden="true"
                                        size={19}
                                    />
                                </Button>
                            </div>
                            <p className="mt-10 max-w-3xl border-t-2 border-ink pt-5 text-sm font-semibold leading-6">
                                {content.closing.note}
                            </p>
                        </Reveal>
                    </div>
                </section>
            </main>
        </div>
    )
}
