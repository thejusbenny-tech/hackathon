"""
Generate all 12 sample documents for the Sales Co-Pilot hackathon.
Run: pip install reportlab python-pptx && python generate_docs.py
Output goes to ./documents/
"""

import os
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
except ImportError:
    raise SystemExit("Install reportlab first:  pip install reportlab")

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
except ImportError:
    raise SystemExit("Install python-pptx first:  pip install python-pptx")

OUT = Path("documents")
OUT.mkdir(exist_ok=True)

# ── Colour palette ──────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#0a2342")
MID_BLUE    = colors.HexColor("#1d4ed8")
LIGHT_BLUE  = colors.HexColor("#bfdbfe")
ACCENT      = colors.HexColor("#7c3aed")
GREY        = colors.HexColor("#374151")
LIGHT_GREY  = colors.HexColor("#f8fafc")

# ── Shared style builder ────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["title"] = ParagraphStyle("title", parent=base["Normal"],
        fontSize=22, fontName="Helvetica-Bold", textColor=DARK_BLUE,
        spaceAfter=6, alignment=TA_LEFT)

    styles["subtitle"] = ParagraphStyle("subtitle", parent=base["Normal"],
        fontSize=12, fontName="Helvetica", textColor=GREY,
        spaceAfter=18, alignment=TA_LEFT)

    styles["h1"] = ParagraphStyle("h1", parent=base["Normal"],
        fontSize=14, fontName="Helvetica-Bold", textColor=MID_BLUE,
        spaceBefore=14, spaceAfter=6)

    styles["h2"] = ParagraphStyle("h2", parent=base["Normal"],
        fontSize=12, fontName="Helvetica-Bold", textColor=DARK_BLUE,
        spaceBefore=10, spaceAfter=4)

    styles["body"] = ParagraphStyle("body", parent=base["Normal"],
        fontSize=10, fontName="Helvetica", textColor=GREY,
        spaceAfter=8, leading=15)

    styles["bullet"] = ParagraphStyle("bullet", parent=base["Normal"],
        fontSize=10, fontName="Helvetica", textColor=GREY,
        spaceAfter=4, leftIndent=16, bulletIndent=4, leading=14)

    styles["metric"] = ParagraphStyle("metric", parent=base["Normal"],
        fontSize=11, fontName="Helvetica-Bold", textColor=ACCENT,
        spaceAfter=4, leading=16)

    styles["footer"] = ParagraphStyle("footer", parent=base["Normal"],
        fontSize=8, fontName="Helvetica", textColor=colors.HexColor("#9ca3af"),
        alignment=TA_CENTER)

    return styles

def header_block(story, styles, title, subtitle, doc_type, year):
    story.append(Paragraph(doc_type.upper(), ParagraphStyle("tag",
        fontSize=9, fontName="Helvetica-Bold", textColor=MID_BLUE, spaceAfter=4)))
    story.append(Paragraph(title, styles["title"]))
    story.append(Paragraph(subtitle, styles["subtitle"]))
    story.append(HRFlowable(width="100%", thickness=2, color=MID_BLUE, spaceAfter=16))

def build_pdf(filename, build_fn):
    path = OUT / filename
    doc = SimpleDocTemplate(str(path), pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm, bottomMargin=2*cm)
    styles = make_styles()
    story = []
    build_fn(story, styles)
    doc.build(story)
    print(f"  ✓  {filename}")

def bullet(text, styles):
    return Paragraph(f"• {text}", styles["bullet"])

def metric_row(story, styles, items):
    """Render a coloured metrics table."""
    data = [[Paragraph(v, ParagraphStyle("mv", fontSize=18, fontName="Helvetica-Bold",
                                          textColor=MID_BLUE, alignment=TA_CENTER)),
             Paragraph(k, ParagraphStyle("mk", fontSize=9, fontName="Helvetica",
                                          textColor=GREY, alignment=TA_CENTER))]
            for k, v in items]
    t = Table([[row[0] for row in data], [row[1] for row in data]],
              colWidths=[4.2*cm]*len(items))
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_GREY),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

# ═══════════════════════════════════════════════════════════════════════════
# CASE STUDIES
# ═══════════════════════════════════════════════════════════════════════════

def cs_smart_factory(story, styles):
    header_block(story, styles,
        "Smart Factory Transformation — Automotive OEM",
        "Case Study  |  Pune, Maharashtra  |  2023",
        "Case Study", "2023")

    story.append(Paragraph("Executive Summary", styles["h1"]))
    story.append(Paragraph(
        "A leading automotive OEM in Pune engaged us to transform three of its high-volume assembly plants "
        "into fully connected smart factories. The 18-month programme—spanning IoT sensor deployment, "
        "MES integration, SCADA modernisation, and real-time Power BI dashboards—delivered measurable "
        "operational improvements and a clear path to further Industry 4.0 maturity.", styles["body"]))

    metric_row(story, styles, [
        ("OEE Improvement", "22%"), ("Downtime Reduction", "15%"),
        ("Annual Savings", "₹12 Cr"), ("Programme Duration", "18 mo"),
    ])

    story.append(Paragraph("Client Context", styles["h1"]))
    story.append(Paragraph(
        "The client—a Tier-0.5 supplier producing 4-wheelers and light commercial vehicles—faced "
        "escalating quality escapes, unpredictable line stoppages, and limited production visibility. "
        "Legacy PLCs ran on isolated networks; shop-floor data existed only in paper shift logs. "
        "The leadership team set an ambitious OEE target of 85% across all lines within two years.", styles["body"]))

    story.append(Paragraph("Scope of Work", styles["h1"]))
    for item in [
        "Deployment of 1,200+ IoT edge sensors (vibration, temperature, cycle-count) across all three plants",
        "MES rollout (SAP ME) integrated with existing ERP (SAP S/4HANA) and quality management systems",
        "SCADA layer upgrade to enable real-time OT data streaming to cloud data platform",
        "Power BI dashboards for plant managers, shift supervisors, and C-suite (12 distinct report views)",
        "Digital twin of Assembly Line 3 for process simulation and capacity planning",
        "Change management & operator training programme (400+ shop-floor staff upskilled)",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Technology Stack", styles["h1"]))
    tech = [["Layer", "Technology", "Vendor/Product"],
            ["IoT Edge", "Edge gateways + MQTT brokers", "Azure IoT Edge"],
            ["MES", "Manufacturing Execution System", "SAP ME 15.4"],
            ["SCADA", "Supervisory control layer", "Wonderware InTouch"],
            ["Analytics", "Real-time dashboards", "Microsoft Power BI"],
            ["Cloud", "Data lake & processing", "Azure (ADX + ADF)"],
            ["Integration", "ERP-MES connector", "Custom middleware (Python)"]]
    t = Table(tech, colWidths=[4*cm, 7*cm, 5.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), MID_BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [LIGHT_GREY, colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Key Outcomes", styles["h1"]))
    for item in [
        "Overall Equipment Effectiveness rose from 61% to 83%, exceeding the 85% target trajectory",
        "Unplanned downtime reduced by 15%; mean-time-to-repair improved by 28%",
        "Annual cost savings of ₹12 Cr through reduced scrap, rework, and energy optimisation",
        "First-pass yield on critical sub-assemblies improved from 94.1% to 98.6%",
        "Real-time production visibility enabled proactive scheduling adjustments, reducing overtime by 22%",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Our Differentiators", styles["h1"]))
    story.append(Paragraph(
        "Our pre-built Industry 4.0 accelerator—comprising 40+ reusable integration adapters and "
        "a validated OT/IT convergence architecture—reduced the integration effort by an estimated "
        "35% compared to a greenfield build. The automotive domain team (average 12 years shop-floor "
        "experience) earned trust with plant engineers rapidly, accelerating the change management phase.", styles["body"]))

    story.append(Paragraph("Team & Timeline", styles["h1"]))
    for item in [
        "Programme team: 25 consultants (8 OT/IIoT engineers, 6 SAP specialists, 4 data engineers, 7 project leads)",
        "Phase 1 (Pilot — Line 1): 4 months",
        "Phase 2 (Scale — Lines 2 & 3): 10 months",
        "Phase 3 (Optimise & Handover): 4 months",
    ]:
        story.append(bullet(item, styles))


def cs_energy(story, styles):
    header_block(story, styles,
        "Energy Optimisation — Steel Manufacturer",
        "Case Study  |  Jamshedpur, Jharkhand  |  2022",
        "Case Study", "2022")

    story.append(Paragraph("Executive Summary", styles["h1"]))
    story.append(Paragraph(
        "A large integrated steel plant in Jamshedpur partnered with us to reduce energy expenditure "
        "across its hot-rolling, cold-rolling, and furnace operations. By deploying IoT-based energy "
        "monitoring and machine-learning predictive analytics, the plant cut energy costs by 18% and "
        "avoided approximately ₹8 Cr in annual overheads within the first year of operation.", styles["body"]))

    metric_row(story, styles, [
        ("Energy Cost Reduction", "18%"), ("Annual Savings", "₹8 Cr"),
        ("Peak Load Shaved", "12 MW"), ("ROI Period", "14 mo"),
    ])

    story.append(Paragraph("Client Context", styles["h1"]))
    story.append(Paragraph(
        "Energy accounts for approximately 30% of total operating cost at an integrated steel plant. "
        "The client's energy team lacked real-time visibility into consumption patterns and had no "
        "predictive model to anticipate peak demand spikes, leading to high Distribution Company "
        "(DISCOM) penalties and missed demand-response incentives.", styles["body"]))

    story.append(Paragraph("Scope of Work", styles["h1"]))
    for item in [
        "IoT sub-metering across 18 major energy consumers (furnaces, rolling mills, compressors)",
        "Real-time energy dashboard with anomaly alerting and threshold notifications",
        "ML models for peak-load forecasting (LSTM + XGBoost ensemble) with 96% accuracy",
        "Demand-response automation: automated load-shedding of non-critical assets during peak windows",
        "Integration with DISCOM's API for real-time tariff optimisation",
        "Energy Performance Indicator (EnPI) reporting aligned to ISO 50001",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Key Outcomes", styles["h1"]))
    for item in [
        "18% reduction in energy cost per tonne of steel produced",
        "₹8 Cr annual savings — payback achieved in 14 months",
        "12 MW peak demand reduction, eliminating DISCOM overdrawal penalties",
        "Carbon intensity reduced by 14% (Scope 2 emissions), supporting ESG reporting targets",
        "ISO 50001 certification achieved in Month 16 of programme",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Technology Stack", styles["h1"]))
    for item in [
        "IoT Edge: Schneider EcoStruxure Power Monitoring Expert with custom MQTT adapters",
        "Data Platform: Azure Time Series Insights + Azure Data Lake Gen2",
        "ML Platform: Azure ML (training) + Docker-deployed inference APIs",
        "Dashboards: Power BI Premium with DirectQuery connections",
        "Integration: REST API connector to DISCOM demand-response portal",
    ]:
        story.append(bullet(item, styles))


def cs_pred_maintenance(story, styles):
    header_block(story, styles,
        "Predictive Maintenance — FMCG Bottling Plant",
        "Case Study  |  Chennai, Tamil Nadu  |  2023",
        "Case Study", "2023")

    story.append(Paragraph("Executive Summary", styles["h1"]))
    story.append(Paragraph(
        "A leading FMCG company's high-speed PET bottling facility in Chennai was suffering from "
        "frequent unplanned stoppages on its filling and capping lines, eroding throughput and "
        "causing costly emergency maintenance callouts. Our predictive maintenance solution—combining "
        "vibration sensors, thermal imaging, and ML-based failure prediction—reduced unplanned "
        "downtime by 40% and improved overall productivity by 12% within nine months of deployment.", styles["body"]))

    metric_row(story, styles, [
        ("Unplanned Downtime ↓", "40%"), ("Productivity Gain", "12%"),
        ("False Alarm Rate", "<3%"), ("Deployment", "9 mo"),
    ])

    story.append(Paragraph("Client Context", styles["h1"]))
    story.append(Paragraph(
        "The Chennai facility runs six high-speed bottling lines at 36,000 bottles per hour each. "
        "Line stoppages during peak production windows (festival seasons) directly impacted customer "
        "service levels. The maintenance team relied on fixed-schedule preventive maintenance, resulting "
        "in unnecessary part replacements and missed early failure signals.", styles["body"]))

    story.append(Paragraph("Scope of Work", styles["h1"]))
    for item in [
        "Deployment of 380 vibration sensors and 60 thermal imaging cameras across 6 bottling lines",
        "Edge computing nodes (NVIDIA Jetson) for real-time signal processing at line level",
        "ML failure-prediction models trained on 18 months of historical breakdown records",
        "Automated work-order generation integrated with SAP PM upon anomaly detection",
        "Maintenance crew mobile app for alert acknowledgment and root-cause capture",
        "Digital twin of Line 2 for maintenance simulation and spare-part optimisation",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("South India Delivery Context", styles["h1"]))
    story.append(Paragraph(
        "This engagement was delivered from our Chennai centre of excellence, which hosts a dedicated "
        "South India manufacturing practice of 45+ consultants. Local delivery enabled rapid "
        "on-site iteration and deep collaboration with the client's Tamil Nadu-based engineering team, "
        "reducing response time for critical issues to under 2 hours.", styles["body"]))

    story.append(Paragraph("Key Outcomes", styles["h1"]))
    for item in [
        "Unplanned downtime reduced by 40% across all 6 bottling lines",
        "12% productivity improvement translating to additional 2.1 million bottles per month",
        "False alarm rate maintained below 3%, preserving maintenance crew trust in the system",
        "Spare parts inventory cost reduced by ₹1.4 Cr annually through condition-based ordering",
        "System expanded to 2 additional plants in Tamil Nadu within 6 months of initial go-live",
    ]:
        story.append(bullet(item, styles))


def cs_tn_cluster(story, styles):
    header_block(story, styles,
        "Digital Quality Platform — Tamil Nadu Automotive Cluster",
        "Case Study  |  Tamil Nadu, South India  |  2023",
        "Case Study", "2023")

    story.append(Paragraph("Executive Summary", styles["h1"]))
    story.append(Paragraph(
        "We designed and deployed a shared digital platform for a consortium of five Tier-2 auto "
        "component manufacturers in the Tamil Nadu automotive cluster. The cloud-based solution "
        "integrated quality management, supplier tracking, and logistics visibility across 12 plants, "
        "delivering a 25% reduction in customer-facing defects and measurably improved on-time delivery.", styles["body"]))

    metric_row(story, styles, [
        ("Defect Reduction", "25%"), ("OTD Improvement", "18pp"),
        ("Plants Covered", "12"), ("Cluster Partners", "5"),
    ])

    story.append(Paragraph("Client Context", styles["h1"]))
    story.append(Paragraph(
        "The Tamil Nadu automotive cluster supplies critical sub-assemblies to three large OEMs in "
        "Chennai and Pune. OEM quality audits had flagged high inter-plant variability and inadequate "
        "digital traceability. The five-member consortium needed a shared platform that would be "
        "cost-effective for mid-size suppliers while meeting OEM data-sharing requirements.", styles["body"]))

    story.append(Paragraph("Scope of Work", styles["h1"]))
    for item in [
        "Design of a multi-tenant cloud architecture (Azure) supporting 5 independent company tenants",
        "Quality Management System (QMS) module: inspection plans, non-conformance workflow, CAPA tracking",
        "Supply chain visibility layer: real-time shipment tracking and inbound material quality gates",
        "OEM portal: read-only view for OEM quality teams to monitor supplier performance KPIs",
        "Mobile QC app for shop-floor inspection entry (works offline in low-connectivity plants)",
        "Data migration from 5 legacy ERP/QMS systems and paper-based processes",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("South India Manufacturing Expertise", styles["h1"]))
    story.append(Paragraph(
        "Our South India practice has deep familiarity with the Tamil Nadu automotive ecosystem, "
        "including understanding of the supplier-OEM relationships, local regulatory requirements, "
        "and the specific challenges of mid-market manufacturers operating with lean IT teams. "
        "This contextual knowledge was critical in designing a solution with low operational overhead.", styles["body"]))

    story.append(Paragraph("Key Outcomes", styles["h1"]))
    for item in [
        "25% reduction in customer-reported defects across the consortium within 12 months",
        "On-time delivery improved by 18 percentage points (from 74% to 92%)",
        "All 5 OEM quality audits passed with 'green' rating post-implementation",
        "Shared platform economics reduced per-company digital investment by ~60% vs individual systems",
        "Programme recognised by CII Tamil Nadu as a model for SME cluster digitalisation",
    ]:
        story.append(bullet(item, styles))


# ═══════════════════════════════════════════════════════════════════════════
# PROPOSALS
# ═══════════════════════════════════════════════════════════════════════════

def prop_tier1_mes(story, styles):
    header_block(story, styles,
        "MES Implementation Across 3 Plants",
        "Proposal  |  Tier-1 Automotive Supplier, Gurugram  |  2022  |  ₹45 Cr",
        "Proposal", "2022")

    story.append(Paragraph("Executive Summary", styles["h1"]))
    story.append(Paragraph(
        "We propose a comprehensive Manufacturing Execution System rollout across your three Gurugram "
        "plants, integrated with your existing SCADA infrastructure and SAP ERP backbone. Leveraging "
        "our pre-built MES accelerator and dedicated automotive domain team, we commit to a 90-day "
        "Phase 1 go-live on Plant 1—significantly faster than comparable engagements.", styles["body"]))

    story.append(Paragraph("Client Situation", styles["h1"]))
    story.append(Paragraph(
        "As a Tier-1 supplier to three major OEMs, the client faces increasing pressure on quality "
        "traceability, production reporting, and just-in-sequence delivery. Current shop-floor systems "
        "are fragmented—paper-based scheduling, siloed SCADA for press lines, and manual shift logs. "
        "OEM audits in Q2 2022 flagged MES readiness as a critical risk for contract renewal.", styles["body"]))

    story.append(Paragraph("Proposed Scope", styles["h1"]))
    for item in [
        "MES rollout (SAP ME) across Plants 1, 2, and 3 (sequential phased approach)",
        "SCADA integration: real-time machine data feeds into MES production tracking",
        "Shop-floor scheduling and dispatch optimisation module",
        "Quality module: in-process inspection, SPC charts, non-conformance workflows",
        "OEM traceability connector: real-time production genealogy data to OEM portals",
        "SAP ERP integration: production confirmations, material movements, costing",
        "Operator training and hypercare support (3 months post-go-live per plant)",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Our Differentiators vs Infosys & Siemens", styles["h1"]))
    diff = [["Dimension", "Our Proposal", "Infosys", "Siemens SI"],
            ["MES Accelerator", "Pre-built; 40+ adapters", "Custom build", "Siemens-only stack"],
            ["OT/IT Expertise", "Dedicated OT team (in-house)", "IT-led, OT subcontracted", "Strong but expensive"],
            ["Phase 1 Timeline", "90 days (Plant 1)", "5–6 months", "6–8 months"],
            ["Automotive Domain", "12-yr avg. experience", "General mfg.", "Strong (but rigid)"],
            ["Commercial Model", "Fixed-price Phase 1", "T&M", "Fixed, less flexible"],
            ["Total Investment", "₹45 Cr (3 plants)", "₹62 Cr (est.)", "₹70 Cr+ (est.)"]]
    t = Table(diff, colWidths=[4*cm, 4.5*cm, 3.5*cm, 4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), MID_BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [LIGHT_GREY, colors.white]),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Commercial Summary", styles["h1"]))
    for item in [
        "Total contract value: ₹45 Cr (fixed price, 3-plant scope)",
        "Phase 1 (Plant 1): ₹12 Cr, 90-day delivery commitment",
        "Phase 2 (Plants 2 & 3): ₹33 Cr, 18-month delivery",
        "Payment milestones aligned to go-live events (not time-based)",
        "Post-go-live support: included for 3 months per plant; AMS available thereafter",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Why We Win This Deal", styles["h1"]))
    story.append(Paragraph(
        "Our pre-built MES accelerator eliminates months of discovery and custom development. "
        "Our automotive OT team—embedded with clients in Pune, Chennai, and Gurugram—speaks "
        "the language of plant engineers, not IT project managers. The 90-day Phase 1 commitment "
        "is backed by our delivery track record across 7 similar engagements in the past 3 years.", styles["body"]))


def prop_fmcg(story, styles):
    header_block(story, styles,
        "Factory Digitisation — Production Monitoring & OEE Analytics",
        "Proposal  |  Large FMCG Manufacturer, Pan-India  |  2021  |  ₹80 Cr",
        "Proposal", "2021")

    story.append(Paragraph("Executive Summary", styles["h1"]))
    story.append(Paragraph(
        "We propose a phased factory digitisation programme spanning 14 plants across India, "
        "delivering real-time production monitoring, OEE tracking, and quality analytics. "
        "Our Industry 4.0 Maturity Assessment Framework ensures we sequence investments for "
        "maximum ROI—plants at Maturity Level 1 are digitised first; advanced analytics layers "
        "follow once the data foundation is proven.", styles["body"]))

    story.append(Paragraph("Industry 4.0 Maturity Assessment Framework", styles["h1"]))
    story.append(Paragraph(
        "Before recommending technology, we conduct a structured assessment across five dimensions: "
        "Data Infrastructure, Process Standardisation, Workforce Capability, Technology Readiness, "
        "and Leadership Commitment. This produces a plant-level heatmap and a sequenced roadmap "
        "that avoids the 'digital island' trap common in large-scale rollouts.", styles["body"]))

    story.append(Paragraph("Proposed Scope", styles["h1"]))
    for item in [
        "Phase 0 (8 weeks): Maturity assessment across all 14 plants; baseline OEE measurement",
        "Phase 1 (12 months): Pilot digitisation of 3 highest-priority plants (IoT, dashboards, OEE)",
        "Phase 2 (18 months): Scale to remaining 11 plants with learnings from Phase 1",
        "Phase 3 (ongoing): Advanced analytics — predictive quality, demand-driven scheduling",
        "Cross-plant benchmarking dashboard for corporate manufacturing leadership",
        "Change management programme: 2,000+ operators and supervisors across 14 plants",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Our Differentiators", styles["h1"]))
    for item in [
        "Industry 4.0 Maturity Assessment Framework — proprietary, refined across 20+ engagements",
        "Phased rollout model minimises disruption and allows learning before scale",
        "Pre-built FMCG-specific OEE templates (line efficiency, batch tracking, CIL standards)",
        "Embedded hypercare model: resident consultant per plant for first 60 days post-go-live",
        "Proven at scale: delivered similar programme for 2 other top-10 FMCG players in India",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Commercial Summary", styles["h1"]))
    for item in [
        "Total programme value: ₹80 Cr over 3 years",
        "Phase 0 (assessment): ₹3 Cr fixed fee",
        "Phase 1 (3-plant pilot): ₹18 Cr fixed price with guaranteed OEE improvement baseline",
        "Phase 2 (11-plant scale): ₹42 Cr, T&M with capped cost",
        "Phase 3 (advanced analytics): ₹17 Cr; scoped post Phase 2 learnings",
    ]:
        story.append(bullet(item, styles))


def prop_kerala(story, styles):
    header_block(story, styles,
        "Process Optimisation & Compliance Analytics",
        "Proposal  |  Chemical/Process Industry, Kochi, Kerala  |  2022  |  ₹25 Cr",
        "Proposal", "2022")

    story.append(Paragraph("Executive Summary", styles["h1"]))
    story.append(Paragraph(
        "We propose a targeted process optimisation programme for your Kochi specialty chemicals "
        "facility, focused on batch analytics, real-time process parameter monitoring, and "
        "regulatory compliance dashboards. Our process industry domain expertise and prior work "
        "in the Kerala industrial corridor give us a distinct advantage in delivering fast value.", styles["body"]))

    story.append(Paragraph("Client Situation", styles["h1"]))
    story.append(Paragraph(
        "The facility operates 18 batch reactors producing specialty chemicals for the pharma and "
        "agricultural sectors. Batch cycle time variability of ±22% is causing schedule overruns "
        "and raw material wastage. Additionally, Kerala Pollution Control Board (KPCB) compliance "
        "reporting is manual and error-prone, creating regulatory risk.", styles["body"]))

    story.append(Paragraph("South India & Kerala Expertise", styles["h1"]))
    story.append(Paragraph(
        "Our South India practice, headquartered in Chennai with a delivery presence in Kochi, "
        "has delivered three prior engagements in Kerala's process and manufacturing sectors. "
        "We understand KPCB compliance requirements, the availability of local engineering talent, "
        "and the operational culture of process industries in the Kerala industrial corridor.", styles["body"]))

    story.append(Paragraph("Proposed Scope", styles["h1"]))
    for item in [
        "Phase 1: Real-time process monitoring — DCS/SCADA data extraction, historian integration",
        "Phase 2: Batch analytics — cycle-time optimisation models, golden-batch benchmarking",
        "Phase 3: Compliance dashboard — automated KPCB emission and effluent reporting",
        "Alarm rationalisation: reduce nuisance alarms by 60%, prioritise actionable events",
        "Operator advisory system: real-time guidance for batch parameter adjustments",
        "Integration with ERP (Oracle) for production order and material reconciliation",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Commercial Summary", styles["h1"]))
    for item in [
        "Total investment: ₹25 Cr over 20 months",
        "Phase 1 (monitoring foundation): ₹8 Cr, 6-month delivery",
        "Phase 2 (batch analytics): ₹10 Cr, 8-month delivery",
        "Phase 3 (compliance): ₹7 Cr, 6-month delivery",
        "Expected ROI: Payback within 26 months through yield improvement and avoided KPCB penalties",
    ]:
        story.append(bullet(item, styles))


def prop_midmarket(story, styles):
    header_block(story, styles,
        "End-to-End Digital Transformation",
        "Proposal  |  Mid-Market Manufacturing Client, Coimbatore, Tamil Nadu  |  2023  |  ₹150 Cr",
        "Proposal", "2023")

    story.append(Paragraph("Executive Summary", styles["h1"]))
    story.append(Paragraph(
        "We propose a comprehensive 24-month digital transformation programme for your Coimbatore "
        "precision engineering facility—covering ERP modernisation (SAP S/4HANA migration), MES "
        "implementation, advanced analytics, and an organisation-wide change management programme. "
        "This is the largest digital engagement in our South India practice and we are fully "
        "committed to its success with a team of 35 dedicated consultants.", styles["body"]))

    metric_row(story, styles, [
        ("Deal Value", "₹150 Cr"), ("Timeline", "24 mo"),
        ("Team Size", "35"), ("Quick Wins", "90 days"),
    ])

    story.append(Paragraph("Why This Programme Will Succeed", styles["h1"]))
    for item in [
        "Strong executive sponsorship: MD and CFO are programme sponsors with weekly steering reviews",
        "Phased approach: tangible Quick Wins in first 90 days build momentum before the heavy ERP lift",
        "South India delivery: our Coimbatore-based team avoids the coordination tax of a distant delivery centre",
        "Change management baked in from Day 1: dedicated OCM workstream, not a last-minute add-on",
        "Fixed-price Phase 1 reduces financial risk for the client during the critical early phase",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Proposed Scope", styles["h1"]))
    for item in [
        "ERP Modernisation: SAP ERP 6.0 → SAP S/4HANA 2023 migration (Greenfield approach)",
        "MES Layer: Production tracking, quality, maintenance integrated with S/4HANA",
        "Advanced Analytics: Supply chain planning, demand forecasting, cost analytics",
        "Supplier Portal: Digital onboarding and performance tracking for 120+ suppliers",
        "Change Management & Training: 800 employees across all functions",
        "Infrastructure: Cloud migration (Azure) of all on-premise systems",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Programme Structure", styles["h1"]))
    for item in [
        "Phase 0 — Blueprint (Months 1–2): Current-state assessment, future-state design, roadmap sign-off",
        "Phase 1 — Quick Wins (Months 3–5): MES pilot on Line 1, OEE dashboards, supplier portal MVP",
        "Phase 2 — Core Build (Months 6–18): S/4HANA build and test, MES scale, analytics layer",
        "Phase 3 — Go-Live & Hypercare (Months 19–24): Cutover, stabilisation, knowledge transfer",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Commercial Summary", styles["h1"]))
    for item in [
        "Total programme investment: ₹150 Cr over 24 months",
        "Phase 0 (Blueprint): ₹5 Cr — fixed fee, 8-week delivery",
        "Phase 1 (Quick Wins): ₹18 Cr — fixed price",
        "Phase 2 (Core Build): ₹95 Cr — T&M with monthly capped spend and milestone gates",
        "Phase 3 (Go-Live): ₹32 Cr — includes 6-month hypercare and knowledge transfer",
        "Payment: 30% upfront per phase, balance on milestone achievement",
    ]:
        story.append(bullet(item, styles))


# ═══════════════════════════════════════════════════════════════════════════
# WHITEPAPERS
# ═══════════════════════════════════════════════════════════════════════════

def wp_digitalization(story, styles):
    header_block(story, styles,
        "Manufacturing Digitalisation Framework",
        "Thought Leadership Whitepaper  |  Industry 4.0 Practice",
        "Whitepaper", "2023")

    story.append(Paragraph("Abstract", styles["h1"]))
    story.append(Paragraph(
        "Manufacturers across sectors are grappling with how to sequence their Industry 4.0 journey "
        "without over-investing in technology that outpaces organisational readiness. This whitepaper "
        "presents our Manufacturing Digitalisation Framework—a five-dimension maturity model that "
        "helps manufacturers assess their current state, prioritise investments, and build a "
        "connected factory architecture that delivers measurable returns at every stage.", styles["body"]))

    story.append(Paragraph("1. The Industry 4.0 Maturity Model", styles["h1"]))
    story.append(Paragraph(
        "We assess manufacturers across five dimensions, each scored on a 1–5 scale:", styles["body"]))
    for item in [
        "Data Infrastructure: Connectivity from machine to cloud (PLC → Edge → Historian → Data Lake)",
        "Process Standardisation: Digital work instructions, standard operating procedures, quality plans",
        "Workforce Capability: Digital literacy of operators, supervisors, and technical staff",
        "Technology Readiness: ERP, MES, SCADA, and IoT platform modernity and integration readiness",
        "Leadership Commitment: Executive sponsorship quality and digital transformation governance",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("2. The Connected Factory Architecture", styles["h1"]))
    story.append(Paragraph(
        "A Connected Factory is not a single product — it is an architecture of integrated layers:", styles["body"]))
    for item in [
        "Level 0 — Field: Sensors, actuators, PLCs collecting raw process data",
        "Level 1 — Control: SCADA/DCS systems providing real-time process visibility",
        "Level 2 — Operations: MES layer connecting business intent to shop-floor execution",
        "Level 3 — Enterprise: ERP, supply chain, and quality systems driving business decisions",
        "Level 4 — Analytics: BI, ML, and digital twin providing predictive and prescriptive insights",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("3. Digital Twin in Manufacturing", styles["h1"]))
    story.append(Paragraph(
        "A digital twin is a virtual replica of a physical asset, process, or system that updates "
        "in real time from IoT sensor data. In manufacturing, digital twins enable: process simulation "
        "to test changes before physical implementation, root-cause analysis using historical replay, "
        "and predictive what-if modelling for capacity planning and energy optimisation.", styles["body"]))

    story.append(Paragraph("4. Key Adoption Statistics", styles["h1"]))
    for item in [
        "Global smart manufacturing market projected to reach USD 658 billion by 2030 (CAGR 14.5%)",
        "Manufacturing firms with mature digital infrastructure achieve 2.5× higher EBITDA growth",
        "Predictive maintenance adoption reduces unplanned downtime by 30–50% on average",
        "Only 29% of Indian manufacturers have reached Maturity Level 3 or above (2023 survey, n=340)",
        "ROI payback period for connected factory programmes: median 18–24 months",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("5. Recommended Transformation Roadmap", styles["h1"]))
    story.append(Paragraph(
        "Regardless of starting point, we recommend a consistent sequencing: (1) Baseline with data "
        "infrastructure and connectivity; (2) Quick wins through OEE dashboards and anomaly alerting; "
        "(3) Optimise with ML-based predictive models; (4) Integrate across the value chain with "
        "supplier and customer digital interfaces; (5) Innovate with digital twins and autonomous "
        "operations. Skipping steps creates technical debt that is expensive to unwind.", styles["body"]))


def wp_esg(story, styles):
    header_block(story, styles,
        "Digital Enablement for ESG Compliance in Manufacturing",
        "Thought Leadership Whitepaper  |  Sustainability Practice",
        "Whitepaper", "2023")

    story.append(Paragraph("Abstract", styles["h1"]))
    story.append(Paragraph(
        "ESG reporting is rapidly transitioning from voluntary to mandatory for large Indian "
        "manufacturers, driven by SEBI's BRSR framework, OEM supply-chain requirements, and "
        "international investor expectations. This whitepaper examines how digital tools — IoT "
        "energy monitoring, waste analytics, and integrated compliance dashboards — enable "
        "manufacturers to move from ad-hoc ESG reporting to real-time, auditable sustainability metrics.", styles["body"]))

    story.append(Paragraph("1. The ESG Reporting Imperative", styles["h1"]))
    story.append(Paragraph(
        "India's Business Responsibility and Sustainability Report (BRSR) requirement now applies "
        "to the top 1,000 listed companies by market capitalisation. Supply chain ESG expectations "
        "are cascading further: automotive and FMCG OEMs are requiring Tier-1 and Tier-2 suppliers "
        "to report Scope 3 emissions data, energy intensity, and water usage. "
        "Manufacturers that cannot provide this data risk losing contracts.", styles["body"]))

    story.append(Paragraph("2. Key ESG Metrics in Manufacturing", styles["h1"]))
    story.append(Paragraph("Energy & Carbon:", styles["h2"]))
    for item in [
        "Energy intensity (GJ per tonne of production) — Scope 1 & 2 emissions tracking",
        "Renewable energy percentage — solar, wind, and green tariff procurement",
        "Carbon footprint tracking aligned to GHG Protocol and ISO 14064",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("Waste & Water:", styles["h2"]))
    for item in [
        "Solid waste generation and recycling rates by category",
        "Effluent treatment performance: BOD, COD, heavy metals against consent limits",
        "Water intensity (kL per unit of production) and water recycling percentage",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("3. Digital Tools for ESG Enablement", styles["h1"]))
    for item in [
        "IoT sub-metering: automatic, granular energy data by asset, line, and building",
        "Waste tracking systems: digital records replacing manual logbooks for CPCB/SPCB compliance",
        "EHS Management Systems: incident tracking, compliance calendar, permit management",
        "ESG Dashboards: real-time BRSR KPIs, audit-ready data export, trend analysis",
        "Carbon accounting software: automatic Scope 1, 2, 3 calculation from operational data",
    ]:
        story.append(bullet(item, styles))

    story.append(Paragraph("4. Suggested Use in Sales Conversations", styles["h1"]))
    story.append(Paragraph(
        "Use this whitepaper to open ESG-adjacent conversations with CFOs and sustainability heads "
        "at large manufacturers. Key conversation hooks: (1) BRSR compliance deadline pressure — "
        "many clients do not yet have auditable digital records; (2) OEM supply-chain ESG requirements "
        "— this is an immediate revenue risk for Tier-1 and Tier-2 suppliers; (3) Cost reduction "
        "framing — energy monitoring pays for itself through consumption reduction before ESG "
        "compliance value is even counted.", styles["body"]))

    story.append(Paragraph("5. Our ESG Digital Capability", styles["h1"]))
    for item in [
        "Carbon footprint baseline assessments completed for 14 manufacturing clients since 2021",
        "IoT-based energy monitoring deployed at 8 facilities, average energy saving of 16%",
        "ESG compliance dashboards live at 6 clients across automotive, FMCG, and process industries",
        "Partnerships with leading carbon accounting platforms for data integration",
        "ISO 14001 and ISO 50001 implementation support available as an add-on service",
    ]:
        story.append(bullet(item, styles))


# ═══════════════════════════════════════════════════════════════════════════
# PITCH DECKS  (PPTX)
# ═══════════════════════════════════════════════════════════════════════════

def hex_rgb(h):
    h = h.lstrip("#")
    return RGBColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

def add_slide(prs, layout_idx=1):
    return prs.slides.add_slide(prs.slide_layouts[layout_idx])

def set_slide_bg(slide, hex_color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = hex_rgb(hex_color)

def add_text_box(slide, text, left, top, width, height,
                  font_size=18, bold=False, color="#f1f5f9",
                  align=PP_ALIGN.LEFT, wrap=True):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = hex_rgb(color)
    return txBox

def add_bullet_box(slide, items, left, top, width, height,
                    font_size=14, color="#cbd5e1", bullet_color="#1d4ed8"):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = f"  •  {item}"
        run.font.size = Pt(font_size)
        run.font.color.rgb = hex_rgb(color)

def build_pitch_i40(path):
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    slides_data = [
        # (title, subtitle_or_body, bullet_items)
        ("Industry 4.0 Capabilities",
         "AI-Powered Sales Knowledge Assistant — Sales Co-Pilot Platform",
         []),
        ("Who We Are",
         "A leading technology consulting firm specialising in industrial digitalisation for manufacturing, "
         "process, and energy sectors across India and South-East Asia.",
         ["Founded 2008  |  2,400+ consultants  |  18 offices",
          "₹3,200 Cr revenue (FY2023)  |  Listed on NSE",
          "Deep OT/IT convergence expertise — not just IT consulting",
          "South India practice: 300+ consultants in Chennai, Coimbatore, Kochi"]),
        ("Our Industry 4.0 Service Portfolio",
         "End-to-end manufacturing digitalisation across the full stack.",
         ["Connected Factory & IoT: sensor deployment, edge computing, OT networking",
          "MES & SCADA: implementation, integration, modernisation",
          "ERP for Manufacturing: SAP S/4HANA, Oracle Cloud",
          "Advanced Analytics & AI: predictive maintenance, quality ML, demand forecasting",
          "Digital Twin: process simulation, capacity planning, maintenance optimisation",
          "ESG & Sustainability: energy monitoring, carbon accounting, BRSR reporting"]),
        ("Key Differentiators",
         "Why we win against larger SIs and product vendors.",
         ["Pre-built Industry 4.0 Accelerator: 40+ reusable adapters, 60% faster integration",
          "Dedicated OT Engineering Team (in-house): no subcontracting of shop-floor work",
          "Automotive Domain Depth: avg 12 yrs experience per senior consultant",
          "South India Manufacturing Expertise: Tamil Nadu, Kerala, Karnataka delivery presence",
          "Fixed-Price Phase 1 Commitment: de-risks early investment for the client",
          "Proven Scale: 85+ manufacturing clients, 200+ plant-level deployments"]),
        ("Client References (Anonymised)",
         "Track record across Tier-1 automotive, FMCG, steel, and specialty chemicals.",
         ["Automotive OEM (Pune): Smart factory — 22% OEE improvement, ₹12 Cr savings",
          "Steel Plant (Jamshedpur): Energy optimisation — 18% cost reduction, ₹8 Cr saved",
          "FMCG Bottling (Chennai): Predictive maintenance — 40% downtime reduction",
          "TN Auto Cluster: Quality platform — 25% defect reduction across 5 suppliers",
          "Mid-Market Mfg (Coimbatore): End-to-end transformation — ₹150 Cr programme"]),
        ("Technology Partnerships",
         "Certified and preferred partner status with leading technology providers.",
         ["Microsoft Azure: Gold Manufacturing Partner  |  3,200+ certifications",
          "SAP: Platinum Partner for ME / S/4HANA Manufacturing",
          "Siemens: Approved System Integrator for MindSphere & Opcenter",
          "PTC: ThingWorx and Windchill implementation partner",
          "NVIDIA: Edge AI partner for predictive maintenance and vision applications",
          "Rockwell Automation: FactoryTalk integration partner"]),
        ("Our South India Practice",
         "Dedicated manufacturing practice covering Tamil Nadu, Kerala, Andhra Pradesh, Karnataka.",
         ["300+ consultants based in South India",
          "Chennai CoE: IoT, MES, SAP for manufacturing",
          "Coimbatore hub: Precision engineering & auto components sector",
          "Kochi presence: Process industry and Kerala industrial corridor",
          "Completed 45+ engagements in South India manufacturing since 2015",
          "Local hiring & training: 60% of team from South Indian engineering colleges"]),
        ("Engagement Models",
         "Flexible commercial structures to match client appetite and risk tolerance.",
         ["Fixed-Price Pilot: Quick wins in 90 days, fully scoped and costed",
          "Phased T&M: Flexibility for complex transformations with monthly governance",
          "Outcome-Based: Shared gain models tied to OEE, energy, or quality KPIs",
          "Managed Services: Post-go-live AMS with SLA-backed support",
          "Staff Augmentation: Senior OT/IT consultants on-site or hybrid"]),
        ("Contact & Next Steps",
         "Ready to start the conversation?",
         ["Request an Industry 4.0 Maturity Assessment (complimentary, 2-week engagement)",
          "Review our case study library at [internal portal]",
          "Schedule a workshop: 'What does Industry 4.0 mean for your plants?'",
          "Contact: South India Practice Head — industry4.south@company.in"]),
    ]

    for i, (title, body, bullets) in enumerate(slides_data):
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
        set_slide_bg(slide, "#020617" if i == 0 else "#0f172a")

        # Left accent bar
        bar = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.08), Inches(7.5))
        bar.fill.solid()
        bar.fill.fore_color.rgb = hex_rgb("#1d4ed8")
        bar.line.fill.background()

        # Slide number
        add_text_box(slide, f"{i+1}", 12.8, 7.1, 0.4, 0.3,
                     font_size=9, color="#334155", align=PP_ALIGN.RIGHT)

        if i == 0:
            # Title slide
            add_text_box(slide, "INDUSTRY 4.0 CAPABILITIES", 0.4, 1.6, 9, 0.5,
                         font_size=11, color="#1d4ed8", bold=True)
            add_text_box(slide, title, 0.4, 2.1, 9, 1.4,
                         font_size=36, bold=True, color="#f1f5f9")
            add_text_box(slide, "2023", 0.4, 3.5, 2, 0.5,
                         font_size=14, color="#64748b")
            add_text_box(slide, "Manufacturing & Industry 4.0 Practice", 0.4, 6.8, 8, 0.5,
                         font_size=11, color="#334155")
        else:
            add_text_box(slide, title, 0.4, 0.3, 11, 0.7,
                         font_size=22, bold=True, color="#f1f5f9")
            # Divider
            line = slide.shapes.add_shape(1, Inches(0.4), Inches(1.1), Inches(12.5), Inches(0.02))
            line.fill.solid(); line.fill.fore_color.rgb = hex_rgb("#1e293b"); line.line.fill.background()

            add_text_box(slide, body, 0.4, 1.2, 12.3, 1.0,
                         font_size=13, color="#94a3b8")
            if bullets:
                add_bullet_box(slide, bullets, 0.4, 2.4, 12.3, 4.5, font_size=14)

    prs.save(str(path))
    print(f"  ✓  {path.name}")


def build_pitch_smart_mfg(path):
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    slides_data = [
        ("Smart Manufacturing Overview",
         "Intelligent Operations for the Modern Factory Floor", []),
        ("What Is Smart Manufacturing?",
         "Smart Manufacturing is the convergence of OT (Operational Technology) and IT (Information Technology) "
         "to create self-optimising, data-driven factory operations.",
         ["Real-time visibility from machine to boardroom",
          "Predictive instead of reactive maintenance",
          "Closed-loop quality control driven by data",
          "Flexible, demand-driven production scheduling",
          "Continuous improvement embedded in digital workflows"]),
        ("Smart Manufacturing Architecture",
         "A layered architecture connects every asset to business insight.",
         ["Layer 1 — Sense: IoT sensors, vision cameras, RFID, edge gateways",
          "Layer 2 — Connect: Industrial protocols (OPC-UA, MQTT), secure OT networking",
          "Layer 3 — Analyse: Historian, time-series DB, ML platform, rule engines",
          "Layer 4 — Act: MES, ERP, advanced planning, operator advisory systems",
          "Layer 5 — Optimise: Digital twins, autonomous adjustments, continuous learning"]),
        ("Our Smart Manufacturing Offerings",
         "Tailored solutions across the smart factory stack.",
         ["Connected Factory Foundation: IoT connectivity, edge infrastructure, data lake",
          "Real-Time OEE & Production Monitoring: live dashboards, shift reporting, loss analysis",
          "Predictive Quality: ML models for defect detection, SPC automation, supplier quality",
          "Predictive Maintenance: vibration, thermal, ML-based failure prediction",
          "Smart Energy Management: sub-metering, peak management, carbon monitoring",
          "Integrated Planning: MES-ERP integration, demand-driven scheduling"]),
        ("Case Study Highlights",
         "Delivered outcomes across automotive, FMCG, steel, and process industries.",
         ["Automotive OEM (Pune, 2023): Smart factory → 22% OEE improvement, ₹12 Cr savings",
          "FMCG Bottling (Chennai, 2023): Predictive maintenance → 40% unplanned downtime reduction",
          "Steel Plant (Jamshedpur, 2022): Energy monitoring → 18% energy cost reduction",
          "TN Auto Cluster (2023): Quality platform → 25% defect reduction, 12 plants",
          "Mid-Market Mfg (Coimbatore, 2023): Full transformation → ₹150 Cr programme"]),
        ("Why Our Clients Choose Us",
         "Differentiation that matters at the factory gate.",
         ["Pre-built accelerators: 40% faster deployment vs custom approaches",
          "OT expertise in-house: no subcontracting of the critical shop-floor layer",
          "Outcome-based models: we share the risk on measurable improvements",
          "South India presence: on-site support within hours, not days",
          "Post-go-live continuity: same team stays through hypercare and AMS"]),
        ("Delivery Approach",
         "Proven phased methodology that minimises risk and accelerates value.",
         ["Week 1–4: Discovery & baseline — assess plants, map data sources, agree KPIs",
          "Week 5–12: Pilot — deploy on 1 line or 1 plant, prove value, tune models",
          "Month 4–12: Scale — roll out across all plants with learnings from pilot",
          "Month 12+: Optimise — advanced analytics, digital twin, autonomous features",
          "Throughout: Change management, training, and hypercare support"]),
        ("Next Steps",
         "Start with a Smart Manufacturing Readiness Assessment.",
         ["2-week assessment: evaluate connectivity, data, process, and workforce readiness",
          "Output: maturity scorecard, prioritised roadmap, ROI estimate",
          "No commitment required — assessment stands alone as a deliverable",
          "Typical assessment team: 2 senior consultants, 1 domain architect",
          "Contact: smartmfg@company.in  |  South India: +91 44 XXXX XXXX"]),
    ]

    for i, (title, body, bullets) in enumerate(slides_data):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_slide_bg(slide, "#020617" if i == 0 else "#0f172a")

        bar = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.08), Inches(7.5))
        bar.fill.solid(); bar.fill.fore_color.rgb = hex_rgb("#7c3aed"); bar.line.fill.background()

        add_text_box(slide, f"{i+1}", 12.8, 7.1, 0.4, 0.3,
                     font_size=9, color="#334155", align=PP_ALIGN.RIGHT)

        if i == 0:
            add_text_box(slide, "SMART MANUFACTURING PRACTICE", 0.4, 1.6, 9, 0.5,
                         font_size=11, color="#7c3aed", bold=True)
            add_text_box(slide, title, 0.4, 2.1, 9, 1.4,
                         font_size=36, bold=True, color="#f1f5f9")
            add_text_box(slide, "2023", 0.4, 3.5, 2, 0.5, font_size=14, color="#64748b")
        else:
            add_text_box(slide, title, 0.4, 0.3, 11, 0.7,
                         font_size=22, bold=True, color="#f1f5f9")
            line = slide.shapes.add_shape(1, Inches(0.4), Inches(1.1), Inches(12.5), Inches(0.02))
            line.fill.solid(); line.fill.fore_color.rgb = hex_rgb("#1e293b"); line.line.fill.background()
            add_text_box(slide, body, 0.4, 1.2, 12.3, 1.1, font_size=13, color="#94a3b8")
            if bullets:
                add_bullet_box(slide, bullets, 0.4, 2.5, 12.3, 4.2, font_size=14)

    prs.save(str(path))
    print(f"  ✓  {path.name}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("Generating test documents...")

    PDFS = [
        ("Case Study - Smart Factory Automotive OEM 2023.pdf",    cs_smart_factory),
        ("Case Study - Energy Optimization 2022.pdf",             cs_energy),
        ("Case Study - Predictive Maintenance 2023.pdf",          cs_pred_maintenance),
        ("Case Study - Tamil Nadu Automotive Cluster 2023.pdf",   cs_tn_cluster),
        ("Proposal - Tier1 Auto Supplier MES Implementation 2022.pdf", prop_tier1_mes),
        ("Proposal - FMCG Manufacturer Digitization 2021.pdf",    prop_fmcg),
        ("Proposal - Kerala Process Industry 2022.pdf",           prop_kerala),
        ("Proposal - Mid Market Manufacturing Client 2023.pdf",   prop_midmarket),
        ("Whitepaper - Manufacturing Digitalization Framework.pdf", wp_digitalization),
        ("Whitepaper - Digital Enablement for ESG Compliance.pdf", wp_esg),
    ]

    for fname, fn in PDFS:
        build_pdf(fname, fn)

    build_pitch_i40(OUT / "Pitch Deck - Industry 4.0 Capabilities 2023.pptx")
    build_pitch_smart_mfg(OUT / "Pitch Deck - Smart Manufacturing Overview.pptx")

    print(f"\nDone! {len(PDFS) + 2} files in ./{OUT}/")
    print("Upload the ./documents/ folder contents to your shared Google Drive folder.")

if __name__ == "__main__":
    main()
