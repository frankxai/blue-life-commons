import { Container, SectionHeading } from "@/components/primitives"

const PRINCIPLES = [
  {
    title: "Grounded, or silent",
    body: "Every claim traces to a citation with a source tier. If we cannot source it, we do not publish it. No speculation dressed as fact.",
  },
  {
    title: "Welfare-first ethics",
    body: "Sensitive locations are generalized. Missions carry ethics review. The Five Domains welfare model frames how we describe animal wellbeing.",
  },
  {
    title: "GitHub decides, the site publishes",
    body: "Contribution, review and versioning happen in the open on GitHub. This website is a rendering of what the community has verified.",
  },
  {
    title: "A commons, not a product",
    body: "Content is CC-BY and free forever. The work is sustained by services and sponsorship — never by locking the knowledge away.",
  },
]

export function Principles() {
  return (
    <section className="py-20 sm:py-28">
      <Container>
        <SectionHeading
          eyebrow="What makes it trustworthy"
          title="Principles we hold, not promises we make"
        />
        <div className="mt-12 grid gap-px overflow-hidden rounded-2xl border border-border bg-border sm:grid-cols-2">
          {PRINCIPLES.map((p) => (
            <article key={p.title} className="bg-card p-8">
              <h3 className="font-serif text-xl font-semibold text-card-foreground">
                {p.title}
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                {p.body}
              </p>
            </article>
          ))}
        </div>
      </Container>
    </section>
  )
}
