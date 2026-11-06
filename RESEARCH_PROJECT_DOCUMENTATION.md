# Research Project Documentation

**Project Working Title:**  
*Decarbonization and Resiliency Optimization of Mission-Critical AI Data Center Microgrids under Severe Grid Instability: A Techno-Economic Case Study in Lagos, Nigeria*

**Target Journals:**  
- *Applied Energy* (Elsevier, IF: ~11.2)
- *IEEE Transactions on Sustainable Energy* / *IEEE Access*
- *Energy Conversion and Management* (Elsevier, IF: ~10.4)

---

## 1. Executive Summary & Problem Statement

### 1.1 The Context: The West African Data Center Boom
Lagos, Nigeria is emerging as the digital hub of West Africa, hosting major subsea telecommunication cable landings (Google's *Equiano*, Meta's *2Africa*, MainOne, and WACS) and hyperscale colocation investments. Concurrently, generative AI workloads require high-density, continuously energized GPU clusters running 24/7.

### 1.2 The Dilemma: Severe Grid Instability vs. Mission-Critical Uptime
* **The Power Grid Reality:** The Nigerian national electricity grid experiences frequent system collapses, load shedding, and voltage instability. Industrial consumers face daily outages lasting anywhere from several hours to multiple consecutive days.
* **The Status Quo:** Modern data centers in Nigeria operate effectively as islanded microgrids powered by **captive diesel and natural gas reciprocating generators running 24/7**.
* **The Pain Points:**
  1. **Extreme Fuel OPEX & Volatility:** Following the deregulation of downstream petroleum products and removal of fuel subsidies, diesel costs have escalated dramatically.
  2. **Severe Carbon Footprint:** Burning diesel around the clock directly opposes global hyperscaler pledges to achieve net-zero and 24/7 Carbon-Free Energy (CFE).
  3. **Fuel Supply Chain Vulnerabilities:** Relying on continuous truck delivery of thousands of liters of diesel daily creates catastrophic single-point failure risks during supply disruptions.

### 1.3 The Core Research Question
> *How can an enterprise/AI data center in an unreliable grid environment transition from fossil-fuel captive generation to high-penetration renewable microgrids (Solar PV + Battery Storage + Fuel Cells) while maintaining Tier-IV reliability (99.999% uptime) at a competitive Levelized Cost of Energy (LCOE)?*

---

## 2. Research Goals & Specific Objectives

### Main Goal
Establish an optimal, cost-effective techno-economic pathway to decarbonize a 20 MW AI data center in a weak-grid African environment without sacrificing mission-critical uptime.

### Specific Objectives:
* **Objective 1: High-Fidelity Load & Tropical PUE Synthesis**  
  Synthesize an 8,760-hour electric load curve for a 20 MW peak AI facility combining dynamic GPU IT compute profiles (~15 MW IT: base inference + cyclical training bursts) with ambient-temperature-dependent Power Usage Effectiveness (PUE ~1.33, ~5 MW cooling/auxiliary overhead in Lagos's hot, humid tropical climate).
* **Objective 2: Establish the Fossil Baseline Benchmark (Status Quo)**  
  Model the current standard Nigerian operating architecture: grid connection with empirical outage frequency + 24/7 captive diesel/gas generation. Calculate the Baseline LCOE ($/MWh), Net Present Value (NPV), and annual CO₂ emissions.
* **Objective 3: 24/7 Carbon-Free Energy (CFE) Pareto Frontier**  
  Perform multi-objective techno-economic optimization in Xendee to determine optimal sizing for Solar PV, BESS, and Fuel Cells across clean energy penetration targets (0%, 50%, 80%, 95%, 99.9% CFE).
* **Objective 4: Resiliency & Islanded Outage Survival**  
  Simulate severe grid collapse events (24-hour, 72-hour, and 7-day continuous blackout) using Xendee's Outage and Resilience module to verify 100% critical load survival without relying solely on diesel.
* **Objective 5: Sensitivity & Policy Scenario Analysis**  
  Analyze the impact of fluctuating diesel/gas prices, BESS capital expenditure declines through 2030, and clean energy carbon credits.

---

## 3. Scenario Matrix for the Journal Paper

| Scenario ID | Name | Description | Research Purpose |
| :--- | :--- | :--- | :--- |
| **S0** | **Business-As-Usual (BAU)** | Unreliable Grid + 100% Diesel Generators | Establishes the real-world baseline cost & carbon in Nigeria |
| **S1** | **Economic Least-Cost** | Grid + Solar PV + BESS + Diesel | Identifies maximum ROI without mandatory clean targets |
| **S2** | **80% CFE Target** | Constrained minimum 80% clean hourly energy | Tests the sweet-spot decarbonization threshold |
| **S3** | **95%+ CFE Target** | High-penetration Solar + BESS + Fuel Cell | Quantifies the "last 10% clean energy cost premium" |
| **S4** | **Grid Collapse Resilience** | Utility severed for 72 hours continuously | Proves Tier-IV availability without relying solely on diesel |
