"""
FALCON Biodiversity & Nature-Credit Audit Engine.

Transforms raw invertebrate detections into ecological health metrics:
- Shannon-Wiener Faunal Diversity Index (H')
- Simpson's Diversity Index (1 - D)
- Pollinator-to-Pest Ratio (PPR)
- Soil Bioturbation Proxy Score
- Cryptographically chained (SHA-256) audit logs for ESG and carbon-plus verification.
"""

from __future__ import annotations

import json
import math
import hashlib
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Tuple


# Baseline 12-class index map matching YOLOv11n best.pt
CLASS_NAMES: Dict[int, str] = {
    0: "Ants",
    1: "Bees",
    2: "Beetles",
    3: "Caterpillars",
    4: "Earthworms",
    5: "Earwigs",
    6: "Grasshoppers",
    7: "Moths",
    8: "Slugs",
    9: "Snails",
    10: "Wasps",
    11: "Weevils",
}

# Ecological Guild Mappings
GUILD_POLLINATORS = {"Bees"}
GUILD_BIOCONTROL = {"Wasps"}
GUILD_SOIL_DETRITIVORES = {"Earthworms", "Slugs", "Snails"}
GUILD_HERBIVORES = {"Caterpillars", "Grasshoppers", "Weevils", "Beetles", "Earwigs", "Ants", "Moths"}


@dataclass
class Detection:
    class_id: int
    class_name: str
    confidence: float
    box: Tuple[float, float, float, float]  # [x1, y1, x2, y2] normalized or pixels


@dataclass
class AerialSample:
    sample_id: str
    timestamp_utc: str
    latitude: float
    longitude: float
    altitude_meters: float
    detections: List[Detection] = field(default_factory=list)


def calculate_faunal_indices(detections: List[Detection]) -> Dict[str, Any]:
    """Computes ecological and biodiversity metrics from a list of detections."""
    counts: Dict[str, int] = {name: 0 for name in CLASS_NAMES.values()}
    for det in detections:
        if det.class_name in counts:
            counts[det.class_name] += 1

    total_individuals = len(detections)
    if total_individuals == 0:
        return {
            "total_count": 0,
            "shannon_index": 0.0,
            "simpson_index": 0.0,
            "pollinator_to_pest_ratio": 0.0,
            "soil_bioturbation_score": 0.0,
            "guild_breakdown": {
                "pollinators": 0,
                "biocontrol": 0,
                "soil_fauna": 0,
                "herbivores": 0,
            },
            "class_counts": counts,
        }

    # Shannon-Wiener Index: H' = - sum(p_i * ln(p_i))
    shannon_h = 0.0
    simpson_sum = 0.0
    for count in counts.values():
        if count > 0:
            p_i = count / total_individuals
            shannon_h -= p_i * math.log(p_i)
            simpson_sum += p_i * p_i

    simpson_diversity = 1.0 - simpson_sum

    # Guild counts
    pollinator_count = sum(counts[c] for c in GUILD_POLLINATORS)
    biocontrol_count = sum(counts[c] for c in GUILD_BIOCONTROL)
    soil_count = sum(counts[c] for c in GUILD_SOIL_DETRITIVORES)
    herbivore_count = sum(counts[c] for c in GUILD_HERBIVORES)

    # Key herbivores for ratio: Weevils + Caterpillars
    target_pests = counts.get("Weevils", 0) + counts.get("Caterpillars", 0)
    beneficials = pollinator_count + biocontrol_count

    ppr = beneficials / (target_pests + 1e-6)

    # Soil score based on earthworms and detritivore counts
    soil_bioturbation_score = round(counts.get("Earthworms", 0) * 1.5 + counts.get("Slugs", 0) * 0.5 + counts.get("Snails", 0) * 0.5, 3)

    return {
        "total_count": total_individuals,
        "shannon_index": round(shannon_h, 4),
        "simpson_index": round(simpson_diversity, 4),
        "pollinator_to_pest_ratio": round(ppr, 4),
        "soil_bioturbation_score": soil_bioturbation_score,
        "guild_breakdown": {
            "pollinators": pollinator_count,
            "biocontrol": biocontrol_count,
            "soil_fauna": soil_count,
            "herbivores": herbivore_count,
        },
        "class_counts": counts,
    }


class BiodiversityAuditLedger:
    """Tamper-evident sequential audit log using SHA-256 chain hashing."""

    def __init__(self, parcel_id: str, operator_id: str = "FALCON_UAV_01"):
        self.parcel_id = parcel_id
        self.operator_id = operator_id
        self.blocks: List[Dict[str, Any]] = []
        self.current_hash = "GENESIS_BLOCK_000000000000000000000000000000000000000000000000"

    def record_sample(self, sample: AerialSample) -> Dict[str, Any]:
        """Appends an aerial observation block with its cryptographic hash."""
        indices = calculate_faunal_indices(sample.detections)
        block_index = len(self.blocks)

        block_payload = {
            "block_index": block_index,
            "previous_hash": self.current_hash,
            "parcel_id": self.parcel_id,
            "operator_id": self.operator_id,
            "sample_id": sample.sample_id,
            "timestamp_utc": sample.timestamp_utc,
            "coordinates": {
                "latitude": sample.latitude,
                "longitude": sample.longitude,
                "altitude_m": sample.altitude_meters,
            },
            "metrics": indices,
            "raw_detection_count": len(sample.detections),
        }

        # Deterministic JSON serialization for hashing
        serialized = json.dumps(block_payload, sort_keys=True).encode("utf-8")
        block_hash = hashlib.sha256(serialized).hexdigest()

        record = {
            "payload": block_payload,
            "block_hash": block_hash,
        }

        self.blocks.append(record)
        self.current_hash = block_hash
        return record

    def verify_integrity(self) -> bool:
        """Validates that no record in the audit chain has been altered."""
        last_hash = "GENESIS_BLOCK_000000000000000000000000000000000000000000000000"
        for block in self.blocks:
            payload = block["payload"]
            if payload["previous_hash"] != last_hash:
                return False
            serialized = json.dumps(payload, sort_keys=True).encode("utf-8")
            recomputed = hashlib.sha256(serialized).hexdigest()
            if recomputed != block["block_hash"]:
                return False
            last_hash = block["block_hash"]
        return True

    def export_geojson(self) -> Dict[str, Any]:
        """Exports audit transect as a GeoJSON FeatureCollection."""
        features = []
        for block in self.blocks:
            payload = block["payload"]
            coords = payload["coordinates"]
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [coords["longitude"], coords["latitude"], coords["altitude_m"]],
                },
                "properties": {
                    "block_index": payload["block_index"],
                    "timestamp": payload["timestamp_utc"],
                    "block_hash": block["block_hash"][:16] + "...",
                    "shannon_index": payload["metrics"]["shannon_index"],
                    "pollinator_to_pest_ratio": payload["metrics"]["pollinator_to_pest_ratio"],
                    "soil_bioturbation_score": payload["metrics"]["soil_bioturbation_score"],
                    "total_count": payload["metrics"]["total_count"],
                    "guilds": payload["metrics"]["guild_breakdown"],
                },
            }
            features.append(feature)

        return {
            "type": "FeatureCollection",
            "name": f"FALCON_Biodiversity_Audit_{self.parcel_id}",
            "features": features,
        }

    def export_certificate(self) -> Dict[str, Any]:
        """Summarizes transect results into an audit certification report."""
        if not self.blocks:
            return {"error": "No records in audit ledger"}

        all_detections: List[Detection] = []
        # Reconstruct cumulative counts
        for block in self.blocks:
            for c_name, c_cnt in block["payload"]["metrics"]["class_counts"].items():
                c_id = next(k for k, v in CLASS_NAMES.items() if v == c_name)
                for _ in range(c_cnt):
                    all_detections.append(Detection(c_id, c_name, 1.0, (0, 0, 0, 0)))

        cumulative_metrics = calculate_faunal_indices(all_detections)

        return {
            "certificate_title": "FALCON Verifiable Terrestrial Biodiversity Audit Certificate",
            "parcel_id": self.parcel_id,
            "operator_id": self.operator_id,
            "issued_at_utc": datetime.now(timezone.utc).isoformat(),
            "total_waypoint_samples": len(self.blocks),
            "chain_valid": self.verify_integrity(),
            "ledger_genesis_hash": self.blocks[0]["payload"]["previous_hash"] if self.blocks else None,
            "ledger_final_hash": self.current_hash,
            "cumulative_ecological_indicators": cumulative_metrics,
        }


# --- RUNNABLE VERIFICATION CHECK ---
if __name__ == "__main__":
    print("[FALCON] Running self-test verification...")

    # 1. Test index calculation
    test_detections = [
        Detection(1, "Bees", 0.95, (10, 10, 50, 50)),
        Detection(1, "Bees", 0.91, (60, 20, 90, 60)),
        Detection(10, "Wasps", 0.88, (100, 100, 130, 140)),
        Detection(4, "Earthworms", 0.92, (200, 200, 240, 210)),
        Detection(11, "Weevils", 0.94, (300, 300, 320, 330)),
        Detection(3, "Caterpillars", 0.82, (400, 400, 450, 420)),
    ]

    metrics = calculate_faunal_indices(test_detections)
    assert metrics["total_count"] == 6
    assert metrics["shannon_index"] > 1.0, "Shannon index should reflect multi-class diversity"
    assert metrics["pollinator_to_pest_ratio"] == 1.5, f"Expected 3 beneficials / 2 pests = 1.5, got {metrics['pollinator_to_pest_ratio']}"
    assert metrics["guild_breakdown"]["pollinators"] == 2
    assert metrics["guild_breakdown"]["biocontrol"] == 1
    assert metrics["guild_breakdown"]["soil_fauna"] == 1

    # 2. Test ledger chain hashing & integrity
    ledger = BiodiversityAuditLedger(parcel_id="AGRI-PARCEL-884")
    sample1 = AerialSample(
        sample_id="SMPL-001",
        timestamp_utc="2026-10-19T10:00:00Z",
        latitude=40.7128,
        longitude=-74.0060,
        altitude_meters=5.0,
        detections=test_detections,
    )
    rec1 = ledger.record_sample(sample1)

    sample2 = AerialSample(
        sample_id="SMPL-002",
        timestamp_utc="2026-10-19T10:01:30Z",
        latitude=40.7130,
        longitude=-74.0058,
        altitude_meters=5.2,
        detections=[Detection(1, "Bees", 0.97, (12, 12, 45, 45))],
    )
    rec2 = ledger.record_sample(sample2)

    assert len(ledger.blocks) == 2
    assert ledger.verify_integrity() is True, "Audit chain integrity check must pass"

    # 3. Test tamper detection
    ledger.blocks[0]["payload"]["metrics"]["shannon_index"] = 99.9
    assert ledger.verify_integrity() is False, "Tampered block must fail verification"
    # Revert modification
    ledger.blocks[0]["payload"]["metrics"]["shannon_index"] = metrics["shannon_index"]
    assert ledger.verify_integrity() is True, "Reverted ledger must pass verification"

    # 4. Test GeoJSON and Certificate export
    geojson_out = ledger.export_geojson()
    assert geojson_out["type"] == "FeatureCollection"
    assert len(geojson_out["features"]) == 2

    cert = ledger.export_certificate()
    assert cert["chain_valid"] is True
    assert cert["total_waypoint_samples"] == 2
    assert cert["cumulative_ecological_indicators"]["guild_breakdown"]["pollinators"] == 3

    print("[FALCON] All self-tests passed successfully. Engine operational.")
