import type { MetadataRoute } from "next"
import { getAllArtifacts } from "@/lib/content"

const SITE_URL = "https://bluelifecommons.org"

export default function sitemap(): MetadataRoute.Sitemap {
  const staticRoutes = [
    "",
    "/species",
    "/species/deep-time",
    "/encyclopedia",
    "/regions",
    "/missions",
    "/research",
    "/guardian",
    "/catalog",
    "/media-intelligence",
    "/impact",
    "/partners",
    "/governance",
    "/privacy",
    "/about",
    "/terms",
    "/contribute",
    "/support",
    "/services",
    "/ecosystem",
  ].map((route) => ({
    url: `${SITE_URL}${route}`,
    changeFrequency: "weekly" as const,
    priority: route === "" ? 1 : route === "/species/deep-time" ? 0.85 : 0.7,
  }))

  const artifactRoutes = getAllArtifacts().map((a) => ({
    url: `${SITE_URL}${a.href}`,
    lastModified: a.last_verified ? new Date(a.last_verified) : undefined,
    changeFrequency: "monthly" as const,
    priority: 0.6,
  }))

  return [...staticRoutes, ...artifactRoutes]
}
