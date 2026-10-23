# FALCON: Autonomous Aerial Biodiversity & Nature-Credit Auditing System

FALCON is an autonomous unmanned aerial system (UAS) for verifying and auditing terrestrial biodiversity, soil faunal indicators, and ecological balance in support of biodiversity net-gain (BNG), regenerative agriculture compliance, and carbon-plus credit certification.

By deploying lightweight vision models (YOLOv11n) across aerial flight transects, FALCON classifies beneficial insects, pollinators, and herbivores simultaneously, transforming raw aerial imagery into tamper-evident biodiversity audit reports and tradeable Green Credit Units (GCUs).

---

## System Architecture

```mermaid
flowchart TD
    subgraph SENSING["1. Aerial Survey & Ingestion"]
        UAV["Autonomous UAV Transect (3-8m AGL)"]
        CAM["Down-facing Gimbal Camera (1024x1024)"]
        GNSS["GNSS Receiver & Barometric Altimeter"]
        UAV --> CAM
        UAV --> GNSS
    end

    subgraph INFERENCE["2. Edge Vision & Classification"]
        CAM --> YOLO["YOLOv11n Edge Detector"]
        YOLO --> DETS["12 Invertebrate Taxa Detections"]
    end

    subgraph GUILDS["3. Ecological Guild Mapping"]
        DETS --> G1["Pollinators (Bees)"]
        DETS --> G2["Biocontrol Predators (Wasps)"]
        DETS --> G3["Soil Detritivores (Earthworms, Slugs, Snails)"]
        DETS --> G4["Herbivore Pressure (Weevils, Caterpillars, etc.)"]
    end

    subgraph ENGINE["4. Biodiversity & Green Credit Engine"]
        G1 & G2 & G3 & G4 --> CALC["Biodiversity Calculation Engine"]
        CALC --> M1["Shannon-Wiener Index (H')"]
        CALC --> M2["Pollinator-to-Pest Ratio (PPR)"]
        CALC --> M3["Soil Bioturbation Score"]
        M1 & M2 & M3 --> GCU["Green Credit Calculator (GCU = Area × ΔQ)"]
    end

    subgraph LEDGER["5. Cryptographic Verification & Export"]
        GNSS & GCU --> BLOCK["SHA-256 Chained Audit Ledger"]
        BLOCK --> CERT["audit_certificate.json (Certified GCUs)"]
        BLOCK --> GEO["audit_transect.geojson (Hotspot Map)"]
    end
```

---

## Project Overview & Progress

> **Completion Status:** ~50% Complete  
> **Repository:** [ashcodes28/FALCON](https://github.com/ashcodes28/FALCON)  
> **Primary Modality:** Autonomous aerial video + GNSS metadata + Edge Deep Learning

### Completed (0% - 50% Phase)
* **Baseline Vision Models:** Evaluated single-modality YOLOv8 and lightweight YOLOv11n on 1024×1024 aerial inputs, achieving 85.5% baseline classification accuracy across 12 invertebrate classes.
* **Airframe & Payload CAD:** Completed 3D structural CAD modeling for the UAV airframe, camera gimbal, and compute payload bay housing the companion edge computer.
* **Architecture & Specification:** Formulated technical specifications and patent claim outlines for autonomous terrestrial biodiversity auditing.
* **Faunal Index Engine:** Built `src/biodiversity_engine.py` to calculate the Shannon-Wiener Faunal Diversity Index, Simpson's index, Pollinator-to-Pest Ratio (PPR), and soil faunal bioturbation indicators.
* **Green Credit Unit (GCU) Calculator:** Added formal ecological quality scoring ($Q$), baseline comparison ($\Delta Q$), and net Green Credit Units per hectare with accreditation tiers (Tier-AAA to Tier-C).
* **Cryptographic Audit Ledger:** Implemented SHA-256 chained audit logs ensuring tamper-evident inspection records for credit underwriters.

### Remaining Phase (50% - 100% Phase)
* **Georeferenced Heatmapping:** Projecting local detections onto field coordinates to generate GeoJSON and raster biodiversity heatmaps.
* **Flight Controller Integration:** Connecting edge vision outputs with MAVLink telemetry for automated transect waypoint surveys.
* **Hardware Edge Optimization:** Exporting TensorRT engines for deployment on an onboard NVIDIA Jetson Orin Nano.
* **Field Trials:** Conducting transect validation on certified organic and regenerative farming parcels.

---

## Functional Ecological Guilds (12 Classes)

FALCON detects 12 biological classes, grouping them into functional ecological guilds to quantify ecosystem health:

| Ecological Guild | Detected Classes | Ecological Significance |
| :--- | :--- | :--- |
| **Pollinators** | Bees | Core indicator of floral resources and reproductive pollination service. |
| **Biocontrol Predators** | Wasps | Parasitoids and predatory regulators that naturally suppress crop damage. |
| **Soil & Detrital Fauna** | Earthworms, Slugs, Snails | Soil aeration, bioturbation, and organic decomposition indicators. |
| **Herbivore Pressure** | Caterpillars, Grasshoppers, Weevils, Beetles, Earwigs, Ants | Primary consumers and vegetation pressure points. |

---

## Core Auditing Metrics

### 1. Shannon-Wiener Faunal Diversity Index ($H'$)
Quantifies species richness and evenness across the surveyed transect:
$$H' = -\sum_{i=1}^{S} p_i \ln p_i$$
where $p_i$ is the proportion of total individuals belonging to the $i$-th detected class, and $S$ is the total number of observed classes.

### 2. Pollinator-to-Pest Ratio (PPR)
Measures the balance of beneficial regulatory services against herbivore pressures:
$$\text{PPR} = \frac{N_{\text{Bees}} + N_{\text{Wasps}}}{N_{\text{Weevils}} + N_{\text{Caterpillars}} + \epsilon}$$

### 3. Soil Bioturbation Proxy
Calculates ground-level activity rates of earthworms and detritivores along low-altitude survey waypoints to verify soil biological vitality without destructive sampling:
$$\text{Score}_{\text{soil}} = 1.5 \cdot N_{\text{Earthworms}} + 0.5 \cdot (N_{\text{Slugs}} + N_{\text{Snails}})$$

### 4. Standardized Green Credit Units (GCUs) & Accreditation Tiers
Combines faunal indicators and surveyed acreage into an accredited, tradeable ecological asset:
$$\text{Ecological Quality Score } Q = 0.40 \cdot \left(\frac{H'}{\ln 12}\right) + 0.35 \cdot \min\left(\frac{\text{PPR}}{2.0}, 1.0\right) + 0.25 \cdot \min\left(\frac{\text{Score}_{\text{soil}}}{10}, 1.0\right)$$
$$\text{Net Ecological Uplift } \Delta Q = \max(Q - Q_{\text{baseline}}, 0.0)$$
$$\text{Net Green Credit Units (GCUs)} = \text{Surveyed Area (Hectares)} \times \Delta Q$$

| Quality Score ($Q$) | Accreditation Tier | Market Description |
| :--- | :--- | :--- |
| **$Q \ge 0.80$** | **Tier-AAA** | Exemplary Biodiversity Net-Gain |
| **$0.65 \le Q < 0.80$** | **Tier-AA** | High Ecological Integrity |
| **$0.50 \le Q < 0.65$** | **Tier-A** | Moderate Ecological Value |
| **$0.35 \le Q < 0.50$** | **Tier-B** | Early Regenerative Transition |
| **$Q < 0.35$** | **Tier-C** | Depleted / Sub-Baseline Monoculture |

---

## Detector Baseline & Performance

Evaluation was conducted using both YOLOv8 and YOLOv11n baseline models (`best.pt`, 5.56 MB):

* **High-Precision Classes:** Snail (1.00), Weevil (1.00), Moth (0.99), Wasp (0.97), and Ants (0.87).
* **Confusion Trends:** Small boundaries cause cross-class confusion between Beetles ↔ Wasps, Caterpillars ↔ Bees/Beetles, and Slugs ↔ Earthworms.
* **Resolution:** 1024×1024 image resolution enables localization of small invertebrate targets from low-altitude hover (3–8 m).

---

## 📂 Datasets & Benchmarks

The vision models in FALCON are trained and evaluated across standard entomological and aerial biodiversity benchmarks:

* [Agricultural Pests Image Dataset (Kaggle)](https://www.kaggle.com/datasets/fihmeh/agricultural-pests-image-dataset): Primary source for the 12-class micro-fauna dataset (Ants, Bees, Beetles, Caterpillars, Earthworms, Earwigs, Grasshoppers, Moths, Slugs, Snails, Wasps, Weevils), compiled for object detection and guild classification.
* [IP102 Insect Recognition Benchmark (CVPR)](https://github.com/xpwu95/IP102): Large-scale reference benchmark with over 75,000 images spanning 102 categories, utilized for pretraining feature extractors across diverse insect life stages.
* [AIDN Aerial Insect Dataset (Remote Sensing)](https://doi.org/10.3390/rs17060962): Aerial invertebrate survey dataset specifically designed for tiny object detection and multi-scale feature calibration in UAV biodiversity monitoring.

---

## System Roadmap

- [x] Technical literature and patent landscape mapping
- [x] Dataset curation & 12-class invertebrate annotation
- [x] Baseline YOLOv8 & YOLOv11n training and validation
- [x] UAV frame, gimbal, and payload bay CAD design
- [x] Automated biodiversity index calculation engine (`src/biodiversity_engine.py`)
- [x] Standardized Green Credit Unit (GCU) calculator and tier accounting
- [x] Cryptographic audit-trail logging with SHA-256 verification
- [x] Real-time Ecological & Green Credit HUD streaming (`src/detection.py`)
- [ ] MAVLink waypoint integration and dynamic transect flight planning
- [ ] Onboard companion computer deployment (Jetson Orin Nano)
- [ ] Field validation on certified regenerative agricultural plots

---

## Documentation & Assets

* [Biodiversity Auditing Specification](Biodiversity_Auditing_Specification.md)
* [Biodiversity Engine](src/biodiversity_engine.py)
* [Live Detection & Audit Script](src/detection.py)
* [Guild Isolation Lab Test](src/lab_test_detection.py)
* [Airframe CAD Visuals](CAD%20Images/)
* [License](LICENSE)
