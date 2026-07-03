/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    viewTransition: true,
  },
  images: {
    remotePatterns: [{ protocol: "https", hostname: "**" }],
  },
}

export default nextConfig
