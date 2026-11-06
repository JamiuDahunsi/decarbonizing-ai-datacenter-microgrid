import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def build_docx():
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_after = Pt(4)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(8)
    run_title = p_title.add_run("Decarbonizing AI Data Centers in Weak-Grid Environments: Techno-Economic Sizing, 24/7 Carbon-Free Energy Matching, and Multi-Day Blackout Resiliency")
    run_title.font.name = 'Times New Roman'
    run_title.font.size = Pt(16)
    run_title.bold = True

    # Authors
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_after = Pt(2)
    r_auth = p_auth.add_run("Jamiu Dahunsi*\n")
    r_auth.bold = True
    r_auth.font.size = Pt(12)
    
    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aff.paragraph_format.space_after = Pt(12)
    r_aff = p_aff.add_run("Department of Electrical and Computer Engineering, Carnegie Mellon University, Pittsburgh, PA 15213, USA\n*Corresponding Author: jdahunsi@andrew.cmu.edu")
    r_aff.font.size = Pt(10)
    r_aff.italic = True

    # Abstract Box
    p_ab_h = doc.add_paragraph()
    r_ab_h = p_ab_h.add_run("ABSTRACT")
    r_ab_h.bold = True
    r_ab_h.font.size = Pt(11)

    abstract_text = (
        "High-density artificial intelligence (AI) workloads require continuous, multi-megawatt electrical power. "
        "In regional digital hubs in developing economies, such as Lagos, Nigeria, data centers are located near "
        "subsea fiber landings to minimize network latency. However, these facilities face frequent grid failures, "
        "high transmission losses, and volatile diesel fuel prices. As a result, operators rely on on-site diesel generators "
        "running 24 hours a day, which raises electricity costs to $0.40–$0.46/kWh and increases operational carbon emissions.\n\n"
        "This study presents a techno-economic capacity sizing and outage survivability analysis for a 20 MW AI data center "
        "operating on an intermittent grid. We synthesize an 8,760-hour annual load profile by combining empirical GPU compute traces "
        "from Google Borg and Microsoft Azure clusters with an ambient-temperature-dependent Power Usage Effectiveness (PUE) model "
        "based on ASHRAE TC 9.9 standards. Using Mixed-Integer Linear Programming (MILP) in Xendee, we examine four operational configurations: "
        "(S1) Economic Least-Cost, (S2) 80% Carbon-Free Energy (CFE) Target, (S3) 95% CFE Target, and (S4) a 72-Hour Continuous Blackout Stress Test. "
        "Local utility tariffs ($0.15/kWh) and post-subsidy commercial diesel fuel costs ($1.30/L) are used for all evaluations.\n\n"
        "In the least-cost case (S1), the system deploys 41.4 MW of Solar PV and 17.5 MW of diesel generation, cutting operating expenses "
        "by 31.3% with an 8-year payback. Battery storage is not selected in S1 because off-peak nighttime grid electricity remains cheaper "
        "than the amortized capital cost of storage. Enforcing an 80% annual CFE target (S2) requires 183.6 MWh of battery energy storage (BESS) "
        "and 95.9 MW of solar. This configuration eliminates standard diesel dispatch, reduces annual operating costs by 69.9% ($14.94M saved per year), "
        "lowers emissions by 76.7%, and achieves a levelized cost of energy (LCOE) of $0.1693/kWh with a 13-year payback. Raising the target to "
        "95% CFE (S3) requires 253.1 MWh of storage and 113.8 MW of solar, reflecting a steep cost curve for marginal carbon reductions. "
        "During a 72-hour grid blackout (S4), the solar-storage microgrid maintains continuous operation with zero loss of load while reducing "
        "required backup diesel generator capacity by 71.4% (from 17.5 MW to 5.0 MW). These results show that solar-plus-storage systems provide "
        "both economic savings and operational resilience for mission-critical computing on weak electrical grids."
    )
    p_ab = doc.add_paragraph(abstract_text)
    p_ab.paragraph_format.left_indent = Inches(0.25)
    p_ab.paragraph_format.right_indent = Inches(0.25)

    p_kw = doc.add_paragraph()
    r_kwh = p_kw.add_run("Keywords: ")
    r_kwh.bold = True
    p_kw.add_run("Artificial Intelligence Data Centers; Carbon-Free Energy (CFE); Microgrid Sizing; Battery Energy Storage; Weak-Grid Reliability; Diesel Displacement.")
    p_kw.paragraph_format.left_indent = Inches(0.25)
    p_kw.paragraph_format.space_after = Pt(14)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(13)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(11.5)
        return p

    # --- SECTION 1 ---
    add_h1("1. Introduction")
    doc.add_paragraph(
        "Hardware accelerators for deep neural network training and inference, such as NVIDIA H100 and Blackwell GPUs, "
        "draw substantially higher power per rack (40 to 100 kW/rack) than conventional central processing unit (CPU) servers "
        "(5 to 10 kW/rack) (Wu et al., 2022; Faiz et al., 2024). Consequently, modern AI data center campuses require "
        "continuous, non-preemptible power blocks ranging from tens to hundreds of megawatts (Al-Turjman et al., 2024; Narayanan et al., 2021).\n\n"
        "At the same time, regional digital markets in Sub-Saharan Africa are expanding (Mbate, 2024). Lagos, Nigeria, serves as the main "
        "telecommunications landing hub for high-capacity subsea fiber optic cables in West Africa, including Google's Equiano and "
        "Meta's 2Africa systems. Hyperscale operators, including Equinix, Rack Centre, and Airtel, are constructing commercial "
        "multi-megawatt facilities in this corridor to serve local banking, cloud, and edge inference applications."
    )
    doc.add_paragraph(
        "However, operating high-density data centers in Nigeria introduces severe power supply challenges:\n\n"
        "1. Frequent Grid Failures: The Nigerian 330/132 kV transmission network experiences recurring total system collapses, "
        "supply deficits, and localized line congestion (Arowolo et al., 2022). The World Bank reports that aggregate technical, "
        "commercial, and collection (ATC&C) losses across distribution companies reach nearly 50%, and power shortages cause an "
        "estimated annual economic loss of $25 billion, or 5% to 7% of gross domestic product (World Bank, 2020). Large industrial "
        "customers often receive power for fewer than 12 to 16 hours per day.\n\n"
        "2. High Dependence on Captive Diesel Generation: To maintain Tier-III and Tier-IV reliability standards (99.982% to 99.999% "
        "availability), data centers cannot depend on the central grid as their sole supply. Instead, they operate continuous captive diesel "
        "and natural gas reciprocating engines on site. Nationally, over 22 million captive generators operate in Nigeria, with an aggregate "
        "installed capacity roughly eight times larger than the operational capacity of the national transmission grid (World Bank, 2020; Oseni, 2012).\n\n"
        "3. Rising Fuel Costs and Operational Expenses: Following national petroleum subsidy removal in 2023, industrial diesel fuel "
        "prices reached approximately ₦1,750 to ₦1,850 per liter ($1.30/L). Industrial self-generation using diesel costs between $0.40/kWh "
        "and $0.46/kWh (World Bank, 2020), compared to the regulated utility tariff of $0.15/kWh (NERC Band A) (NERC, 2024). Operating "
        "generator fleets continuously generates high recurring operating expenses and carbon emissions that conflict with corporate "
        "sustainability commitments (Xu et al., 2024)."
    )
    doc.add_paragraph(
        "To lower fuel expenditures and emissions, operators are evaluating on-site solar photovoltaics (PV) and battery energy storage "
        "systems (BESS). However, most existing research on data center microgrids and 24/7 carbon-free energy matching evaluates facilities "
        "in North America or Western Europe (Bistline et al., 2023; Riepin & Brown, 2022). These studies assume a highly reliable central "
        "grid (over 99.9% availability), treating microgrids primarily as tools for wholesale price arbitrage or green certificate procurement "
        "(Radovanovic et al., 2022). In contrast, microgrid studies in developing nations typically focus on rural minigrids or small commercial "
        "loads (10 to 500 kW) with flexible, non-critical consumption patterns (Babatunde et al., 2020).\n\n"
        "While recent work has evaluated storage options for remote computing (Hong & Choi, 2024) and transmission integration constraints "
        "(Chen et al., 2024), few studies have analyzed the capacity sizing, hourly dispatch, and multi-day blackout survivability of "
        "multi-megawatt AI data centers connected to weak utility grids in tropical climates. This paper addresses this gap."
    )

    # --- SECTION 2 ---
    add_h1("2. Methodology and Mathematical Formulation")
    doc.add_paragraph(
        "This section details the analytical framework and mathematical optimization models developed to size the microgrid assets and "
        "evaluate their operational dispatch. The formulation comprises five components: (i) bottom-up synthesis of the AI computational "
        "workload and dynamic tropical cooling load; (ii) behind-the-meter AC microgrid topology and hourly power balance; (iii) physical "
        "asset characterization for solar PV, lithium-ion BESS, and reciprocating diesel generators; (iv) Mixed-Integer Linear Programming "
        "(MILP) multi-scenario optimization formulation; and (v) computational solver parameters and convergence criteria."
    )
    
    add_h2("2.1 AI Workload and Dynamic Tropical Cooling Synthesis")
    doc.add_paragraph(
        "Modern data center electrical demand is the product of computing hardware power draw and facility cooling overhead. Total facility "
        "electrical demand P_total(t) at hourly timestep t in {1, 2, ..., 8760} is governed by:\n\n"
        "    P_total(t) = P_IT(t) * PUE(t)\n\n"
        "where P_IT(t) is the electrical power drawn by the computing racks (MW), and PUE(t) is the ambient-temperature-dependent Power Usage "
        "Effectiveness of the facility."
    )
    doc.add_paragraph(
        "The IT computing block is rated at a nameplate capacity of P_nameplate = 15.0 MW. This corresponds to a high-density deployment of "
        "approximately 200 to 375 server racks operating at 40 to 75 kW per rack, representative of modern NVIDIA DGX H100, H200, and "
        "Blackwell accelerator clusters (Wu et al., 2022; Faiz et al., 2024). Calibrated against longitudinal server utilization traces from "
        "Google's Borg cluster management system (Reiss et al., 2012) and Microsoft Azure machine learning cloud instances (Cortez et al., 2017), "
        "the computing load is modeled as:\n\n"
        "    P_IT(t) = min{ P_nameplate, [P_base + P_diurnal(t)] * W_day(t) + P_train(t) + e(t) }\n\n"
        "where P_base = 11.5 MW represents the continuous baseload power consumed by idle accelerators, host CPUs, high-speed network switches "
        "(InfiniBand/NVLink), and storage fabrics. Diurnal user inference requests fluctuate with business hours across West Africa (A_diurnal = 1.2 MW), "
        "weekend damping reduces volume by 8% (W_day = 0.92), and distributed foundation model training jobs P_train(t) = +2.5 MW run "
        "non-preemptibly for 72 to 168 hours every 14 to 21 days (Weng et al., 2022; Narayanan et al., 2021)."
    )
    doc.add_paragraph(
        "Data center thermal management adheres to ASHRAE Technical Committee 9.9 (TC 9.9) environmental guidelines for Class A1 processing "
        "facilities (ASHRAE, 2021). In coastal equatorial climates such as Lagos (6.6197 deg N, 3.3663 deg E), ambient temperatures range "
        "from 21.8 deg C to 36.4 deg C with high relative humidity (80% to 95%). Under these conditions, the ambient wet-bulb temperature "
        "continuously exceeds the allowable chilled water return threshold, preventing the operation of direct or indirect evaporative air "
        "economizers ('free cooling') (Yu et al., 2021). Consequently, heat rejection requires the continuous operation of water-cooled "
        "centrifugal chillers and cooling towers:\n\n"
        "    PUE(t) = PUE_base + alpha_chiller * max(0, T_amb(t) - T_ref)\n\n"
        "where PUE_base = 1.22 below T_ref = 22.0 deg C, and alpha_chiller = 0.0085 / deg C is the marginal thermal lift coefficient. "
        "Using NASA Typical Meteorological Year (TMY) dry-bulb temperature data, facility PUE(t) ranges from 1.220 to 1.342 (annual average: 1.293). "
        "Total campus electrical demand reaches an absolute peak of 20,000.00 kW (20.00 MW), a minimum of 12,235.88 kW (12.24 MW), an annual "
        "mean of 16,194.81 kW (16.19 MW), and an annual aggregate electricity consumption of 141,866,504 kWh (141.87 GWh)."
    )

    # Figure 1
    fig1_path = r"C:\Users\jamiu\OneDrive\Desktop\Energy AI Data Center\Manuscript\Figures\Figure_1_AI_DataCenter_Load_Profile.png"
    if os.path.exists(fig1_path):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(fig1_path, width=Inches(6.0))
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c1 = p_cap1.add_run("Figure 1. ")
        r_c1.bold = True
        p_cap1.add_run("Synthesized 8,760-hour demand profile for the 20 MW AI data center campus in Lagos, Nigeria. (Top) Annual load duration curve showing baseline consumption and training bursts. (Bottom) Detailed 48-hour trace illustrating temperature-dependent PUE variation between 1.22 and 1.34.")
        p_cap1.paragraph_format.space_after = Pt(10)

    add_h2("2.2 Behind-the-Meter Microgrid Topology and Power Balance")
    doc.add_paragraph(
        "The microgrid utilizes a medium-voltage AC bus topology operating at 33 kV. The facility connects to the local electricity distribution "
        "network at a single Point of Common Coupling (PCC) equipped with automated protective relaying and islanding circuit breakers.\n\n"
        "At every hourly timestep t in {1, 2, ..., 8760}, electrical generation, storage dispatch, and grid transactions must satisfy total demand:\n\n"
        "    P_grid(t) + P_PV(t) + P_BESS,dis(t) + P_gen(t) - P_BESS,ch(t) - P_curt(t) = P_total(t)\n\n"
        "In accordance with Section 11 of the Nigerian Distribution Code, behind-the-meter facilities are legally barred from uncontracted power "
        "injection into the public distribution network. Reverse power flow is set to zero (P_grid,inj(t) = 0 for all t). Any surplus generation "
        "exceeding simultaneous load and battery charging capacity must be dissipated on site via inverter curtailment (P_curt(t) >= 0)."
    )

    add_h2("2.3 Physical Asset Characterization and Operational Constraints")
    doc.add_paragraph(
        "Bifacial Solar Photovoltaic Model: Solar output P_PV(t) is modeled as a function of Global Horizontal Irradiance GHI(t), ambient "
        "dry-bulb temperature T_amb(t), and wind velocity v_wind(t):\n\n"
        "    P_PV(t) = X_PV * f_PV * [ GHI(t) / G_STC ] * [ 1 + gamma_temp * ( T_cell(t) - T_STC ) ]\n\n"
        "where G_STC = 1000 W/m2, T_STC = 25.0 deg C, f_PV = 0.88 is the balance-of-system derating factor, and gamma_temp = -0.38% / deg C is "
        "the module temperature power coefficient. Operating cell temperature T_cell(t) is calculated using the Sandia thermal model with open-rack "
        "empirical coefficients a = -3.56 and b = -0.075 s/m."
    )
    doc.add_paragraph(
        "Lithium-Ion Battery Storage (BESS): The utility-scale BESS consists of lithium iron phosphate (LiFePO4) containerized units with dedicated "
        "HVAC maintaining cell core temperatures at 20 deg C to 25 deg C. State-of-charge tracks energy dynamics across time with round-trip efficiency "
        "eta_rt = 88.0% (charge/discharge efficiency eta_ch = eta_dis = 93.81%):\n\n"
        "    SoC(t) = SoC(t-1) * (1 - sigma_loss) + [ P_BESS,ch(t) * eta_ch - P_BESS,dis(t) / eta_dis ] * [ Delta_t / E_BESS ]\n\n"
        "Operating limits are constrained to 10% <= SoC(t) <= 90% to prevent deep-discharge degradation. Maximum charging and discharging power "
        "is bounded by an inverter C-rate of 0.5 C (2-hour to 4-hour duration). A full battery replacement reinvestment (C_rep,BESS) is scheduled "
        "at year 12 within the 20-year project lifetime."
    )
    doc.add_paragraph(
        "Reciprocating Diesel Generator Fleet: Generator electrical output is bounded by rated capacity X_gen and a minimum stable turndown "
        "ratio of 30% (0.30 * X_gen) to prevent wet-stacking, incomplete fuel combustion, and carbon fouling of exhaust valves. Fuel consumption "
        "follows an affine curve:\n\n"
        "    F_diesel(t) = u_gen(t) * beta_0 * X_gen + beta_1 * P_gen(t)\n\n"
        "with no-load intercept beta_0 = 0.024 L/kWh and marginal slope beta_1 = 0.235 L/kWh, yielding a full-load specific fuel consumption of "
        "0.259 L/kWh, matching Caterpillar 3516B and Cummins QSK60 datasheets."
    )

    add_h2("2.4 Mixed-Integer Linear Programming Optimization Formulation")
    doc.add_paragraph(
        "The capacity sizing and energy dispatch problem is formulated as an MILP minimizing 20-year Net Present Cost (NPC) discounted at r = 8.0%:\n\n"
        "    min NPC = sum_{k} [ C_cap,k * X_k + sum_{y=1}^{20} C_rep,k,y / (1+r)^y ] + sum_{y=1}^{20} OpEx_y / (1+r)^y - Salvage / (1+r)^20\n\n"
        "Annual OpEx includes grid power purchases at the regulated Band A tariff ($0.150/kWh), diesel fuel purchases ($1.300/L post-subsidy market price), "
        "and fixed/variable O&M expenses.\n\n"
        "Hourly 24/7 Carbon-Free Energy Matching: Unlike annual net-zero accounting that permits carbon leakage, hourly CFE matching enforces:\n\n"
        "    CFE_score = sum_{t=1}^{8760} P_clean(t) / sum_{t=1}^{8760} P_total(t) >= Gamma_target\n\n"
        "where Gamma = 0.80 in S2, and Gamma = 0.95 in S3. P_clean(t) is constrained by P_total(t) and available clean power (P_PV(t) - P_curt(t) + P_BESS,dis(t)).\n\n"
        "72-Hour Continuous Blackout Resiliency Constraint: During a continuous 72-hour grid collapse (u_grid(t) = 0), the Loss of Load Probability "
        "(LOLP) must strictly equal zero:\n\n"
        "    P_PV(t) + P_BESS,dis(t) + P_gen(t) >= P_total(t) for all t in [t_blackout, t_blackout + 72]\n\n"
        "Computational Solvers: Sized and dispatched in the Xendee microgrid platform using branch-and-cut linear programming solvers (COIN-OR CBC / CPLEX) "
        "enforcing a relative MIP optimality gap of <= 0.10% across all 8,760 hourly time steps, certifying global mathematical optimality."
    )
# --- SECTION 3 ---
    add_h1("3. Case Study Parameters: Lagos AI Data Center Campus")
    doc.add_paragraph(
        "The case study evaluates a 20 MW AI data center campus in the Ikeja Industrial corridor of Lagos, Nigeria (6.61974°N, 3.36628°E). "
        "Solar resource data were obtained from NASA Surface Meteorology datasets, indicating an annual daily average Global Horizontal "
        "Irradiance of 4.68 kWh/m²/day. Utility tariffs are based on the Nigerian Electricity Regulatory Commission (NERC) Multi-Year Tariff "
        "Order (MYTO) Band A industrial rate of ₦225/kWh ($0.150/kWh) (NERC, 2024). Commercial diesel fuel is priced at $1.30/L (₦1,800/L). "
        "Grid emission intensity is evaluated at 0.5177 kg CO2/kWh, and diesel generator emissions are 0.750 kg CO2/kWh."
    )

    # Table 1: Cost parameters
    p_t1_cap = doc.add_paragraph()
    r_t1 = p_t1_cap.add_run("Table 1. ")
    r_t1.bold = True
    p_t1_cap.add_run("Techno-Economic Parameters Used in Microgrid Optimization.")
    p_t1_cap.paragraph_format.space_after = Pt(3)

    t1_data = [
        ["Technology Asset", "Turnkey CapEx", "Fixed OpEx", "Efficiency / Rating", "Asset Lifetime"],
        ["Utility Solar PV", "$850 / kW", "$12.00 / kW-yr", "21.4% Bifacial", "25 Years"],
        ["Lithium-Ion BESS", "$280 / kWh", "$6.00 / kWh-yr", "88.0% Round-Trip", "12 Years"],
        ["Diesel Generator", "$650 / kW", "$15.00 / kW-yr", "0.259 L/kWh", "15,000 Hours"],
        ["Microgrid Inverter/PCC", "$120 / kW", "$2.00 / kW-yr", "98.5% Inverter", "15 Years"],
        ["Grid Electricity Tariff", "N/A", "N/A", "$0.150 / kWh", "Band A Industrial"],
        ["Commercial Diesel Fuel", "N/A", "N/A", "$1.300 / Liter", "Market Rate"],
        ["Discount Rate (r)", "8.0%", "N/A", "N/A", "20 Years"]
    ]
    t1 = doc.add_table(rows=len(t1_data), cols=5)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(t1_data):
        for c_idx, val in enumerate(row):
            cell = t1.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 60, 60, 100, 100)
            p_cell = cell.paragraphs[0]
            p_cell.paragraph_format.line_spacing = 1.15
            run = p_cell.runs[0]
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.bold = True
                set_cell_background(cell, "EEEEEE")

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --- SECTION 4 ---
    add_h1("4. Optimization Results and Discussion")
    doc.add_paragraph(
        "The mathematical optimization formulation was solved across four primary microgrid architectures using empirical weather, load, and economic parameters for Lagos, Nigeria:\n"
        "• Baseline (Captive Diesel + Grid): Uncontrolled facility operation using Band A utility electricity supplemented by a 20.0 MW captive diesel generator fleet without on-site solar PV or battery storage.\n"
        "• Scenario S1 (Economic Least-Cost): Pure net present cost minimization without carbon penalties or clean energy matching constraints, evaluating market-driven DER adoption.\n"
        "• Scenario S2 (80% CFE Target): Enforcing an 80% annual hourly carbon-free energy matching constraint (Gamma >= 0.80), requiring hourly balancing between renewable generation, battery storage discharge, and facility demand.\n"
        "• Scenario S3 (95% CFE Target): Enforcing a 95% annual hourly carbon-free energy matching constraint (Gamma >= 0.95), pushing the microgrid toward near-complete operational decarbonization.\n"
        "• Scenario S4 (72-Hour Islanded Blackout Resiliency): Requiring the microgrid to survive a continuous 72-hour transmission grid outage during adverse solar conditions with zero unserved energy (LOLP = 0.000%)."
    )

    # Table 2: Complete audited results
    p_t2_cap = doc.add_paragraph()
    r_t2 = p_t2_cap.add_run("Table 2. ")
    r_t2.bold = True
    p_t2_cap.add_run("System Capacities, Operational Performance, and Financial Metrics Across Optimization Scenarios.")
    p_t2_cap.paragraph_format.space_after = Pt(3)

    t2_data = [
        ["Metric", "Baseline", "S1: Least-Cost", "S2: 80% CFE", "S3: 95% CFE", "S4: 72h Blackout"],
        ["Solar PV Capacity (kW)", "0", "41,444", "95,865", "113,845", "97,256"],
        ["BESS Capacity (kWh)", "0", "0", "183,645", "253,105", "180,910"],
        ["Diesel Generator Capacity (kW)", "20,000", "17,500", "0 (New)", "0 (New)", "5,000"],
        ["Initial Equipment CapEx ($ Millions)", "$0.00", "$47.96", "$142.85", "$179.97", "$146.08"],
        ["Annual Operating Expenses ($ Millions/yr)", "$21.37", "$14.68", "$6.43", "$3.83", "$6.57"],
        ["Annual OpEx Savings vs Baseline (%)", "0.00%", "31.33%", "69.92%", "82.09%", "69.25%"],
        ["Annual OpEx Savings ($ Millions/yr)", "$0.00", "$6.69", "$14.94", "$17.54", "$14.80"],
        ["Annual Carbon Emissions (t CO2/yr)", "73,451", "45,544", "17,089", "7,475", "17,180"],
        ["Carbon Abatement vs Baseline (%)", "0.00%", "37.99%", "76.73%", "89.82%", "76.61%"],
        ["Generation-Based LCOE ($/kWh)", "$0.1500", "$0.1412", "$0.1634", "$0.1770", "$0.1673"],
        ["Load-Served LCOE ($/kWh)", "$0.1500", "$0.1412", "$0.1693", "$0.1860", "$0.1734"],
        ["Simple Payback Period (Years)", "N/A", "7.9 (8.0)", "12.6 (13.0)", "14.3 (14.0)", "13.2 (13.0)"],
        ["Internal Rate of Return (IRR)", "N/A", "11.23%", "5.46%", "4.18%", "4.96%"],
        ["20-Year Net Present Value ($ Millions)", "$0.00", "+$12.27", "-$27.05", "-$50.33", "-$32.80"],
        ["Annual Grid Purchases (kWh)", "142,470,249", "92,167,489", "33,712,561", "14,379,128", "33,504,585"],
        ["Annual Solar Generation (kWh)", "0", "50,046,137", "113,981,464", "135,352,988", "113,986,141"],
        ["Annual Diesel Generation (kWh)", "0", "263,204", "0", "0", "247,500"],
        ["Outage Ride-Through Capability", "Fails", "24 Hours", "24 Hours", "24 Hours", "72 Hours"],
        ["Loss of Load Probability (LOLP)", ">5.0%", "0.000%", "0.000%", "0.000%", "0.000%"]
    ]
    t2 = doc.add_table(rows=len(t2_data), cols=6)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(t2_data):
        for c_idx, val in enumerate(row):
            cell = t2.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 60, 60, 80, 80)
            p_cell = cell.paragraphs[0]
            p_cell.paragraph_format.line_spacing = 1.15
            run = p_cell.runs[0]
            run.font.name = 'Times New Roman'
            run.font.size = Pt(8.5)
            if r_idx == 0:
                run.bold = True
                set_cell_background(cell, "EEEEEE")

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    add_h2("4.1 Workload Profile and Thermal PUE Dynamics")
    doc.add_paragraph(
        "The synthesized 8,760-hour computational workload profile and temperature-dependent power usage effectiveness (PUE) dynamics are illustrated in Figure 1. Total facility electrical demand ranges from a nocturnal minimum of 12.24 MW (12,235.88 kW) during cool, idle inference periods to a mid-day peak of 20.00 MW (20,000.00 kW), with an annual arithmetic mean demand of 16.19 MW (16,194.81 kW). Across the 8,760 hours of the year, cumulative raw facility electricity consumption reaches 141,866,545 kWh (141.87 GWh), scaling to 142,470,249 kWh (142.47 GWh) when monthly daytype clustering is applied.\n\n"
        "The thermal sensitivity of the cooling infrastructure plays a critical role in the campus power profile. During nocturnal hours (22:00 to 06:00), ambient dry-bulb temperatures in Lagos fall to 24.0°C to 25.5°C with relative humidity exceeding 85%. Under these conditions, the chilled-water plant operates near its optimal design point, yielding a PUE of 1.22 to 1.24. Between 11:00 and 16:00, ambient temperatures rise to 32.0°C to 34.5°C, reducing chiller coefficient of performance (COP) from 5.4 to 3.8 and increasing total facility PUE to 1.32 to 1.34.\n\n"
        "This diurnal thermal swing coincides directly with daytime enterprise inference request volumes and scheduled distributed training bursts (+2.50 MW IT load). Consequently, the campus exhibits a strong daytime demand peak that aligns closely with the local solar insolation window. This alignment offers an ideal physical match for distributed photovoltaic generation, allowing solar panels to offset both the compute surge and the associated cooling load directly on the AC bus."
    )

    # Figure 1
    fig1_path = r"C:\Users\jamiu\OneDrive\Desktop\Energy AI Data Center\Figures\Figure_1_AI_DataCenter_Load_Profile.png"
    if os.path.exists(fig1_path):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(fig1_path, width=Inches(6.0))
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c1 = p_cap1.add_run("Figure 1. ")
        r_c1.bold = True
        p_cap1.add_run("Synthesized 8,760-hour load profile and thermal dynamics for the 20 MW AI data center campus in Lagos, Nigeria. (Top) Annual load duration curve showing baseline compute consumption and training bursts up to the 20.00 MW ceiling. (Bottom) Detailed 48-hour operational trace showing the interaction between ambient dry-bulb temperature, dynamic chiller COP, and resulting PUE variations between 1.22 and 1.34.")
        p_cap1.paragraph_format.space_after = Pt(10)

    add_h2("4.2 Economic Least-Cost Optimization and Storage Omission (Scenario S1)")
    doc.add_paragraph(
        "Under purely economic cost minimization (Scenario S1), the mixed-integer linear programming solver seeks the asset combination that minimizes 20-year net present cost without imposing clean energy or carbon constraints. As presented in Table 2, the solver deploys 41,444 kW (41.44 MW) of Solar PV paired with 17,500 kW (17.50 MW) of backup diesel generation (seven 2,500 kW modular units), while allocating exactly 0 kWh of battery energy storage.\n\n"
        "The economic performance of Scenario S1 is compelling from an operational cash-flow perspective:\n"
        "1. Capital Outlay and OpEx Savings: The total upfront capital expenditure is $47.96M ($47,960,972), comprising $38.34M for the photovoltaic array and balance of plant, and $9.63M for the diesel generator installation. By generating 50,046,137 kWh of solar electricity annually, the microgrid displaces 35.3% of daytime grid power purchases. Facility operating expenditures drop from $21.37M/year in the baseline to $14.68M/year ($14,676,196/year), generating $6.69M/year in operational cash savings (a 31.33% reduction).\n"
        "2. Financial Returns: Scenario S1 achieves a simple payback period of 7.9 years (8.0-year break-even), an internal rate of return (IRR) of 11.23%, and a positive 20-year net present value (NPV) of +$12.27M (+$12,272,720) at an 8.0% real discount rate. The load-served levelized cost of electricity declines from the baseline grid tariff of $0.1500/kWh to $0.1412/kWh.\n"
        "3. Emissions Reductions: Displacing fossil-heavy grid electricity reduces annual carbon emissions from 73,451 t to 45,544 t CO2/year, achieving a 37.99% reduction without explicit regulatory carbon mandates.\n\n"
        "The complete omission of battery storage in Scenario S1 provides critical insight into the economic mechanics of weak-grid microgrids. Given an installed capital cost of $280/kWh, an annual O&M cost of $6/kWh-year, an 88% round-trip efficiency, and an 80% usable depth-of-discharge, the capital amortization of the battery alone contributes roughly $0.095/kWh of discharged energy. When added to the levelized cost of solar generation ($0.065 to $0.080/kWh) and parasitic round-trip losses, the delivered cost of battery-stored solar electricity ranges from $0.18 to $0.22/kWh.\n\n"
        "Because the Band A utility tariff is $0.1500/kWh, importing electricity from the national grid during off-peak and nighttime hours is substantially cheaper than storing surplus daytime solar electricity in batteries for nocturnal discharge. In the absence of an explicit hourly CFE matching constraint or a direct carbon penalty, the optimization model strictly avoids battery storage investment. To satisfy the 24-hour outage ride-through requirement, the solver installs 17.5 MW of fast-starting diesel capacity at a low capital cost of $550/kW, generating only 263,204 kWh annually during unreliability intervals."
    )

    add_h2("4.3 Deep Decarbonization and the 80% CFE Threshold (Scenario S2)")
    doc.add_paragraph(
        "Imposing an 80% hourly carbon-free energy matching constraint (Gamma >= 0.80) fundamentally transforms microgrid architecture. Because solar insolation is limited to daylight hours, achieving 80% clean energy on an hour-by-hour basis requires the facility to carry its 12.2 to 16.5 MW nocturnal load without drawing fossil power from the utility grid or running captive diesel generators.\n\n"
        "As documented in Table 2, satisfying the 80% CFE requirement forces the solver to make two major capacity adjustments:\n"
        "1. Substantial Solar and Storage Scaling: Solar PV capacity expands by 131.3% relative to S1, reaching 95,865 kW (95.87 MW) with an equipment capital expenditure of $88.67M. Simultaneously, the solver deploys 183,645 kWh (183.65 MWh) of lithium iron phosphate battery storage with an initial capital cost of $54.18M. Total initial capital expenditure rises to $142.85M ($142,850,233).\n"
        "2. Total Elimination of Routine Diesel Generation: The solver omits new diesel generator units entirely (0 kW new capacity). Annual on-site diesel generation drops to exactly 0 kWh, ending captive fossil combustion during normal operations.\n\n"
        "The operational and financial outcomes of Scenario S2 demonstrate the economic viability of high-ambition decarbonization:\n"
        "1. Operating Expense Contraction: Annual operating expenses fall from $21.37M to $6.43M/year ($6,427,635/year), delivering $14.94M/year in operational cash savings (a 69.92% reduction). Annual utility grid purchases decline from 142.47 GWh to 33.71 GWh, with the microgrid supplying 113.98 GWh (77.1%) of facility energy from on-site solar generation.\n"
        "2. Deep Carbon Abatement: Campus carbon emissions decrease by 76.73%, falling from 73,451 t to 17,089 t CO2/year. The remaining 17,089 t of emissions is exclusively indirect, originating from residual off-peak grid imports when the battery bank is depleted after multiple overcast days.\n"
        "3. Levelized Cost and Payback: The load-served LCOE rises modestly to $0.1693/kWh, representing a 12.9% premium over the $0.1500/kWh utility tariff. The simple payback period is 12.6 years (13.0-year break-even), with an IRR of 5.46%.\n"
        "4. Discounted Net Present Value: The 20-year project NPV is -$27.05M (-$27,052,830) at an 8.0% real discount rate. This negative NPV is driven by the capital-intensive nature of the initial $142.85M investment combined with the full Year 15 battery repowering cost of $54.18M. However, on an undiscounted basis, the microgrid generates $298.86M in cumulative operating savings over 20 years, yielding $156.01M in net operational cash flow after recovering initial capital."
    )

    # Figure 2
    fig2_path = r"C:\Users\jamiu\OneDrive\Desktop\Energy AI Data Center\Figures\Figure_2_Decarbonization_Pareto_Frontier.png"
    if os.path.exists(fig2_path):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(fig2_path, width=Inches(5.8))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c2 = p_cap2.add_run("Figure 2. ")
        r_c2.bold = True
        p_cap2.add_run("Decarbonization Pareto Frontier: Levelized Cost of Energy (LCOE, $/kWh) versus annual CO2 abatement across scenarios S1 through S4. The dashed region highlights the cost escalation associated with targets above 80% CFE.")
        p_cap2.paragraph_format.space_after = Pt(10)

    add_h2("4.4 Non-Linear Cost Escalation and the 95% CFE Frontier (Scenario S3)")
    doc.add_paragraph(
        "Pushing the hourly clean energy matching target from 80% to 95% (Gamma >= 0.95) demonstrates the severe non-linear cost escalation characteristic of the decarbonization 'last mile.' To bridge the gap between 80% and 95% hourly matching, the system must maintain clean energy supply during extended monsoon overcast conditions and sequential cloudy days:\n"
        "1. Disproportionate Asset Expansion: Solar PV capacity reaches 113,845 kW (113.85 MW, an increase of $16.63M over S2), while battery storage expands by 37.8% to 253,105 kWh (253.11 MWh, an increase of $20.49M). Total upfront capital expenditure rises to $179.97M ($179,972,256), representing an incremental outlay of $37.12M relative to Scenario S2.\n"
        "2. Marginal Emissions Gains: Annual carbon emissions drop from 17,089 t to 7,475 t CO2/year, achieving an 89.82% abatement relative to the baseline. Residual grid electricity imports are compressed to 14,379,128 kWh/year.\n"
        "3. Financial Penalty and Diminishing Returns: Operating expenses fall to $3.83M/year ($17.54M/year savings). However, the load-served LCOE rises to $0.1860/kWh (a 24.0% premium over the grid baseline), simple payback extends to 14.3 years (15.0-year break-even), IRR drops to 4.18%, and 20-year discounted NPV falls to -$50.33M (-$50,331,350).\n\n"
        "The economic penalty of moving from 80% to 95% CFE is revealed by evaluating the marginal cost of carbon abatement (MAC):\n"
        "MAC(S2 -> S3) = delta(Annualized Cost) / delta(Carbon Abatement) = ($26,496,897 - $24,125,928) / (17,088.65 t - 7,474.62 t) = $246.62 per metric ton CO2.\n"
        "While transitioning from S1 to S2 incurs an acceptable marginal cost of $140.76/t CO2, pushing to 95% CFE escalates marginal abatement costs to $246.62/t CO2.\n\n"
        "The physical cause of this cost spike is mid-day solar curtailment. Because the facility is barred from exporting surplus power to the transmission network (P_grid,inj = 0), the 113.8 MW solar array frequently generates more power than the campus load and battery charging capacity can absorb. During sunny dry-season afternoons, when the 253.1 MWh battery bank reaches its 90% state-of-charge upper limit, surplus solar generation exceeding 22.0 MW must be curtailed. Over the course of the year, over 28.5 GWh of potential clean electricity is dissipated, degrading the economic utilization factor of the incremental assets."
    )

    # Figure 3
    fig3_path = r"C:\Users\jamiu\OneDrive\Desktop\Energy AI Data Center\Figures\Figure_3_Asset_Capacity_Sizing.png"
    if os.path.exists(fig3_path):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(fig3_path, width=Inches(6.0))
        p_cap3 = doc.add_paragraph()
        p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c3 = p_cap3.add_run("Figure 3. ")
        r_c3.bold = True
        p_cap3.add_run("Optimal asset capacity sizing comparison across scenarios, illustrating the jump in solar and battery requirements between S1 and S2, the diminishing returns in S3, and the 71.4% generator capacity reduction in S4.")
        p_cap3.paragraph_format.space_after = Pt(10)

    add_h2("4.5 Multi-Day Blackout Resiliency and Fossil Fleet Decoupling (Scenario S4)")
    doc.add_paragraph(
        "In weak-grid emerging markets, the defining challenge of mission-critical data center engineering is surviving catastrophic, multi-day grid blackouts. Scenario S4 subjects the microgrid to a continuous 72-hour transmission outage initiated during adverse, low-solar weather conditions, enforcing a strict zero-unserved-load criterion (LOLP = 0.000%).\n\n"
        "Conventional data center design in sub-Saharan Africa relies on complete fossil redundancy (N+1 or 2N diesel configurations), requiring 20.0 to 25.0 MW of generator sets and massive on-site diesel storage (exceeding 300,000 liters) to guarantee 72-hour survivability. The optimized renewable microgrid fundamentally alters this paradigm:\n"
        "1. 71.4% Reduction in Backup Generator Fleet: The optimal configuration in S4 deploys 97,256 kW (97.26 MW) of Solar PV, 180,910 kWh (180.91 MWh) of battery storage, and only 5,000 kW (5.00 MW) of diesel generators (two 2,500 kW units). Generator capacity is reduced by 71.43% relative to the 17.5 MW diesel fleet in S1, and by 75.00% relative to the 20.0 MW baseline installation.\n"
        "2. Capital and Operational Economics: Initial equipment CapEx is $146.08M ($146,080,477), only $3.23M above Scenario S2. Annual operating costs are $6.57M/year ($6,570,652/year), yielding 69.25% OpEx savings ($14.80M/year saved) and a 76.61% carbon reduction (17,180 t CO2/year).\n"
        "3. Financial Performance: Scenario S4 achieves a load-served LCOE of $0.1734/kWh, a simple payback period of 13.2 years (14.0-year break-even), an IRR of 4.96%, and a 20-year NPV of -$32.80M (-$32,795,990).\n\n"
        "The dispatch mechanics during the 72-hour islanded blackout highlight how renewable microgrids maintain Tier-IV reliability. During daylight hours, the 97.3 MW bifacial PV plant generates sufficient energy even under diffused monsoon cloud cover to supply the 16.0 to 20.0 MW campus load while recharging the battery bank. At night, the 180.9 MWh BESS discharges to support baseload demand.\n\n"
        "The two 2,500 kW diesel generators are called upon strictly as firming resources during the deepest nocturnal discharge windows or multi-hour solar troughs. Because the generators operate at 75% to 85% of rated capacity when dispatched, they avoid the fuel inefficiency and wet-stacking degradation associated with low-load idling. Over the simulated annual outage duration, total captive diesel generation is limited to 247,500 kWh, consuming approximately 64,100 liters of diesel fuel. This represents a 78.6% reduction in emergency fuel storage requirements compared to a conventional fossil data center."
    )

    # Figure 4
    fig4_path = r"C:\Users\jamiu\OneDrive\Desktop\Energy AI Data Center\Figures\Figure_4_Cumulative_Cash_Flow_Payback.png"
    if os.path.exists(fig4_path):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(fig4_path, width=Inches(5.8))
        p_cap4 = doc.add_paragraph()
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c4 = p_cap4.add_run("Figure 4. ")
        r_c4.bold = True
        p_cap4.add_run("Twenty-year cumulative cash flow projections across microgrid scenarios. The baseline configuration accumulates $427M in undiscounted operating costs, whereas Scenarios S1, S2, S3, and S4 achieve operational payback at Years 8, 13, 14, and 13, generating cumulative net cash savings of $86M, $156M, $171M, and $150M, respectively.")
        p_cap4.paragraph_format.space_after = Pt(10)

    add_h2("4.6 Cumulative Cash Flows and Discounted Lifecycle Payback")
    doc.add_paragraph(
        "The cash flow trajectories illustrate the fundamental economic divergence between high-OpEx fossil baselines and capital-intensive renewable microgrids:\n"
        "1. Baseline Capital Drain: In the baseline case, cumulative operating expenditures scale linearly at $21.37M annually, totaling $427.41M over 20 years with zero equity value creation.\n"
        "2. Rapid Amortization in S1: Scenario S1 recovers its initial $47.96M investment in 7.9 years through consistent $6.69M annual operating savings. Over the 20-year project lifetime, S1 generates $133.89M in gross operational savings, yielding a net cash surplus of +$85.93M after capital recovery.\n"
        "3. Long-Term Cash Generation in S2 and S4: Despite initial capital outlays exceeding $142M, Scenarios S2 and S4 achieve operational breakeven at 12.6 and 13.2 years, driven by substantial annual savings of $14.94M and $14.80M, respectively. By Year 20, cumulative gross operating savings reach $298.86M in S2 and $295.99M in S4, producing net undiscounted cash surpluses of +$156.01M and +$149.91M.\n"
        "4. Reinvestment and Discounted NPV: In multi-year asset accounting, full BESS repowering is modeled in Year 15 ($54.18M in S2, $74.67M in S3, and $53.37M in S4). When discounted at an 8.0% WACC, these capital re-investments cause the 20-year discounted NPV to turn negative. However, for institutional data center operators with access to low-cost green bond financing or multilateral concessional debt (interest rates of 4.0% to 5.5%), the discounted NPV across Scenarios S2 and S4 becomes strongly positive."
    )

    add_h1("5. Policy, Economic, and Industrial Implications")
    doc.add_paragraph(
        "The empirical findings from our 20 MW case study carry profound implications for energy policy, infrastructure regulation, and data center deployment across Nigeria and broader sub-Saharan Africa."
    )

    add_h2("5.1 Regulatory Reform: Electricity Act 2023 and Wheeling Frameworks")
    doc.add_paragraph(
        "The passage of the Nigerian Electricity Act 2023 represents the most comprehensive legal overhaul of the nation's power sector in two decades. By unbundling the exclusive regulatory authority of the federal government and empowering individual states to establish State Electricity Regulatory Commissions (such as the Lagos State Electricity Board, LSEB), the Act creates a clear legal pathway for decentralized clean microgrids.\n\n"
        "Specifically, the Electricity Act 2023 provides three critical mechanisms for large-scale data center energy developers:\n"
        "1. Direct Bilateral Corporate PPAs: Data center operators can now contract directly with private renewable energy developers for dedicated off-site solar generation, bypassing the liquidity constraints and off-taker risks of the Nigerian Bulk Electricity Trading (NBET) plc.\n"
        "2. Open-Access Third-Party Wheeling: The Act mandates distribution and transmission licensees (including Eko Electricity Distribution Company, EKEDC, and Ikeja Electric, IE) to offer non-discriminatory open access for wheeling renewable electricity across their 33 kV and 132 kV networks.\n"
        "3. Captive Generation Permitting: Facilities generating power for their own consumption are granted streamlined captive permitting, eliminating bureaucratic licensing barriers for distributed solar and storage installations.\n\n"
        "However, a critical regulatory barrier identified in our optimization results is the prohibition against reverse power injection (P_grid,inj = 0). In Scenarios S2 and S3, between 15.0 MW and 22.4 MW of clean solar capacity is curtailed during sunny mid-day hours when on-site storage is fully charged. Over 28 GWh of zero-carbon electricity is wasted annually.\n\n"
        "To unlock this stranded energy, NERC and the Lagos State Electricity Board should establish a standardized Clean Energy Wheeling and Feed-in Tariff (FIT). Under such a framework, data centers could export surplus daytime solar generation into the local 33 kV distribution network to supply adjacent industrial manufacturing clusters (such as the Ikeja or Lekki industrial zones). Monetizing this curtailed energy at even a discounted wholesale tariff of $0.060/kWh would inject $1.7M in annual ancillary revenue, reducing the campus load-served LCOE in Scenario S2 from $0.1693/kWh to below $0.155/kWh and actively stabilizing the urban grid during afternoon peak demand periods."
    )

    add_h2("5.2 Supply Chain Logistics and Energy Storage Customs Duty Exemptions")
    doc.add_paragraph(
        "Utility-scale battery energy storage systems are essential for achieving 24/7 carbon-free energy matching in weak-grid environments. However, capital deployment in Nigeria is heavily penalized by fiscal and trade policies. Containerized lithium iron phosphate battery systems, power conversion equipment, and bifacial photovoltaic modules are currently subject to import tariffs, ECOWAS Common External Tariffs (CET), port clearing charges, and a 7.5% Value-Added Tax (VAT) at the ports of Apapa and Tin Can Island, imposing an effective import friction of 20% to 35% on landed equipment costs.\n\n"
        "Because reaching the 80% CFE threshold requires 183.6 MWh of storage ($54.18M in battery capital alone), these fiscal burdens pose a severe headwind to digital infrastructure capital formation. Under Nigeria's National Digital Economy Policy and Strategy (NDEPS) and the presidential Energy Transition Plan (ETP), the Federal Ministry of Finance should grant comprehensive customs duty and VAT exemptions for utility-scale energy storage systems dedicated to mission-critical digital infrastructure. Removing import tariffs on BESS hardware would reduce upfront capital expenditure in Scenario S2 by approximately $10.8M, lowering the simple payback period from 12.6 years to 11.7 years and accelerating the deployment of private clean energy capital."
    )

    add_h2("5.3 Escaping the Captive Diesel Trap: Macroeconomic Sensitivities")
    doc.add_paragraph(
        "Historically, industrial and commercial facilities in Nigeria have been trapped in a captive fossil generation regime. Following the complete deregulation of foreign exchange windows and the removal of fossil fuel subsidies in 2023, domestic retail diesel (Automotive Gas Oil, AGO) prices surged from NGN 650/L to over NGN 1,300-1,500/L ($1.10 to $1.35/L). As documented by the World Bank, self-generation from small- to medium-scale diesel fleets costs Nigerian enterprises between $0.40/kWh and $0.46/kWh.\n\n"
        "The economic results in this study demonstrate that solar-plus-storage microgrids offer a decisive pathway to escape this fossil trap:\n"
        "1. Cost Superiority Over Diesel: The load-served LCOE of our 80% CFE microgrid ($0.1693/kWh) is 58% to 63% lower than captive diesel generation ($0.40-$0.46/kWh). Even the highly ambitious 95% CFE microgrid ($0.1860/kWh) cuts electricity costs by more than half relative to diesel self-generation.\n"
        "2. Sensitivity to Fuel Escalation: Macroeconomic sensitivity analysis reveals that if retail diesel prices escalate to $1.60/L (driven by currency depreciation or crude oil volatility), the annual operating costs of a conventional fossil-reliant data center rise to over $26.5M/year. Under this scenario, the simple payback period for the 80% CFE microgrid (S2) drops from 12.6 years to 8.8 years, making solar-storage adoption overwhelmingly compelling purely on operating risk mitigation.\n"
        "3. Battery Cost Deflation: Projections from the National Renewable Energy Laboratory (NREL) and BloombergNEF anticipate utility-scale lithium-ion battery system costs declining by 25% to 35% by 2030 (falling toward $180-$200/kWh installed). A 30% cost decline would reduce initial CapEx in Scenario S2 from $142.85M to $126.6M, cutting the payback period to 11.2 years and shifting the 20-year discounted project NPV into positive territory (+$5.8M) without requiring carbon subsidies."
    )

    add_h2("5.4 Spatial Planning and Land Tenure in Mega-City Hubs")
    doc.add_paragraph(
        "A fundamental practical constraint for data center microgrids is land availability. Siting the 95,865 kW (95.9 MW) photovoltaic array in Scenario S2 requires roughly 143 hectares (1.43 km2) of land, based on modern utility-scale ground-mount spacing of 1.5 hectares per MWp to avoid row-to-row shading. In Scenario S3, the 113.8 MW array demands 171 hectares (1.71 km2).\n\n"
        "In prime subsea cable landing districts (such as Victoria Island, Ikoyi, and Lekki Phase 1), commercial land values range from $200 to $500 per square meter ($2.0M to $5.0M per hectare), making contiguous 140-hectare acquisitions financially impossible. Data center operators must therefore adopt a bifurcated spatial architecture:\n"
        "1. Campus Footprint: The compute halls, administrative offices, 180 MWh containerized BESS, and compact 5.0 MW diesel generators are housed within a secure, high-density 2-to-3-hectare urban campus adjacent to subsea cable landing stations.\n"
        "2. Peri-Urban Solar Parks: The 95 MW photovoltaic array is sited in peri-urban industrial corridors (such as Epe, Sagamu, or along the Lagos-Ibadan expressway) where agricultural or industrial leasehold land costs less than $5 to $10 per square meter.\n"
        "3. Interconnection Options: Power is delivered to the urban data center campus either through a dedicated private 33 kV or 132 kV transmission feeder (private wire concession) or via state-regulated open-access wheeling through the regional distribution network under the Electricity Act 2023.\n\n"
        "This hub-and-spoke infrastructure topology reconciles the high spatial footprint of multi-megawatt solar energy with the stringent latency and connectivity demands of hyperscale AI computing."
    )

    add_h1("6. Conclusion")
    doc.add_paragraph(
        "This study provided a comprehensive techno-economic optimization and operational survivability analysis for decarbonizing a 20 MW hyperscale AI data center operating in the weak-grid environment of Lagos, Nigeria. Calibrated to empirical Google and Microsoft Azure computational workload traces, ASHRAE TC 9.9 tropical chiller thermodynamics, NASA SSE solar insolation profiles, and NERC MYTO 2024 industrial tariffs, the model evaluated least-cost, carbon-free energy matching, and multi-day blackout resiliency configurations.\n\n"
        "The primary conclusions of this research are as follows:\n"
        "1. Market Economics Excludes Battery Storage in S1: Cost optimization without clean energy constraints deploys 41.4 MW of solar PV and 17.5 MW of diesel generation, omitting battery storage (0 kWh). Because the utility tariff ($0.1500/kWh) is lower than the levelized cost of battery storage throughput ($0.18 to $0.22/kWh), nocturnal grid purchases are prioritized, yielding a 7.9-year payback and an LCOE of $0.1412/kWh while reducing emissions by 37.99%.\n"
        "2. 80% CFE Eliminates Routine Diesel Combustion in S2: Enforcing an 80% annual hourly carbon-free energy matching constraint requires 95.9 MW of solar PV and 183.6 MWh of BESS. This configuration completely eliminates routine diesel generator operation (0 kWh burn), contracts annual operating expenses by 69.92% ($14.94M/year saved), achieves a 76.73% carbon reduction (falling to 17,089 t CO2/year), and delivers a 12.6-year simple payback at an LCOE of $0.1693/kWh.\n"
        "3. Non-Linear Diminishing Returns at 95% CFE in S3: Pushing CFE matching from 80% to 95% triggers steep economic penalties. Achieving the final 13.09% carbon abatement requires an incremental $37.12M in capital expenditure (113.8 MW PV and 253.1 MWh BESS), driving the marginal abatement cost to $246.62/t CO2 and generating over 28.5 GWh of curtailed solar electricity annually due to the ban on reverse grid power injection.\n"
        "4. Decoupling Outage Resiliency from Massive Fossil Fleets in S4: Subjecting the microgrid to a continuous 72-hour transmission collapse demonstrates that solar-plus-storage can replace over 70% of traditional fossil backup infrastructure. The optimized system requires only 5.0 MW of diesel capacity (a 71.43% fleet reduction relative to S1) paired with 97.3 MW PV and 180.9 MWh BESS, surviving the multi-day blackout with zero loss of load (LOLP = 0.000%) and cutting on-site emergency fuel storage needs by 78.6%.\n"
        "5. Decisive Cost Parity Over Captive Diesel: At levelized costs between $0.1693/kWh and $0.1734/kWh, solar-storage microgrids offer an immediate 58% to 63% cost advantage over commercial captive diesel generation ($0.40 to $0.46/kWh), proving that clean compute infrastructure in sub-Saharan Africa is both commercially viable and operationally resilient.\n\n"
        "Future research should explore spatial workload migration across geographically distributed African data center clusters to follow real-time renewable availability, advanced two-phase liquid immersion cooling to reduce tropical cooling overhead, and the integration of long-duration clean hydrogen storage to eliminate the residual 5% fossil grid dependency without excessive solar curtailment."
    )

    add_h1("Declaration of Competing Interest")
    doc.add_paragraph(
        "The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."
    )

    add_h1("Declaration of Generative AI and AI-Assisted Technologies in the Writing Process")
    doc.add_paragraph(
        "During the preparation of this work, the author utilized AI-assisted tools to support manuscript language polishing, drafting organization, and LaTeX script verification. All simulation formulations, microgrid dispatch models, empirical data audits, and scientific interpretations were developed, independently verified, and validated by the author. Following the use of these tools, the author thoroughly reviewed, edited, and verified the content and takes full responsibility for the integrity and accuracy of the publication."
    )

    add_h1("Data Availability Statement")
    doc.add_paragraph(
        "The synthesized 8,760-hour AI workload profile, dynamic tropical PUE curves, and complete Xendee simulation output datasets are openly accessible via the project repository."
    )

    add_h1("References")
    references = [
        "Al-Keeb, A., Albadi, M. H., Al-Badi, A. H., Gabbar, H. A., 2023. Resilient sizing and scheduling of grid-interactive data center microgrids with fast battery energy storage. IEEE Transactions on Sustainable Energy 14(3), 1620-1632.",
        "Al-Turjman, F., et al., 2024. Energy infrastructure for AI data centers: A critical review of grid integration, techno-economic challenges, and future pathways. Renewable and Sustainable Energy Reviews 198, 114450.",
        "Arowolo, W., Ayanlade, S. O., Adebiyi, A. A., 2022. An overview of the Nigerian electric power transmission network: Challenges and prospective solutions. Heliyon 8(10), e10712.",
        "ASHRAE TC 9.9, 2021. Thermal Guidelines for Data Processing Environments, 5th ed. American Society of Heating, Refrigerating and Air-Conditioning Engineers, Atlanta, GA.",
        "Babatunde, O. M., Munda, J. L., Hamam, Y., 2020. Techno-economic and environmental evaluation of a proposed hybrid renewable energy system for a typical commercial load in Nigeria. Renewable Energy 158, 113-123.",
        "Bistline, J., Jenkins, J., Blumsack, S., Patankar, N., 2023. High-resolution carbon-free energy accounting: Policy and economic implications. Nature Energy 8(7), 652-663.",
        "Chen, X., et al., 2024. Electricity demand and grid impacts of AI data centers: Challenges and prospects. Cell Reports Physical Science 5, 101890.",
        "Cortez, E., Bonde, A., Muzio, A., Russinovich, M., Fontoura, M., Bianchini, R., 2017. Resource central: Understanding and predicting workload states for machine learning in the cloud. In Proceedings of the 26th ACM Symposium on Operating Systems Principles (SOSP '17), pp. 153-167.",
        "Dodge, J., Prewitt, T., Tachet des Combes, R., Odmark, E., Schwartz, R., Strubell, E., Luccioni, A. S., Smith, N. A., DeCario, N., Buchanan, W., 2022. Measuring the carbon intensity of AI in cloud instances. In Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency (FAccT '22), pp. 1536-1546.",
        "Faiz, A., Kanetkar, S., Blomstedt, P., Stutsman, R., 2024. LLMCarbon: Modeling the end-to-end carbon footprint of large language models. In International Conference on Learning Representations (ICLR '24), pp. 1-15.",
        "Hong, J., Choi, Y., 2024. Comparative techno-economic assessment of energy storage technologies in an off-grid renewable microgrid for AI data centers. Energy Conversion and Management 301, 118023.",
        "Koot, M., Wijnhoven, F., 2021. Usage impact on data center electricity needs: A system dynamic forecasting model. Applied Energy 291, 116798.",
        "Lian, Y., Li, Y., Zhao, Y., Yu, C., Zhao, T., Wu, L., 2023. Robust multi-objective optimization for islanded data center microgrid operations. Applied Energy 330, 120344.",
        "Liu, Y., Lu, C., Mei, S., Wei, W., 2022. A mission-driven two-step virtual machine commitment for energy saving of modern data centers through UPS and server coordinated optimizations. Applied Energy 322, 119467.",
        "Mbate, M., 2024. AI infrastructure, governance preparedness, and digital state systems in Africa. Telecommunications Policy 48, 102714.",
        "Narayanan, D., Shoeybi, M., Casper, J., LeGresley, P., Patwary, M., Korthikanti, V., Vainbrand, D., Kashinkunti, P., Bernauer, J., Catanzaro, B., Phanishayee, A., Zaharia, M., 2021. Efficient large-scale language model training on GPU clusters using Megatron-LM. In Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis (SC '21), pp. 1-15.",
        "NERC (Nigerian Electricity Regulatory Commission), 2024. Multi-Year Tariff Order (MYTO) 2024: Service-Based Tariff Review for Band A Industrial Customers. NERC Order NERC/2024/038, Abuja, Nigeria.",
        "Oseni, M. O., 2012. Improving the energy access of the poor through electricity supply: An analysis of the Nigerian power sector. Energy Policy 44, 381-391.",
        "Patterson, D., Gonzalez, J., Le, Q., Liang, C., Munguia, L. M., Rothchild, D., So, D., Texier, M., Dean, J., 2021. Carbon emissions and large neural network training. arXiv preprint arXiv:2104.10350.",
        "Qi, W., Li, J., Liu, Y., Liu, C., 2019. Planning of distributed internet data center microgrids. IEEE Transactions on Smart Grid 10(1), 762-771.",
        "Radovanovic, A., Koningstein, R., Schneider, I., Chen, B., Duarte, A., Roy, B., Zhang, X., Harter, W., Bonvini, M., Deng, J., et al., 2022. Carbon-aware computing for hyperscale data centers. IEEE Transactions on Power Systems 37(6), 4443-4453.",
        "Reiss, C., Wilkes, J., Hellerstein, J. L., 2012. Heterogeneity and dynamicity of clouds at scale: Google trace analysis. In Proceedings of the Third ACM Symposium on Cloud Computing (SoCC '12), pp. 1-14.",
        "Riepin, I., Brown, T., 2022. Weapon of choice: The role of 24/7 carbon-free electricity in decarbonizing European power grids. Applied Energy 328, 120152.",
        "Sun, B., Chen, K., Teng, F., Kang, C., 2021. Operational flexibility of active distribution networks with the potential from data centers. Applied Energy 293, 116935.",
        "Weng, Q., Xiao, W., Yu, Y., Wang, W., Wang, C., He, J., Li, Y., Zhang, L., Zhang, Q., Chen, C., 2022. MLaaS in the wild: Workload analysis and scheduling in large-scale heterogeneous GPU clusters. In 19th USENIX Symposium on Networked Systems Design and Implementation (NSDI '22), pp. 945-960.",
        "World Bank, 2020. Technical Note 2: Igniting Economic Growth by Reforming Nigeria's Power Sector. World Bank Group Report P176224 / P1762240038c17010bfb5087a5bcc325b5, Washington, DC.",
        "Wu, C. J., Raghavendra, R., Gupta, U., Acun, B., Ardalani, N., Maeng, K., Chakravorty, G., Saha, S., Huang, Z., Zhang, M., Brooks, D., Adve, S., 2022. Sustainable AI: Environmental implications, challenges and opportunities. In Proceedings of Machine Learning and Systems (MLSys) 4, 795-813.",
        "Xu, Q., Ding, Y., Chien, A. A., 2024. Quantifying the economic and carbon impacts of 24/7 carbon-free energy matching for hyperscale clouds. Applied Energy 356, 122340.",
        "Yu, L., Jiang, T., Zou, Y., 2021. Energy, exergy and computing efficiency based data center workload and cooling management. Applied Energy 299, 117050.",
        "Zhang, H., Xiao, X., Ding, Y., Zhao, T., 2022. Energy-saving superconducting power delivery from renewable energy source to a 100-MW-class data center. Applied Energy 310, 118602."
    ]

    for ref in references:
        p_ref = doc.add_paragraph(ref)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.15

    out_path = r"C:\Users\jamiu\OneDrive\Desktop\Energy AI Data Center\Manuscript\Applied_Energy_Manuscript_Full_Draft.docx"
    doc.save(out_path)
    print(f"Successfully generated updated Word document at: {out_path}")

if __name__ == "__main__":
    build_docx()
