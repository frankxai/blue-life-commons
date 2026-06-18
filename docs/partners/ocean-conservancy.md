# Ocean Conservancy — Marine Debris Data Integration

| Field | Value |
|---|---|
| Partner | Ocean Conservancy (oceanconservancy.org) |
| Programme | International Coastal Cleanup (ICC) |
| Scale | 350,000+ volunteers · 220+ countries · 300M+ lbs documented since 1986 |
| Data Platform | TrashBlaster (coastalcleanupdata.org) |
| OIS Connector Status | Planned — TrashBlaster API integration not yet implemented |
| Volunteer / Data Submission | oceanconservancy.org/what-you-can-do/international-coastal-cleanup/trashblaster/ |

Ocean Conservancy runs the International Coastal Cleanup — the world's largest single-day volunteer event dedicated to removing and documenting marine debris. Since 1986, ICC has mobilised more than 350,000 volunteers across 220+ countries, documenting over 300 million pounds of trash. The structured data collection methodology and global geographic coverage make ICC records a practical citizen science baseline for plastic type composition and debris hotspot analysis.

---

## Integration Points

### BLC Plastic Removal Content (`content/practices/ocean-plastic-removal.md`)

The ICC annual report data (available at [coastalcleanupdata.org](https://coastalcleanupdata.org)) provides per-region debris counts and itemised plastic type breakdowns — bottles, bags, straws, cigarette filters, and dozens of additional categories — collected using a consistent data card methodology. BLC wisdom articles and practice guides that address ocean plastic reference ICC data as the citizen science baseline for composition ratios. Cite the specific ICC Annual Report year rather than a generic reference.

### OIS Plastic Monitoring (Planned)

There is currently no implemented OIS connector for ICC data. The planned integration path runs through the **TrashBlaster API** (oceanconservancy.org/trash-free-seas/international-coastal-cleanup/trashblaster/). When implemented, the connector will support:

- Per-region debris count queries by cleanup date and geography
- Plastic type composition breakdowns for BLC species pages and habitat briefings
- Trend analysis across multiple ICC event years

This connector is on the OIS roadmap. Contributors interested in accelerating this integration should open an issue referencing this guide and the TrashBlaster API documentation.

### Field Mission Design

ICC cleanup events are natural candidates for BLC `/field-mission` artifacts. The programme provides:

- A standardised data collection card (consistent with ICC methodology)
- A global volunteer network for coordinating parallel events
- A well-documented submission path via TrashBlaster

Field mission authors embedding ICC methodology should reference the ICC Data Card in their protocol section and direct participants to submit records through TrashBlaster, ensuring BLC-affiliated cleanup data enters the global ICC dataset.

### For Content Creators

The ICC Annual Report is a reliable, annually updated source for plastic pollution figures at regional and global scale. It is frequently cited in peer-reviewed literature and by policy bodies, making it appropriate for BLC content that requires citable data. Access previous reports at [coastalcleanupdata.org](https://coastalcleanupdata.org).

---

## Attribution Standard

BLC content that references ICC data cites the organisation and the specific report year:

```
Marine debris data: Ocean Conservancy International Coastal Cleanup,
[Year] Annual Report (coastalcleanupdata.org)
```

---

*Built on SIP · Blue Life Commons (CC-BY-4.0)*
