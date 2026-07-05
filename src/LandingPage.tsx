import { Button, Card, Chip, Link } from '@heroui/react'

import {
    ArrowUpRight,
    Blocks,
    CircleDot,
    Code2,
    Cpu,
    Mail,
    Radar,
} from 'lucide-react'

const workstreams = [
    {
        label: 'Interfaces',
        title: 'Screens that stay understandable under pressure.',
        Icon: Blocks,
    },
    {
        label: 'Systems',
        title: 'Small services with clear contracts and low ceremony.',
        Icon: Cpu,
    },
    {
        label: 'Experiments',
        title: 'Fast prototypes that still respect the future codebase.',
        Icon: Radar,
    },
]

const principles = [
    'Plain language',
    'Sharp edges where they help',
    'Shipping over theatre',
    'Careful defaults',
]

function contact(): void {
    globalThis.location.href = 'mailto:hello@graah.se'
}

function scrollToWork(): void {
    globalThis.document
        .getElementById('work')
        ?.scrollIntoView({ behavior: 'smooth' })
}

export function LandingPage() {
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
                <section className="relative isolate flex min-h-[88svh] items-end overflow-hidden border-b-2 border-ink bg-grid px-4 pb-12 pt-24 sm:px-6 lg:px-8">
                    <div className="absolute right-[-5rem] top-20 -z-10 h-[72vmin] max-h-[720px] min-h-[340px] w-[72vmin] min-w-[340px] max-w-[720px] rotate-6 opacity-95">
                        <img
                            alt=""
                            className="h-full w-full object-contain drop-shadow-solid"
                            src="/graah-mark.svg"
                        />
                    </div>
                    <div className="mx-auto grid w-full max-w-7xl gap-10 lg:grid-cols-[minmax(0,0.78fr)_minmax(280px,0.22fr)] lg:items-end">
                        <div className="max-w-5xl">
                            <Chip className="mb-5 rounded-md border-2 border-ink bg-blue px-3 font-bold text-ink">
                                Independent web studio
                            </Chip>
                            <h1 className="max-w-4xl font-display text-[clamp(4.5rem,16vw,12.5rem)] font-black uppercase leading-[0.8] tracking-normal">
                                GRAAH
                            </h1>
                            <p className="mt-7 max-w-2xl text-balance text-xl font-semibold leading-8 sm:text-2xl sm:leading-9">
                                Precise products, durable interfaces, and useful
                                experiments for the internet.
                            </p>
                            <div className="mt-9 flex flex-wrap gap-3">
                                <Button
                                    className="h-12 rounded-md border-2 border-ink bg-ink px-5 font-bold text-paper shadow-hard"
                                    onPress={contact}
                                    variant="primary"
                                >
                                    Start a thread
                                    <ArrowUpRight
                                        aria-hidden="true"
                                        size={19}
                                    />
                                </Button>
                                <Button
                                    className="h-12 rounded-md border-2 border-ink bg-paper px-5 font-bold text-ink shadow-hard"
                                    onPress={scrollToWork}
                                    variant="outline"
                                >
                                    See the shape
                                    <CircleDot aria-hidden="true" size={18} />
                                </Button>
                            </div>
                        </div>
                        <aside className="grid gap-3 text-sm font-bold uppercase tracking-normal">
                            {principles.map((principle) => (
                                <div
                                    className="border-2 border-ink bg-paper px-4 py-3 shadow-hard"
                                    key={principle}
                                >
                                    {principle}
                                </div>
                            ))}
                        </aside>
                    </div>
                </section>

                <section
                    className="border-b-2 border-ink bg-ink py-16 text-paper sm:py-20"
                    id="work"
                >
                    <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
                        <div className="mb-8 flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
                            <div>
                                <p className="font-mono text-sm uppercase tracking-normal text-blue">
                                    Work
                                </p>
                                <h2 className="mt-2 max-w-3xl font-display text-4xl font-black tracking-normal sm:text-6xl">
                                    Compact teams, direct execution.
                                </h2>
                            </div>
                            <p className="max-w-md text-base leading-7 text-paper/74">
                                The page is new; the bias is already decided:
                                make the thing clear, make it run, make it easy
                                to change.
                            </p>
                        </div>
                        <div className="grid gap-4 md:grid-cols-3">
                            {workstreams.map(({ Icon, label, title }) => (
                                <Card
                                    className="rounded-lg border-2 border-paper bg-paper text-ink shadow-paper"
                                    key={label}
                                >
                                    <Card.Content className="gap-8 p-5">
                                        <div className="flex items-center justify-between">
                                            <span className="font-mono text-sm font-bold uppercase tracking-normal">
                                                {label}
                                            </span>
                                            <span className="grid size-11 place-items-center rounded-md border-2 border-ink bg-signal">
                                                <Icon
                                                    aria-hidden="true"
                                                    size={22}
                                                    strokeWidth={2.4}
                                                />
                                            </span>
                                        </div>
                                        <h3 className="font-display text-2xl font-black leading-7 tracking-normal">
                                            {title}
                                        </h3>
                                    </Card.Content>
                                </Card>
                            ))}
                        </div>
                    </div>
                </section>

                <section className="bg-coral px-4 py-14 text-ink sm:px-6 lg:px-8">
                    <div className="mx-auto flex max-w-7xl flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
                        <div>
                            <p className="font-mono text-sm font-bold uppercase tracking-normal">
                                hello@graah.se
                            </p>
                            <h2 className="mt-2 max-w-3xl font-display text-4xl font-black tracking-normal sm:text-6xl">
                                Bring a hard problem or a half-shaped idea.
                            </h2>
                        </div>
                        <Button
                            className="h-12 w-fit rounded-md border-2 border-ink bg-paper px-5 font-bold text-ink shadow-hard"
                            onPress={contact}
                            variant="outline"
                        >
                            Write GRAAH
                            <Code2 aria-hidden="true" size={19} />
                        </Button>
                    </div>
                </section>
            </main>
        </div>
    )
}
