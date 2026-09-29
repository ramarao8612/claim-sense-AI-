import { useEffect, useState } from 'react'
import { api } from '../api'

/** SDD screen: claims queue — claim number, status, severity, priority, risk, age. */
export default function ClaimsQueue() {
  const [claims, setClaims] = useState<any[]>([])
  useEffect(() => { api.listClaims().then(setClaims).catch(console.error) }, [])
  return (
    <section>
      <h2>Claims queue</h2>
      {claims.length === 0 && <p>No claims yet. Create one from “New claim”.</p>}
      <ul>{claims.map((c) => <li key={c.id}>{c.policy_number} — {c.status} — ${c.amount}</li>)}</ul>
    </section>
  )
}
