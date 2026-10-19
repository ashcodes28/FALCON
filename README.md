# FALCON: Autonomous Aerial Biodiversity & Nature-Credit Auditing System

FALCON is an autonomous unmanned aerial system (UAS) for verifying and auditing terrestrial biodiversity, soil faunal indicators, and ecological balance. Originally conceived as an agricultural pest surveillance and spraying platform, the system has transitioned into an ecological auditing platform for biodiversity net-gain (BNG), regenerative farming compliance, and carbon-plus credit certification.

By deploying lightweight vision models (YOLOv11n) across aerial flight transects, FALCON classifies beneficial insects, pollinators, and pests simultaneously, transforming raw aerial imagery into tamper-evident biodiversity audit reports.

---

## Project Overview & Progress

> **Completion Status:** ~50% Complete  
> **Repository:** [ashcodes28/FALCON](https://github.com/ashcodes28/FALCON)  
> **Primary Modality:** Autonomous aerial video + GNSS metadata + Edge Deep Learning

### Completed (0% - 50% Phase)
* **Baseline Vision Models:** Evaluated single-modality YOLOv8 and lightweight YOLOv11n on 1024×1024 aerial inputs, achieving 85.5% baseline classification accuracy across 12 invertebrate classes.
* **Airframe & Payload CAD:** Completed 3D structural CAD modeling for the UAV airframe, camera gimbal, and compute payload bay housing the companion edge computer.
* **Landscape Analysis:** Comprehensive literature and patent review covering aerial remote sensing, small-target insect detection, and precision actuation.

### Remaining Phase (50% - 100% Phase)
* **Faunal Index Engine:** Implementing automated computation of the Shannon-Wiener Faunal Diversity Index, Pollinator-to-Pest Ratio (PPR), and soil faunal bioturbation indicators.
* **Georeferenced Heatmapping:** Projecting local detections onto field coordinates to generate GeoJSON and raster biodiversity heatmaps.
* **Tamper-Evident Audit Trails:** Generating cryptographically hashed (SHA-256) inspection logs linking raw video frames, GPS coordinates, and detection matrices for third-party credit underwriters.
* **Flight Controller Integration:** Connecting edge vision outputs with MAVLink telemetry for automated transect waypoint surveys.

---

## Functional Ecological Guilds (12 Classes)

FALCON detects 12 biological classes, grouping them into functional ecological guilds to quantify ecosystem health rather than treating all invertebrates as targets for eradication:

| Ecological Guild | Detected Classes | Ecological Significance |
| :--- | :--- | :--- |
| **Pollinators** | Bees | Core indicator of floral resources and reproductive pollination service. |
| **Biocontrol Predators** | Wasps | Parasitoids and predatory regulators that naturally suppress crop damage. |
| **Soil & Detrital Fauna** | Earthworms, Slugs, Snails | Soil aeration, bioturbation, and organic decomposition indicators. |
| **Herbivore Pressure** | Caterpillars, Grasshoppers, Weevils, Beetles, Earwigs, Ants | Primary consumers and economic damage pressure points. |

---

## Core Auditing Metrics

### 1. Shannon-Wiener Faunal Diversity Index ($H'$)
Quantifies the species evenness and richness across the surveyed transect:
$$H' = -\sum_{i=1}^{S} p_i \ln p_i$$
where $p_i$ is the proportion of total individuals belonging to the $i$-th detected class, and $S$ is the total number of observed classes.

### 2. Pollinator-to-Pest Ratio (PPR)
Measures the balance of beneficial regulatory services against herbivore pressures:
$$\text{PPR} = \frac{N_{\text{Bees}} + N_{\text{Wasps}}}{N_{\text{Weevils}} + N_{\text{Caterpillars}} + \epsilon}$$

### 3. Soil Bioturbation Proxy
Calculates ground-level activity rates of earthworms and detritivores along low-altitude survey waypoints to verify soil biological vitality without destructive sampling.

---

## Detector Baseline & Performance

Evaluation was conducted using both YOLOv8 and YOLOv11n baseline models (`best.pt`, 5.56 MB):

* **High-Precision Classes:** Snail (1.00), Weevil (1.00), Moth (0.99), Wasp (0.97), and Ants (0.87).
* **Confusion Trends:** Small boundaries cause cross-class confusion between Beetles ↔ Wasps, Caterpillars ↔ Bees/Beetles, and Slugs ↔ Earthworms.
* **Resolution:** 1024×1024 image resolution enables localization of small invertebrate targets from low-altitude hover (3–10 m).

---

## System Roadmap

- [x] Literature review and patent landscape mapping
- [x] Dataset curation & 12-class invertebrate annotation
- [x] Baseline YOLOv8 & YOLOv11n training and validation
- [x] UAV frame, gimbal, and payload bay CAD design
- [x] Strategic pivot to autonomous biodiversity and nature-credit auditing
- [x] Automated biodiversity index calculation engine (`src/biodiversity_engine.py`)
- [x] Cryptographic audit-trail logging with SHA-256 verification
- [ ] MAVLink waypoint integration and dynamic transect flight planning
- [ ] Onboard companion computer deployment (Jetson Orin Nano)
- [ ] Field validation on certified regenerative agricultural plots

---

## Documentation & Assets

* [Literature Review & Patent Survey](Literature%20Review%20&%20Patent%20Survey.md)
* [Biodiversity Engine](src/biodiversity_engine.py)
* [Baseline Detection Script](src/detection.py)
* [Lab Test Script](src/lab_test_detection.py)
* [Airframe CAD Visuals](CAD%20Images/)
* [License](LICENSE)
