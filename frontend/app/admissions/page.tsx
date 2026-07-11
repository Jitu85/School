'use client'

import React, { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

interface Enquiry {
  id: string
  first_name: string
  last_name: string
  email: string
  phone_number: string
  enquiry_date: string
  source: string
  status: string
  preferred_course: string
  expected_start_date: string
  notes: string
}

interface Application {
  id: string
  application_number: string
  application_date: string
  status: string
  first_name: string
  last_name: string
  email: string
  phone_number: string
  applied_for_class: string
  preferred_stream: string
}

export default function AdmissionsDashboard() {
  const router = useRouter()
  const [enquiries, setEnquiries] = useState<Enquiry[]>([])
  const [applications, setApplications] = useState<Application[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'enquiries' | 'applications'>('enquiries')

  useEffect(() => {
    async function verifyAuthAndFetch() {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
        
        // 1. Verify user session
        const authRes = await fetch(`${apiUrl}/auth/me/`, { credentials: 'include' })
        if (!authRes.ok) {
          router.push('/login')
          return
        }

        // 2. Fetch data with session cookies
        const [enquiriesRes, applicationsRes] = await Promise.all([
          fetch(`${apiUrl}/admissions/enquiries/`, { credentials: 'include' }),
          fetch(`${apiUrl}/admissions/applications/`, { credentials: 'include' })
        ])

        if (!enquiriesRes.ok || !applicationsRes.ok) {
          throw new Error('Failed to fetch admissions records')
        }

        const enquiriesData = await enquiriesRes.json()
        const applicationsData = await applicationsRes.json()

        // DRF returns pagination object with results list
        setEnquiries(enquiriesData.results || enquiriesData)
        setApplications(applicationsData.results || applicationsData)
      } catch (err: any) {
        setError(err.message || 'An error occurred while loading data')
      } finally {
        setLoading(false)
      }
    }

    verifyAuthAndFetch()
  }, [router])

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'new':
      case 'submitted':
        return 'bg-blue-50 text-blue-700 border-blue-200'
      case 'contacted':
      case 'under_review':
        return 'bg-amber-50 text-amber-700 border-amber-200'
      case 'follow_up':
      case 'waitlisted':
        return 'bg-purple-50 text-purple-700 border-purple-200'
      case 'converted':
      case 'approved':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200'
      case 'lost':
      case 'rejected':
        return 'bg-rose-50 text-rose-700 border-rose-200'
      default:
        return 'bg-slate-50 text-slate-700 border-slate-200'
    }
  }

  const getStatusLabel = (status: string) => {
    return status.replace('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase())
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Top Header Section */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight">Admissions Dashboard</h1>
          <p className="text-slate-500 mt-1">Manage prospective student enquiries and formal applications.</p>
        </div>
        <div className="flex gap-3">
          <Link
            href="/admissions/enquiries/new"
            className="px-4 py-2 text-sm font-semibold rounded-lg bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 shadow-sm transition duration-150"
          >
            New Enquiry
          </Link>
          <Link
            href="/admissions/applications/new"
            className="px-4 py-2 text-sm font-semibold rounded-lg bg-sky-600 hover:bg-sky-700 text-white shadow-md shadow-sky-200 transition duration-150"
          >
            New Application
          </Link>
        </div>
      </div>

      {/* Stats Cards Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition duration-200">
          <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider">Total Enquiries</h3>
          <p className="text-3xl font-bold text-slate-800 mt-2">{enquiries.length}</p>
          <div className="mt-2 text-xs text-emerald-600 font-semibold flex items-center gap-1">
            <span>Active Enquiries Queue</span>
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition duration-200">
          <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider">Total Applications</h3>
          <p className="text-3xl font-bold text-slate-800 mt-2">{applications.length}</p>
          <div className="mt-2 text-xs text-sky-600 font-semibold flex items-center gap-1">
            <span>Pending Review: {applications.filter(a => a.status === 'submitted' || a.status === 'under_review').length}</span>
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition duration-200">
          <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider">Approved Admissions</h3>
          <p className="text-3xl font-bold text-slate-800 mt-2">{applications.filter(a => a.status === 'approved').length}</p>
          <div className="mt-2 text-xs text-emerald-600 font-semibold flex items-center gap-1">
            <span>Ready for Student Enrollment</span>
          </div>
        </div>
      </div>

      {/* Main Tab Controls */}
      <div className="border-b border-slate-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('enquiries')}
            className={`pb-4 px-1 border-b-2 font-semibold text-sm transition-all duration-200 ${
              activeTab === 'enquiries'
                ? 'border-sky-600 text-sky-600'
                : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
            }`}
          >
            Prospective Enquiries ({enquiries.length})
          </button>
          <button
            onClick={() => setActiveTab('applications')}
            className={`pb-4 px-1 border-b-2 font-semibold text-sm transition-all duration-200 ${
              activeTab === 'applications'
                ? 'border-sky-600 text-sky-600'
                : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
            }`}
          >
            Formal Applications ({applications.length})
          </button>
        </nav>
      </div>

      {/* Loading & Error States */}
      {loading && (
        <div className="text-center py-12 bg-white rounded-2xl border border-slate-200 shadow-sm">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-sky-600 mx-auto"></div>
          <p className="text-slate-500 mt-4 font-medium">Fetching records from admissions database...</p>
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm font-medium">
          ⚠️ {error}
        </div>
      )}

      {/* Data Table Section */}
      {!loading && !error && (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          {activeTab === 'enquiries' ? (
            enquiries.length === 0 ? (
              <div className="text-center py-16">
                <p className="text-slate-400 text-lg font-medium">No enquiries recorded yet.</p>
                <Link
                  href="/admissions/enquiries/new"
                  className="mt-4 inline-flex px-4 py-2 text-sm font-semibold rounded-lg bg-sky-600 text-white hover:bg-sky-700 transition"
                >
                  Create First Enquiry
                </Link>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-200 text-left">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Date</th>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Name</th>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Contact</th>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Course Preference</th>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Source</th>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {enquiries.map((enquiry) => (
                      <tr key={enquiry.id} className="hover:bg-slate-50/50 transition">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600 font-medium">
                          {new Date(enquiry.enquiry_date).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-800">
                          {enquiry.first_name} {enquiry.last_name}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                          <div>{enquiry.email}</div>
                          <div className="text-slate-400 text-xs mt-0.5">{enquiry.phone_number}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-800 font-medium">
                          {enquiry.preferred_course}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500 capitalize">
                          {enquiry.source}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${getStatusColor(enquiry.status)}`}>
                            {getStatusLabel(enquiry.status)}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )
          ) : (
            applications.length === 0 ? (
              <div className="text-center py-16">
                <p className="text-slate-400 text-lg font-medium">No formal applications recorded yet.</p>
                <Link
                  href="/admissions/applications/new"
                  className="mt-4 inline-flex px-4 py-2 text-sm font-semibold rounded-lg bg-sky-600 text-white hover:bg-sky-700 transition"
                >
                  Create First Application
                </Link>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-200 text-left">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">App Number</th>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Date</th>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Name</th>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Class & Stream</th>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Contact</th>
                      <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {applications.map((app) => (
                      <tr key={app.id} className="hover:bg-slate-50/50 transition">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-sky-700 font-bold">
                          {app.application_number}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600 font-medium">
                          {new Date(app.application_date).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-800">
                          {app.first_name} {app.last_name}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-800 font-medium">
                          <div>{app.applied_for_class}</div>
                          {app.preferred_stream && (
                            <div className="text-slate-400 text-xs mt-0.5">{app.preferred_stream}</div>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                          <div>{app.email}</div>
                          <div className="text-slate-400 text-xs mt-0.5">{app.phone_number}</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${getStatusColor(app.status)}`}>
                            {getStatusLabel(app.status)}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )
          )}
        </div>
      )}
    </div>
  )
}
