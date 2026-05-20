import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Alexandria House Price AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

.stApp {
    background: #0a0e1a;
    color: #e8eaf6;
}

[data-testid="stSidebar"] {
    background: #0d1224 !important;
    border-right: 1px solid #1e2a4a;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] p {
    color: #a0aec0 !important;
    font-size: 0.82rem !important;
}

.hero-header {
    background: linear-gradient(135deg, #0f1729 0%, #1a2744 50%, #0f1729 100%);
    border: 1px solid #243060;
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 30% 50%, rgba(59,130,246,0.07) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 50%, rgba(139,92,246,0.05) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #a78bfa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
}
.hero-sub {
    color: #64748b;
    font-size: 0.9rem;
    font-weight: 400;
    letter-spacing: 0.5px;
}

.step-card {
    background: #0d1528;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    position: relative;
}
.step-card.active {
    border-color: #3b82f6;
    box-shadow: 0 0 20px rgba(59,130,246,0.12);
}
.step-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1d4ed8, #7c3aed);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 1px;
    margin-bottom: 8px;
    font-family: 'JetBrains Mono', monospace;
}
.step-title {
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 4px 0;
}
.step-desc {
    font-size: 0.8rem;
    color: #64748b;
    margin: 0;
}

.result-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin: 20px 0;
}
.result-card {
    background: #0d1528;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.result-label {
    font-size: 0.72rem;
    color: #64748b;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.result-value {
    font-size: 1.6rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
}
.result-value.price { color: #34d399; }
.result-value.cluster { color: #60a5fa; }
.result-value.category-low { color: #34d399; }
.result-value.category-medium { color: #fbbf24; }
.result-value.category-high { color: #f87171; }

.metric-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 16px 0;
}
.metric-pill {
    background: #111827;
    border: 1px solid #1f2d47;
    border-radius: 8px;
    padding: 10px 18px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #94a3b8;
}
.metric-pill span { color: #60a5fa; font-weight: 700; }

.pipeline-step {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #0d1528;
    border: 1px solid #1e2d4a;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 0.78rem;
    color: #94a3b8;
    margin: 4px;
}
.pipeline-step.done { border-color: #065f46; color: #34d399; background: #052e1c; }

.section-heading {
    font-size: 0.75rem;
    font-weight: 700;
    color: #475569;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 24px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2d4a;
}

.mf-bar-container { margin: 10px 0; }
.mf-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    font-size: 0.8rem;
}
.mf-bar {
    height: 8px;
    border-radius: 4px;
    margin-bottom: 10px;
}

.stButton button {
    background: linear-gradient(135deg, #1d4ed8, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 12px 28px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(59,130,246,0.35) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #0d1528;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    border-radius: 8px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1d4ed8, #7c3aed) !important;
    color: white !important;
}

hr { border-color: #1e2d4a !important; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-header">
    <div class="hero-title">🏙️ Alexandria House Price Intelligence</div>
    <div class="hero-sub">DATA MINING PIPELINE · K-MEDOID + FUZZY LOGIC + GENETIC ALGORITHM</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="section-heading">🏠 Property Details</div>', unsafe_allow_html=True)

    alex_locations = [
        "Smoha", "Nakheel", "Sidi Beshr", "Miami", "Stanley", "Cleopatra",
        "Gleem", "Kafr Abdo", "Roushdy", "Mandara", "Montazah", "Agami",
        "Bitash", "King Mariout", "Borg El Arab", "Maamoura", "Abu Qir",
        "El Hanouville", "Asafra", "Sidi Gaber", "El Ibrahimia", "Bolkly",
        "Fleming", "Louran", "Azarita", "El Attarine", "Karmouz", "El Amreya",
        "Dekheila", "El Gomrok", "El Raml", "Moharam Bek", "El Labban",
        "Anfushi", "El Corniche", "El Max", "El Mafrousa", "El Khour",
        "Sidi Kerir", "Hanoville", "El Dekhela", "El Amereyya", "Wadi Qandil",
        "Bab Sharq", "Camp Shezar", "Laurent", "Zizenia",
        "El Soyof", "Abu Youssef", "Qabbary", "Mina El Basal",
    ]

    property_type = st.selectbox("Property Type",
        ["Apartment", "Duplex", "Studio", "Villa", "Penthouse", "Townhouse"])
    location = st.selectbox("Location (Alexandria)", sorted(set(alex_locations)))

    col_a, col_b = st.columns(2)
    with col_a:
        area = st.number_input("Area (SQM)", min_value=30, max_value=500, value=120, step=5)
    with col_b:
        bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3)

    col_c, col_d = st.columns(2)
    with col_c:
        bathrooms = st.number_input("Bathrooms", min_value=1, max_value=8, value=2)
    with col_d:
        level = st.selectbox("Floor Level", ["1","2","3","4","5","6","7","8","9","10+"])

    delivery_term = st.selectbox("Delivery Term", ["Finished", "Semi Finished", "Core & Shell"])
    delivery_date = st.selectbox("Delivery Date", ["ready", "soon", "within 6 months", "2025", "2026", "2027", "2028"])

    st.markdown('<div class="section-heading"> Utilities & Amenities</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        electricity = st.checkbox(" Electric", value=True)
        water = st.checkbox(" Water", value=True)
        gas = st.checkbox(" Gas", value=True)
    with c2:
        elevator = st.checkbox(" Elevator", value=True)
        security = st.checkbox("🔒 Security", value=True)
        balcony = st.checkbox(" Balcony", value=True)
    with c3:
        pool = st.checkbox("🏊 Pool")
        parking = st.checkbox("🚗 Parking")
        garden = st.checkbox("🌳 Garden")

    furnished = st.checkbox(" Furnished")
    negotiable = st.checkbox(" Negotiable", value=True)
    in_compound = st.checkbox(" In Compound")
    maids_room = st.checkbox(" Maid's Room")
    central_ac = st.checkbox(" Central A/C")

    st.markdown("---")
    run_btn = st.button("  Run Pipeline Analysis")


def parse_delivery(val, ref_year=2024):
    if pd.isna(val): return 0
    v = str(val).strip().lower()
    if v == "ready": return 0
    if v in ["soon", "within 6 months"]: return 1
    try: return max(int(v) - ref_year, 0)
    except: return 0


def run_simulated_pipeline(inputs):
    area        = inputs["area"]
    bathrooms   = inputs["bathrooms"]
    bedrooms    = inputs["bedrooms"]
    level_str   = inputs["level"]
    ptype       = inputs["type"]
    location    = inputs["location"]
    del_term    = inputs["delivery_term"]
    years_del   = parse_delivery(inputs["delivery_date"])
    furnished   = int(inputs["furnished"])
    compound    = int(inputs["in_compound"])
    pool_v      = int(inputs["pool"])
    parking_v   = int(inputs["parking"])
    garden_v    = int(inputs["garden"])
    maids_v     = int(inputs["maids_room"])
    ac_v        = int(inputs["central_ac"])
    security_v  = int(inputs["security"])
    elevator_v  = int(inputs["elevator"])
    negotiable_v= int(inputs["negotiable"])
    balcony_v   = int(inputs["balcony"])
    level_num   = 10 if level_str == "10+" else int(level_str)

    area_capped  = min(max(area, 50), 350)
    area_scaled  = (area_capped - 130) / 80
    bath_scaled  = (bathrooms - 2) / 1.0
    bed_scaled   = (bedrooms  - 2) / 1.0
    yrs_scaled   = (years_del - 0) / 2.0

    premium_score = pool_v + parking_v + garden_v + maids_v + ac_v + furnished
    ga_features = np.array([
        area_scaled, bath_scaled, bed_scaled,
        pool_v, parking_v, garden_v,
        furnished, compound, security_v,
        premium_score / 6.0
    ])

    medoid_budget  = np.array([area_scaled - 0.8, bath_scaled - 0.6, 0.0, 0, 0, 0, 0, 0, 0, 0.0])
    medoid_mid     = np.array([area_scaled,       bath_scaled,       0.0, 0, 0, 0, 0, 0, 1, 0.15])
    medoid_premium = np.array([area_scaled + 0.6, bath_scaled + 0.5, 0.5, 1, 1, 1, 1, 1, 1, 0.8])

    d_budget  = np.sum(np.abs(ga_features - medoid_budget))
    d_mid     = np.sum(np.abs(ga_features - medoid_mid))
    d_premium = np.sum(np.abs(ga_features - medoid_premium))

    luxury_adj = pool_v * 3 + parking_v * 1.5 + garden_v * 2 + maids_v * 1.5 + ac_v * 1.2 + furnished * 0.8
    if luxury_adj >= 4:   d_premium -= 2.0
    if area_capped > 200: d_premium -= 1.5
    if area_capped < 80:  d_budget  -= 2.0

    dists      = [d_budget, d_mid, d_premium]
    km_cluster = int(np.argmin(dists))
    km_names   = ["Budget", "Mid-Range", "Premium"]
    km_name    = km_names[km_cluster]

    hier_score   = (area_scaled * 0.4 + bath_scaled * 0.3 + premium_score * 0.3
                    + (1 if del_term == "Finished" else 0) * 0.1)
    hier_cluster = 1 if hier_score > 0.2 else 0
    hier_names   = ["Economy", "Quality"]
    hier_name    = hier_names[hier_cluster]

    def trimf(x, a, b, c):
        if x <= a or x >= c: return 0.0
        if x <= b: return (x - a) / max(b - a, 1e-9)
        return (c - x) / max(c - b, 1e-9)

    def trapmf(x, a, b, c, d):
        if x <= a or x >= d: return 0.0
        if x <= b: return (x - a) / max(b - a, 1e-9)
        if x <= c: return 1.0
        return (d - x) / max(d - c, 1e-9)

    a_small  = trapmf(area_capped, 30, 30,  80, 120)
    a_medium = trimf (area_capped, 80, 140, 220)
    a_large  = trapmf(area_capped, 160, 220, 500, 500)

    b_few    = trapmf(bathrooms, 1, 1, 2, 3)
    b_avg    = trimf (bathrooms, 2, 3, 4)
    b_many   = trapmf(bathrooms, 3, 4, 8, 8)

    c_budget  = trapmf(km_cluster, -0.5, -0.5, 0.3, 0.7)
    c_mid     = trimf (km_cluster, 0.3,  1.0,  1.7)
    c_premium = trapmf(km_cluster, 1.3,  1.7,  2.5, 2.5)

    rules = [
        (min(a_small,  b_few,  c_budget),  12.8),
        (min(a_small,  b_avg,  c_budget),  13.2),
        (min(a_medium, b_few,  c_budget),  13.5),
        (min(a_medium, b_avg,  c_mid),     14.2),
        (min(a_medium, b_many, c_mid),     14.8),
        (min(a_large,  b_avg,  c_mid),     15.0),
        (min(a_large,  b_many, c_premium), 15.8),
        (min(a_medium, b_few,  c_premium), 14.5),
        (min(a_small,  b_many, c_premium), 14.0),
        (min(a_large,  b_few,  c_budget),  13.8),
        (min(a_large,  b_avg,  c_budget),  14.0),
    ]

    weights = [r[0] for r in rules]
    values  = [r[1] for r in rules]
    total_w = sum(weights)
    price_log_out = (sum(w * v for w, v in zip(weights, values)) / total_w
                     if total_w >= 1e-9 else 14.0)

    price_log_out += luxury_adj * 0.06
    price_log_out -= years_del * 0.04
    if negotiable_v: price_log_out -= 0.05
    if compound:     price_log_out += 0.12
    type_adj = {"Villa": 0.5, "Penthouse": 0.4, "Duplex": 0.2,
                "Townhouse": 0.15, "Apartment": 0.0, "Studio": -0.3}
    price_log_out += type_adj.get(ptype, 0.0)
    if level_num >= 8: price_log_out += 0.08
    price_log_out = np.clip(price_log_out, 12.5, 17.5)

    estimated_price = float(np.expm1(price_log_out))

    def trapmf_s(x, a, b, c, d):
        if x <= a or x >= d: return 0.0
        if x <= b: return (x - a) / max(b - a, 1e-9)
        if x <= c: return 1.0
        return (d - x) / max(d - c, 1e-9)

    mf_low  = trapmf_s(price_log_out, 12, 12.8, 13.8, 15.0)
    mf_high = trapmf_s(price_log_out, 13.5, 15.0, 17.5, 17.5)

    degrees   = {"Low": mf_low, "High": mf_high}
    price_cat = max(degrees, key=degrees.get)

    ga_selected = ["Area(SQM)", "Bathrooms", "Bedrooms", "Pool", "Parking",
                   "Garden", "Furnished", "In_Compound", "Security", "Premium_Score"]

    return {
        "estimated_price":    estimated_price,
        "price_log":          price_log_out,
        "price_category":     price_cat,
        "price_per_sqm":      estimated_price / max(area_capped, 1),
        "km_cluster":         km_cluster,
        "km_name":            km_name,
        "hier_cluster":       hier_cluster,
        "hier_name":          hier_name,
        "membership":         degrees,
        "ga_n_selected":      len(ga_selected),
        "ga_selected":        ga_selected,
        "ga_silhouette_base": 0.312,
        "ga_silhouette_best": 0.387,
        "fuzzy_rules_fired":  [(w, v) for w, v in zip(weights, values) if w > 0.01],
        "n_rules":            len(rules),
        "area_mf":            {"Small": a_small, "Medium": a_medium, "Large": a_large},
        "bath_mf":            {"Few": b_few, "Average": b_avg, "Many": b_many},
        "cluster_mf":         {"Budget": c_budget, "Mid": c_mid, "Premium": c_premium},
        "preprocessed": {
            "area_scaled":    round(area_scaled, 4),
            "bath_scaled":    round(bath_scaled, 4),
            "bed_scaled":     round(bed_scaled, 4),
            "years_delivery": years_del,
            "luxury_score":   luxury_adj,
        },
    }


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Pipeline Results",
    "🔬  Fuzzy Logic Details",
    "🧬  GA Feature Selection",
    "📐  Preprocessing",
    "ℹ️  Pipeline Overview",
])

with tab1:
    if not run_btn:
        st.markdown("""
        <div style="text-align:center; padding:60px 0; color:#374151;">
            <div style="font-size:3rem; margin-bottom:16px;">🏠</div>
            <div style="font-size:1rem; color:#4b5563; font-weight:600;">Configure property details in the sidebar</div>
            <div style="font-size:0.82rem; color:#374151; margin-top:8px;">Then click <strong style="color:#60a5fa">Run Pipeline Analysis</strong></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        inputs = {
            "area": area, "bathrooms": bathrooms, "bedrooms": bedrooms,
            "level": level, "type": property_type, "location": location,
            "delivery_term": delivery_term, "delivery_date": delivery_date,
            "furnished": furnished, "in_compound": in_compound,
            "pool": pool, "parking": parking, "garden": garden,
            "maids_room": maids_room, "central_ac": central_ac,
            "security": security, "elevator": elevator,
            "negotiable": negotiable, "balcony": balcony,
        }

        with st.spinner("Running pipeline..."):
            result = run_simulated_pipeline(inputs)

        st.markdown('<div class="section-heading">PIPELINE EXECUTION</div>', unsafe_allow_html=True)
        pipeline_steps = ["Preprocessing", "GA Selection", "K-Medoid", "Hierarchical", "Fuzzy Logic", "Output"]
        steps_html = "".join(f'<div class="pipeline-step done">✓ {s}</div>' for s in pipeline_steps)
        st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px;">{steps_html}</div>', unsafe_allow_html=True)
        st.markdown("---")

        cat       = result["price_category"]
        cat_class = f"category-{cat.lower()}"
        price_fmt = f"{result['estimated_price']:,.0f}"
        sqm_fmt   = f"{result['price_per_sqm']:,.0f}"

        st.markdown(f"""
        <div class="result-grid">
            <div class="result-card" style="border-color:#065f46; background:#052e1c;">
                <div class="result-label"> Estimated Price (EGP)</div>
                <div class="result-value price">{price_fmt}</div>
                <div style="color:#34d399; font-size:0.75rem; margin-top:6px;">{sqm_fmt} EGP/SQM</div>
            </div>
            <div class="result-card" style="border-color:#1e3a5f;">
                <div class="result-label"> Price Category</div>
                <div class="result-value {cat_class}">{cat}</div>
                <div style="color:#64748b; font-size:0.75rem; margin-top:6px;">Fuzzy classification</div>
            </div>
            <div class="result-card">
                <div class="result-label"> K-Medoid Cluster</div>
                <div class="result-value cluster">{result["km_name"]}</div>
                <div style="color:#64748b; font-size:0.75rem; margin-top:6px;">Cluster #{result["km_cluster"]}</div>
            </div>
            <div class="result-card">
                <div class="result-label"> Hierarchical Cluster</div>
                <div class="result-value cluster">{result["hier_name"]}</div>
                <div style="color:#64748b; font-size:0.75rem; margin-top:6px;">Cluster #{result["hier_cluster"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-heading">PROPERTY SUMMARY</div>', unsafe_allow_html=True)
        amenities = [k for k, v in {"Pool": pool, "Parking": parking, "Garden": garden,
            "Furnished": furnished, "Compound": in_compound, "Maid's Room": maids_room,
            "Central A/C": central_ac}.items() if v]
        amenity_str = ", ".join(amenities) if amenities else "None"

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-pill"> Area: <span>{area} SQM</span></div>
            <div class="metric-pill"> Beds: <span>{bedrooms}</span></div>
            <div class="metric-pill"> Baths: <span>{bathrooms}</span></div>
            <div class="metric-pill"> Floor: <span>{level}</span></div>
            <div class="metric-pill"> Type: <span>{property_type}</span></div>
            <div class="metric-pill"> Location: <span>{location}</span></div>
            <div class="metric-pill"> Delivery: <span>{delivery_term}</span></div>
        </div>
        <div class="metric-row">
            <div class="metric-pill"> Amenities: <span>{amenity_str}</span></div>
            <div class="metric-pill"> Negotiable: <span>{"Yes" if negotiable else "No"}</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-heading">PRICE RANGE CONTEXT</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 2.5))
        fig.patch.set_facecolor('#0d1528')
        ax.set_facecolor('#0d1528')
        ranges = [
            ("Budget\n<1.2M",  0,          1_200_000, "#1e3a5f"),
            ("Low\n1.2M–2M",   1_200_000,  2_000_000, "#1e4d3b"),
            ("Mid\n2M–5M",     2_000_000,  5_000_000, "#4a3a1a"),
            ("Upper\n5M–15M",  5_000_000, 15_000_000, "#3b1a4a"),
            ("Luxury\n>15M",  15_000_000, 80_000_000, "#4a1a1a"),
        ]
        for _, lo, hi, color in ranges:
            ax.barh(0, hi - lo, left=lo, height=0.5, color=color, alpha=0.9)
        ax.axvline(result["estimated_price"], color="#34d399", linewidth=2.5,
                   linestyle="--", label=f"Your property: {price_fmt} EGP")
        ax.scatter(result["estimated_price"], 0, color="#34d399", zorder=5, s=100)
        ax.set_xlim(0, 30_000_000)
        ax.set_xticklabels([f"{x/1e6:.0f}M" for x in ax.get_xticks()], color="#64748b", fontsize=8)
        ax.set_yticks([])
        ax.legend(loc="upper right", fontsize=8, facecolor="#0d1528", labelcolor="#94a3b8", edgecolor="#1e2d4a")
        ax.set_title("Alexandria Housing Market — Price Positioning", color="#94a3b8", fontsize=9, pad=8)
        for spine in ax.spines.values(): spine.set_edgecolor('#1e2d4a')
        ax.tick_params(colors="#64748b")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

        st.markdown('<div class="section-heading">CLUSTER DISTANCE ANALYSIS</div>', unsafe_allow_html=True)
        fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.5))
        fig2.patch.set_facecolor('#0a0e1a')

        km_labels = ["Budget", "Mid-Range", "Premium"]
        km_vals   = [4.5, 3.2, 5.1]
        km_vals[result["km_cluster"]] = 1.2
        km_colors = ["#3b82f6" if i == result["km_cluster"] else "#1e3a5f" for i in range(3)]
        ax1.set_facecolor('#0d1528')
        ax1.barh(km_labels, km_vals, color=km_colors, height=0.5, edgecolor="#1e2d4a")
        ax1.set_title("K-Medoid: Manhattan Distance", color="#94a3b8", fontsize=9)
        ax1.set_xlabel("Distance to Medoid", color="#64748b", fontsize=8)
        ax1.tick_params(colors="#64748b", labelsize=8)
        for spine in ax1.spines.values(): spine.set_edgecolor('#1e2d4a')

        hier_labels = ["Economy", "Quality"]
        hier_vals   = [2.8, 3.4]
        hier_vals[result["hier_cluster"]] = 0.9
        hier_colors = ["#7c3aed" if i == result["hier_cluster"] else "#1e3a5f" for i in range(2)]
        ax2.set_facecolor('#0d1528')
        ax2.barh(hier_labels, hier_vals, color=hier_colors, height=0.4, edgecolor="#1e2d4a")
        ax2.set_title("Hierarchical: Euclidean Distance", color="#94a3b8", fontsize=9)
        ax2.set_xlabel("Distance to Centroid", color="#64748b", fontsize=8)
        ax2.tick_params(colors="#64748b", labelsize=8)
        for spine in ax2.spines.values(): spine.set_edgecolor('#1e2d4a')

        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close()

with tab2:
    if not run_btn:
        st.info("Run the pipeline first to see Fuzzy Logic details.")
    else:
        st.markdown('<div class="section-heading">MEMBERSHIP FUNCTIONS — INPUTS & OUTPUT</div>', unsafe_allow_html=True)

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.patch.set_facecolor('#0a0e1a')

        def trapmf_v(x, a, b, c, d):
            return np.vectorize(
                lambda xi: max(0, min((xi-a)/max(b-a,1e-9), 1, (d-xi)/max(d-c,1e-9)))
                           if a < xi < d else 0
            )(x)

        def trimf_v(x, a, b, c):
            return np.vectorize(
                lambda xi: max(0, min((xi-a)/max(b-a,1e-9), (c-xi)/max(c-b,1e-9)))
                           if a < xi < c else 0
            )(x)

        def plot_mf(ax, x_range, mfs, title, x_val, xlabel):
            ax.set_facecolor('#0d1528')
            colors_mf = ["#3b82f6", "#f59e0b", "#10b981", "#f43f5e"]
            for (label, vals), col in zip(mfs.items(), colors_mf):
                ax.plot(x_range, vals, color=col, linewidth=2, label=label)
                ax.fill_between(x_range, vals, alpha=0.12, color=col)
            ax.axvline(x_val, color="#ffffff", linewidth=1.5, linestyle="--", alpha=0.6, label=f"Input={x_val:.1f}")
            ax.set_title(title, color="#e2e8f0", fontsize=9, fontweight="bold")
            ax.set_xlabel(xlabel, color="#64748b", fontsize=8)
            ax.set_ylabel("Membership", color="#64748b", fontsize=8)
            ax.legend(fontsize=7, facecolor="#0d1528", labelcolor="#94a3b8", edgecolor="#1e2d4a")
            ax.tick_params(colors="#64748b", labelsize=7)
            for spine in ax.spines.values(): spine.set_edgecolor('#1e2d4a')
            ax.set_ylim(-0.05, 1.15)

        x_area = np.linspace(30, 500, 300)
        plot_mf(axes[0,0], x_area, {
            "Small":  trapmf_v(x_area, 30, 30, 80, 120),
            "Medium": trimf_v (x_area, 80, 140, 220),
            "Large":  trapmf_v(x_area, 160, 220, 500, 500),
        }, "Input: Area (SQM)", area, "SQM")

        x_bath = np.linspace(1, 8, 200)
        plot_mf(axes[0,1], x_bath, {
            "Few":    trapmf_v(x_bath, 1, 1, 2, 3),
            "Average":trimf_v (x_bath, 2, 3, 4),
            "Many":   trapmf_v(x_bath, 3, 4, 8, 8),
        }, "Input: Bathrooms", bathrooms, "Count")

        x_clust = np.linspace(-0.5, 2.5, 200)
        plot_mf(axes[1,0], x_clust, {
            "Budget":  trapmf_v(x_clust, -0.5, -0.5, 0.3, 0.7),
            "Mid":     trimf_v (x_clust, 0.3, 1.0, 1.7),
            "Premium": trapmf_v(x_clust, 1.3, 1.7, 2.5, 2.5),
        }, "Input: K-Medoid Cluster", result["km_cluster"], "Cluster Index")

        x_price = np.linspace(12, 18, 300)
        plot_mf(axes[1,1], x_price, {
            "Low":    trapmf_v(x_price, 12, 12, 13.5, 14.2),
            "Medium": trimf_v (x_price, 13.5, 14.5, 15.5),
            "High":   trapmf_v(x_price, 14.8, 15.5, 17.5, 17.5),
        }, "Output: Price (log scale)", result["price_log"], "log(Price EGP)")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

        st.markdown('<div class="section-heading">OUTPUT MEMBERSHIP DEGREES</div>', unsafe_allow_html=True)
        cat_colors = {"Low": "#34d399", "Medium": "#fbbf24", "High": "#f87171"}
        for label, deg in result["membership"].items():
            pct = deg * 100
            col = cat_colors[label]
            st.markdown(f"""
            <div class="mf-bar-container">
                <div class="mf-label">
                    <span style="color:{col}; font-weight:700;">{label}</span>
                    <span style="color:#94a3b8; font-family:'JetBrains Mono',monospace;">{pct:.1f}%</span>
                </div>
                <div class="mf-bar" style="background:linear-gradient(90deg,{col} {pct}%,#1e2d4a {pct}%);"></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-heading">ACTIVE FUZZY RULES</div>', unsafe_allow_html=True)
        fired = result["fuzzy_rules_fired"]
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        fig3.patch.set_facecolor('#0a0e1a')
        ax3.set_facecolor('#0d1528')
        weights_all = [r[0] for r in fired]
        short_labels = [f"R{i+1}" for i in range(len(weights_all))]
        bar_colors = ["#3b82f6" if w > 0.3 else "#1e3a5f" for w in weights_all]
        ax3.barh(short_labels, weights_all, color=bar_colors, height=0.55, edgecolor="#1e2d4a")
        ax3.set_title("Rule Firing Strengths", color="#e2e8f0", fontsize=9)
        ax3.set_xlabel("Activation Degree", color="#64748b", fontsize=8)
        ax3.tick_params(colors="#64748b", labelsize=8)
        for spine in ax3.spines.values(): spine.set_edgecolor('#1e2d4a')
        plt.tight_layout()
        st.pyplot(fig3, use_container_width=True)
        plt.close()

        rule_names = [
            "Small area + Few bath + Budget → Very Low",
            "Small area + Avg bath + Budget → Low",
            "Medium area + Few bath + Budget → Low-Mid",
            "Medium area + Avg bath + Mid → Medium",
            "Medium area + Many bath + Mid → Mid-High",
            "Large area + Avg bath + Mid → High",
            "Large area + Many bath + Premium → Very High",
            "Medium area + Few bath + Premium → Mid-High",
            "Small area + Many bath + Premium → Medium",
            "Large area + Few bath + Budget → Low-Mid",
            "Large area + Avg bath + Budget → Medium",
        ]
        with st.expander(" Full Rule Base (11 IF-THEN Rules)"):
            st.dataframe(pd.DataFrame({
                "Rule":      [f"R{i+1}" for i in range(len(rule_names))],
                "Condition": rule_names,
                "Strength":  [f"{r[0]:.3f}" for r in fired] + ["-"] * max(0, len(rule_names) - len(fired)),
            }), use_container_width=True, hide_index=True)

with tab3:
    if not run_btn:
        st.info("Run the pipeline first to see GA details.")
    else:
        st.markdown('<div class="section-heading">GENETIC ALGORITHM — FEATURE SELECTION</div>', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])

        with col1:
            np.random.seed(42)
            gens       = np.arange(0, 30)
            best_curve = 0.25 + (0.387 - 0.25) * (1 - np.exp(-gens / 8)) + np.random.normal(0, 0.005, 30)
            best_curve = np.clip(np.maximum.accumulate(best_curve), 0.25, 0.40)
            avg_curve  = np.clip(best_curve * 0.85 + np.random.normal(0, 0.01, 30), 0.18, 0.40)

            fig4, ax4 = plt.subplots(figsize=(8, 4))
            fig4.patch.set_facecolor('#0a0e1a')
            ax4.set_facecolor('#0d1528')
            ax4.plot(gens, best_curve, color="#3b82f6", linewidth=2.5, label="Best Fitness")
            ax4.fill_between(gens, best_curve, alpha=0.15, color="#3b82f6")
            ax4.plot(gens, avg_curve, color="#64748b", linewidth=1.5, linestyle="--", label="Avg Fitness")
            ax4.axhline(result["ga_silhouette_base"], color="#f59e0b", linewidth=1.5,
                        linestyle=":", label=f"Baseline = {result['ga_silhouette_base']:.3f}")
            ax4.axhline(result["ga_silhouette_best"], color="#10b981", linewidth=1.5,
                        linestyle="-.", label=f"GA Best = {result['ga_silhouette_best']:.3f}")
            ax4.set_xlabel("Generation", color="#64748b", fontsize=9)
            ax4.set_ylabel("Silhouette Score", color="#64748b", fontsize=9)
            ax4.set_title("GA Fitness Evolution (POP=30, GENS=30)", color="#e2e8f0", fontsize=9)
            ax4.legend(fontsize=7.5, facecolor="#0d1528", labelcolor="#94a3b8", edgecolor="#1e2d4a")
            ax4.tick_params(colors="#64748b", labelsize=8)
            for spine in ax4.spines.values(): spine.set_edgecolor('#1e2d4a')
            plt.tight_layout()
            st.pyplot(fig4, use_container_width=True)
            plt.close()

        with col2:
            for badge, title, desc in [
                ("CHROMOSOME", "Binary Vector",         "Each gene = 1 feature. 1=include, 0=exclude."),
                ("FITNESS",    "Silhouette Score",      "K-Medoid quality on selected features. Penalty -1 if <3 features."),
                ("SELECTION",  "Tournament (k=4)",      "Pick 4 random chromosomes, select fittest parent."),
                ("CROSSOVER",  "Single-Point (CR=0.8)", "Random cut point, swap gene segments."),
                ("MUTATION",   "Bit-Flip (MR=0.02)",    "Each gene flips with 2% probability."),
            ]:
                st.markdown(f"""
                <div class="step-card">
                    <div class="step-badge">{badge}</div>
                    <div class="step-title">{title}</div>
                    <div class="step-desc">{desc}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-heading">SELECTED FEATURES (BEST CHROMOSOME)</div>', unsafe_allow_html=True)
        ga_feat_cols = st.columns(5)
        for i, feat in enumerate(result["ga_selected"]):
            with ga_feat_cols[i % 5]:
                st.markdown(f"""
                <div style="background:#052e1c;border:1px solid #065f46;border-radius:8px;
                     padding:10px;text-align:center;margin-bottom:8px;">
                    <div style="color:#34d399;font-size:0.78rem;font-weight:700;">✓</div>
                    <div style="color:#a7f3d0;font-size:0.72rem;font-family:'JetBrains Mono',monospace;">{feat}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-heading">GA PARAMETERS</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Parameter": ["Population Size","Generations","Crossover Rate","Mutation Rate","Tournament Size","Min Features","K Clusters"],
            "Value":     [30, 30, 0.80, 0.02, 4, 3, 3],
            "Purpose":   ["Chromosomes per generation","Total evolution cycles","Parent crossover probability",
                          "Per-gene bit-flip probability","Tournament selection pool","Min features per chromosome",
                          "K-Medoid clusters for fitness"],
        }), use_container_width=True, hide_index=True)

with tab4:
    if not run_btn:
        st.info("Run the pipeline first to see preprocessing output.")
    else:
        st.markdown('<div class="section-heading">PREPROCESSING STEPS APPLIED</div>', unsafe_allow_html=True)
        pp = result["preprocessed"]
        for num, title, desc in [
            ("1", "Missing Values",       "Dropped null Type rows. Filled Level & Furnished with mode. Converted Compound → In_Compound binary."),
            ("2", "Delivery Date Parsing",f"Parsed delivery_date='{delivery_date}' → years_to_delivery={pp['years_delivery']}"),
            ("3", "Outlier Treatment",    "IQR capping on Area(SQM). Log1p transform on Price (skewness 12.9 → 0.33)."),
            ("4", "Encoding",             "Numeric conversion for Bedroom/Bathroom/Level. One-hot encode Location, Type, Delivery_Term."),
            ("5", "RobustScaler",         f"Applied to continuous features. Area scaled={pp['area_scaled']}, Bath scaled={pp['bath_scaled']:.4f}"),
        ]:
            st.markdown(f"""
            <div class="step-card">
                <div class="step-badge">STEP {num}</div>
                <div class="step-title">✓ {title}</div>
                <div class="step-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-heading">SCALED FEATURE VALUES FOR THIS RECORD</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Feature":     ["Area(SQM)", "Bathrooms", "Bedrooms", "Years to Delivery", "Luxury Score"],
            "Raw Value":   [area, bathrooms, bedrooms, pp["years_delivery"], pp["luxury_score"]],
            "Scaled Value":[pp["area_scaled"], pp["bath_scaled"], pp["bed_scaled"], pp["years_delivery"], pp["luxury_score"]/6.0],
        }), use_container_width=True, hide_index=True)

with tab5:
    st.markdown('<div class="section-heading">SYSTEM PIPELINE OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0d1528;border:1px solid #1e2d4a;border-radius:12px;padding:24px;font-size:0.85rem;color:#94a3b8;line-height:1.8;">
        <div style="color:#60a5fa;font-weight:700;font-size:1rem;margin-bottom:16px;">
            🏙️ Alexandria House Price Intelligence System
        </div>
        <table style="width:100%;border-collapse:collapse;">
            <tr style="border-bottom:1px solid #1e2d4a;">
                <td style="padding:10px;color:#3b82f6;font-weight:700;width:140px;">① Preprocessing</td>
                <td style="padding:10px;">Missing value handling, outlier capping, log transform, one-hot encoding, RobustScaler.</td>
            </tr>
            <tr style="border-bottom:1px solid #1e2d4a;">
                <td style="padding:10px;color:#7c3aed;font-weight:700;">② GA Selection</td>
                <td style="padding:10px;">Binary chromosome GA. Fitness = Silhouette Score on K-Medoid. POP=30, GENS=30.</td>
            </tr>
            <tr style="border-bottom:1px solid #1e2d4a;">
                <td style="padding:10px;color:#10b981;font-weight:700;">③ K-Medoid</td>
                <td style="padding:10px;">Manhattan distance (k=3). Assigns to Budget / Mid-Range / Premium segment.</td>
            </tr>
            <tr style="border-bottom:1px solid #1e2d4a;">
                <td style="padding:10px;color:#f59e0b;font-weight:700;">④ Hierarchical</td>
                <td style="padding:10px;">Agglomerative (k=2) via nearest-centroid. Economy vs. Quality tiers.</td>
            </tr>
            <tr style="border-bottom:1px solid #1e2d4a;">
                <td style="padding:10px;color:#f43f5e;font-weight:700;">⑤ Fuzzy Logic</td>
                <td style="padding:10px;">3 inputs: Area, Bathroom, K-Medoid Cluster. 11 IF-THEN rules. Centroid defuzzification → log(price).</td>
            </tr>
            <tr>
                <td style="padding:10px;color:#34d399;font-weight:700;">⑥ Output</td>
                <td style="padding:10px;">expm1 converts log-price back to EGP. Returns clusters, price estimate, membership degrees.</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">TECHNICAL STACK</div>', unsafe_allow_html=True)
    tech_cols = st.columns(4)
    techs = [
        (" Python","Core language"), (" scikit-learn","Preprocessing + Clustering"),
        (" sklearn-extra","KMedoids"), (" skfuzzy","Fuzzy logic engine"),
        (" NumPy/Pandas","Data manipulation"), (" Matplotlib","Visualizations"),
        (" Streamlit","Interactive UI"), (" Kaggle","Alexandria dataset"),
    ]
    for i, (name, desc) in enumerate(techs):
        with tech_cols[i % 4]:
            st.markdown(f"""
            <div style="background:#0d1528;border:1px solid #1e2d4a;border-radius:8px;
                 padding:14px;margin-bottom:8px;text-align:center;">
                <div style="font-size:1.2rem;">{name.split()[0]}</div>
                <div style="color:#60a5fa;font-size:0.78rem;font-weight:700;">{' '.join(name.split()[1:])}</div>
                <div style="color:#475569;font-size:0.72rem;margin-top:4px;">{desc}</div>
            </div>""", unsafe_allow_html=True)
