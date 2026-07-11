import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Smart School Management System',
  description: 'Designed & Developed by ABHIJIT KUMAR MISRA',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
