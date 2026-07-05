export interface Mood {
    label: string
    bg: string
}

export interface ImageCopy {
    src: string
    alt: string
    caption?: string
}

export interface ChronicleStat {
    value: string
    label: string
    bg: string
}

export interface Source {
    label: string
    href?: string
}

export interface Chapter {
    id: string
    image?: ImageCopy
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
    sources?: Source[]
}

export interface Bearer {
    icon: 'radio' | 'snowflake'
    img?: Omit<ImageCopy, 'caption'>
    name: string
    years: string
    deed: string
    source?: Source
}

export interface TimelineStop {
    year: string
    text: string
}

export interface HistoryContent {
    meta: {
        htmlTitle: string
        defaultTitle: string
        description: string
        ogTitle: string
        ogDescription: string
    }
    languageSwitcher: {
        legend: string
        options: Record<
            string,
            {
                label: string
                ariaLabel: string
            }
        >
    }
    nav: {
        logoAlt: string
        brand: string
    }
    hero: {
        crestAlt: string
        chip: string
        titleLines: string[]
        intro: string
        introEmphasis: string
        startYear: string
        endYear: string
    }
    chronicleStats: ChronicleStat[]
    nameForms: string[]
    chapterRecordHeading: string
    chapterSourcesHeading: string
    chapters: Chapter[]
    fireInterstitial: {
        label: string
        titlePrefix: string
        titleEmphasis: string
        body: string
        sources?: Source[]
    }
    bearersSection: {
        eyebrow: string
        title: string
        intro: string
        figure: ImageCopy
        bearers: Bearer[]
    }
    timelineSection: {
        eyebrow: string
        title: string
        stops: TimelineStop[]
    }
    closing: {
        eyebrow: string
        title: string
        body: string
        cta: string
        note: string
    }
}
