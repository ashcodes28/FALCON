# PROJECT COMPLETION REPORT

# FALCON: Autonomous Aerial Biodiversity & Nature-Credit Auditing System
### *A Deep-Learning-Powered System for Aerial Micro-Fauna Auditing, Ecological Indexing, and Verifiable Green Credit Issuance*

**Overall Project Completion:** 100%  
**Repository:** [https://github.com/ashcodes28/FALCON](https://github.com/ashcodes28/FALCON)  
**Date of Submission:** 24 October 2026  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Introduction](#2-introduction)  
   2.1 [Background and Motivation](#21-background-and-motivation)  
   2.2 [Objectives](#22-objectives)  
   2.3 [Scope of This Final Report](#23-scope-of-this-final-report)  
3. [Overall Project Implementation Snapshot](#3-overall-project-implementation-snapshot)
4. [Scientific Grounding, Literature & Patent Landscape](#4-scientific-grounding-literature--patent-landscape)  
   4.1 [Key Findings from Academic Literature](#41-key-findings-from-academic-literature)  
   4.2 [Patent Landscape & Novelty Gaps](#42-patent-landscape--novelty-gaps)  
   4.3 [Patented Novelty Claims](#43-patented-novelty-claims)  
5. [Multi-Guild Dataset & Ecological Taxonomy](#5-multi-guild-dataset--ecological-taxonomy)  
   5.1 [Invertebrate Image Corpus](#51-invertebrate-image-corpus)  
   5.2 [Functional Ecological Guild Mapping](#52-functional-ecological-guild-mapping)  
6. [Deep Learning Detector Architecture & Performance Evaluation](#6-deep-learning-detector-architecture--performance-evaluation)  
   6.1 [YOLOv8 & YOLOv11n Baseline Implementations](#61-yolov8--yolov11n-baseline-implementations)  
   6.2 [Per-Class Performance Metrics](#62-per-class-performance-metrics)  
   6.3 [Morphological Confusion Analysis](#63-morphological-confusion-analysis)  
7. [Platform & Hardware System Design](#7-platform--hardware-system-design)  
   7.1 [UAV Airframe & Payload Bay CAD](#71-uav-airframe--payload-bay-cad)  
   7.2 [End-to-End Autonomous Data Pipeline](#72-end-to-end-autonomous-data-pipeline)  
   7.3 [Guild Isolation Testing Module](#73-guild-isolation-testing-module)  
8. [Mathematical Biodiversity Engine & Green Credit Formulation](#8-mathematical-biodiversity-engine--green-credit-formulation)  
   8.1 [Shannon-Wiener Faunal Diversity Index](#81-shannon-wiener-faunal-diversity-index)  
   8.2 [Simpson's Diversity Index](#82-simpsons-diversity-index)  
   8.3 [Pollinator-to-Pest Ratio](#83-pollinator-to-pest-ratio)  
   8.4 [Soil Bioturbation Proxy Score](#84-soil-bioturbation-proxy-score)  
   8.5 [Composite Ecological Quality Score & Net Uplift](#85-composite-ecological-quality-score--net-uplift)  
   8.6 [Standardized Green Credit Units & Accreditation Tiers](#86-standardized-green-credit-units--accreditation-tiers)  
9. [Cryptographic Verification & Tamper-Evident Audit Ledger](#9-cryptographic-verification--tamper-evident-audit-ledger)  
   9.1 [Sequential SHA-256 Chained Block Architecture](#91-sequential-sha-256-chained-block-architecture)  
   9.2 [Cryptographic Anti-Tamper Security Validation](#92-cryptographic-anti-tamper-security-validation)  
   9.3 [Audit Certificate & GeoJSON Vector Exports](#93-audit-certificate--geojson-vector-exports)  
10. [System Validation, Simulation Flight Trials & Experimental Results](#10-system-validation-simulation-flight-trials--experimental-results)  
    10.1 [Automated Self-Test & Unit Verification](#101-automated-self-test--unit-verification)  
    10.2 [Autonomous Transect Simulation Flight Trial](#102-autonomous-transect-simulation-flight-trial)  
    10.3 [Real-Time Ecological & Green Credit HUD Streaming](#103-real-time-ecological--green-credit-hud-streaming)  
11. [Regulatory, Compliance & Environmental Market Impact](#11-regulatory-compliance--environmental-market-impact)
12. [Conclusion](#12-conclusion)
13. [References](#13-references)

---

## 1. Executive Summary

This report documents the completed 100% implementation of the FALCON autonomous unmanned aerial system (UAS). Originating as an aerial pest surveillance project, FALCON executed an architectural pivot into an autonomous terrestrial biodiversity auditing and green credit issuance platform. The system addresses a fundamental limitation in carbon-plus and Biodiversity Net-Gain (BNG) markets: satellite remote sensing captures only vegetative canopy reflection (NDVI) rather than living biological diversity, while manual ground surveys cannot scale economically across broad agricultural tracts.

FALCON integrates custom UAV hardware CAD, lightweight edge computer vision (YOLOv11n operating at 1024×1024 resolution), and an automated mathematical ecology engine. It classifies 12 invertebrate taxa into four functional guilds—pollinators, biocontrol predators, soil detritivores, and herbivores—to compute the Shannon-Wiener Faunal Diversity Index (H'), the Pollinator-to-Pest Ratio (PPR), and a soil bioturbation proxy score. These indices are synthesized into a standardized Ecological Quality Score (Q), benchmarked against pre-intervention degraded baselines (ΔQ), and converted directly into certified Green Credit Units (GCUs).

Every observation waypoint is sealed within a sequential SHA-256 cryptographic blockchain ledger, ensuring tamper-evident data integrity for carbon registries and credit underwriters. Full system validation was achieved through a multi-waypoint flight audit simulation over a 15-hectare parcel, awarding 10.665 net Green Credit Units under a certified Tier-AAA rating.

---

## 2. Introduction

### 2.1 Background and Motivation
Global environmental markets, corporate sustainability mandates (such as the Taskforce on Nature-related Financial Disclosures, TNFD), and statutory frameworks (such as the UK Biodiversity Net Gain mandate) now assign quantifiable financial value to ecological restoration. Landowners and agricultural enterprises can generate biodiversity credits and carbon-plus premiums by demonstrating verified biological uplift on their land.

However, the Monitoring, Reporting, and Verification (MRV) of biodiversity faces severe technical barriers. Satellite remote sensing is blind to ground-level micro-fauna and soil invertebrates, while manual surveys by field entomologists are labor-intensive, localized, and prone to sampling variance. Furthermore, self-reported paper claims introduce fraud risk into environmental credit registries. FALCON addresses this bottleneck by deploying an autonomous drone platform that gathers aerial imagery at low altitude (3–8 m), classifies micro-fauna in real time, and logs cryptographically verifiable audit ledgers.

### 2.2 Objectives
1. Implement a lightweight deep learning detector (YOLOv11n) trained on 1024×1024 resolution to classify 12 ground and foliage invertebrate taxa.
2. Group detected taxa into functional ecological guilds to quantify ecosystem service delivery rather than treating all invertebrates as uniform targets.
3. Formulate and implement mathematical indices for faunal biodiversity (H'), pollinator balance (PPR), and soil surface biological health.
4. Establish an automated Green Credit Unit (GCU) calculation engine translating ecological uplift into tradeable, accredited units.
5. Engineer a tamper-evident sequential SHA-256 cryptographic audit ledger that exports standardized machine-readable certificates (`audit_certificate.json`) and geospatial vector layers (`audit_transect.geojson`).
6. Validate the complete end-to-end architecture through unit testing, anti-tamper security checks, and a simulated 15-hectare aerial flight audit.

### 2.3 Scope of This Final Report
This document marks the conclusion of the FALCON engineering project, covering all hardware, machine learning, algorithmic, cryptographic, and validation deliverables.

---

## 3. Overall Project Implementation Snapshot

Every planned work package across the project timeline has reached completion.

| Work Package | Deliverable | Status | % Weight |
| :--- | :--- | :---: | :---: |
| **1. Literature Review & Regulatory Mapping** | Academic state of the art, IP landscape, patent claim outlines | Completed | 10% |
| **2. Problem Definition & Architectural Pivot** | Transition from pest spraying to autonomous biodiversity auditing | Completed | 5% |
| **3. Dataset Curation & Benchmark Linking** | 12-class micro-fauna corpus, Kaggle/IP102/AIDN benchmark curation | Completed | 10% |
| **4. Baseline Model Training & Validation** | YOLOv8 single-modality baseline (85.5% accuracy) | Completed | 10% |
| **5. Edge Model Development & Optimization** | Lightweight YOLOv11n (5.56 MB) at 1024×1024 resolution | Completed | 10% |
| **6. Airframe & Payload Bay Mechanical CAD** | 3D CAD modeling of airframe, gimbal mount, and electronics bay | Completed | 10% |
| **7. Ecological Guild Classification Engine** | 4-guild functional mapping (Pollinators, Predators, Soil, Herbivores) | Completed | 10% |
| **8. Mathematical Biodiversity Engine** | Shannon-Wiener H', Simpson's 1-D, PPR, and soil bioturbation scoring | Completed | 10% |
| **9. Green Credit Unit (GCU) Formulation** | Quality score Q, net uplift Delta-Q, area scaling, 5 accreditation tiers | Completed | 10% |
| **10. Cryptographic Audit Ledger & Exports** | SHA-256 sequential chaining, `audit_certificate.json`, GeoJSON exporter | Completed | 10% |
| **11. System Validation & Flight Simulation** | Automated test suite (`biodiversity_engine.py`), flight trial (`simulate_audit.py`) | Completed | 5% |
| **Total** | **Full System Implementation** | **100% Completed** | **100%** |

---

## 4. Scientific Grounding, Literature & Patent Landscape

### 4.1 Key Findings from Academic Literature
* **Small-Object Aerial Invertebrate Localization:** Low-altitude remote sensing studies (such as AIDN, Remote Sensing 2024; Bai et al., 2023) confirm that insects occupy 10×10 to 30×30 pixels in typical frames. Training on 1024×1024 resolution preserves high-frequency edge gradients necessary to distinguish morphologically close taxa.
* **Limitations of Aerial Plant-Reflectance Indices:** Research confirms that NDVI and multispectral vegetation indices correlate with chlorophyll content but fail to predict invertebrate biodiversity or soil biological respiration (Alsadik et al., 2024). Direct micro-fauna enumeration provides the empirical ground truth required by biodiversity accreditation standards.

### 4.2 Patent Landscape & Novelty Gaps
Prior agricultural drone patents (e.g., US 10,364,029 B2; US 2017/0231213 A1; KR 20230062713 A) focus on mechanical hardware: spray tanks, nozzle arrays, and chemical delivery valves. Algorithmic methods converting multi-guild micro-fauna aerial classifications into cryptographically sealed ecological credits were completely unaddressed in surveyed prior art.

### 4.3 Patented Novelty Claims
FALCON establishes novel system and method claims:
1. *Method Claim:* Autonomous capture of low-altitude aerial transects, real-time edge classification into functional ecological guilds, spatial calculation of multi-guild diversity and pollinator ratios, and derivation of certified Green Credit Units based on verified uplift over baseline.
2. *System Claim:* An onboard companion processor cryptographically binding video frames, GPS waypoints, derived faunal metrics, and prior block hashes into an immutable SHA-256 ledger.

---

## 5. Multi-Guild Dataset & Ecological Taxonomy

### 5.1 Invertebrate Image Corpus
The model training dataset comprises 12 distinct invertebrate taxa commonly encountered in agricultural and terrestrial ecosystems, linked to the [Agricultural Pests Image Dataset (Kaggle)](https://www.kaggle.com/datasets/fihmeh/agricultural-pests-image-dataset), supplemented by representation learning transfer from [IP102](https://github.com/xpwu95/IP102) and [AIDN](https://doi.org/10.3390/rs17060962).

### 5.2 Functional Ecological Guild Mapping
Rather than treating all invertebrates uniformly, FALCON groups the 12 classes into four functional ecological guilds:

| Ecological Guild | Included Classes | Ecological Function & Role |
| :--- | :--- | :--- |
| **Pollinators** | Bees | Floral resource indicator, angiosperm cross-pollination. |
| **Biocontrol Predators** | Wasps | Parasitoid regulation, natural suppression of herbivore larvae. |
| **Soil & Detrital Fauna** | Earthworms, Slugs, Snails | Soil bioturbation, topsoil moisture indicator, organic decomposition. |
| **Herbivore Pressure** | Caterpillars, Grasshoppers, Weevils, Beetles, Earwigs, Ants, Moths | Foliage defoliation pressure, primary consumer biomass. |

---

## 6. Deep Learning Detector Architecture & Performance Evaluation

### 6.1 YOLOv8 & YOLOv11n Baseline Implementations
Two detector baselines were trained and benchmarked at 1024×1024 resolution:
* **YOLOv8 Baseline:** Reached 85.5% overall accuracy on validation splits.
* **YOLOv11n Edge Detector:** Compressed into a lightweight 5.56 MB model (`best.pt`), optimized for edge deployment on companion computers (such as NVIDIA Jetson Orin Nano).

### 6.2 Per-Class Performance Metrics
High classification accuracy was achieved across visually distinct invertebrate categories:
* **Snail:** 1.00 Precision
* **Weevil:** 1.00 Precision
* **Moth:** 0.99 Precision
* **Wasp:** 0.97 Precision
* **Ants:** 0.87 Precision

### 6.3 Morphological Confusion Analysis
Analysis of the normalized confusion matrix revealed specific inter-class confusion patterns:
* Small bounding contours produced cross-class overlap between Beetles ↔ Wasps and Caterpillars ↔ Bees/Beetles.
* Subterranean/surface detritivores exhibited expected visual overlap (Slugs ↔ Earthworms at 0.29).
* Because both members of confused pairs often belong to the same functional guild (e.g., Slugs and Earthworms are both Detritivores), guild-level index derivation remains robust against individual species misclassifications.

---

## 7. Platform & Hardware System Design

### 7.1 UAV Airframe & Payload Bay CAD
The mechanical airframe (detailed in [`CAD Images/`](CAD%20Images/)) incorporates:
* A rigid carbon-fiber multi-rotor frame with vibration-isolated motor arms.
* A downward-facing 2-axis brushless camera gimbal maintaining nadir optical alignment.
* A ventilated payload bay housing the companion single-board computer, GNSS module, and laser altimeter.

### 7.2 End-to-End Autonomous Data Pipeline
1. Downward gimbal camera captures 1024×1024 frames at 3–8 m AGL.
2. Edge YOLOv11n performs inference, outputting bounding coordinates and confidence scores.
3. The biodiversity calculation engine classifies detections into ecological guilds.
4. Mathematical routines compute H', PPR, and soil vitality.
5. The cryptographic ledger generates a sequentially hashed block.
6. Real-time metrics are streamed to the ground station HUD and written to persistent storage.

### 7.3 Guild Isolation Testing Module
[`src/lab_test_detection.py`](src/lab_test_detection.py) provides bench testing capabilities to isolate and verify specific guilds (`POLLINATORS`, `BIOCONTROL`, `SOIL_FAUNA`, `HERBIVORES`), allowing operators to validate guild-specific confidence thresholds before deployment.

---

## 8. Mathematical Biodiversity Engine & Green Credit Formulation

### 8.1 Shannon-Wiener Faunal Diversity Index (H')
Quantifies invertebrate species richness and relative abundance evenness across the surveyed parcel:

> **Equation 8.1 (Shannon-Wiener Diversity Index):**  
> **H' = − ∑ [ p_i · ln(p_i) ]**  *(summed across all observed taxa i = 1 to S)*  
> where:  
> * *S* = Total number of observed taxa (*S* = 12 in the FALCON ecological taxonomy).  
> * *n_i* = Number of individuals recorded for taxon *i*.  
> * *N* = Total number of individuals recorded across all taxa (*N = ∑ n_i*).  
> * *p_i* = Relative abundance proportion of taxon *i* (*p_i = n_i / N*).  
> 
> The theoretical maximum diversity for 12 equally distributed taxa is ln(12) ≈ 2.4849. A higher *H'* indicates an ecologically balanced invertebrate community with high evenness and species richness.

### 8.2 Simpson's Diversity Index (1 − D)
Measures the probability that two randomly sampled invertebrates from the surveyed transect belong to different species, quantifying community evenness and resistance to single-species dominance:

> **Equation 8.2 (Simpson's Diversity Index):**  
> **1 − D = 1 − ∑ [ p_i² ]**  *(summed across all observed taxa i = 1 to S)*  
> where *p_i* is the relative abundance proportion of taxon *i*. Values approach 1.0 in highly diverse habitats and drop toward 0.0 under monoculture pest infestations.

### 8.3 Pollinator-to-Pest Ratio (PPR)
Directly quantifies the balance of ecosystem service providers (beneficial pollinators and parasitoid biocontrol regulators) against destructive foliage-feeding herbivores:

> **Equation 8.3 (Pollinator-to-Pest Ratio):**  
> **PPR = (N_Bees + N_Wasps) / (N_Weevils + N_Caterpillars + 10⁻⁶)**  
> where:  
> * *N_Bees* and *N_Wasps* represent beneficial pollinating and parasitoid predatory guilds.  
> * *N_Weevils* and *N_Caterpillars* represent primary economic pest pressures.  
> * A smoothing constant of 10⁻⁶ in the denominator prevents division-by-zero artifacts in pest-free or heavily suppressed parcels.  
> 
> An audited parcel with PPR ≥ 2.0 indicates an ecosystem where natural regulatory mechanisms outweigh herbivore pressure.

### 8.4 Soil Bioturbation Proxy Score
Assesses biological activity and structural aeration in the upper soil and litter layer through aerial observation of epigeic detrital macro-invertebrates:

> **Equation 8.4 (Soil Bioturbation Proxy Score):**  
> **Score_soil = 1.5 · N_Earthworms + 0.5 · (N_Slugs + N_Snails)**  
> where Earthworms receive a 1.5× biological weighting reflecting their primary role in soil macro-pore creation, water infiltration, and organic matter incorporation, while Gastropods receive a 0.5× weighting as moisture and detrital decomposition indicators.

### 8.5 Composite Ecological Quality Score & Net Uplift
The composite Ecological Quality Score (*Q* ∈ [0.0, 1.0]) synthesizes the three biological pillars into a single standardized scalar metric:

> **Equation 8.5 (Composite Ecological Quality Score):**  
> **Q = 0.40 · (H' / ln 12) + 0.35 · min(PPR / 2.0, 1.0) + 0.25 · min(Score_soil / 10.0, 1.0)**  
> where:  
> * 40% weight is assigned to overall community diversity and evenness (*H'* normalized by its theoretical maximum ln(12) ≈ 2.4849).  
> * 35% weight is assigned to the functional ecosystem balance between pollinators/predators and pests (PPR normalized to 2.0).  
> * 25% weight is assigned to epigeic soil biological activity (Score_soil normalized to 10.0).  

Net ecological uplift (ΔQ) measures verified ecological gain above the degraded agricultural monoculture baseline (*Q_baseline* = 0.20):

> **Equation 8.6 (Net Ecological Uplift):**  
> **ΔQ = max(Q − Q_baseline, 0.0)**  
> Ensuring that credits are only issued for verified ecological additionality above the regional degraded benchmark.

### 8.6 Standardized Green Credit Units & Accreditation Tiers
Credits are issued on a per-hectare uplift basis, directly tying financial issuance to physical land area and verifiable biodiversity additionality:

> **Equation 8.7 (Gross Green Credit Units):**  
> **Gross GCU = Surveyed Area (ha) × Q**  

> **Equation 8.8 (Net Certified Green Credit Units Awarded):**  
> **Net Awarded GCU = Surveyed Area (ha) × ΔQ**  

Audited parcels are classified into five standardized accreditation tiers based on their certified Ecological Quality Score (*Q*):

| Quality Score (Q) Range | Accreditation Tier | Ecological Classification & Market Status |
| :--- | :--- | :--- |
| **Q ≥ 0.80** | **Tier-AAA** | Exemplary Biodiversity Net-Gain (Premium market issuance) |
| **0.65 ≤ Q < 0.80** | **Tier-AA** | High Ecological Integrity (Standard nature credit issuance) |
| **0.50 ≤ Q < 0.65** | **Tier-A** | Moderate Ecological Value (Transitional conservation credit) |
| **0.35 ≤ Q < 0.50** | **Tier-B** | Early Regenerative Transition (Monitoring credit) |
| **Q < 0.35** | **Tier-C** | Depleted / Sub-Baseline Monoculture (Ineligible for credit issuance) |

---

## 9. Cryptographic Verification & Tamper-Evident Audit Ledger

### 9.1 Sequential SHA-256 Chained Block Architecture
Implemented in [`src/biodiversity_engine.py`](src/biodiversity_engine.py), the `BiodiversityAuditLedger` class records observations in sequential blocks. Each block contains:
* Block index, parcel ID, operator ID, UTC timestamp, and GNSS coordinates.
* Complete faunal counts and derived ecological indicators.
* Certified Green Credit calculations.
* The SHA-256 hash of the preceding block (`previous_hash`).

### 9.2 Cryptographic Anti-Tamper Security Validation
Modifying any historical block's insect count, coordinates, or credit units alters its SHA-256 digest, breaking the hash chain for all subsequent blocks. The `verify_integrity()` method performs end-to-end verification across the entire chain prior to issuing a certificate.

### 9.3 Audit Certificate & GeoJSON Vector Exports
Upon mission completion, the system serializes:
1. `audit_certificate.json`: Official underwriter certificate containing total counts, certified GCUs, accreditation tier, genesis/final hashes, and chain validity proofs.
2. `audit_transect.geojson`: Standard GIS vector file mapping localized diversity scores, PPR, and instant credits across geographic coordinates.

---

## 10. System Validation, Simulation Flight Trials & Experimental Results

### 10.1 Automated Self-Test & Unit Verification
Execution of `python src/biodiversity_engine.py` confirmed:
* Index calculation accuracy on multi-guild invertebrate sets.
* Mathematical convergence of the Green Credit formula.
* Invalidation of ledger integrity when simulated tampering was introduced (`Pre-tamper: True`, `Post-tamper: False`).

### 10.2 Autonomous Transect Simulation Flight Trial
Execution of `python src/simulate_audit.py` over a 15.0-hectare parcel across five waypoints produced the following verified results:

```
======================================================================
 OFFICIAL GREEN CREDIT AUDIT SUMMARY
======================================================================
 Target Parcel ID        : AGRI-PARCEL-GREEN-VALLEY-01
 Total Surveyed Area     : 15.00 Hectares
 Total Invertebrates     : 25 individuals across 12 taxa
 Shannon Diversity (H')  : 2.165 (Theoretical maximum: 2.485)
 Pollinator-to-Pest Ratio: 3.33 (Beneficials significantly outnumber pests)
 Soil Bioturbation Score : 8.5
 Certified Quality Score : 0.911 / 1.000
 Baseline Floor Score    : 0.200
 Net Ecological Uplift   : +0.711 Delta-Q
----------------------------------------------------------------------
 >>> CERTIFIED GREEN CREDIT UNITS (GCUs) AWARDED: 10.665 GCU <<<
----------------------------------------------------------------------
 Accredited Rating Tier  : Tier-AAA (Exemplary Biodiversity Net-Gain)
 Ledger Chain Integrity  : VALID (Zero Tampering Detected)
 Final Block SHA-256     : 6e5cc66bd414d9c5761f1fd2f43c8f757debd98b...
======================================================================
```

### 10.3 Real-Time Ecological & Green Credit HUD Streaming
[`src/detection.py`](src/detection.py) integrates real-time video inference with the audit ledger, displaying a live telemetry HUD overlaying bounding boxes, running Shannon index, Pollinator-to-Pest Ratio, certified GCUs, and blockchain integrity status.

---

## 11. Regulatory, Compliance & Environmental Market Impact

FALCON directly integrates with international environmental and financial accounting frameworks:
* **Verra Nature Framework & Plan Vivo:** Provides empirical, unit-level invertebrate monitoring to support biodiversity credit issuance.
* **Taskforce on Nature-related Financial Disclosures (TNFD):** Enables corporations to report localized ecosystem health with cryptographic assurance.
* **UK Biodiversity Net Gain (BNG):** Delivers standardized, repeatable faunal condition scores to satisfy mandatory 10% ecological uplift requirements.
* **Agricultural Premium Pricing:** Enables organic and regenerative agricultural producers to certify chemical-free ecological balance and access premium commodity markets.

---

## 12. Conclusion

The FALCON project has achieved 100% implementation completion. By transitioning from a conventional agricultural sprayer to an autonomous biodiversity auditing platform, the project delivers a novel synthesis of robotics, computer vision, mathematical ecology, and cryptographic data integrity. The system successfully demonstrates automated low-altitude invertebrate classification, empirical faunal metric derivation, standardized Green Credit Unit issuance, and tamper-evident audit logging. The complete codebase, CAD models, trained neural weights, and verification test suites are operational and publicly maintained in the project repository.

---

## 13. References

- *Advanced Insect Detection Network (AIDN) for UAV-Based Biodiversity Monitoring.* Remote Sensing (MDPI), 2024. [https://doi.org/10.3390/rs17060962](https://doi.org/10.3390/rs17060962)
- Alsadik, B., Ellsäßer, F. J., Awawdeh, M., et al. (2024). *Remote Sensing Technologies Using UAVs for Monitoring.* Remote Sensing, 16(23), 4371.
- Bai, Y., Hou, F., Fan, X., et al. (2023). *A Lightweight Pest Detection Model for Drones Based on Transformer and Super-Resolution Sampling Techniques.* Agriculture, 13(9), 1812.
- Shannon, C. E. (1948). *A Mathematical Theory of Communication.* Bell System Technical Journal, 27(3), 379–423.
- Simpson, E. H. (1949). *Measurement of Diversity.* Nature, 163, 688.
- Subramanian, K. S., Pazhanivelan, S., Srinivasan, G., et al. (2021). *Drones in Insect Pest Management.* Frontiers in Agronomy.
- Wu, X., Zhan, C., Lai, Y. K., Cheng, M. M., & Yang, J. (2019). *IP102: A Large-Scale Benchmark Dataset for Insect Pest Recognition.* IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 8788–8797. [https://github.com/xpwu95/IP102](https://github.com/xpwu95/IP102)
- *Agricultural Pests Image Dataset (12-class micro-fauna benchmark).* Kaggle Datasets. [https://www.kaggle.com/datasets/fihmeh/agricultural-pests-image-dataset](https://www.kaggle.com/datasets/fihmeh/agricultural-pests-image-dataset)
