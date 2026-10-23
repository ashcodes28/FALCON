"""
FALCON Biodiversity & Nature-Credit Audit Engine.

Transforms raw invertebrate detections into verifiable ecological health metrics
and standardized Green Credit Units (GCUs):
- Shannon-Wiener Faunal Diversity Index (H')
- Simpson's Diversity Index (1 - D)
- Pollinator-to-Pest Ratio (PPR)
- Soil Bioturbation Proxy Score
- Ecological Quality Score (Q)
- Gross & Net Green Credit Units (GCUs)
- Cryptographically chained (SHA-256) audit logs for ESG, BNG, and carbon-plus verification.
"""

from __future__ import annotations

import json
import math
import hashlib
from datetime import datetime, timezone
from dataclasses import dataclass, field
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

# Weightings for Ecological Quality Score Q (sum = 1.0)
WEIGHT_DIVERSITY = 0.40
WEIGHT_POLLINATOR_BALANCE = 0.35
WEIGHT_SOIL_HEALTH = 0.25

# Standard baseline for degraded / conventional agricultural monoculture
DEFAULT_BASELINE_SCORE = 0.20


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
    """Computes ecological, biodiversity, and functional guild metrics from detections."""
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

    # Soil score based on earthworms (heavily weighted) and detritivore counts
    soil_bioturbation_score = round(
        counts.get("Earthworms", 0) * 1.5 + counts.get("Slugs", 0) * 0.5 + counts.get("Snails", 0) * 0.5,
        3,
    )

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


def calculate_green_credits(
    faunal_metrics: Dict[str, Any],
    area_hectares: float = 1.0,
    baseline_score: float = DEFAULT_BASELINE_SCORE,
) -> Dict[str, Any]:
    """Calculates standardized Green Credit Units (GCUs) and rating tier.
    
    Formula:
        Diversity Factor (E) = min(H' / ln(12), 1.0)
        Pollinator Factor (B) = min(PPR / 2.0, 1.0)
        Soil Factor (S) = min(Score_soil / 10.0, 1.0)
        Ecological Quality Score (Q) = 0.40*E + 0.35*B + 0.25*S
        Net Uplift (delta_Q) = max(Q - baseline_score, 0.0)
        Gross GCU = area_hectares * Q
        Net Uplift GCU = area_hectares * delta_Q
    """
    total_count = faunal_metrics.get("total_count", 0)
    if total_count == 0:
        return {
            "area_hectares": area_hectares,
            "ecological_quality_score": 0.0,
            "baseline_score": baseline_score,
            "net_uplift": 0.0,
            "gross_green_credits": 0.0,
            "net_green_credits": 0.0,
            "credit_tier": "Tier-C (Depleted / Sub-Baseline)",
            "components": {
                "diversity_factor": 0.0,
                "pollinator_balance_factor": 0.0,
                "soil_vitality_factor": 0.0,
            },
        }

    h_prime = faunal_metrics.get("shannon_index", 0.0)
    ppr = faunal_metrics.get("pollinator_to_pest_ratio", 0.0)
    soil_score = faunal_metrics.get("soil_bioturbation_score", 0.0)

    # 1. Normalized diversity factor against max theoretical ln(12)
    max_h = math.log(len(CLASS_NAMES))
    diversity_factor = min(max(h_prime / max_h, 0.0), 1.0)

    # 2. Pollinator balance factor (PPR >= 2.0 yields maximum score)
    pollinator_factor = min(max(ppr / 2.0, 0.0), 1.0)

    # 3. Soil vitality factor (Score >= 10.0 yields maximum score)
    soil_factor = min(max(soil_score / 10.0, 0.0), 1.0)

    # Composite Ecological Quality Score Q
    q_score = (
        WEIGHT_DIVERSITY * diversity_factor
        + WEIGHT_POLLINATOR_BALANCE * pollinator_factor
        + WEIGHT_SOIL_HEALTH * soil_factor
    )
    q_score = round(min(max(q_score, 0.0), 1.0), 4)

    # Net ecological uplift compared to pre-intervention baseline
    net_uplift = round(max(q_score - baseline_score, 0.0), 4)

    # Credits = Area * Score
    gross_gcu = round(area_hectares * q_score, 3)
    net_gcu = round(area_hectares * net_uplift, 3)

    # Accreditation Tier assignment
    if q_score >= 0.80:
        tier = "Tier-AAA (Exemplary Biodiversity Net-Gain)"
    elif q_score >= 0.65:
        tier = "Tier-AA (High Ecological Integrity)"
    elif q_score >= 0.50:
        tier = "Tier-A (Moderate Ecological Value)"
    elif q_score >= 0.35:
        tier = "Tier-B (Early Regenerative Transition)"
    else:
        tier = "Tier-C (Depleted / Sub-Baseline)"

    return {
        "area_hectares": area_hectares,
        "ecological_quality_score": q_score,
        "baseline_score": baseline_score,
        "net_uplift": net_uplift,
        "gross_green_credits": gross_gcu,
        "net_green_credits": net_gcu,
        "credit_tier": tier,
        "components": {
            "diversity_factor": round(diversity_factor, 4),
            "pollinator_balance_factor": round(pollinator_factor, 4),
            "soil_vitality_factor": round(soil_factor, 4),
        },
    }


class BiodiversityAuditLedger:
    """Tamper-evident sequential audit log using SHA-256 chain hashing."""

    def __init__(
        self,
        parcel_id: str,
        area_hectares: float = 1.0,
        baseline_score: float = DEFAULT_BASELINE_SCORE,
        operator_id: str = "FALCON_UAV_01",
    ):
        self.parcel_id = parcel_id
        self.area_hectares = area_hectares
        self.baseline_score = baseline_score
        self.operator_id = operator_id
        self.blocks: List[Dict[str, Any]] = []
        self.current_hash = "GENESIS_BLOCK_000000000000000000000000000000000000000000000000"

    def record_sample(self, sample: AerialSample) -> Dict[str, Any]:
        """Appends an aerial observation block with its cryptographic hash."""
        faunal = calculate_faunal_indices(sample.detections)
        green_credits = calculate_green_credits(
            faunal,
            area_hectares=self.area_hectares,
            baseline_score=self.baseline_score,
        )
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
            "faunal_metrics": faunal,
            "green_credit_metrics": green_credits,
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
            faunal = payload["faunal_metrics"]
            gcu = payload["green_credit_metrics"]
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
                    "shannon_index": faunal["shannon_index"],
                    "pollinator_to_pest_ratio": faunal["pollinator_to_pest_ratio"],
                    "soil_bioturbation_score": faunal["soil_bioturbation_score"],
                    "quality_score": gcu["ecological_quality_score"],
                    "instant_gcu": gcu["net_green_credits"],
                    "credit_tier": gcu["credit_tier"],
                    "total_count": faunal["total_count"],
                    "guilds": faunal["guild_breakdown"],
                },
            }
            features.append(feature)

        return {
            "type": "FeatureCollection",
            "name": f"FALCON_Biodiversity_Audit_{self.parcel_id}",
            "features": features,
        }

    def export_certificate(self) -> Dict[str, Any]:
        """Summarizes transect results into an official Green Credit audit certificate."""
        if not self.blocks:
            return {"error": "No records in audit ledger"}

        all_detections: List[Detection] = []
        for block in self.blocks:
            for c_name, c_cnt in block["payload"]["faunal_metrics"]["class_counts"].items():
                c_id = next(k for k, v in CLASS_NAMES.items() if v == c_name)
                for _ in range(c_cnt):
                    all_detections.append(Detection(c_id, c_name, 1.0, (0, 0, 0, 0)))

        cumulative_faunal = calculate_faunal_indices(all_detections)
        cumulative_credits = calculate_green_credits(
            cumulative_faunal,
            area_hectares=self.area_hectares,
            baseline_score=self.baseline_score,
        )

        return {
            "certificate_title": "FALCON Verifiable Terrestrial Biodiversity & Green Credit Certificate",
            "parcel_id": self.parcel_id,
            "operator_id": self.operator_id,
            "registry_standard": "Verra Nature Framework & TNFD Tier-1 Compatible",
            "issued_at_utc": datetime.now(timezone.utc).isoformat(),
            "surveyed_area_hectares": self.area_hectares,
            "total_waypoint_samples": len(self.blocks),
            "green_credit_accounting": {
                "baseline_ecological_score": cumulative_credits["baseline_score"],
                "certified_ecological_score": cumulative_credits["ecological_quality_score"],
                "net_ecological_uplift": cumulative_credits["net_uplift"],
                "gross_green_credit_units": cumulative_credits["gross_green_credits"],
                "net_green_credit_units_awarded": cumulative_credits["net_green_credits"],
                "accreditation_tier": cumulative_credits["credit_tier"],
            },
            "ecological_indicators": cumulative_faunal,
            "cryptographic_verification": {
                "ledger_chain_valid": self.verify_integrity(),
                "genesis_hash": self.blocks[0]["payload"]["previous_hash"] if self.blocks else None,
                "final_block_hash": self.current_hash,
                "total_ledger_blocks": len(self.blocks),
            },
        }


# --- RUNNABLE VERIFICATION CHECK ---
if __name__ == "__main__":
    print("[FALCON] Running Green Credit Unit (GCU) verification self-test...")

    test_detections = [
        Detection(1, "Bees", 0.95, (10, 10, 50, 50)),
        Detection(1, "Bees", 0.91, (60, 20, 90, 60)),
        Detection(10, "Wasps", 0.88, (100, 100, 130, 140)),
        Detection(4, "Earthworms", 0.92, (200, 200, 240, 210)),
        Detection(4, "Earthworms", 0.89, (250, 250, 290, 280)),
        Detection(11, "Weevils", 0.94, (300, 300, 320, 330)),
        Detection(3, "Caterpillars", 0.82, (400, 400, 450, 420)),
    ]

    # 1. Test Faunal Indices
    faunal = calculate_faunal_indices(test_detections)
    assert faunal["total_count"] == 7
    assert faunal["shannon_index"] > 1.2
    assert faunal["pollinator_to_pest_ratio"] == 1.5  # 3 beneficials (2 bees, 1 wasp) / 2 pests

    # 2. Test Green Credit Calculation
    gcu_data = calculate_green_credits(faunal, area_hectares=10.0, baseline_score=0.20)
    assert gcu_data["ecological_quality_score"] > 0.40, "Quality score should reflect balanced community"
    assert gcu_data["net_uplift"] > 0.0, "Net uplift should be positive over degraded baseline"
    assert gcu_data["gross_green_credits"] > 0.0
    assert gcu_data["net_green_credits"] > 0.0
    assert "Tier-" in gcu_data["credit_tier"]

    # 3. Test Ledger Integration with Area & Baseline
    ledger = BiodiversityAuditLedger(
        parcel_id="AGRI-PARCEL-884",
        area_hectares=12.5,
        baseline_score=0.20,
        operator_id="UAV_PILOT_ALPHA",
    )

    sample1 = AerialSample(
        sample_id="SMPL-001",
        timestamp_utc="2026-10-24T00:00:00Z",
        latitude=40.7128,
        longitude=-74.0060,
        altitude_meters=5.0,
        detections=test_detections,
    )
    rec1 = ledger.record_sample(sample1)
    assert "green_credit_metrics" in rec1["payload"]

    # 4. Test Certificate Export
    cert = ledger.export_certificate()
    accounting = cert["green_credit_accounting"]
    assert accounting["net_green_credit_units_awarded"] > 0.0
    assert cert["cryptographic_verification"]["ledger_chain_valid"] is True
    assert cert["surveyed_area_hectares"] == 12.5

    # 5. Test Tamper Invalidation
    orig_credits = ledger.blocks[0]["payload"]["green_credit_metrics"]["net_green_credits"]
    ledger.blocks[0]["payload"]["green_credit_metrics"]["net_green_credits"] = 9999.0
    assert ledger.verify_integrity() is False, "Altering green credits must break the ledger chain"
    ledger.blocks[0]["payload"]["green_credit_metrics"]["net_green_credits"] = orig_credits
    assert ledger.verify_integrity() is True

    print(f"[FALCON] Self-test passed! Quality Score: {accounting['certified_ecological_score']:.3f} | Net GCU: {accounting['net_green_credit_units_awarded']:.2f} GCU | {accounting['accreditation_tier']}")
