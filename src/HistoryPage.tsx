import type { ReactNode } from 'react'
import { useEffect } from 'react'

import { Button, Chip, Link } from '@heroui/react'

import { motion, useReducedMotion } from 'framer-motion'
import {
    Anchor,
    ArrowDown,
    ArrowUpRight,
    Flame,
    Mail,
    Radio,
    Snowflake,
} from 'lucide-react'

interface Mood {
    label: string
    bg: string
}

const chronicleStats = [
    { value: '1', label: 'castle lost to a king', bg: 'bg-coral' },
    { value: '3', label: 'kingdoms called home', bg: 'bg-blue' },
    { value: '12,000', label: 'spindles on one river', bg: 'bg-signal' },
    { value: '7', label: 'spellings of one name', bg: 'bg-mint' },
]

interface Chapter {
    id: string
    numeral: string
    years: string
    place: string
    title: string
    kicker: string
    mood: Mood
    theme: 'paper' | 'grid' | 'blue' | 'ink' | 'mint'
    paragraphs: string[]
    record: Array<{ year: string; text: string }>
    aside?: { title: string; text: string }
    image?: { src: string; alt: string; caption: string }
}

const chapters: Chapter[] = [
    {
        id: 'manor',
        image: {
            src: '/history/manor-1866.jpg',
            alt: 'Nineteenth-century engraving of the manor Søllestedgård with its tower and gardens',
            caption: 'Søllestedgård itself, drawn in 1866',
        },
        numeral: 'I',
        years: '1462–1550',
        place: 'Søllestedgård, Lolland, Denmark',
        title: 'The Stolen Castle',
        kicker: 'A castle, a king, and a grudge the family has carried for five hundred years',
        mood: { label: 'A royal grudge', bg: 'bg-coral' },
        theme: 'grid',
        paragraphs: [
            'It begins with a castle. Søllestedgård, on the Danish island of Lolland: land, arms and power. For three generations it belonged to the Graas — Anders Graa took it in the 1460s, his formidable widow Gertrud Munk ran it after him, and their son Jørgen held it like a lord of the old school.',
            'Then, in 1530, the King took it. Twenty years later Christian III handed the estate to Jørgen Brahe — uncle of Tycho Brahe, the most famous astronomer ever to lose his nose in a duel. The Brahes got the castle. The Graas got the road.',
            'All that survived was the name, and a signet ring bearing the old family arms — which, in perfect Graah fashion, was later lost in a fire. Five centuries on, the family still tells the story. Nobody asks for the Brahes’ side.',
        ],
        record: [
            { year: '1462', text: 'Anders Graa holds Søllestedgård' },
            { year: '1530', text: 'The estate passes to the Danish Crown' },
            {
                year: '1550',
                text: 'Christian III sells it to Jørgen Brahe, Tycho’s uncle',
            },
            {
                year: '—',
                text: 'A signet with the family arms, lost in a fire',
            },
        ],
    },
    {
        id: 'pulpit',
        image: {
            src: '/history/skaarup-kirke.jpg',
            alt: 'The whitewashed medieval church of Skårup on Funen with its red tile roof',
            caption: 'Skårup church — the family throne for 80 years',
        },
        numeral: 'II',
        years: '1591–1670',
        place: 'Skårup & Tved, Funen',
        title: 'Eighty Years in the Pulpit',
        kicker: 'When the priest ran everything, the Graas were the priests',
        mood: { label: 'God & power', bg: 'bg-blue' },
        theme: 'paper',
        paragraphs: [
            'Stripped of the castle, the family found a new throne: the pulpit. In 1591 John Olufsen Graa took the parishes of Skårup and Tved on Funen, and by 1622 he was provost — the crown’s top churchman in the district. In post-Reformation Denmark that made him far more than a preacher: keeper of the records, master of the school, judge of morals and the king’s eyes in the parish.',
            'When he died, his son Hans took the pulpit and held it until 1670. Eighty years, father and son, one family running the spiritual machinery of a corner of Denmark — and quietly banking the literacy, standing and connections that would launch everything that came next.',
        ],
        record: [
            { year: '1591', text: 'John Olufsen Graa gains Skårup and Tved' },
            { year: '1622', text: 'Appointed provost' },
            { year: '1670', text: 'Hans Johnsen Graa dies; the dynasty ends' },
        ],
    },
    {
        id: 'broker',
        image: {
            src: '/history/budolfi-aalborg.jpg',
            alt: 'The white tower of Budolfi Church rising over an Aalborg street',
            caption: 'Budolfi Church, Aalborg — where the broker was baptised',
        },
        numeral: 'III',
        years: '1666–1775',
        place: 'Aalborg, Jutland',
        title: 'The King’s Broker',
        kicker: 'Three generations turning harbour gossip into hard currency',
        mood: { label: 'Salt & gold', bg: 'bg-signal' },
        theme: 'paper',
        paragraphs: [
            'By the 1700s the family is in Aalborg, one of Denmark’s great port towns, and the trade is no longer souls — it is ships, cargo and credit. David Olufsen Graae started as a købmandskarl, a merchant’s apprentice, and clawed his way up until in 1767 the king himself licensed him as a broker: the man every serious deal in the harbour had to pass through.',
            'The harbour gave, and the harbour took. David buried two wives before his third outlived him by thirty-five years. And in the family’s Svendborg branch, Gommine Kristine Graae married the skipper Ole Bondo in March 1836 — one year later, almost to the day, the sea took him off the English coast.',
        ],
        record: [
            {
                year: '1727',
                text: 'David Olufsen Graae baptised, Budolfi Church',
            },
            {
                year: '1767',
                text: 'Royal broker’s licence — bevilling som mægler',
            },
            {
                year: '1837',
                text: 'Skipper Ole Bondo lost off the English coast',
            },
        ],
        aside: {
            title: 'Married in March, drowned in March',
            text: 'Gommine Kristine Graae wed Ole Bondo on 8 March 1836. He went down off England on 11 March 1837. In a merchant family, the sea was both the fortune and the risk.',
        },
    },
    {
        id: 'crossing',
        image: {
            src: '/history/christiania-1800.jpg',
            alt: 'Hand-coloured view of the city of Christiania and its fjord, painted around 1800',
            caption: 'Christiania, painted around 1800 — the city they bet on',
        },
        numeral: 'IV',
        years: '1826–1859',
        place: 'Christiania, Norway',
        title: 'The Crossing',
        kicker: 'Two sons of a Danish priest bet everything on a brand-new capital',
        mood: { label: 'The gamble', bg: 'bg-coral' },
        theme: 'blue',
        paragraphs: [
            'The priest Knud David Graah raised his children in a Danish parsonage — and watched them leave, one by one, for Norway. The old union had just collapsed, Christiania was a capital in a hurry, and a country in a hurry needs everything: money, goods, ideas, nerve. The Graahs brought all four.',
            'David Graah went first, in 1826, and built a merchant house. Then he did something strange for a rich man of his century: he started giving it away — founding Norway’s first animal-protection society, endowing funds for women in need, building kindergartens. His little brother Knud landed in 1833, sixteen years old, straight off the boat from Jutland, starting behind a shop counter. Remember the name.',
        ],
        record: [
            { year: '1826', text: 'David Graah settles in Christiania' },
            { year: '1833', text: 'Knud Graah arrives, aged sixteen' },
            {
                year: '1859',
                text: 'David founds Norway’s first animal-protection society',
            },
        ],
    },
    {
        id: 'cotton',
        image: {
            src: '/history/knud-graah.jpg',
            alt: 'Oil portrait of Knud Graah, white-haired with medals on his black coat',
            caption: 'Knud Graah — shop boy, cotton king',
        },
        numeral: 'V',
        years: '1844–1859',
        place: 'Manchester → the Akerselva',
        title: 'Cotton & Water',
        kicker: 'He went to England for machines and came home with an industry',
        mood: { label: 'Revolution', bg: 'bg-blue' },
        theme: 'paper',
        paragraphs: [
            'When Britain finally loosened its grip on the machines that had made it rich, Knud Graah went straight to the source: Manchester — the loudest, dirtiest, richest industrial city on earth. There, the story goes, he ran into Adam Hiorth, another Norwegian hunting the very same machines. They sized each other up, sailed home, and built rival mills on the same river.',
            'Graah’s masterstroke came in 1844: he bought the waterfall at Nedre Vøyen on the Akerselva. No electricity existed — the river was the power grid, and now he owned a piece of it. Two years later Vøiens Bomuldsspinderi thundered to life: British machines, Norwegian water, a great iron waterwheel, eighty workers — and its own gasworks, the first in Christiania, so the spindles never had to stop for darkness.',
        ],
        record: [
            { year: '1844', text: 'Buys the waterfall rights at Nedre Vøyen' },
            { year: '1846', text: 'Vøiens Bomuldsspinderi opens' },
            { year: '1854', text: 'Buys out his partner and brother-in-law' },
        ],
    },
    {
        id: 'ashes',
        image: {
            src: '/history/graah-mill.jpg',
            alt: 'The brick buildings of Knud Graah’s mill beside the waterfall on the Akerselva',
            caption: 'The rebuilt mill and its waterfall on the Akerselva',
        },
        numeral: 'VI',
        years: '1860–1909',
        place: 'Kristiania',
        title: 'Out of the Ashes',
        kicker: 'The mill burned down. He built it back bigger — then saved a bank',
        mood: { label: 'Phoenix', bg: 'bg-signal' },
        theme: 'paper',
        paragraphs: [
            'For most men the fire would have been the end. For Knud Graah it was barely an intermission — because the man who gambled on machines never gambled with money, and every brick, bobbin and bale was insured. He hired the architect Oluf N. Roll, and within a year a new four-storey mill towered over the river, bigger and more modern than the one still smoking. By 1889 it ran twelve thousand spindles.',
            'The same ice-cold nerve made him a banker. He joined the board of Christiania Bank og Kreditkasse in 1881 and rose to chairman — and when the great Kristiania crash of 1899 vaporised the speculators and toppled banks all around, his bank came through standing. At eighty-nine he was still in charge, reorganising the empire as A/S Knud Graah & Co., 350 workers strong. His brick mills still stand on the Akerselva today.',
        ],
        record: [
            {
                year: '1860',
                text: 'New four-storey mill by architect Oluf N. Roll',
            },
            { year: '1889', text: '12,000 spindles running at Vøien' },
            {
                year: '1899',
                text: 'Kreditkassen rides out the Kristiania crash',
            },
            { year: '1906', text: 'A/S Knud Graah & Co. — ~350 employees' },
        ],
    },
    {
        id: 'voice',
        image: {
            src: '/history/white-buses-1945.jpg',
            alt: 'Freed prisoners crowd a ferry deck between white Red Cross buses, spring 1945',
            caption: 'The White Buses bring them home, spring 1945',
        },
        numeral: 'VII',
        years: '1908–2001',
        place: 'Oslo — Grini — Ravensbrück — NRK',
        title: 'The Voice That Survived',
        kicker: 'The mill-owner’s granddaughter chose resistance over comfort',
        mood: { label: 'Defiance', bg: 'bg-coral' },
        theme: 'ink',
        paragraphs: [
            'Anne Knudsdatter Graah — everyone called her Lille — was born in Kristiania in January 1908, granddaughter of the industrialist. Her father died the same year she was born. She grew up an heiress to the family’s name and standing, and when Germany occupied Norway she put all of it at risk: she went to work for the illegal press, the underground newspapers that kept the truth moving.',
            'In 1942 the Gestapo arrested her. Grini prison camp first; then deportation to Ravensbrück, the concentration camp for women. She survived it. In the spring of 1945 the Swedish Red Cross White Buses carried her home.',
            'And then she gave Norway her voice. Lille Graah joined NRK and became one of the country’s most recognisable radio presences, above all through Ønskekonserten, the request concert that stitched the postwar country back together one dedication at a time. In 1948 she helped found a relief association for Czechoslovak refugees; in 1977 Oslo gave her the St. Hallvard Medal. From privilege, to resistance, to survival, to service.',
        ],
        record: [
            {
                year: '1942',
                text: 'Arrested by the Gestapo; imprisoned at Grini',
            },
            { year: '1943', text: 'Deported to Ravensbrück' },
            { year: '1945', text: 'Comes home with the White Buses' },
            { year: '1977', text: 'Awarded Oslo’s St. Hallvard Medal' },
        ],
    },
    {
        id: 'hyphen',
        image: {
            src: '/history/malmo-1859.jpg',
            alt: 'Engraving of Malmö’s great square with strollers and the town hall, 1859',
            caption: 'Malmö’s Stortorget, 1859 — the family’s next stage',
        },
        numeral: 'VIII',
        years: '1892–1982',
        place: 'Malmö · Helsingborg · Stockholm',
        title: 'The Hyphen That Saved a Name',
        kicker: 'A dying mother, a newborn son, and a name that refused to disappear',
        mood: { label: 'The name lives', bg: 'bg-mint' },
        theme: 'paper',
        paragraphs: [
            'Ingeborg Graah, of the mill-king’s own line, married the Swede Gustaf Hagelbäck and crossed the water. In March 1892 their son Knut was born in Malmö — and that same year Ingeborg died, twenty-nine years old. What she left her son was the name.',
            'The family made it official: he would be Knut Graah-Hagelbäck, hyphen and all. The old heralds would have sniffed — names pass through sons, they’d say, not daughters. The family ignored them. Through Knut and his son Björn — an officer in Sweden’s Cold War defence planning — the name marched on through Swedish life: officers, architects, psychologists, engineers, security specialists.',
        ],
        record: [
            { year: '1892', text: 'Knut Graah-Hagelbäck born in Malmö' },
            { year: '1892', text: 'Ingeborg Graah dies, aged twenty-nine' },
            {
                year: '1921',
                text: 'Björn Graah-Hagelbäck, later defence planner',
            },
        ],
    },
    {
        id: 'wallet',
        image: {
            src: '/history/oresund-bridge.jpg',
            alt: 'Aerial view of the Öresund bridge running out to sea from the Swedish coast',
            caption: 'The bridge out of Skåne — cross the border and build',
        },
        numeral: 'IX',
        years: '1982–now',
        place: 'Lund → the internet',
        title: 'From Waterwheel to Wallet',
        kicker: 'The short name returns — and so does the family pattern',
        mood: { label: 'Full circle', bg: 'bg-paper' },
        theme: 'mint',
        paragraphs: [
            'Hannes Sebastian Graah was born in Lund in 1982, son of Kristian Graah-Hagelbäck. Professionally he dropped the hyphen and took back the short old name — Graah — and then did something the family had done before: he went where the new machinery was.',
            'He helped scale Spotify through its years of international expansion, led growth at the fintech Revolut, founded the stablecoin protocol Gro, and then founded Zeal, a self-custodial crypto wallet built to make open finance usable in daily life.',
            'In 1844 Knud Graah bought a waterfall, because whoever controls the power source controls the mill. In the 2020s the scarce resource is custody — direct control of your own money on open networks. Different century, same move: find the new infrastructure of the age, cross whatever border is in the way, and build the tools that make it work for ordinary people.',
        ],
        record: [
            { year: '1982', text: 'Born in Lund; the short name returns' },
            { year: '2010s', text: 'Growth at Spotify, then Revolut' },
            {
                year: 'now',
                text: 'Founder of Gro and Zeal — self-custody for all',
            },
        ],
    },
]

const nameForms = [
    'GROH',
    'GRAA',
    'GRÅ',
    'GRAAE',
    'GRAAH',
    'GRAAH-HAGELBÄCK',
    'GRAAH',
]

const bearers = [
    {
        Icon: Snowflake,
        img: {
            src: '/history/wa-graah.jpg',
            alt: 'Engraved oval portrait of captain Wilhelm August Graah with his signature',
        },
        name: 'Wilhelm August Graah',
        years: '1793–1863',
        deed: 'Sent by the Danish king to find the lost Norse colony of Greenland’s east coast. Travelled 1828–31 in Greenlandic umiaks with Greenlandic crews, wintered in the ice, nearly starved — and proved the myth wrong, redrawing the map on the way.',
    },
    {
        Icon: Radio,
        img: undefined,
        name: 'Jutta Graae — “Storhertuginden”',
        years: '1906–1997',
        deed: 'The Grand Duchess of the Danish resistance. Moved money and microfilm for the underground intelligence networks, fled to Sweden in 1943, and worked from London with the British SOE until liberation.',
    },
]

const timeline = [
    { year: '1462', text: 'Anders Graa at Søllestedgård' },
    { year: '1530', text: 'The Crown takes the manor' },
    { year: '1550', text: 'Sold to Jørgen Brahe' },
    { year: '1591', text: 'Graa priests take Skårup & Tved' },
    { year: '1767', text: 'Royal broker’s licence in Aalborg' },
    { year: '1826', text: 'David Graah crosses to Christiania' },
    { year: '1833', text: 'Knud Graah follows, aged 16' },
    { year: '1844', text: 'Knud buys the waterfall' },
    { year: '1846', text: 'The cotton mill starts spinning' },
    { year: '1859', text: 'Fire destroys the mill at Christmas' },
    { year: '1860', text: 'Rebuilt — four storeys, more modern' },
    { year: '1881', text: 'Knud joins the Kreditkassen board' },
    { year: '1892', text: 'The name crosses into Sweden' },
    { year: '1899', text: 'The bank survives the great crash' },
    { year: '1942', text: 'Lille Graah arrested by the Gestapo' },
    { year: '1945', text: 'Home on the White Buses' },
    { year: '1977', text: 'St. Hallvard Medal for Lille' },
    { year: '1982', text: 'Hannes Graah born in Lund' },
    { year: 'now', text: 'Zeal — self-custody for everyone' },
]

const themeStyles: Record<Chapter['theme'], string> = {
    paper: 'bg-paper text-ink',
    grid: 'bg-paper bg-grid text-ink',
    blue: 'bg-blue text-ink',
    ink: 'bg-ink text-paper',
    mint: 'bg-mint text-ink',
}

function contact(): void {
    globalThis.location.href = 'mailto:hello@graah.se'
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
}: {
    chapter: Chapter
    index: number
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
                                <figcaption className="px-1 pb-1 pt-2 font-mono text-xs font-bold uppercase tracking-normal">
                                    {chapter.image.caption}
                                </figcaption>
                            </figure>
                        ) : null}
                        <div
                            className={`border-2 ${borderColor} ${shadow} ${
                                dark ? 'bg-ink' : 'bg-paper'
                            } p-5`}
                        >
                            <p className="font-mono text-xs font-bold uppercase tracking-normal">
                                The receipts
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

function FireInterstitial() {
    return (
        <section className="border-b-2 border-ink bg-ink bg-stripes-coral px-4 py-20 text-paper sm:px-6 sm:py-28 lg:px-8">
            <div className="mx-auto w-full max-w-7xl">
                <Reveal>
                    <p className="flex items-center gap-3 font-mono text-sm font-bold uppercase tracking-normal text-coral">
                        <Flame aria-hidden="true" size={18} />
                        Tuesday 20 December 1859 · around 23:00
                    </p>
                    <p className="mt-6 max-w-6xl font-display text-[clamp(3rem,10vw,8.5rem)] font-black uppercase leading-[0.85] tracking-normal">
                        The mill is <span className="text-coral">burning</span>
                    </p>
                    <p className="mt-8 max-w-2xl font-serif text-xl italic leading-9 text-paper/85 sm:text-2xl sm:leading-10">
                        Cotton dust, wooden floors, oil and gaslight — in the
                        dark of the Christmas week, thirteen years of work went
                        up in a single night. What Knud Graah did next is the
                        whole family in one move: he had insured everything.
                    </p>
                </Reveal>
            </div>
        </section>
    )
}

function NameTicker() {
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
    useEffect(() => {
        globalThis.document.title =
            'The Graah Chronicle — five centuries of comebacks'
        return () => {
            globalThis.document.title = 'GRAAH'
        }
    }, [])

    return (
        <div className="min-h-screen bg-paper text-ink">
            <header className="fixed inset-x-0 top-0 z-40 border-b-2 border-ink bg-paper/92 backdrop-blur">
                <nav className="mx-auto flex h-16 w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
                    <Link className="flex items-center gap-3 text-ink" href="/">
                        <img
                            alt=""
                            className="size-9 border-2 border-ink"
                            src="/graah-mark.svg"
                        />
                        <span className="font-display text-xl font-black tracking-normal">
                            GRAAH
                        </span>
                    </Link>
                    <Button
                        className="h-10 rounded-md border-2 border-ink bg-signal px-4 font-bold text-ink shadow-hard"
                        onPress={contact}
                        variant="secondary"
                    >
                        Contact
                        <Mail aria-hidden="true" size={17} />
                    </Button>
                </nav>
            </header>

            <main>
                <section className="relative isolate overflow-hidden border-b-2 border-ink bg-grid px-4 pb-14 pt-28 sm:px-6 sm:pb-20 sm:pt-36 lg:px-8">
                    <div className="absolute right-[-16rem] top-24 -z-10 h-[70vmin] max-h-[680px] min-h-[320px] w-[70vmin] min-w-[320px] max-w-[680px] -rotate-6 opacity-15 sm:right-[-6rem]">
                        <img
                            alt=""
                            className="h-full w-full object-contain"
                            src="/graah-mark.svg"
                        />
                    </div>
                    <div className="mx-auto w-full max-w-7xl">
                        <Chip className="mb-6 rounded-md border-2 border-ink bg-coral px-3 font-bold text-ink">
                            The family chronicle
                        </Chip>
                        <h1 className="max-w-6xl font-display text-[clamp(3.2rem,11vw,9.5rem)] font-black uppercase leading-[0.82] tracking-normal">
                            Five centuries.
                            <br />
                            One name.
                        </h1>
                        <p className="mt-8 max-w-3xl font-serif text-xl leading-9 sm:text-2xl sm:leading-10">
                            A castle lost to a king. Priests who ran a province,
                            brokers who ran a harbour, a cotton baron who bought
                            a waterfall, a resistance heroine who became the
                            voice of a nation — and a wallet for the open
                            internet.{' '}
                            <em>
                                Five hundred years of kings, fires, fortunes and
                                comebacks. Buckle up.
                            </em>
                        </p>
                        <div className="mt-10 flex flex-wrap items-center gap-3">
                            <span className="border-2 border-ink bg-ink px-4 py-2 font-display text-2xl font-black text-paper shadow-hard sm:text-3xl">
                                1462
                            </span>
                            <ArrowDown
                                aria-hidden="true"
                                className="-rotate-90"
                                size={26}
                            />
                            <span className="border-2 border-ink bg-mint px-4 py-2 font-display text-2xl font-black text-ink shadow-hard sm:text-3xl">
                                NOW
                            </span>
                        </div>
                        <div className="mt-12 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                            {chronicleStats.map(({ bg, label, value }) => (
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
                            ))}
                        </div>
                    </div>
                </section>

                <NameTicker />

                {chapters.slice(0, 5).map((chapter, index) => (
                    <ChapterSection
                        chapter={chapter}
                        index={index}
                        key={chapter.id}
                    />
                ))}

                <FireInterstitial />

                {chapters.slice(5).map((chapter, index) => (
                    <ChapterSection
                        chapter={chapter}
                        index={index + 5}
                        key={chapter.id}
                    />
                ))}

                <section className="border-b-2 border-ink bg-ink py-16 text-paper sm:py-24">
                    <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
                        <Reveal>
                            <p className="font-mono text-sm font-bold uppercase tracking-normal text-blue">
                                Bearers of the name
                            </p>
                            <h2 className="mt-2 max-w-4xl font-display text-4xl font-black uppercase tracking-normal sm:text-6xl">
                                Same name, wilder stories
                            </h2>
                            <p className="mt-4 max-w-2xl font-serif text-lg italic leading-8 text-paper/80">
                                Wherever history got dangerous, a Graah kept
                                turning up — on the Greenland ice, and behind
                                enemy lines.
                            </p>
                        </Reveal>
                        <Reveal>
                            <figure className="mt-10 -rotate-1 border-2 border-paper bg-paper p-2 text-ink shadow-paper">
                                <img
                                    alt="Engraving of an umiak rowed through heavy seas by its Greenlandic crew"
                                    className="w-full border-2 border-ink object-cover"
                                    loading="lazy"
                                    src="/history/umiak-graah.jpg"
                                />
                                <figcaption className="px-1 pb-1 pt-2 font-mono text-xs font-bold uppercase tracking-normal">
                                    An umiak in open water off East Greenland —
                                    drawn by captain W.A. Graah himself
                                </figcaption>
                            </figure>
                        </Reveal>
                        <div className="mt-6 grid gap-4 md:grid-cols-2">
                            {bearers.map(({ Icon, deed, img, name, years }) => (
                                <Reveal key={name}>
                                    <div className="h-full border-2 border-paper bg-paper p-6 text-ink shadow-paper">
                                        <div className="flex items-center justify-between">
                                            <span className="font-mono text-sm font-bold uppercase tracking-normal">
                                                {years}
                                            </span>
                                            {img ? (
                                                <img
                                                    alt={img.alt}
                                                    className="w-20 border-2 border-ink object-cover"
                                                    loading="lazy"
                                                    src={img.src}
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
                                            {name}
                                        </h3>
                                        <p className="mt-3 font-serif text-base leading-7">
                                            {deed}
                                        </p>
                                    </div>
                                </Reveal>
                            ))}
                        </div>
                    </div>
                </section>

                <section className="border-b-2 border-ink bg-paper py-16 sm:py-20">
                    <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
                        <Reveal>
                            <p className="font-mono text-sm font-bold uppercase tracking-normal">
                                The long arc
                            </p>
                            <h2 className="mt-2 font-display text-4xl font-black uppercase tracking-normal sm:text-6xl">
                                1462 → now
                            </h2>
                        </Reveal>
                    </div>
                    <div className="mt-8 overflow-x-auto pb-6">
                        <div className="mx-auto flex w-max gap-4 px-4 sm:px-6 lg:px-8">
                            {timeline.map((stop) => (
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
                                What it all adds up to
                            </p>
                            <h2 className="mt-3 max-w-6xl font-display text-[clamp(2.6rem,7.5vw,6.5rem)] font-black uppercase leading-[0.88] tracking-normal">
                                A family that kept rebuilding the tools of its
                                age
                            </h2>
                            <p className="mt-8 max-w-3xl font-serif text-xl leading-9">
                                Land, then pulpits. Pulpits, then harbours.
                                Harbours, then waterfalls and spindles. Banks,
                                underground newspapers, a radio microphone — and
                                now open finance. The pattern never changed:
                                find the new infrastructure of the age, cross
                                the border, and build.
                            </p>
                            <div className="mt-10 flex flex-wrap gap-3">
                                <Button
                                    className="h-12 rounded-md border-2 border-ink bg-ink px-5 font-bold text-paper shadow-hard"
                                    onPress={contact}
                                    variant="primary"
                                >
                                    Write to the family
                                    <ArrowUpRight
                                        aria-hidden="true"
                                        size={19}
                                    />
                                </Button>
                            </div>
                            <p className="mt-10 max-w-3xl border-t-2 border-ink pt-5 text-sm font-semibold leading-6">
                                Told the way the family tells it — the good
                                parts kept in, the dull parts left out, and the
                                dates as true as we can make them. The archives
                                are still coughing up surprises. Check back.
                                Pictures via Wikimedia Commons:
                                Nasjonalbiblioteket, Nasjonalmuseet and Oslo
                                Museum (Norway), News Øresund (CC BY), Hideko
                                Bondesen and Liberaler Humanist (CC BY-SA).
                            </p>
                        </Reveal>
                    </div>
                </section>
            </main>
        </div>
    )
}
