import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import ClaimsQueue from './ClaimsQueue'
import NewClaim from './NewClaim'
import ReviewWorkspace from './ReviewWorkspace'
import PolicyAdmin from './PolicyAdmin'

export default function App() {
  return (
    <div style={{ fontFamily: 'system-ui', maxWidth: 1100, margin: '0 auto', padding: 24 }}>
      <header style={{ borderBottom: '2px solid #111', paddingBottom: 12, marginBottom: 24 }}>
        <h1>ClaimSense AI</h1>
        <p style={{ color: '#555' }}>AI assists → adjuster reviews → adjuster decides</p>
        <nav style={{ display: 'flex', gap: 16 }}>
          <Link to="/">Queue</Link>
          <Link to="/new">New claim</Link>
          <Link to="/policies">Policies</Link>
        </nav>
      </header>
      <main>
        {/* Wire react-router Routes here in Step 10 of the guide */}
        <ClaimsQueue />
      </main>
    </div>
  )
}
