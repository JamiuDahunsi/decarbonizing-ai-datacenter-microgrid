# Spatial-Temporal Siting and Resiliency Optimization of Renewable Microgrids for AI Data Centers in Weak-Grid Environments: Decoupling Training and Inference across Nigeria

**Target Journal:** *Applied Energy* (Elsevier) / *IEEE Transactions on Sustainable Energy*

---

## Abstract

The exponential proliferation of generative artificial intelligence (AI) workloads has precipitated unprecedented electrical demand, with modern hyperscale facilities requiring continuous, multi-megawatt baseload power. In emerging digital hubs across Sub-Saharan Africa—such as Lagos, Nigeria—the co-location of international subsea cable landings with high-density AI infrastructure is severely hindered by chronic transmission grid instability, frequent nationwide system collapses, and post-subsidy fossil fuel inflation. Consequently, mission-critical facilities rely extensively on captive diesel generation running 24/7, incurring severe financial costs and carbon footprints that violate corporate net-zero pledges. 

This paper investigates the techno-economic feasibility, optimal asset sizing, and outage survivability of transitioning a 20 MW hyperscale AI data center from captive fossil generation to high-penetration solar-plus-storage microgrids under weak-grid constraints. Using a bottom-up physical methodology, an 8,760-hour facility load curve is synthesized by coupling empirical GPU compute traces (Google and Microsoft Azure distributions) with an ambient-temperature-dependent Power Usage Effectiveness (PUE) model following ASHRAE TC 9.9 tropical chiller standards. A Mixed-Integer Linear Programming (MILP) framework implemented in Xendee evaluates four operational architectures: (S1) Economic Least-Cost, (S2) 80% Carbon-Free Energy (CFE) Target, (S3) 95% CFE Target, and (S4) a 72-Hour System Blackout Stress Test under NERC Band A industrial tariffs ($0.15/kWh) and post-subsidy diesel rates ($1.30/L).

Results reveal that under pure economic optimization (S1), an unconstrained microgrid deploys 41.4 MW of Solar PV and 17.5 MW of modular diesel engines, achieving 38.0% carbon abatement and an 8-year payback without battery storage, as the nocturnal grid remains cheaper than storage capital costs. However, enforcing corporate clean energy mandates (S2: 80% CFE) unlocks a massive 183.6 MWh Battery Energy Storage System (BESS) and 95.9 MW of solar, slashing facility carbon emissions by 76.7%, eliminating operational diesel burn to zero, and reducing annual recurring electricity expenditures by 69.9% ($14.94M/yr saved). Pushing to near-complete decarbonization (S3: 95% CFE) reveals a sharp "green premium," requiring 253.1 MWh of BESS and 113.8 MW of PV to eliminate 89.8% of emissions, generating $17.54M/year in operational bill savings and $350.9M in 20-year cumulative cash preservation. Crucially, under a 72-hour national grid collapse (S4), the solar-storage microgrid guarantees 100% critical load survival (Loss of Load Probability = 0%) while reducing the required backup generator fleet by 71.4% (from 17.5 MW down to 5.0 MW). These findings provide the first empirical roadmap for powering gigawatt-era AI compute across weak grids in the Global South.

**Keywords:** Artificial Intelligence Data Centers; 24/7 Carbon-Free Energy (CFE); Microgrid Optimization; Battery Energy Storage Systems; Weak-Grid Resilience; Sub-Saharan Africa.

---

## 1. Introduction

The global computing landscape is undergoing a structural paradigm shift driven by generative artificial intelligence (AI), large language models (LLMs), and high-density accelerator architectures (e.g., NVIDIA H100 and Blackwell B200 GPUs). Unlike conventional cloud infrastructure characterized by elastic, CPU-dominated diurnal workloads, AI data center campuses require continuous, dense, and non-preemptible power blocks ranging from tens to hundreds of megawatts.

Concurrently, Sub-Saharan Africa is experiencing a digital infrastructure boom. Lagos, Nigeria has emerged as the premier telecommunications gateway for West Africa, hosting the landing stations for high-capacity subsea fiber optic cables, including Google’s *Equiano* and Meta’s *2Africa*. Hyperscale colocation operators (e.g., Equinix/MainOne, Rack Centre, Airtel/Nxtra, and Kasi Cloud) have initiated multi-megawatt campus expansions to capture localized inference, financial technology, and sovereign cloud demands.

However, deploying gigawatt-era compute in Nigeria faces a fundamental paradox:
1. **Severe Grid Instability & Structural Deficit:** The Nigerian national transmission network suffers from chronic supply deficits, high Aggregate Technical, Commercial, and Collection (ATC&C) losses (~50%), and recurring nationwide system collapses, resulting in industrial grid availability frequently falling below 50% (World Bank, 2020). Nationwide economic losses stemming from unserved energy are estimated at US$25 billion annually, representing 5% to 7% of national GDP (World Bank, 2020).
2. **The Captive Diesel Trap:** To maintain Tier-III and Tier-IV mission-critical availability standards (99.982% to 99.999% uptime), data center operators function essentially as islanded microgrids relying on captive reciprocating diesel and gas generators. Nationally, over 22 million captive generators operate across Nigeria, possessing an aggregate net capacity estimated at eight times the total operational capacity of the national transmission grid (World Bank, 2020).
3. **Severe Economic & Carbon Penalties:** Following downstream petroleum deregulation and the removal of federal fuel subsidies, diesel prices reached approximately ₦1,750–₦1,850/L ($1.30/L). Consequently, commercial and industrial enterprises incur effective generation costs between US$0.40/kWh and US$0.46/kWh—nearly triple the cost-reflective utility tariff of US$0.14–$0.15/kWh (World Bank, 2020). Burning tens of thousands of liters of fossil fuel daily generates millions of dollars in recurring operating expenses (OpEx) and heavy Scope 1 emissions that directly violate global hyperscaler pledges to achieve 24/7 Carbon-Free Energy (CFE) by 2030.

While existing literature has extensively examined data center microgrids and 24/7 CFE in North America (PJM, ERCOT) and Western Europe, the prevailing body of research uniformly assumes a highly reliable, interconnected transmission grid with 99.9%+ availability, where microgrids function primarily as financial arbitrage or green-tariff tools. Virtually no peer-reviewed studies have investigated the techno-economic trade-offs, battery sizing dynamics, and extreme multi-day blackout survivability of mission-critical AI facilities operating under weak, intermittent grid conditions in the Global South.

This study directly addresses this research gap. The core contributions are:
1. **High-Fidelity Workload & Tropical PUE Synthesis:** Developing an 8,760-hour empirical demand profile coupling GPU compute trace dynamics with ASHRAE TC 9.9 tropical chiller thermodynamic curves.
2. **Empirical Techno-Economic Frontier:** Sizing Solar PV, BESS, and captive generation across four distinct architectural scenarios in Lagos using Mixed-Integer Linear Programming.
3. **Resilience & Generator Fleet Abatement:** Demonstrating that solar-plus-storage microgrids reduce backup fossil engine requirements by over 71% while surviving a 72-hour continuous grid blackout with zero loss of load.

---

## 2. Methodology & Mathematical Formulation

### 2.1 20 MW Facility Load & Tropical Cooling Model
The total electrical demand $P_{\text{total}}(t)$ at each hour $t \in [1, 8760]$ is defined by:

$$P_{\text{total}}(t) = P_{\text{IT}}(t) \times \text{PUE}(t)$$

#### 2.1.1 Computational Workload Layer ($P_{\text{IT}}$)
Calibrated against Google cluster workload traces (Reiss et al., 2012) and Microsoft Azure VM traces (Cortez et al., 2017), computational power combines base inference, diurnal consumer activity, and stochastic multi-day deep learning pre-training epochs (Weng et al., 2022):

$$P_{\text{IT}}(t) = \left[ P_{\text{base}} + P_{\text{diurnal}}(t) \right] \cdot W_{\text{day}}(t) + P_{\text{training}}(t) + \epsilon(t)$$

Where $P_{\text{base}} = 11.5\text{ MW}$, $P_{\text{diurnal}}(t)$ accounts for diurnal variations in West African Time ($\pm 1.2\text{ MW}$), $W_{\text{day}}(t) \in [0.92, 1.0]$ dampens weekend traffic, and $P_{\text{training}}(t) = +2.5\text{ MW}$ models stochastic 72-to-168 hour foundation model training bursts, clamped to a nameplate IT ceiling of $15.0\text{ MW}$.

#### 2.1.2 Temperature-Dependent Cooling Overhead ($\text{PUE}$)
Under ASHRAE TC 9.9 tropical data center standards, chiller coefficient of performance (COP) degrades with ambient dry-bulb temperature $T_{\text{amb}}(t)$:

$$\text{PUE}(t) = \text{PUE}_{\text{base}} + \alpha \cdot \left( T_{\text{amb}}(t) - T_{\text{ref}} \right)$$

With $\text{PUE}_{\text{base}} = 1.22$, $\alpha = 0.0085\text{ /}^\circ\text{C}$, and $T_{\text{ref}} = 22.0^\circ\text{C}$. PUE fluctuates between $1.22$ and $1.38$ (annual mean = $1.31$), yielding a normalized annual peak facility demand of exactly $20,000.0\text{ kW}$ ($20.0\text{ MW}$) and annual consumption of $141.87\text{ GWh}$.

### 2.2 Mathematical Optimization Framework (MILP)
The microgrid dispatch and investment problem is formulated as a Mixed-Integer Linear Program minimizing the 20-year Net Present Cost ($\text{NPC}$):

$$\min \quad \text{NPC} = \text{CapEx}_{\text{total}} + \sum_{y=1}^{N} \frac{\text{OpEx}(y)}{(1 + r)^y}$$

Subject to the hourly power balance:
$$P_{\text{grid}}(t) + P_{\text{PV}}(t) + P_{\text{BESS,dis}}(t) + P_{\text{gen}}(t) - P_{\text{BESS,ch}}(t) = P_{\text{total}}(t) \quad \forall t$$

Battery state-of-charge dynamics:
$$\text{SoC}(t) = \text{SoC}(t-1) \cdot (1 - \sigma) + \left[ P_{\text{BESS,ch}}(t) \cdot \eta_{\text{ch}} - \frac{P_{\text{BESS,dis}}(t)}{\eta_{\text{dis}}} \right] \frac{\Delta t}{E_{\text{BESS}}}$$
$$0.10 \le \text{SoC}(t) \le 0.90$$

And the resilience constraint during grid collapse windows:
$$P_{\text{grid}}(t) = 0, \quad P_{\text{PV}}(t) + P_{\text{BESS,dis}}(t) + P_{\text{gen}}(t) \ge P_{\text{total}}(t) \quad (\text{LOLP} = 0)$$

---

## 3. Techno-Economic Results & Discussion

### 3.1 Comparative Performance Summary

| Metric | Baseline | Scenario S1 (Least-Cost) | Scenario S2 (80% CFE) | Scenario S3 (95% CFE) | Scenario S4 (72h Blackout) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Solar PV Installed (kW)** | $0$ | $41,444$ | $95,865$ | $113,845$ | $97,256$ |
| **BESS Capacity (kWh)** | $0$ | $0$ | $183,645$ | $253,105$ | $180,910$ |
| **Genset Capacity (kW)** | $20,000$ | $17,500$ | $0$ (New) | $0$ (New) | $5,000$ |
| **Total Initial CapEx ($M)** | $\$0$ | $\$47.96$ | $\$142.85$ | $\$179.97$ | $\$146.08$ |
| **Annual OpEx ($M/yr)** | $\$21.37$ | $\$14.68$ | $\$6.43$ | $\$3.83$ | $\$6.57$ |
| **OpEx Savings vs Base (%)** | $0.0\%$ | $31.33\%$ | $69.92\%$ | $82.09\%$ | $69.25\%$ |
| **Annual CO2 Emissions (t)** | $73,451$ | $45,544$ | $17,089$ | $7,475$ | $17,180$ |
| **CO2 Reduction (%)** | $0.0\%$ | $37.99\%$ | $76.73\%$ | $89.82\%$ | $76.61\%$ |
| **Levelized Cost ($/kWh)** | $\$0.1500$ | $\$0.1412$ | $\$0.1693$ | $\$0.1860$ | $\$0.1734$ |
| **Payback Period (Years)** | — | $8$ | $13$ | $14$ | $13$ |
| **Outage Ride-Through** | Fails / Dirty | $24\text{ Hours}$ | $24\text{ Hours}$ | $24\text{ Hours}$ | $72\text{ Hours}$ |

### 3.2 Key Analytical Insights

#### 1. Economic Omission of Storage in Unconstrained Dispatch (S1)
Under pure least-cost optimization (S1), Solar PV is deployed aggressively ($41.4\text{ MW}$), reducing annual OpEx by $31.33\%$ and abating $38.0\%$ of emissions. However, battery storage is entirely omitted ($0\text{ kWh}$). Because nocturnal grid tariffs ($0.15\text{ \$/kWh}$) remain below the levelized amortized storage cost, the solver prioritizes grid imports at night and relies on diesel gensets strictly for emergency outage ride-through.

#### 2. The Storage Threshold and the 80% CFE Inflection (S2)
Enforcing an 80% clean energy threshold fundamentally alters system economics. BESS transitions from an economically non-viable asset to a mandatory baseload enabler ($183.6\text{ MWh}$). Remarkably, captive diesel operation drops to **$0\text{ kWh}$**, slashing carbon emissions by $76.73\%$ and liberating **$\$14.94\text{ Million in operational cash savings annually}$**, achieving project payback within 13 years.

#### 3. The "Last-Mile" Green Premium (S3)
Pushing clean energy penetration from 80% to 95% incurs a steep marginal capital penalty. An additional $69.5\text{ MWh}$ of battery storage ($+37.8\%$) and $18.0\text{ MW}$ of PV are required to eliminate intermittent weather shortfalls, shifting LCOE from $\$0.1693$ to $\$0.1860\text{ /kWh}$. Nonetheless, S3 achieves an extraordinary **$89.82\%$ carbon abatement**, demonstrating that near-complete data center decarbonization is technically viable in tropical developing economies.

#### 4. Generator Fleet Abatement under Extended Blackouts (S4)
Under a severe 72-hour system collapse, the presence of the $180.9\text{ MWh}$ battery bank and $97.3\text{ MW}$ solar farm allows the data center to operate autonomously through three diurnal cycles. Consequently, the required diesel generation capacity is slashed from **$17.5\text{ MW}$ down to just $5.0\text{ MW}$ (a $71.4\%$ physical asset reduction)**, proving that renewable microgrids dramatically mitigate fuel logistics risks and capital lock-in for critical infrastructure.

---

## 4. Policy & Industry Recommendations

1. **Regulatory Tariff Reform (NERC):** Implementation of time-of-use (TOU) and clean energy wheeling tariffs would allow enterprise microgrids to monetize surplus daytime solar generation ($>15\text{ MW}$ curtailed during afternoon peaks in S2/S3).
2. **Duty Exemptions on High-Capacity BESS:** Customs duties and import tariffs on utility-scale lithium-ion battery containers represent a primary barrier to reaching the 80% CFE threshold.
3. **Decoupled AI Siting Strategy:** While inference workloads must remain co-located in Lagos adjacent to subsea cable landing stations, delay-tolerant foundation model training clusters should be geographically decoupled and sited in Northern Nigeria (e.g., Kano/Kaduna), where solar GHI is 35% higher and industrial land costs are 80% lower.

---

## 5. Conclusion

This study presented the first rigorous techno-economic and resiliency optimization of an AI data center microgrid operating under severe grid instability in Sub-Saharan Africa. Through synthesized 8,760-hour computational and thermal load modeling and MILP optimization, we proved that:
* Solar PV without storage is economically superior to grid-only operation in Nigeria, saving 31.3% in operational costs with an 8-year payback.
* Achieving 80% 24/7 Carbon-Free Energy requires 183.6 MWh of storage, completely eliminating captive diesel operation and slashing carbon emissions by 76.7%.
* The microgrid provides full survivability across a 72-hour nationwide grid collapse while reducing the backup generator fleet by over 71%.

These findings demonstrate that clean renewable microgrids provide both an economic shield against fossil fuel volatility and the ultimate resiliency architecture for the African digital economy.

---

## Declaration of Competing Interest
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Declaration of Generative AI and AI-Assisted Technologies in the Writing Process
During the preparation of this work, the author utilized AI-assisted tools to support manuscript language polishing, drafting organization, and LaTeX script verification. All simulation formulations, microgrid dispatch models, empirical data audits, and scientific interpretations were developed, independently verified, and validated by the author. Following the use of these tools, the author thoroughly reviewed, edited, and verified the content and takes full responsibility for the integrity and accuracy of the publication.

## Data Availability Statement
The synthesized 8,760-hour AI workload profile, dynamic tropical PUE curves, and complete Xendee simulation output datasets are openly accessible via the project repository.

## References

1. **World Bank (2020).** *Technical Note 2: Igniting Economic Growth by Reforming Nigeria's Power Sector*. World Bank Group, Report No. P176224. [Direct Link](https://documents1.worldbank.org/curated/en/099061723133022449/pdf/P1762240038c17010bfb5087a5bcc325b5.pdf)
2. **Xu, Q., Ding, Y., & Chien, A. A. (2024).** Quantifying the economic and carbon impacts of 24/7 carbon-free energy matching for hyperscale clouds. *Applied Energy*, 356, 122340. https://doi.org/10.1016/j.apenergy.2023.122340
3. **Lian, Y., Li, Y., Zhao, Y., Yu, C., Zhao, T., & Wu, L. (2023).** Robust multi-objective optimization for islanded data center microgrid operations. *Applied Energy*, 330, 120344. https://doi.org/10.1016/j.apenergy.2022.120344
4. **Reiss, C., Wilkes, J., & Hellerstein, J. L. (2012).** Heterogeneity and dynamicity of clouds at scale: Google trace analysis. In *Proceedings of the Third ACM Symposium on Cloud Computing* (SoCC '12), 1-14. https://doi.org/10.1145/2391229.2391236
5. **Cortez, E., Bonde, A., Muzio, A., Russinovich, M., Fontoura, M., & Bianchini, R. (2017).** Resource central: Understanding and predicting workload states for machine learning in the cloud. In *Proceedings of the 26th Symposium on Operating Systems Principles* (SOSP '17), 153-167. https://doi.org/10.1145/3132747.3132772
6. **Weng, Q., Xiao, W., Yu, Y., Wang, W., Wang, C., He, J., ... & Lin, C. (2022).** MLaaS in the wild: Workload analysis and scheduling in large-scale heterogeneous GPU clusters. In *19th USENIX Symposium on Networked Systems Design and Implementation* (NSDI '22), 945-960.
7. **Yu, L., Jiang, T., & Zou, Y. (2021).** Energy, exergy and computing efficiency based data center workload and cooling management. *Applied Energy*, 299, 117050. https://doi.org/10.1016/j.apenergy.2021.117050
8. **Koot, M., & Wijnhoven, F. (2021).** Usage impact on data center electricity needs: A system dynamic forecasting model. *Applied Energy*, 291, 116798. https://doi.org/10.1016/j.apenergy.2021.116798
9. **Sun, B., Chen, K., Teng, F., & Kang, C. (2021).** Operational flexibility of active distribution networks with the potential from data centers. *Applied Energy*, 293, 116935. https://doi.org/10.1016/j.apenergy.2021.116935
10. **Liu, Y., Lu, C., et al. (2022).** A mission-driven two-step virtual machine commitment for energy saving of modern data centers through UPS and server coordinated optimizations. *Applied Energy*, 322, 119467. https://doi.org/10.1016/j.apenergy.2022.119467

