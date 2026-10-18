import { useEffect, useState } from 'react'

import type { Key } from '@heroui/react'
import {
    Accordion,
    Alert,
    Button,
    Card,
    Chip,
    Description,
    Dropdown,
    Label,
    Link,
    ProgressBar,
    Separator,
    Switch,
    Tabs,
    ToggleButton,
    ToggleButtonGroup,
    Tooltip,
} from '@heroui/react'

import { Arms, NightHero, Runes, Seal } from '../../graah-theme/react'
import type { Locale } from '../i18n'
import { getHistoryContent, localeOptions } from '../i18n'

type LabTheme = 'graah' | 'dark'

const SHOWCASE_CHAPTERS = [0, 3, 6] as const

const TOKENS: ReadonlyArray<[string, string, string]> = [
    ['--background', '#0B0F1A', 'Polar night'],
    ['--surface', '#111829', 'Deep fjord'],
    ['--foreground', '#DCE6EE', 'Glacier'],
    ['--muted', '#8EA0B8', 'Sea smoke'],
    ['--accent', '#C9A15E', 'Brass'],
    ['--link', '#E9C98A', 'Rune glow'],
    ['--danger', '#C8283A', 'Star red'],
    ['--border', '#26304A', 'Fjord line'],
]

const LOCALE_NAMES: Record<Locale, string> = {
    da: 'Dansk',
    sv: 'Svenska',
    nb: 'Norsk',
    fi: 'Suomi',
    is: 'Íslenska',
    fo: 'Føroyskt',
    fr: 'Français',
    en: 'English',
}

function Panel({
    label,
    children,
    className = '',
}: {
    label: string
    children: React.ReactNode
    className?: string
}) {
    return (
        <section
            className={`lab-panel flex flex-col gap-5 rounded-sm p-6 ${className}`}
        >
            <span className="graah-label">{label}</span>
            {children}
        </section>
    )
}

export function ThemeLab() {
    const [theme, setTheme] = useState<LabTheme>(() =>
        new URLSearchParams(globalThis.location.search).get('theme') === 'dark'
            ? 'dark'
            : 'graah'
    )
    const [newsreader, setNewsreader] = useState(false)
    const [locale, setLocale] = useState<Locale>('en')
    const [chapterKey, setChapterKey] = useState<Key>('ch-3')

    const content = getHistoryContent(locale)
    const recordChapter = content.chapters[3]

    useEffect(() => {
        const root = document.documentElement
        root.dataset.theme = theme
        root.classList.toggle('dark', theme === 'dark')
        if (newsreader) {
            root.dataset.body = 'newsreader'
        } else {
            delete root.dataset.body
        }
        root.lang = locale
    }, [theme, newsreader, locale])

    return (
        <div className="min-h-screen bg-background font-graah-body text-foreground">
            {/* Lab toolbar */}
            <div className="sticky top-0 z-30 border-b border-border bg-background/90 backdrop-blur">
                <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-5 py-3">
                    <div className="font-graah-mono text-[11px] uppercase tracking-[0.18em] text-muted">
                        Theme lab v0.7 · <Link href="/theme-lab/v6/">v0.6</Link>{' '}
                        · <Link href="/theme-lab/v5/">v0.5</Link>
                    </div>
                    <ToggleButtonGroup
                        aria-label="Theme"
                        disallowEmptySelection
                        onSelectionChange={(keys) => {
                            const [next] = [...keys]
                            if (next === 'graah' || next === 'dark') {
                                setTheme(next)
                            }
                        }}
                        selectedKeys={[theme]}
                        selectionMode="single"
                        size="sm"
                    >
                        <ToggleButton id="graah">Graah theme</ToggleButton>
                        <ToggleButton id="dark">
                            <ToggleButtonGroup.Separator />
                            HeroUI default
                        </ToggleButton>
                    </ToggleButtonGroup>
                </div>
            </div>

            {/* Hero: Graah brand art from graah-theme/react + HeroUI controls */}
            <NightHero
                top={
                    <nav className="mx-auto flex w-full max-w-6xl items-center justify-between gap-4 px-5 py-5">
                        <a
                            className="graah-signature flex items-center gap-3 text-sm no-underline"
                            href="#top"
                        >
                            <Arms className="h-6 w-auto" title="" />
                            GRAAH
                        </a>
                        <div className="hidden items-center gap-6 md:flex">
                            <Link href="#components">Chronicle</Link>
                            <Link href="#receipts">Receipts</Link>
                            <Link href="#tokens">Tokens</Link>
                        </div>
                        <Dropdown>
                            <Dropdown.Trigger>
                                <Button size="sm" variant="tertiary">
                                    {localeOptions.find(
                                        (o) => o.locale === locale
                                    )?.flag ?? ''}{' '}
                                    {LOCALE_NAMES[locale]}
                                </Button>
                            </Dropdown.Trigger>
                            <Dropdown.Popover placement="bottom end">
                                <Dropdown.Menu
                                    aria-label="Language"
                                    onAction={(key) => {
                                        const next = localeOptions.find(
                                            (o) => o.locale === key
                                        )
                                        if (next) {
                                            setLocale(next.locale)
                                        }
                                    }}
                                    selectedKeys={[locale]}
                                    selectionMode="single"
                                >
                                    {localeOptions.map((option) => (
                                        <Dropdown.Item
                                            id={option.locale}
                                            key={option.locale}
                                            textValue={
                                                LOCALE_NAMES[option.locale]
                                            }
                                        >
                                            <Label>
                                                {option.flag}{' '}
                                                {LOCALE_NAMES[option.locale]}
                                            </Label>
                                            <Dropdown.ItemIndicator />
                                        </Dropdown.Item>
                                    ))}
                                </Dropdown.Menu>
                            </Dropdown.Popover>
                        </Dropdown>
                    </nav>
                }
            >
                <div className="flex max-w-4xl flex-col items-center" id="top">
                    <Arms
                        className="mb-6 h-auto w-[clamp(84px,12vw,150px)] drop-shadow-[0_0_28px_rgba(62,98,184,0.3)]"
                        title={content.hero.crestAlt}
                    />
                    <h1 className="graah-wordmark mt-0 mb-0 text-[clamp(56px,13vw,176px)]">
                        GRAAH
                    </h1>
                    <Tooltip delay={200}>
                        <Tooltip.Trigger>
                            <Runes className="mt-3 inline-block text-[clamp(16px,2vw,26px)]" />
                        </Tooltip.Trigger>
                        <Tooltip.Content showArrow>
                            <Tooltip.Arrow />
                            GRAAH in Younger Futhark: kaun, reið, ár, ár, hagall
                        </Tooltip.Content>
                    </Tooltip>
                    <p className="mt-6 max-w-2xl text-base leading-relaxed text-[#A6B3C4] sm:text-lg">
                        {content.hero.intro}
                    </p>
                    <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
                        <Button
                            onPress={() => {
                                document
                                    .getElementById('components')
                                    ?.scrollIntoView()
                            }}
                        >
                            Read the chronicle
                        </Button>
                        <Button variant="tertiary">The arms</Button>
                    </div>
                </div>
            </NightHero>

            <main className="mx-auto max-w-6xl px-5 py-20">
                <p className="graah-label mb-3">HeroUI × Graah</p>
                <h2 className="m-0 font-graah-display text-[clamp(40px,6vw,76px)] leading-none font-normal">
                    Real HeroUI components, wearing the Graah theme
                </h2>
                <p className="mt-5 max-w-3xl text-lg leading-relaxed text-muted">
                    Every control on this page is a stock HeroUI v3 component.
                    The look comes from the{' '}
                    <Link href="https://github.com/graadient/graah/tree/main/graah-theme">
                        graah-theme
                    </Link>{' '}
                    directory, which any product can use. Use the switch at the
                    top to see the same components in HeroUI's default dark
                    theme.
                </p>

                <div
                    className="mt-12 grid gap-6 lg:grid-cols-[1.35fr_1fr]"
                    id="components"
                >
                    <Panel label="Tabs · Card · Chip · Button">
                        <Tabs
                            onSelectionChange={setChapterKey}
                            selectedKey={String(chapterKey)}
                        >
                            <Tabs.ListContainer>
                                <Tabs.List aria-label="Chapters">
                                    {SHOWCASE_CHAPTERS.map((index) => (
                                        <Tabs.Tab
                                            id={`ch-${index}`}
                                            key={index}
                                        >
                                            {content.chapters[index].numeral}
                                            <Tabs.Indicator />
                                        </Tabs.Tab>
                                    ))}
                                </Tabs.List>
                            </Tabs.ListContainer>
                            {SHOWCASE_CHAPTERS.map((index) => {
                                const chapter = content.chapters[index]
                                return (
                                    <Tabs.Panel
                                        className="pt-5"
                                        id={`ch-${index}`}
                                        key={index}
                                    >
                                        <Card>
                                            <Card.Header>
                                                <Card.Description>
                                                    {chapter.years} ·{' '}
                                                    {chapter.place}
                                                </Card.Description>
                                                <Card.Title>
                                                    {chapter.title}
                                                </Card.Title>
                                            </Card.Header>
                                            <Card.Content>
                                                <p className="m-0 leading-relaxed text-muted">
                                                    {chapter.kicker}
                                                </p>
                                            </Card.Content>
                                            <Card.Footer className="flex flex-wrap items-center gap-3">
                                                <Chip
                                                    color="danger"
                                                    variant="soft"
                                                >
                                                    {chapter.mood.label}
                                                </Chip>
                                                <Button
                                                    className="ml-auto"
                                                    size="sm"
                                                    variant="ghost"
                                                >
                                                    Read chapter →
                                                </Button>
                                            </Card.Footer>
                                        </Card>
                                    </Tabs.Panel>
                                )
                            })}
                        </Tabs>
                    </Panel>

                    <Panel label="Switch · Progress · Alert">
                        <Switch
                            isSelected={newsreader}
                            onChange={setNewsreader}
                        >
                            <Switch.Control>
                                <Switch.Thumb />
                            </Switch.Control>
                            <Switch.Content className="flex-col items-start gap-1">
                                <Label>Newsreader body text</Label>
                                <Description>
                                    Off: Geist (modern). On: Newsreader
                                    (bookish). Changes the whole page.
                                </Description>
                            </Switch.Content>
                        </Switch>
                        <Separator />
                        <ProgressBar value={44}>
                            <Label>Chapter IV of IX</Label>
                            <ProgressBar.Output />
                            <ProgressBar.Track>
                                <ProgressBar.Fill />
                            </ProgressBar.Track>
                        </ProgressBar>
                        <Separator />
                        <Alert status="accent">
                            <Alert.Indicator />
                            <Alert.Content>
                                <Alert.Title>
                                    {content.chapterSourcesHeading}
                                </Alert.Title>
                                <Alert.Description>
                                    Each chapter lists its archive sources.
                                    Dates before 1600 rest on few documents.
                                </Alert.Description>
                            </Alert.Content>
                        </Alert>
                    </Panel>

                    <Panel label="Buttons">
                        <div className="flex flex-wrap gap-3">
                            <Button>Primary</Button>
                            <Button variant="secondary">Secondary</Button>
                            <Button variant="tertiary">Tertiary</Button>
                            <Button variant="ghost">Ghost</Button>
                            <Button variant="danger">Danger</Button>
                        </div>
                        <div className="flex flex-wrap items-center gap-3">
                            <Button size="sm">Small</Button>
                            <Button size="md">Medium</Button>
                            <Button size="lg">Large</Button>
                            <Button isDisabled>Disabled</Button>
                        </div>
                    </Panel>

                    <Panel label="Chips">
                        <div className="flex flex-wrap gap-2">
                            <Chip>Default</Chip>
                            <Chip color="accent">Brass</Chip>
                            <Chip color="danger">Star red</Chip>
                            <Chip color="warning">Ember</Chip>
                            <Chip color="success">Moss</Chip>
                        </div>
                        <div className="flex flex-wrap gap-2">
                            {content.chapters.slice(0, 6).map((chapter) => (
                                <Chip
                                    color="accent"
                                    key={chapter.id}
                                    variant="soft"
                                >
                                    {chapter.mood.label}
                                </Chip>
                            ))}
                        </div>
                    </Panel>
                </div>

                <div
                    className="mt-6 grid gap-6 lg:grid-cols-[1.35fr_1fr]"
                    id="receipts"
                >
                    <Panel label="Accordion">
                        <Accordion defaultExpandedKeys={['record']}>
                            <Accordion.Item id="record">
                                <Accordion.Heading>
                                    <Accordion.Trigger>
                                        {content.chapterRecordHeading} ·{' '}
                                        {recordChapter.title}
                                        <Accordion.Indicator />
                                    </Accordion.Trigger>
                                </Accordion.Heading>
                                <Accordion.Panel>
                                    <Accordion.Body>
                                        <ul className="m-0 list-none p-0">
                                            {recordChapter.record.map((row) => (
                                                <li
                                                    className="grid grid-cols-[56px_1fr] gap-3 border-t border-separator py-2.5 text-sm"
                                                    key={row.text}
                                                >
                                                    <span className="font-graah-mono text-accent">
                                                        {row.year}
                                                    </span>
                                                    {row.text}
                                                </li>
                                            ))}
                                        </ul>
                                    </Accordion.Body>
                                </Accordion.Panel>
                            </Accordion.Item>
                            {content.chapters.slice(6, 8).map((chapter) => (
                                <Accordion.Item
                                    id={chapter.id}
                                    key={chapter.id}
                                >
                                    <Accordion.Heading>
                                        <Accordion.Trigger>
                                            {chapter.numeral} · {chapter.title}
                                            <Accordion.Indicator />
                                        </Accordion.Trigger>
                                    </Accordion.Heading>
                                    <Accordion.Panel>
                                        <Accordion.Body>
                                            <p className="m-0 leading-relaxed text-muted">
                                                {chapter.kicker}
                                            </p>
                                        </Accordion.Body>
                                    </Accordion.Panel>
                                </Accordion.Item>
                            ))}
                        </Accordion>
                    </Panel>

                    <Panel label="Brand pieces (custom, not HeroUI)">
                        <div className="flex flex-wrap items-center justify-center gap-8 py-2">
                            <Seal size={150} />
                            <Arms className="h-36 w-auto" />
                        </div>
                        <p className="m-0 text-sm leading-relaxed text-muted">
                            The sky, aurora arc, glowing runes, arms and seal
                            are hand-built brand art. They stay the same in both
                            themes. HeroUI handles everything you click.
                        </p>
                    </Panel>
                </div>

                <section className="mt-20" id="tokens">
                    <p className="graah-label mb-3">Theme tokens</p>
                    <h2 className="m-0 font-graah-display text-[clamp(34px,4.6vw,56px)] leading-none font-normal">
                        HeroUI's variables, Graah's values
                    </h2>
                    <div className="mt-8 grid gap-px overflow-hidden rounded-sm border border-border bg-border sm:grid-cols-2 lg:grid-cols-4">
                        {TOKENS.map(([token, hex, name]) => (
                            <div
                                className="flex items-center gap-4 bg-background p-4"
                                key={token}
                            >
                                <span
                                    className="size-11 shrink-0 rounded-sm ring-1 ring-white/10"
                                    style={{ background: hex }}
                                />
                                <span className="flex flex-col gap-1">
                                    <span className="font-graah-mono text-xs text-link">
                                        {token}
                                    </span>
                                    <span className="text-sm">
                                        {name} · {hex}
                                    </span>
                                </span>
                            </div>
                        ))}
                    </div>
                    <div className="mt-6 grid gap-6 md:grid-cols-3">
                        {[
                            [
                                'Fonts',
                                'Forum for titles and card headings. Geist or Newsreader for body. Geist Mono for tabs, chips and labels.',
                            ],
                            [
                                'Shape',
                                'Pill-shaped buttons and tabs. Square-ish cards, alerts and fields (2–4px corners) with a hairline edge.',
                            ],
                            [
                                'Light',
                                'Brass glows on hover and on the active tab, like the runes. Focus rings are brass.',
                            ],
                        ].map(([title, body]) => (
                            <div
                                className="border-t border-border pt-4"
                                key={title}
                            >
                                <h3 className="graah-label m-0 mb-2 font-normal">
                                    {title}
                                </h3>
                                <p className="m-0 text-[15px] leading-relaxed text-muted">
                                    {body}
                                </p>
                            </div>
                        ))}
                    </div>
                </section>
            </main>

            <footer className="border-t border-border bg-[#080b14]">
                <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-8 px-5 py-10">
                    <Seal size={96} />
                    <div>
                        <div className="graah-signature text-2xl">GRAAH</div>
                        <Runes className="mt-2 block text-sm" />
                    </div>
                    <p className="m-0 ml-auto max-w-sm text-sm text-muted">
                        The theme lives in graah-theme/ in the graah repo.
                        graah.se itself still uses the template theme.
                    </p>
                </div>
            </footer>
        </div>
    )
}
