import type { MetadataRoute } from "next"

const AI_BOTS = ["GPTBot", "ChatGPT-User", "Google-Extended", "Anthropic-ai", "Claude-Web", "PerplexityBot"]

export default function robots(): MetadataRoute.Robots {
  // Previews and branch deployments stay fully closed: one disallow-all group, no
  // per-bot allow groups (a bot matching its own group would ignore the wildcard).
  if (process.env.VERCEL_ENV !== "production") {
    return { rules: [{ userAgent: "*", disallow: "/" }] }
  }
  return {
    rules: [
      { userAgent: "*", allow: "/" },
      { userAgent: AI_BOTS, allow: "/" },
    ],
    sitemap: "https://bluelifecommons.org/sitemap.xml",
  }
}
