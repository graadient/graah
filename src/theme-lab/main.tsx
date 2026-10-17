import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import './theme-lab.css'
import { ThemeLab } from './ThemeLab.tsx'

const rootElement = document.getElementById('root')

if (rootElement !== null) {
    createRoot(rootElement).render(
        <StrictMode>
            <ThemeLab />
        </StrictMode>
    )
}
