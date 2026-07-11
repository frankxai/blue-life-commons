import type { MetadataRoute } from "next"

export default function robots(): MetadataRoute.Robots {
  const isProduction = process.env.VERCEL_ENV === "production"
  return {
    rules: isProduction
      ? { userAgent: "*", allow: "/" }
      : { userAgent: "*", disallow: "/" },
    sitemap: "https://bluelifecommons.org/sitemap.xml",
  }
}
