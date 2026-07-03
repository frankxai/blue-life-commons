import { Container, SectionHeading } from "@/components/primitives"

const LAYERS = [
  {
    n: "01",
    name: "The Commons",
    tag: "This site · open & free",
    body: "A public library of ocean intelligence — species pages, region briefings, missions, datasets. Peer-reviewed, cited, CC-BY licensed. The trust layer everything else builds on.",
  },
  {
    n: "02",
    name: "Ocean Intelligence System",
    tag: "The engine",
    body: "Agents, connectors and an MCP server that turn the commons into living signals — pulling from NOAA, OBIS and GBIF to keep knowledge current and machine-readable.",
  },
  {
    n: "03",
    name: "Starlight Systems",
    tag: "Sustains the work",
    body: "Implementation for NGOs, sanctuaries and agencies — regional portals, research operating systems, custom connectors. Revenue funds the commons; the commons stays free.",
  },
]

export function ModelSection() {
  return (
    <section className="border-y border-border bg-paper py-20 sm:py-28">
      <Container>
        <SectionHeading
          eyebrow="How it fits together"
          title="One commons, three layers"
          description="Knowledge is created and governed in the open, made intelligent by shared systems, and sustained by a business that never gates the public good."
        />

        <ol className="mt-12 grid gap-5 md:grid-cols-3">
          {LAYERS.map((layer) => (
            <li
              key={layer.n}
              className="relative flex flex-col rounded-2xl border border-border bg-card p-7"
            >
              <span className="font-mono text-sm text-accent-foreground/60">
                {layer.n}
              </span>
              <h3 className="mt-3 font-serif text-xl font-semibold text-card-foreground">
                {layer.name}
              </h3>
              <span className="mt-1 text-xs font-medium uppercase tracking-wide text-primary">
                {layer.tag}
              </span>
              <p className="mt-4 text-sm leading-relaxed text-muted-foreground">
                {layer.body}
              </p>
            </li>
          ))}
        </ol>
      </Container>
    </section>
  )
}
