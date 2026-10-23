"""
FALCON Simulated Flight Mission & Green Credit Audit Runner.

Simulates an autonomous drone transect over a designated agricultural parcel.
Requires no camera, GPU, or video file. Generates real, verifiable output:
- audit_certificate.json
- audit_transect.geojson
"""

import json
from datetime import datetime, timezone
from biodiversity_engine import (
    Detection,
    AerialSample,
    BiodiversityAuditLedger,
    CLASS_NAMES,
)

def run_simulation(
    parcel_id: str = "AGRI-PARCEL-GREEN-VALLEY-01",
    area_hectares: float = 15.0,
    baseline_score: float = 0.20,
):
    print("=" * 70)
    print(" FALCON AUTONOMOUS AERIAL BIODIVERSITY & GREEN CREDIT AUDIT")
    print("=" * 70)
    print(f"Target Parcel ID   : {parcel_id}")
    print(f"Surveyed Area      : {area_hectares:.1f} Hectares")
    print(f"Degraded Baseline  : {baseline_score:.2f} (Conventional Monoculture Baseline)")
    print(f"Mission Start Time : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("-" * 70)

    # Initialize the cryptographic audit ledger
    ledger = BiodiversityAuditLedger(
        parcel_id=parcel_id,
        area_hectares=area_hectares,
        baseline_score=baseline_score,
        operator_id="UAV_PILOT_FALCON_01",
    )

    # Simulated aerial waypoints across the field transect
    waypoints = [
        {
            "id": "WP-001 (Field Margin & Wildflower Border)",
            "coords": (40.7128, -74.0060, 4.5),
            "detections": [
                Detection(1, "Bees", 0.94, (120, 80, 150, 110)),
                Detection(1, "Bees", 0.91, (200, 140, 230, 170)),
                Detection(1, "Bees", 0.88, (310, 220, 340, 250)),
                Detection(10, "Wasps", 0.92, (450, 300, 480, 330)),
                Detection(0, "Ants", 0.85, (500, 420, 520, 440)),
            ],
        },
        {
            "id": "WP-002 (Cover Crop Row A)",
            "coords": (40.7135, -74.0055, 4.8),
            "detections": [
                Detection(1, "Bees", 0.93, (80, 90, 110, 120)),
                Detection(4, "Earthworms", 0.95, (160, 210, 200, 240)),
                Detection(4, "Earthworms", 0.89, (270, 310, 310, 340)),
                Detection(10, "Wasps", 0.87, (380, 150, 410, 180)),
                Detection(11, "Weevils", 0.82, (520, 280, 540, 300)),
            ],
        },
        {
            "id": "WP-003 (Center Orchard Canopy)",
            "coords": (40.7142, -74.0050, 5.0),
            "detections": [
                Detection(1, "Bees", 0.96, (140, 180, 170, 210)),
                Detection(1, "Bees", 0.92, (260, 120, 290, 150)),
                Detection(7, "Moths", 0.91, (340, 390, 380, 430)),
                Detection(3, "Caterpillars", 0.84, (410, 220, 440, 240)),
                Detection(2, "Beetles", 0.88, (190, 320, 220, 350)),
            ],
        },
        {
            "id": "WP-004 (Moist Drainage Swale)",
            "coords": (40.7149, -74.0045, 4.2),
            "detections": [
                Detection(4, "Earthworms", 0.96, (100, 150, 140, 180)),
                Detection(4, "Earthworms", 0.93, (220, 280, 260, 310)),
                Detection(8, "Slugs", 0.89, (310, 350, 350, 380)),
                Detection(9, "Snails", 0.92, (400, 190, 430, 220)),
                Detection(10, "Wasps", 0.90, (480, 110, 510, 140)),
            ],
        },
        {
            "id": "WP-005 (Organic Transition Border)",
            "coords": (40.7156, -74.0040, 4.6),
            "detections": [
                Detection(1, "Bees", 0.95, (130, 140, 160, 170)),
                Detection(6, "Grasshoppers", 0.86, (250, 220, 280, 250)),
                Detection(5, "Earwigs", 0.83, (320, 310, 350, 340)),
                Detection(11, "Weevils", 0.80, (410, 400, 430, 420)),
                Detection(4, "Earthworms", 0.91, (180, 290, 220, 320)),
            ],
        },
    ]

    for i, wp in enumerate(waypoints, start=1):
        sample = AerialSample(
            sample_id=f"SAMPLE_{i:03d}",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            latitude=wp["coords"][0],
            longitude=wp["coords"][1],
            altitude_meters=wp["coords"][2],
            detections=wp["detections"],
        )
        rec = ledger.record_sample(sample)
        block = rec["payload"]
        gcu = block["green_credit_metrics"]
        print(f"-> Logged Block #{block['block_index'] + 1:02d} at {wp['id']}")
        print(f"   Detections: {len(wp['detections'])} | Quality Score Q: {gcu['ecological_quality_score']:.3f} | Block Hash: {rec['block_hash'][:16]}...")

    print("-" * 70)
    print(" MISSION COMPLETE: COMPILING AUDIT LEDGER & CERTIFICATE")
    print("-" * 70)

    # Export Certificate & GeoJSON
    certificate = ledger.export_certificate()
    geojson = ledger.export_geojson()

    with open("audit_certificate.json", "w", encoding="utf-8") as f:
        json.dump(certificate, f, indent=2)

    with open("audit_transect.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2)

    accounting = certificate["green_credit_accounting"]
    crypto = certificate["cryptographic_verification"]
    eco = certificate["ecological_indicators"]

    print("\n" + "=" * 70)
    print(" OFFICIAL GREEN CREDIT AUDIT SUMMARY")
    print("=" * 70)
    print(f" Accredited Rating Tier : {accounting['accreditation_tier']}")
    print(f" Certified Quality Score: {accounting['certified_ecological_score']:.3f} / 1.000")
    print(f" Baseline Floor Score   : {accounting['baseline_ecological_score']:.3f}")
    print(f" Net Ecological Uplift  : +{accounting['net_ecological_uplift']:.3f} Delta-Q")
    print(f" Total Surveyed Area    : {certificate['surveyed_area_hectares']:.2f} Hectares")
    print("-" * 70)
    print(f" >>> CERTIFIED GREEN CREDIT UNITS (GCUs) AWARDED: {accounting['net_green_credit_units_awarded']:.2f} GCU <<<")
    print("-" * 70)
    print(" Ecological Breakdown:")
    print(f"   - Total Invertebrates Identified : {eco['total_count']}")
    print(f"   - Shannon Diversity Index (H')   : {eco['shannon_index']:.3f}")
    print(f"   - Pollinator-to-Pest Ratio (PPR) : {eco['pollinator_to_pest_ratio']:.2f} (Beneficials / Pests)")
    print(f"   - Soil Bioturbation Score        : {eco['soil_bioturbation_score']:.1f}")
    print(f"   - Guild Breakdown: Pollinators={eco['guild_breakdown']['pollinators']}, Biocontrol={eco['guild_breakdown']['biocontrol']}, Soil Fauna={eco['guild_breakdown']['soil_fauna']}, Herbivores={eco['guild_breakdown']['herbivores']}")
    print("-" * 70)
    print(" Cryptographic Verification Proof:")
    print(f"   - Ledger Chain Integrity         : {'VALID (Zero Tampering Detected)' if crypto['ledger_chain_valid'] else 'INVALID'}")
    print(f"   - Total Cryptographic Blocks     : {crypto['total_ledger_blocks']}")
    print(f"   - Final Block SHA-256 Hash       : {crypto['final_block_hash']}")
    print("-" * 70)
    print(" Generated Artifacts:")
    print("   1. audit_certificate.json  (Formal credit underwriter certificate)")
    print("   2. audit_transect.geojson   (QGIS/ArcGIS parcel biodiversity map)")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_simulation()
