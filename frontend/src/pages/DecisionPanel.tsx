import { useState } from 'react'
import { api } from '../api'

/** SDD screen: decision panel — recommendation, adjuster action,
 *  MANDATORY rationale, claim-version warning. */
export default function DecisionPanel({ claimId, claimVersion }: { claimId: string; claimVersion: number }) {
  const [action, setAction] = useState('approve')
  const [rationale, setRationale] = useState('')

  async function submit() {
    if (rationale.trim().length < 10) { alert('Rationale is required (min 10 chars).'); return }
    await api.recordDecision(claimId, { action, rationale, recorded_by: 'adjuster-1' })
    alert('Decision recorded for claim version ' + claimVersion)
  }

  return (
    <section style={{ border: '1px solid #ccc', padding: 16, marginTop: 16 }}>
      <h3>Adjuster decision (claim version {claimVersion})</h3>
      <select value={action} onChange={(e) => setAction(e.target.value)}>
        <option value="approve">Approve</option>
        <option value="deny">Deny</option>
        <option value="request_info">Request info</option>
        <option value="refer">Refer to SIU</option>
      </select>
      <textarea placeholder="Rationale (required)" value={rationale}
        onChange={(e) => setRationale(e.target.value)} style={{ display: 'block', width: '100%', marginTop: 8 }} />
      <button onClick={submit} style={{ marginTop: 8 }}>Record decision</button>
    </section>
  )
}
