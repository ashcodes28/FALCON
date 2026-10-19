# Project Memory: FALCON (Autonomous Aerial Biodiversity Auditing System)

## Core Facts & Baseline
- Project directory: `FALCON/`
- Current state: ~50% implementation completed; transitioned from pest surveillance to biodiversity and nature-credit auditing.
- Hardware & CAD: Hexacopter/quadcopter airframe, camera gimbal, and compute payload bay CAD models completed (`CAD Images/`).
- Machine Learning Baseline: YOLOv11n and YOLOv8 trained at 1024x1024 resolution on a 12-class insect/fauna dataset (`YOLOv11n - Model Weights/best.pt`).
- Functional Guilds:
  - Pollinators: Bees (1)
  - Biocontrol Predators: Wasps (10)
  - Soil & Detrital Fauna: Earthworms (4), Slugs (8), Snails (9)
  - Herbivores / Pest Pressures: Caterpillars (3), Grasshoppers (6), Weevils (11), Beetles (2), Earwigs (5), Ants (0), Moths (7)
- Detection Performance: 85.5% baseline accuracy; high precision on snails, weevils, moths, wasps, and ants; confusion identified around beetles, caterpillars, earwigs, and earthworms.
- Implemented Auditing Core (`src/biodiversity_engine.py`):
  - Shannon-Wiener Faunal Diversity Index ($H'$)
  - Simpson's Diversity Index ($1 - D$)
  - Pollinator-to-Pest Ratio (PPR)
  - Soil Bioturbation Proxy Score
  - Cryptographically chained (SHA-256) audit logs with tamper detection
  - GeoJSON feature collection exporter and summary audit certificate generator
- Live Detection Integration (`src/detection.py`):
  - Real-time video inference with live on-screen Ecological HUD (Shannon H', PPR, Soil Score, Chain Validity) and automatic export of `audit_certificate.json` and `audit_transect.geojson`.
