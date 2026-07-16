import type { Metadata } from "next"
import { DeepTimeHub } from "@/components/deep-time-hub"

export const metadata: Metadata = {
  title: "Deep Time Marine Reptiles",
  description:
    "Ocean “dinosaurs” explained: mosasaurs, plesiosaurs, pliosaurs, and ichthyosaurs — sourced deep-time entries with concept reconstruction media inside Blue Life Commons.",
  alternates: { canonical: "/species/deep-time" },
  openGraph: { url: "/species/deep-time" },
}

export default function DeepTimePage() {
  return <DeepTimeHub />
}
