'use client'

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function NewApplicationForm() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    date_of_birth: '',
    gender: 'M',
    email: '',
    phone_number: '',
    address: '',
    previous_school: '',
    previous_class_grade: '',
    percentage_marks: '',
    applied_for_class: '',
    preferred_stream: '',
    father_name: '',
    father_occupation: '',
    father_phone: '',
    mother_name: '',
    mother_occupation: '',
    mother_phone: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [fieldErrors, setFieldErrors] = useState<Record<string, string[]>>({})

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
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

    // Clean up decimal percentage_marks to be float or null
    const submissionData = {
      ...formData,
      percentage_marks: formData.percentage_marks ? parseFloat(formData.percentage_marks) : null,
    }

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
      const res = await fetch(`${apiUrl}/admissions/applications/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(submissionData),
      })

      const data = await res.json()

      if (!res.ok) {
        if (res.status === 400) {
          setFieldErrors(data)
          throw new Error('Please correct the highlighted fields.')
        } else {
          throw new Error(data.detail || 'Failed to submit application')
        }
      }

      router.push('/admissions')
    } catch (err: any) {
      setError(err.message || 'An error occurred during submission')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto animate-fade-in pb-12">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight">Formal Admission Application</h1>
        <p className="text-slate-500 mt-1">Submit full details to apply for student enrollment.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {error && (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm font-medium shadow-sm">
            ⚠️ {error}
          </div>
        )}

        {/* Section 1: Applicant Info */}
        <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <h2 className="text-xl font-bold text-slate-800 pb-3 border-b border-slate-100">1. Applicant Details</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <label htmlFor="first_name" className="block text-sm font-semibold text-slate-700 mb-2">First Name *</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                required
                value={formData.first_name}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              {fieldErrors.first_name && <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.first_name[0]}</p>}
            </div>
            <div>
              <label htmlFor="last_name" className="block text-sm font-semibold text-slate-700 mb-2">Last Name *</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                required
                value={formData.last_name}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              {fieldErrors.last_name && <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.last_name[0]}</p>}
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <label htmlFor="date_of_birth" className="block text-sm font-semibold text-slate-700 mb-2">Date of Birth *</label>
              <input
                type="date"
                id="date_of_birth"
                name="date_of_birth"
                required
                value={formData.date_of_birth}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              {fieldErrors.date_of_birth && <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.date_of_birth[0]}</p>}
            </div>
            <div>
              <label htmlFor="gender" className="block text-sm font-semibold text-slate-700 mb-2">Gender *</label>
              <select
                id="gender"
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              >
                <option value="M">Male</option>
                <option value="F">Female</option>
                <option value="O">Other</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <label htmlFor="email" className="block text-sm font-semibold text-slate-700 mb-2">Email Address *</label>
              <input
                type="email"
                id="email"
                name="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              {fieldErrors.email && <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.email[0]}</p>}
            </div>
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
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              {fieldErrors.phone_number && <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.phone_number[0]}</p>}
            </div>
          </div>

          <div>
            <label htmlFor="address" className="block text-sm font-semibold text-slate-700 mb-2">Residential Address *</label>
            <textarea
              id="address"
              name="address"
              rows={3}
              required
              value={formData.address}
              onChange={handleChange}
              className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
            ></textarea>
            {fieldErrors.address && <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.address[0]}</p>}
          </div>
        </div>

        {/* Section 2: Academic Info */}
        <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <h2 className="text-xl font-bold text-slate-800 pb-3 border-b border-slate-100">2. Academic Information</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <label htmlFor="applied_for_class" className="block text-sm font-semibold text-slate-700 mb-2">Applied For Class *</label>
              <input
                type="text"
                id="applied_for_class"
                name="applied_for_class"
                required
                placeholder="e.g. Grade 11"
                value={formData.applied_for_class}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              {fieldErrors.applied_for_class && <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.applied_for_class[0]}</p>}
            </div>
            <div>
              <label htmlFor="preferred_stream" className="block text-sm font-semibold text-slate-700 mb-2">Preferred Stream (if applicable)</label>
              <input
                type="text"
                id="preferred_stream"
                name="preferred_stream"
                placeholder="e.g. Science, Commerce, Arts"
                value={formData.preferred_stream}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div className="sm:col-span-2">
              <label htmlFor="previous_school" className="block text-sm font-semibold text-slate-700 mb-2">Previous School Name</label>
              <input
                type="text"
                id="previous_school"
                name="previous_school"
                value={formData.previous_school}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
            </div>
            <div>
              <label htmlFor="percentage_marks" className="block text-sm font-semibold text-slate-700 mb-2">Qualifying Marks (%)</label>
              <input
                type="number"
                step="0.01"
                id="percentage_marks"
                name="percentage_marks"
                placeholder="e.g. 85.5"
                value={formData.percentage_marks}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
              {fieldErrors.percentage_marks && <p className="mt-1 text-xs text-rose-600 font-semibold">{fieldErrors.percentage_marks[0]}</p>}
            </div>
          </div>
        </div>

        {/* Section 3: Parent Info */}
        <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <h2 className="text-xl font-bold text-slate-800 pb-3 border-b border-slate-100">3. Parent / Guardian Details</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div className="sm:col-span-1">
              <label htmlFor="father_name" className="block text-sm font-semibold text-slate-700 mb-2">Father's Name</label>
              <input
                type="text"
                id="father_name"
                name="father_name"
                value={formData.father_name}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
            </div>
            <div>
              <label htmlFor="father_occupation" className="block text-sm font-semibold text-slate-700 mb-2">Occupation</label>
              <input
                type="text"
                id="father_occupation"
                name="father_occupation"
                value={formData.father_occupation}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
            </div>
            <div>
              <label htmlFor="father_phone" className="block text-sm font-semibold text-slate-700 mb-2">Contact Number</label>
              <input
                type="text"
                id="father_phone"
                name="father_phone"
                value={formData.father_phone}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-4 border-t border-slate-100">
            <div className="sm:col-span-1">
              <label htmlFor="mother_name" className="block text-sm font-semibold text-slate-700 mb-2">Mother's Name</label>
              <input
                type="text"
                id="mother_name"
                name="mother_name"
                value={formData.mother_name}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
            </div>
            <div>
              <label htmlFor="mother_occupation" className="block text-sm font-semibold text-slate-700 mb-2">Occupation</label>
              <input
                type="text"
                id="mother_occupation"
                name="mother_occupation"
                value={formData.mother_occupation}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
            </div>
            <div>
              <label htmlFor="mother_phone" className="block text-sm font-semibold text-slate-700 mb-2">Contact Number</label>
              <input
                type="text"
                id="mother_phone"
                name="mother_phone"
                value={formData.mother_phone}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 text-sm font-medium transition duration-150 focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
            </div>
          </div>
        </div>

        {/* Buttons */}
        <div className="flex justify-end gap-3 pt-4 border-t border-slate-200">
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
            Submit Application
          </button>
        </div>
      </form>
    </div>
  )
}
