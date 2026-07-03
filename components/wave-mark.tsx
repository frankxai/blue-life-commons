export function WaveMark({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 32 32"
      fill="none"
      className={className}
      aria-hidden
      role="img"
    >
      <circle cx="16" cy="16" r="15" stroke="currentColor" strokeWidth="1.5" opacity="0.35" />
      <path
        d="M4 18c2.4 0 2.4-2.6 4.8-2.6S11.2 18 13.6 18s2.4-2.6 4.8-2.6S20.8 18 23.2 18s2.4-2.6 4.8-2.6"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
      />
      <path
        d="M6 22.5c2 0 2-2.2 4-2.2s2 2.2 4 2.2 2-2.2 4-2.2 2 2.2 4 2.2"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        opacity="0.55"
      />
      <circle cx="16" cy="10" r="2.1" fill="currentColor" />
    </svg>
  )
}
