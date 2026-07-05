import { HistoryPage } from './HistoryPage.tsx'
import { LandingPage } from './LandingPage.tsx'

export function App() {
    const path = globalThis.location.pathname.replace(/\/+$/, '')
    if (path === '/history') {
        return <HistoryPage />
    }
    return <LandingPage />
}
