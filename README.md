# ♻️ EcoLoop Bharat: LiveAI™ Circular Traceability Engine

**"Achieving Zero-Displacement Waste through Real-time Closed-Loop Tracking"**

[![Made with Pathway](https://img.shields.io/badge/Powered%20By-Pathway%20LiveAI-blue?style=for-the-badge&logo=python)](https://pathway.com/)
[![Hackathon](https://img.shields.io/badge/Hackathon-Hack%20For%20Green%20Bharat-green?style=for-the-badge)](https://pathway.com/hackathon)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

## 👥 Team: TechnoForge
**Institution:** East West Institute of Technology (EWIT), Bengaluru  
**Department:** Computer Science & Engineering (2nd Year)  

| Name | Role | Profile |
| :--- | :--- | :--- |
| **Shashank P** | Lead Developer | [GitHub](https://github.com/YOUR_GITHUB) |
| **Gagana CC** | System Architect / Data Logic | [GitHub](https://github.com/GAGANA_GITHUB) |

---
## 🌟 The Vision
India’s industrial waste management is currently a **"Linear Leak."** Once a product leaves the factory, it becomes invisible to the producer, eventually polluting Bharat’s soil and water. **EcoLoop Bharat** transforms this into a **Circular Economy**. 

Using **Pathway**, we create a real-time "Digital Twin" of every industrial product, ensuring it loops back from the consumer to the recycler, and finally back to the industry for zero-displacement waste.

## 🚀 Why Pathway? (The LiveAI™ Edge)
Standard databases are **retrospective**—they tell you what was dumped yesterday. **EcoLoop Bharat** is **proactive**. 

* **Rust-Powered Joins:** We perform sub-second streaming joins between Factory Production streams and Recycling Return streams.
* **Unified Logic:** We handle both historical batch data and high-speed live streams of waste collection in one Python-native framework.
* **Scalability:** Built to handle millions of "Recovery Events" across India's Tier-1 and Tier-2 cities simultaneously.



## 🏗️ Architecture
1.  **Data Ingestion:** Mock IoT streams simulate Factory Output (Production) and QR/Scanner logs (Recovery).
2.  **Pathway Processor:** The engine calculates the "Leakage Delta" (Production vs. Recovery) in real-time.
3.  **Anomaly Detection:** Products not returned within the threshold trigger **"Leakage Alerts."**
4.  **Live Dashboard:** A Streamlit UI providing situational awareness for industries and regulators.

## 📁 File Structure
```text
EcoLoop-Bharat/
├── data/                   # Simulation Layer
│   ├── mock_data_generator.py
│   └── live/               # Pathway Live Output Buffers
├── engine/                 # Logic Layer
│   ├── schema.py           # Product Digital Twin definitions
│   └── processor.py        # Core Pathway Streaming Joins
├── ui/                     # Presentation Layer
│   └── dashboard.py        # Streamlit Real-time UI
├── requirements.txt
└── run.sh                  # One-click Execution
