'use client'

import { useEffect, useRef } from 'react'
import { Container, ButtonLink } from "@/components/primitives"

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  const headingRef = useRef<HTMLHeadingElement>(null)

  useEffect(() => {
    // Log the error digest to the console (never expose to users directly)
    if (error.digest) {
      console.error('Error digest:', error.digest)
    } else {
      console.error(error)
    }
  }, [error])

  useEffect(() => {
    // Move focus to the heading for screen readers and keyboard navigation
    headingRef.current?.focus()
  }, [])

  return (
    <div className="bg-abyss">
      <Container className="flex min-h-[60vh] flex-col items-center justify-center gap-6 py-24 text-center">
        <span className="text-xs font-semibold uppercase tracking-[0.2em] text-glow">
          Unexpected disturbance
        </span>
        <h1
          ref={headingRef}
          tabIndex={-1}
          className="max-w-xl text-balance font-serif text-4xl font-semibold leading-tight text-abyss-foreground sm:text-5xl outline-none focus-visible:outline-glow focus-visible:outline-2 focus-visible:outline-offset-4"
        >
          We encountered an issue
        </h1>
        <p className="max-w-md text-pretty text-base leading-relaxed text-abyss-muted">
          A temporary disturbance has occurred. You can try reloading the segment, or return to the surface.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <button
            onClick={() => reset()}
            className="inline-flex items-center justify-center gap-2 rounded-full px-5 py-2.5 text-sm font-semibold transition-[color,transform] duration-200 bg-glow text-abyss-deep hover:-translate-y-0.5"
          >
            Try again
          </button>
          <ButtonLink href="/" variant="onDarkGhost">
            Return home
          </ButtonLink>
        </div>
      </Container>
    </div>
  )
}
