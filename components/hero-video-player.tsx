"use client"

import { useEffect, useRef, useState } from "react"
import { cn } from "@/lib/utils"

/**
 * Accessible cinematic video: autoplay muted by default, with play/pause + mute controls.
 * Respects prefers-reduced-motion (shows poster only until user plays).
 */
export function HeroVideoPlayer({
  src,
  poster,
  ariaLabel,
  className,
}: {
  src: string
  poster?: string
  ariaLabel: string
  className?: string
}) {
  const ref = useRef<HTMLVideoElement>(null)
  const [muted, setMuted] = useState(true)
  const [playing, setPlaying] = useState(false)
  const [reducedMotion, setReducedMotion] = useState(false)

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)")
    const apply = () => setReducedMotion(mq.matches)
    apply()
    mq.addEventListener?.("change", apply)
    return () => mq.removeEventListener?.("change", apply)
  }, [])

  useEffect(() => {
    const el = ref.current
    if (!el) return
    if (reducedMotion) {
      el.pause()
      setPlaying(false)
      return
    }
    el.muted = true
    const p = el.play()
    if (p) {
      p.then(() => setPlaying(true)).catch(() => setPlaying(false))
    }
  }, [reducedMotion, src])

  const togglePlay = () => {
    const el = ref.current
    if (!el) return
    if (el.paused) {
      void el.play().then(() => setPlaying(true)).catch(() => setPlaying(false))
    } else {
      el.pause()
      setPlaying(false)
    }
  }

  const toggleMute = () => {
    const el = ref.current
    if (!el) return
    el.muted = !el.muted
    setMuted(el.muted)
  }

  return (
    <div className={cn("absolute inset-0", className)}>
      <video
        ref={ref}
        className="absolute inset-0 h-full w-full object-cover"
        loop
        playsInline
        muted={muted}
        poster={poster}
        aria-label={ariaLabel}
        // Autoplay only when motion is allowed; controls remain for all users.
        autoPlay={!reducedMotion}
      >
        <source src={src} type="video/mp4" />
      </video>

      <div className="pointer-events-none absolute inset-x-0 top-0 z-10 flex justify-end p-3 sm:p-4">
        <div className="pointer-events-auto flex items-center gap-2 rounded-full border border-white/20 bg-black/45 p-1 backdrop-blur-md">
          <button
            type="button"
            onClick={togglePlay}
            className="inline-flex h-9 min-w-9 items-center justify-center rounded-full px-3 text-xs font-semibold text-white transition hover:bg-white/15 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
            aria-label={playing ? "Pause video" : "Play video"}
          >
            {playing ? "Pause" : "Play"}
          </button>
          <button
            type="button"
            onClick={toggleMute}
            className="inline-flex h-9 min-w-9 items-center justify-center rounded-full px-3 text-xs font-semibold text-white transition hover:bg-white/15 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
            aria-label={muted ? "Unmute video" : "Mute video"}
            aria-pressed={!muted}
          >
            {muted ? "Unmute" : "Mute"}
          </button>
        </div>
      </div>
    </div>
  )
}
