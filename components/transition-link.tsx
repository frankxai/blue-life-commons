"use client"

import Link from "next/link"
import { useRouter } from "next/navigation"
import { startTransition, type ComponentProps } from "react"

// @ts-expect-error - addTransitionType is a React canary API bundled with Next 16
import { unstable_addTransitionType as addTransitionType } from "react"

type Props = ComponentProps<typeof Link> & {
  direction?: "forward" | "back"
}

/**
 * Link that tags the navigation with a view-transition type so pages can
 * animate directionally. Falls back gracefully where unsupported.
 */
export function TransitionLink({ direction = "forward", href, ...props }: Props) {
  const router = useRouter()

  return (
    <Link
      href={href}
      {...props}
      onClick={(e) => {
        props.onClick?.(e)
        if (
          e.defaultPrevented ||
          e.metaKey ||
          e.ctrlKey ||
          e.shiftKey ||
          e.button !== 0
        ) {
          return
        }
        if (typeof addTransitionType !== "function") return
        e.preventDefault()
        startTransition(() => {
          addTransitionType(
            direction === "back" ? "nav-back" : "nav-forward",
          )
          router.push(String(href))
        })
      }}
    />
  )
}
