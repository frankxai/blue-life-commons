"""Critical release-gate cases for open kit manifests."""

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from validate_kits import invariant_errors, schema_errors, validate_file  # noqa: E402


class KitContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / "schema" / "kit-schema.json").read_text())
        cls.valid = json.loads((ROOT / "kits" / "k0-sampling" / "manifest.json").read_text())

    def test_proposed_k0_passes_both_gates(self):
        errors, _ = validate_file(ROOT / "kits" / "k0-sampling" / "manifest.json", self.schema)
        self.assertEqual([], errors)

    def test_false_measured_claim_is_rejected(self):
        kit = copy.deepcopy(self.valid)
        kit["claims"] = [{
            "kind": "measured",
            "text": "This kit cleaned canal water",
            "evidence_urls": ["https://example.org/speculative"],
        }]
        self.assertTrue(any("measured claim" in error for error in invariant_errors(kit)))

    def test_public_coordinates_are_rejected_even_nested(self):
        kit = copy.deepcopy(self.valid)
        kit["parts"][0]["coordinates"] = "private"
        self.assertTrue(any("private location" in error for error in invariant_errors(kit)))
        self.assertTrue(schema_errors(kit, self.schema, self.schema["$defs"]))

    def test_budget_must_cover_line_item_maximum(self):
        kit = copy.deepcopy(self.valid)
        kit["budget_eur"]["max"] = 80
        self.assertTrue(any("line-item totals" in error for error in invariant_errors(kit)))

    def test_field_claim_needs_reviews_report_and_approval(self):
        kit = copy.deepcopy(self.valid)
        kit["maturity"] = "authorized-field-trial"
        errors = invariant_errors(kit)
        self.assertTrue(any("test_report_path" in e for e in errors))
        self.assertTrue(any("all reviewers" in e for e in errors))
        self.assertTrue(any("approval_reference" in e for e in errors))

    def test_vendor_listing_needs_url_and_date(self):
        kit = copy.deepcopy(self.valid)
        kit["parts"][0]["price_basis"] = "vendor-listing"
        self.assertTrue(any("vendor listing" in e for e in invariant_errors(kit)))

    def test_source_file_cannot_escape_repository(self):
        kit = copy.deepcopy(self.valid)
        kit["protocol_path"] = "../../private-notes.md"
        self.assertTrue(any("repository-relative" in e for e in invariant_errors(kit)))


if __name__ == "__main__":
    unittest.main()
