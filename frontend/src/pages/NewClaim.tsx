import { useState } from 'react'
import { api } from '../api'

/** SDD screen: new claim form + evidence upload. */
export default function NewClaim() {
  const [form, setForm] = useState({ policy_number: '', loss_date: '', loss_type: 'collision', description: '', amount: '' })
  const set = (k: string) => (e: any) => setForm({ ...form, [k]: e.target.value })

  async function submit(e: any) {
    e.preventDefault()
    const claim = await api.createClaim({ ...form, amount: Number(form.amount), loss_date: new Date(form.loss_date).toISOString() })
    alert('Claim created: ' + claim.id)
  }

  return (
    <section>
      <h2>New claim</h2>
      <form onSubmit={submit} style={{ display: 'grid', gap: 8, maxWidth: 420 }}>
        <input placeholder="Policy number" value={form.policy_number} onChange={set('policy_number')} required />
        <input type="date" value={form.loss_date} onChange={set('loss_date')} required />
        <select value={form.loss_type} onChange={set('loss_type')}>
          <option>collision</option><option>theft</option><option>vandalism</option><option>weather</option>
        </select>
        <textarea placeholder="What happened?" value={form.description} onChange={set('description')} required />
        <input type="number" placeholder="Claimed amount" value={form.amount} onChange={set('amount')} required />
        <button type="submit">Create claim</button>
      </form>
      {/* TODO: file input -> api.uploadDocument(claimId, file) */}
    </section>
  )
}
