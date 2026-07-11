import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24 bg-gradient-to-tr from-slate-50 to-sky-50">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
          Smart School Management System&nbsp;
        </p>
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-transparent">
          <span className="pointer-events-none flex place-items-center gap-2 p-8 lg:p-0 font-semibold text-sky-700">
            v1.0.0
          </span>
        </div>
      </div>

      <div className="relative flex flex-col place-items-center my-16">
        <h1 className="text-4xl lg:text-6xl font-extrabold tracking-tight text-slate-800 text-center mb-4">
          Smart School Management
        </h1>
        <p className="text-lg text-slate-600 text-center max-w-2xl mb-8">
          A modern, secure, and integrated platform to manage admissions, attendance, fees, exams, and school operations.
        </p>
        <div className="flex gap-4">
          <Link
            href="/admissions"
            className="px-6 py-3 rounded-lg bg-sky-600 hover:bg-sky-700 text-white font-semibold shadow-lg shadow-sky-200 transition-all duration-200 transform hover:-translate-y-0.5"
          >
            Admissions Desk
          </Link>
          <a
            href="http://localhost:8000/admin/"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 font-semibold shadow-sm transition-all duration-200 transform hover:-translate-y-0.5"
          >
            Admin Panel (Django)
          </a>
        </div>
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left gap-6">
        <div className="group rounded-xl border border-transparent px-5 py-4 transition-colors hover:border-slate-200 hover:bg-slate-100/50">
          <h2 className="mb-3 text-2xl font-semibold text-slate-800">
            Admissions{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-70 text-slate-600">
            Manage enquiries, review application forms, and enroll students.
          </p>
        </div>

        <div className="group rounded-xl border border-transparent px-5 py-4 transition-colors hover:border-slate-200 hover:bg-slate-100/50">
          <h2 className="mb-3 text-2xl font-semibold text-slate-800">
            Attendance{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-70 text-slate-600">
            Quick attendance grids, leave management, and daily register logs.
          </p>
        </div>

        <div className="group rounded-xl border border-transparent px-5 py-4 transition-colors hover:border-slate-200 hover:bg-slate-100/50">
          <h2 className="mb-3 text-2xl font-semibold text-slate-800">
            Fees & Accounts{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-70 text-slate-600">
            Generate invoices, allocate payments, print receipts, and check ledger books.
          </p>
        </div>

        <div className="group rounded-xl border border-transparent px-5 py-4 transition-colors hover:border-slate-200 hover:bg-slate-100/50">
          <h2 className="mb-3 text-2xl font-semibold text-slate-800">
            Examinations{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-70 text-slate-600">
            Input marks, define grading scales, and publish report cards.
          </p>
        </div>
      </div>

      <footer className="w-full text-center border-t border-slate-200 pt-8 mt-16 text-sm text-slate-500 font-medium">
        Designed & Developed by ABHIJIT KUMAR MISRA
      </footer>
    </main>
  )
}
