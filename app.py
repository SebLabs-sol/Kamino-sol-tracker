import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Kamino Multiply Comprehensive Tracker", page_icon="⚡", layout="wide")

st.title("⚡ Kamino Ultra-Multiply: Complete SOL & LST Multi-Market Tracker")
st.markdown("This terminal analyzes and decomposes loop mathematics for all major Solana LSTs across Kamino markets.")
st.markdown("---")

@st.cache_data(ttl=60)
def get_kamino_data():
    # Fetching from the main aggregated metrics routing engine
    url = "https://api.kamino.finance/kamino-market/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/reserves/metrics"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json(), False
    except Exception:
        pass
    return None, True

raw_data, using_fallbacks = get_kamino_data()

# 1. EXPANDED LIST: Comprehensive Solana LST Staking Database
LST_STAKING_YIELDS = {
    "JitoSOL": 7.35,
    "mSOL": 7.15,
    "bSOL": 6.95,
    "jupSOL": 7.85,
    "stkeSOL": 8.10,   # STKE SOL Strategy
    "picSOL": 7.40,    # Pico SOL
    "hubSOL": 7.65,    # Solhub
    "vSOL": 7.20,      # Vice/Vigil SOL
    "infSOL": 7.90     # Infinity SOL
}

# 2. EXPANDED RISK RULES: Maximum Allowed LTV (Loan-To-Value) for absolute leverage metrics
LST_RISK_PARAMETERS = {
    "JitoSOL": {"ltv": 0.90, "market": "Kamino Main Market"},
    "mSOL": {"ltv": 0.88, "market": "Kamino Main Market"},
    "bSOL": {"ltv": 0.85, "market": "Kamino Main Market"},
    "jupSOL": {"ltv": 0.91, "market": "Kamino Main Market"},
    "stkeSOL": {"ltv": 0.85, "market": "Kamino Alt LST Market"},
    "picSOL": {"ltv": 0.85, "market": "Kamino Alt LST Market"},
    "hubSOL": {"ltv": 0.82, "market": "Kamino Alt LST Market"},
    "vSOL": {"ltv": 0.80, "market": "Kamino Alt LST Market"},
    "infSOL": {"ltv": 0.88, "market": "Kamino Multi-Asset Market"}
}

kamino_metrics = {}
if not using_fallbacks and isinstance(raw_data, list):
    for item in raw_data:
        token = item.get("token", "")
        supply_apy = float(item.get("supplyApy", 0)) * 100
        borrow_apy = float(item.get("borrowApy", 0)) * 100
        reward_apy = float(item.get("rewardApy", 0)) * 100
        available_liquidity = float(item.get("availableLiquidity", 0))
        max_capacity = float(item.get("depositLimit", 0))
        
        kamino_metrics[token] = {
            "supply": supply_apy, "borrow": borrow_apy, "reward": reward_apy,
            "available": available_liquidity, "capacity": max_capacity
        }
else:
    # Populating broad structural data metrics
    for token in LST_STAKING_YIELDS.keys():
        kamino_metrics[token] = {"supply": 0.25, "borrow": 7.90, "reward": 0.40, "available": 15000, "capacity": 100000}
    kamino_metrics["SOL"] = {"supply": 0.15, "borrow": 6.85, "reward": 0.00, "available": 50000, "capacity": 500000}

sol_borrow_apy = kamino_metrics.get("SOL", {}).get("borrow", 6.85)

if using_fallbacks:
    st.warning("⚠️ Serving calculations via system backup data profiles.")
else:
    st.success("🟢 Connected live to Kamino Cross-Market API Registries.")

# 3. ADVANCED CALCULATION LOOP WITH YIELD DECOMPOSITION
processed_pairs = []

for lst_name, staking_yield in LST_STAKING_YIELDS.items():
    metrics = kamino_metrics.get(lst_name, {"supply": 0.25, "reward": 0.0, "available": 5000, "capacity": 50000})
    supply_apy = metrics["supply"]
    reward_apy = metrics["reward"]
    available_tokens = metrics["available"]
    max_capacity = metrics["capacity"]
    
    risk_info = LST_RISK_PARAMETERS.get(lst_name, {"ltv": 0.85, "market": "Kamino Alt Market"})
    ltv = risk_info["ltv"]
    market_origin = risk_info["market"]
    
    # Calculate Dynamic Leverage Cap
    max_leverage = 1.0 / (1.0 - ltv)
    debt_multiplier = max_leverage - 1.0
    
    # Mathematical Decomposition Formulation
    leveraged_staking = max_leverage * staking_yield
    leveraged_supply = max_leverage * supply_apy
    leveraged_rewards = max_leverage * reward_apy
    gross_loop_yield = leveraged_staking + leveraged_supply + leveraged_rewards
    
    total_borrow_cost = debt_multiplier * sol_borrow_apy
    net_apy = gross_loop_yield - total_borrow_cost
    
    processed_pairs.append({
        "Asset Pairing": f"{lst_name} / SOL",
        "Target Market": market_origin,
        "Max Leverage": f"{max_leverage:.2f}x",
        "Base Staking APY": f"{staking_yield:.2f}%",
        "Kamino Supply APY": f"{supply_apy:.2f}%",
        "Kamino Reward APY": f"{reward_apy:.2f}%",
        "Leveraged Staking Yield": f"{leveraged_staking:.2f}%",
        "Leveraged Supply APY": f"{leveraged_supply:.2f}%",
        "Leveraged Reward APY": f"{leveraged_rewards:.2f}%",
        "Total Gross Loop APY": f"{gross_loop_yield:.2f}%",
        "SOL Debt Cost": f"-{total_borrow_cost:.2f}%",
        "Net Loop APY (Float)": net_apy,
        "Net Loop APY": f"{net_apy:.2f}%",
        "Available Liquidity": f"{available_tokens:,.0f} {lst_name}",
        "Vault Capacity Limit": f"{max_capacity:,.0f} {lst_name}"
    })

df = pd.DataFrame(processed_pairs)
df = df.sort_values(by="Net Loop APY (Float)", ascending=False).drop(columns=["Net Loop APY (Float)"])

# 4. GRAPHICAL DISPLAY INTERFACE
st.write("### Comprehensive Multi-Market Strategy Grid")
display_cols = ["Asset Pairing", "Target Market", "Max Leverage", "Total Gross Loop APY", "SOL Debt Cost", "Net Loop APY"]
st.dataframe(df[display_cols].set_index("Asset Pairing"), use_container_width=True)

st.write("---")
st.write("### Complete Analytical Breakdown Matrix (Yield Source Decomposition & Capacities)")

# Display complete transparency row logs
for idx, row in df.iterrows():
    with st.expander(f"🔍 Detailed Math & Capacity Profile: {row['Asset Pairing']} ({row['Target Market']})", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Leverage & Market Metadata**")
            st.markdown(f"- **Home Market Platform:** {row['Target Market']}")
            st.markdown(f"- **Applied Max Leverage:** {row['Max Leverage']}")
            st.markdown(f"- **Available Liquidity Capacity:** {row['Available Liquidity']}")
            st.markdown(f"- **Max Pool Caps:** {row['Vault Capacity Limit']}")
        with c2:
            st.markdown("**Unleveraged Inputs (1x base)**")
            st.markdown(f"- **Native Validation Staking:** {row['Base Staking APY']}")
            st.markdown(f"- **Isolated Supply Interest:** {row['Kamino Supply APY']}")
            st.markdown(f"- **Liquidity Mining Incentives:** {row['Kamino Reward APY']}")
        with c3:
            st.markdown("**Leveraged Results (Decomposed Loop Yields)**")
            st.markdown(f"📈 **Leveraged Staking Earnings:** {row['Leveraged Staking Yield']}")
            st.markdown(f"📈 **Leveraged Supply Earnings:** {row['Leveraged Supply APY']}")
            st.markdown(f"🎁 **Leveraged Token Rewards:** {row['Leveraged Reward APY']}")
            st.markdown(f"📉 **Subtracted Borrow Cost (SOL):** {row['SOL Debt Cost']}")
            st.markdown(f"🏆 **Final Realized NET APY:** `{row['Net Loop APY']}`")

st.markdown("---")
st.caption("_Disclaimer: The underlying mathematical matrix multiplies underlying components linearly relative to debt expansion. Changing structural asset weights or token peg changes could distort metrics._")
