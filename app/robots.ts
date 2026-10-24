import type { MetadataRoute } from "next"

export default function robots(): MetadataRoute.Robots {
  const isProduction = process.env.VERCEL_ENV === "production"
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: !isProduction ? "/" : undefined,
      },
      {
        userAgent: ["GPTBot", "ChatGPT-User", "Google-Extended", "Anthropic-ai", "Claude-Web", "PerplexityBot"],
        allow: "/",
      }
    ],
    sitemap: "https://bluelifecommons.org/sitemap.xml",
  }
}
