# UAV-Assisted Agricultural Pest Surveillance

UAV-Assisted Agricultural Pest Surveillance is a deep learning-powered system for detecting and monitoring crop pests using aerial imagery captured by drones. Leveraging YOLO-based object detection, it enables day and night pest surveillance to support precision agriculture and reduce crop losses.

## 📊 Project Overview & Progress

> **Completion Status:** ~50% Complete  
> **Repository:** [ashcodes28/FALCON](https://github.com/ashcodes28/FALCON)

This project integrates deep learning detection models with custom UAV hardware design to automate field scouting.

* **Baseline Detectors:** Evaluated single-modality YOLOv8 (85.5% accuracy) and lightweight YOLOv11n for edge deployment.
* **System Design:** Completed CAD modeling for the UAV airframe, camera gimbal, and compute payload bay.
* **In Progress:** Addressing confusion-class error trends through targeted data augmentation, class re-balancing, and super-resolution pre-processing.

---

## 📚 Documentation

🔗 [Literature Review & Patent Survey](https://github.com/ashcodes28/FALCON/blob/main/Literature%20Review%20%26%20Patent%20Survey.md)

📄 [License](https://github.com/ashcodes28/FALCON/blob/main/LICENSE)

---

## 📖 Reference Research Papers

- [A Lightweight Pest Detection Model for Drones Based on Transformer and Super-Resolution Sampling Techniques](https://www.mdpi.com/2077-0472/13/9/1812)
- [Advanced Insect Detection Network (AIDN) for UAV-Based Biodiversity Monitoring](https://www.mdpi.com/2072-4292/17/6/962)
- [Remote Sensing Technologies Using UAVs for Pest and Disease Monitoring](https://www.mdpi.com/2072-4292/16/23/4371)
- [Drones in Insect Pest Management](https://www.frontiersin.org/articles/10.3389/fagro.2021.640885/full)
- [A Framework for Agricultural Pest and Disease Monitoring Based on IoT and UAVs](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7085563/)
- [Artificial Intelligence Driven Drone Observation and Pest Control in Banana Crop](https://doi.org/10.71146/kjmr197)
- [Design and Development of Agricultural Drone for Precision Fertilizer Application](https://doi.org/10.1016/j.rineng.2025.106267)
- [Reducing Energy and Environmental Footprint in Agriculture: Drone Spraying vs. Conventional Methods](https://doi.org/10.1371/journal.pone.0323779)

---

## 🏛️ Reference Patents

- [US 2017/0231213 A1 - Pest Abatement Utilizing an Aerial Drone](https://patents.google.com/patent/US20170231213A1/en)
- [US 2017/0089761 A1 - Spectral Imaging System for Remote and Noninvasive Detection](https://patents.google.com/patent/US20170089761A1/en)
- [US 2022/0211026 A1 - System and Method for Field Treatment and Monitoring](https://patents.google.com/patent/US20220211026A1/en)
- [US 10,364,029 B2 - Drone for Agriculture](https://patents.google.com/patent/US10364029B2)
- [US 11,147,257 B2 - Autonomous Agricultural System with Pest Detection](https://patents.google.com/patent/US11147257B2/en)
- [WO 2021/196062 A1 - Agricultural Drone System for Pest Control](https://patents.google.com/patent/WO2021196062A1/en)
- [JP 3217561 U - Pest Control Drone Utility Model](https://patents.google.com/patent/JP3217561U/en)
- [KR 20230062713 A - Smart Pest Control Drone System](https://patents.google.com/patent/KR20230062713A/en)

---

## 🔬 Detector Baseline & Performance

Evaluation was conducted using both **YOLOv8** and **YOLOv11n** baseline models. Overall classification accuracy reached **85.5%** on the annotated dataset.

### High Accuracy Classes:
- **Snail** (1.00), **Weevil** (1.00), **Moth** (0.99), **Wasp** (0.97), and **Ants** (0.87) are classified with high precision.

### Confusion Trends & Limitations:
- **Beetle**, **Caterpillar**, and **Earwig** show noticeable misclassifications due to small object boundaries and texture similarities.
- Cross-class confusion is observed between Beetles ↔ Wasps, Caterpillars ↔ Bees/Beetles, and Slugs ↔ Earthworms.

---

## 🛠️ System Roadmap & Remaining Work

- [x] Literature review and patent landscape mapping
- [x] Dataset curation & annotation
- [x] Baseline YOLOv8 & YOLOv11n evaluation
- [x] UAV frame & payload bay CAD design
- [ ] Confusion-class data augmentation & re-balancing *(In Progress)*
- [ ] Selective ResNet super-resolution module for low-confidence regions
- [ ] Multimodal RGB + Thermal attention fusion pipeline
- [ ] Onboard edge deployment & flight controller integration
- [ ] Field trials and performance validation
