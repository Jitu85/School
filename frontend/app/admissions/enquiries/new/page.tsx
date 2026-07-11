'use client'

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function NewEnquiryForm() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    preferred_course: '',
    expected_start_date: '',
    source: 'website',
    notes: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [fieldErrors, setFieldErrors] = useState<Record<string, string[]>>({})

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    // Clear field-specific error when user types
    if (fieldErrors[name]) {
      setFieldErrors((prev) => {
        const copy = { ...prev }
        delete copy[name]
        return copy
      })
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setFieldErrors({})

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
      const res = await fetch(`${apiUrl}/admissions/enquiries/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(formData),
      })

      const data = await res.json()

      if (!res.ok) {
        // Handle DRF validation error response
        if (data.error && data.error.fields) {
          setFieldErrors(data.error.fields)
          throw new Error(data.error.message || 'Validation error')
        } else if (res.status === 400) {
          // Standard DRF field errors
          setFieldErrors(data)
          throw new Error('Please correct the highlighted fields.')
        } else {
          throw new Error(data.detail || 'Failed to submit enquiry')
        }
      }

      // Success, redirect to dashboard
      router.push('/admissions')
    } catch (err: any) {
      setError(err.message || 'An error occurred during submission')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto animate-fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight">Record Admission Enquiry</h1>
        <p className="text-slate-500 mt-1">Capture basic information from prospective students or parents.</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
        {error && (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm font-medium">
            ⚠️ {error}
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {/* First Name */}
          <div>
            <label htmlFor="first_name" className="block text-sm font-semibold text-slate-700 mb-2">First Name *</label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              required
              value={formData.first_name}
              onChange={handleChange}
              className={`w-full px-4 py-2.5 rounded-lg border text-sm font-medium transition duration-150 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 ${
                fieldErrors.first_name ? 'border-rose-300 bg-rose-50/20' : 'border-slate-300'
              }`}
            />
            {fieldErrors.first_name && (
              <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.first_name[0]}</p>
            )}
          </div>

          {/* Last Name */}
          <div>
            <label htmlFor="last_name" className="block text-sm font-semibold text-slate-700 mb-2">Last Name *</label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              required
              value={formData.last_name}
              onChange={handleChange}
              className={`w-full px-4 py-2.5 rounded-lg border text-sm font-medium transition duration-150 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 ${
                fieldErrors.last_name ? 'border-rose-300 bg-rose-50/20' : 'border-slate-300'
              }`}
            />
            {fieldErrors.last_name && (
              <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.last_name[0]}</p>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-semibold text-slate-700 mb-2">Email Address *</label>
            <input
              type="email"
              id="email"
              name="email"
              required
              value={formData.email}
              onChange={handleChange}
              className={`w-full px-4 py-2.5 rounded-lg border text-sm font-medium transition duration-150 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 ${
                fieldErrors.email ? 'border-rose-300 bg-rose-50/20' : 'border-slate-300'
              }`}
            />
            {fieldErrors.email && (
              <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.email[0]}</p>
            )}
          </div>

          {/* Phone Number */}
          <div>
            <label htmlFor="phone_number" className="block text-sm font-semibold text-slate-700 mb-2">Phone Number *</label>
            <input
              type="text"
              id="phone_number"
              name="phone_number"
              required
              placeholder="+1234567890"
              value={formData.phone_number}
              onChange={handleChange}
              className={`w-full px-4 py-2.5 rounded-lg border text-sm font-medium transition duration-150 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 ${
                fieldErrors.phone_number ? 'border-rose-300 bg-rose-50/20' : 'border-slate-300'
              }`}
            />
            {fieldErrors.phone_number && (
              <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.phone_number[0]}</p>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {/* Preferred Course/Class */}
          <div>
            <label htmlFor="preferred_course" className="block text-sm font-semibold text-slate-700 mb-2">Preferred Class/Course *</label>
            <input
              type="text"
              id="preferred_course"
              name="preferred_course"
              required
              placeholder="e.g. Grade 11 Science"
              value={formData.preferred_course}
              onChange={handleChange}
              className={`w-full px-4 py-2.5 rounded-lg border text-sm font-medium transition duration-150 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 ${
                fieldErrors.preferred_course ? 'border-rose-300 bg-rose-50/20' : 'border-slate-300'
              }`}
            />
            {fieldErrors.preferred_course && (
              <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.preferred_course[0]}</p>
            )}
          </div>

          {/* Expected Start Date */}
          <div>
            <label htmlFor="expected_start_date" className="block text-sm font-semibold text-slate-700 mb-2">Expected Start Date *</label>
            <input
              type="date"
              id="expected_start_date"
              name="expected_start_date"
              required
              value={formData.expected_start_date}
              onChange={handleChange}
              className={`w-full px-4 py-2.5 rounded-lg border text-sm font-medium transition duration-150 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 ${
                fieldErrors.expected_start_date ? 'border-rose-300 bg-rose-50/20' : 'border-slate-300'
              }`}
            />
            {fieldErrors.expected_start_date && (
              <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.expected_start_date[0]}</p>
            )}
          </div>
        </div>

        {/* Source */}
        <div>
          <label htmlFor="source" className="block text-sm font-semibold text-slate-700 mb-2">Enquiry Source *</label>
          <select
            id="source"
            name="source"
            value={formData.source}
            onChange={handleChange}
            className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
          >
            <option value="website">Website</option>
            <option value="referral">Referral</option>
            <option value="social_media">Social Media</option>
            <option value="advertisement">Advertisement</option>
            <option value="walk_in">Walk-in</option>
            <option value="other">Other</option>
          </select>
        </div>

        {/* Notes */}
        <div>
          <label htmlFor="notes" className="block text-sm font-semibold text-slate-700 mb-2">Follow-up Notes / Comments</label>
          <textarea
            id="notes"
            name="notes"
            rows={4}
            placeholder="Add any specific requirements or discussion details here..."
            value={formData.notes}
            onChange={handleChange}
            className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
          ></textarea>
        </div>

        {/* Buttons */}
        <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
          <button
            type="button"
            onClick={() => router.push('/admissions')}
            className="px-5 py-2.5 rounded-lg border border-slate-300 text-slate-700 text-sm font-semibold hover:bg-slate-50 transition"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2.5 rounded-lg bg-sky-600 hover:bg-sky-700 disabled:bg-sky-400 text-white text-sm font-semibold shadow-md shadow-sky-200 transition flex items-center gap-2"
          >
            {loading && <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>}
            Save Enquiry
          </button>
        </div>
      </form>
    </div>
  )
}
