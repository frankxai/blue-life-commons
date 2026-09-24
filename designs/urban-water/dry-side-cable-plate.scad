// SPDX-License-Identifier: CC-BY-4.0
// Proposal v0.1: non-structural dry-side cable label/retainer plate.
// Never mount at the water edge without separate material and retrieval review.
// Print flat; verify fit, material aging and tie retention before use.

plate_width = 100;      // mm: across the rail
plate_height = 46;      // mm: along the rail
plate_thickness = 4;    // mm
edge_radius = 4;        // mm
slot_width = 4.4;       // mm: allow selected cable tie + print tolerance
slot_length = 10;       // mm
rail_tie_spacing = 26;  // mm, centre-to-centre
cable_tie_x = 15;       // mm, each cable slot offset from centre
rail_tie_x = 36;        // mm, rail tie column offset from centre
label_width = 24;       // mm, flat upper central label area
label_height = 12;      // mm

assert(plate_width >= 2*(rail_tie_x + slot_width/2 + edge_radius));
assert(rail_tie_spacing + slot_length + 2*edge_radius <= plate_height);
assert(label_width < 2*cable_tie_x - slot_width);
assert(label_height + slot_length + 8 <= plate_height);

module rounded_plate(w, h, r, t) {
    linear_extrude(height=t)
        offset(r=r) square([w-2*r, h-2*r], center=true);
}

module through_slot(x, y) {
    translate([x, y, -0.2])
        cube([slot_width, slot_length, plate_thickness+0.4], center=false);
}

difference() {
    rounded_plate(plate_width, plate_height, edge_radius, plate_thickness);
    // Outer slots tie this plate to a cabinet rail; cables carry no load.
    for (x = [-rail_tie_x-slot_width/2, rail_tie_x-slot_width/2])
        for (y = [-rail_tie_spacing/2-slot_length/2,
                   rail_tie_spacing/2-slot_length/2])
            through_slot(x, y);
    // Inner slots hold a cable in the lower part of the plate; the upper
    // centre has a shallow label recess for a printed adhesive ID/QR code.
    for (x = [-cable_tie_x-slot_width/2,
               cable_tie_x-slot_width/2])
        through_slot(x, -17);
    translate([-label_width/2, 4, plate_thickness-0.35])
        cube([label_width, label_height, 0.5]);
}
