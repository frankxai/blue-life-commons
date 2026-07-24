import type { Metadata } from "next"
import { Container, SectionHeading, ButtonLink, ArrowRight } from "@/components/primitives"
import { PUBLIC_MARINE_MCP_URL } from "@/lib/utils"

export const metadata: Metadata = {
  title: "Services — Starlight Intelligence Systems",
  description:
    "The commons is free. Starlight Intelligence Systems builds the private, production-grade marine intelligence systems that fund it — for research institutions, marine parks, NGOs and governments.",
}

const OFFERINGS = [
  {
    title: "Ocean Intelligence deployments",
    body: "Private instances of the Ocean Intelligence System — connectors, agents and dashboards wired to your own data, jurisdictions and species of concern.",
  },
  {
    title: "Custom species & region intelligence",
    body: "Commissioned, expert-reviewed intelligence artifacts for your protected areas, built to the same open schema and delivered with full provenance.",
  },
  {
    title: "Monitoring & alerting pipelines",
    body: "Bleaching alerts, biodiversity anomaly detection and stranding-response workflows, integrated with the tools your team already uses.",
  },
  {
    title: "Advisory & enablement",
    body: "Design open marine-data practices, source and review workflows, and publication controls that your team can inspect and operate.",
  },
]

export default function ServicesPage() {
  return (
    <main>
      <div className="bg-abyss py-16 sm:py-20">
        <Container>
          <SectionHeading
            eyebrow="Starlight Intelligence Systems"
            tone="dark"
            title="The commons is free. The systems that power it are our craft."
            description="Blue Life Commons is stewarded by Starlight Intelligence Systems. The public knowledge stays open forever — and the private, production-grade deployments we build for institutions are what sustain it. This is the honest funnel: give the intelligence away, sell the implementation."
          />
          <div className="mt-8 flex flex-wrap gap-3">
            <ButtonLink href="mailto:hello@starlight.systems?subject=Marine%20intelligence%20system" variant="onDark">
              Start a conversation
              <ArrowRight />
            </ButtonLink>
            <ButtonLink href={PUBLIC_MARINE_MCP_URL} variant="onDarkGhost" external>
              Inspect the public MCP
            </ButtonLink>
          </div>
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <div className="grid gap-5 md:grid-cols-2">
          {OFFERINGS.map((o) => (
            <div key={o.title} className="rounded-2xl border border-border bg-card p-6 sm:p-7">
              <h2 className="font-serif text-xl font-semibold text-foreground">
                {o.title}
              </h2>
              <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                {o.body}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-14 grid gap-6 rounded-2xl border border-border bg-secondary p-6 sm:grid-cols-3 sm:p-8">
          <div>
            <h3 className="font-serif text-lg font-semibold text-foreground">Public foundation</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
              The commons and marine-mcp are public. Institution-specific
              deployments may remain private and are not represented as open
              source.
            </p>
          </div>
          <div>
            <h3 className="font-serif text-lg font-semibold text-foreground">No lock-in</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
              Deliverables follow the open artifact schema. If you leave, your
              intelligence stays portable and yours.
            </p>
          </div>
          <div>
            <h3 className="font-serif text-lg font-semibold text-foreground">Impact reinvested</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
              A share of commercial work funds review, missions and
              infrastructure back in the free commons.
            </p>
          </div>
        </div>
      </Container>
    </main>
  )
}
