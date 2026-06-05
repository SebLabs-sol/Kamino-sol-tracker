import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Kamino Multiply Terminal", page_icon="⚡", layout="wide")

# Custom CSS injected to style the cards beautifully on mobile and desktop
st.markdown("""
    <style>
    .metric-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .badge {
        background-color: #2e7d32;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    .market-badge {
        background-color: #1976d2;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_with_html=True)

st.title("⚡ Kamino Ultra-Multiply: SOL Yield Engine")
st.markdown("Real-time automated looping optimization across diverse Solana LST environments.")
st.markdown("---")

@st.cache_data(ttl=60)
def get_kamino_data():
    url = "https://api.kamino.finance/kamino-market/7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF/reserves/metrics"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json(), False
    except Exception:
        pass
    return None, True

raw_data, using_fallbacks = get_kamino_data()

# Comprehensive Solana LST Staking Database
LST_STAKING_YIELDS = {
    "JitoSOL": 7.35,
    "mSOL": 7.15,
    "bSOL": 6.95,
    "jupSOL": 7.85,
    "stkeSOL": 8.10,
    "picSOL": 7.40,
    "hubSOL": 7.65,
    "vSOL": 7.20,
    "infSOL": 7.90
}

# Maximum Allowed LTV (Loan-To-Value) parameters per Kamino risk models
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
    for token in LST_STAKING_YIELDS.keys():
        kamino_metrics[token] = {"supply": 0.25, "borrow": 7.90, "reward": 0.40, "available": 15000, "capacity": 100000}
    kamino_metrics["SOL"] = {"supply": 0.15, "borrow": 6.85, "reward": 0.00, "available": 50000, "capacity": 500000}

sol_borrow_apy = kamino_metrics.get("SOL", {}).get("borrow", 6.85)

if using_fallbacks:
    st.warning("⚠️ Serving calculations via system backup data profiles.")
else:
    st.success("🟢 Connected live to Kamino Cross-Market API Registries.")

# Process Strategy Matrices
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
    
    max_leverage = 1.0 / (1.0 - ltv)
    debt_multiplier = max_leverage - 1.0
    
    leveraged_staking = max_leverage * staking_yield
    leveraged_supply = max_leverage * supply_apy
    leveraged_rewards = max_leverage * reward_apy
    gross_loop_yield = leveraged_staking + leveraged_supply + leveraged_rewards
    
    total_borrow_cost = debt_multiplier * sol_borrow_apy
    net_apy = gross_loop_yield - total_borrow_cost
    
    processed_pairs.append({
        "name": lst_name,
        "pairing": f"{lst_name} / SOL",
        "market": market_origin,
        "max_leverage": max_leverage,
        "base_staking": staking_yield,
        "base_supply": supply_apy,
        "base_reward": reward_apy,
        "lev_staking": leveraged_staking,
        "lev_supply": leveraged_supply,
        "lev_reward": leveraged_rewards,
        "gross_apy": gross_loop_yield,
        "borrow_cost": total_borrow_cost,
        "net_apy": net_apy,
        "available": available_tokens,
        "capacity": max_capacity
    })

# Sort strategies by highest yield
processed_pairs = sorted(processed_pairs, key=lambda x: x["net_apy"], reverse=True)

# 2. RENDER STRATEGIES IN USER-FRIENDLY CARDS
st.write("### Active Multiply Opportunities")

for idx, strategy in enumerate(processed_pairs):
    # Creating a cleaner visual card boundary using a streamlit container
    with st.container():
        st.markdown(f"""
        <div class="metric-card">
            <span class="market-badge">{strategy['market']}</span>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                <h2 style="margin: 0;">{strategy['pairing']}</h2>
                <h1 style="margin: 0; color: #00e676;">{strategy['net_apy']:.2f}% <span style="font-size: 14px; color: #888;">NET APY</span></h1>
            </div>
            <p style="margin: 5px 0 0 0; color: #aaa;">Max Multiplier: <b>{strategy['max_leverage']:.2f}x Leverage</b></p>
        </div>
        """, unsafe_with_html=True)
        
        # Expandable Detail Container nestled directly underneath the Card header
        with st.expander("🔍 View Math & Capacity Breakdown"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📊 Yield Deconstruction")
                st.write(f"📈 **Leveraged Staking Yield:** +{strategy['lev_staking']:.2f}% *(Base: {strategy['base_staking']:.2f}%)*")
                st.write(f"📈 **Leveraged Supply APY:** +{strategy['lev_supply']:.2f}% *(Base: {strategy['base_supply']:.2f}%)*")
                st.write(f"🎁 **Leveraged Mining Rewards:** +{strategy['lev_reward']:.2f}% *(Base: {strategy['base_reward']:.2f}%)*")
                st.write(f"🛑 **Gross Multiplied Yield:** {strategy['gross_apy']:.2f}%")
                st.write(f"📉 **Subtracted SOL Debt Cost:** -{strategy['borrow_cost']:.2f}% *(Base SOL Borrow: {sol_borrow_apy:.2f}%)*")
                st.markdown(f"🏆 **Final Realized Return:** `{strategy['net_apy']:.2f}% NET APY`")
            with col2:
                st.markdown("#### 🛢️ Vault Capacities")
                st.write(f"🔓 **Available Liquidity:** {strategy['available']:,.0f} {strategy['name']}")
                st.write(f"📦 **Max Vault Storage Cap:** {strategy['capacity']:,.0f} {strategy['name']}")
                
                # Dynamic Capacity Usage Bar Gauge
                if strategy['capacity'] > 0:
                    pct_used = ((strategy['capacity'] - strategy['available']) / strategy['capacity'])
                    st.progress(min(max(pct_used, 0.0), 1.0), text=f"Vault Utilization: {pct_used*100:.1f}%")
        st.markdown("<br>", unsafe_with_html=True)

# 3. EXPLANATION LIST / LEARNING LEGEND AT THE BOTTOM
st.markdown("---")
st.markdown("### 📘 Terminal Explanation List & Metric Glossary")

st.markdown("""
Here is a comprehensive breakdown of how the platform calculates these variables and what each data point implies for your open positions:

* **Asset Pairing (e.g., JitoSOL / SOL)**
  The process of utilizing a Liquid Staking Token (LST) as collateral to borrow base native SOL, which is then traded back for more LST to loop the yield profile.
* **Net APY (Net Annual Percentage Yield)**
  Your true annualized take-home yield. This is computed automatically via the core algorithm: 
  $$\\text{{Net APY}} = [\\text{{Leverage}} \\times (\\text{{Staking APY}} + \\text{{Supply APY}} + \\text{{Reward APY}})] - [(\\text{{Leverage}} - 1) \\times \\text{{SOL Borrow APY}}]$$
* **Max Allowed Leverage**
  The maximum legal multiplier limit before instant liquidation occurs on Kamino. This is driven entirely by the token's **LTV (Loan-To-Value)** parameter. For example, a 90% LTV means you can borrow up to 90% of your collateral's value, translating to a maximum leverage cap of $1 / (1 - 0.90) = 10\\text{{x}}$.
* **Leveraged Staking Yield**
  The protocol-level staking rewards generated natively by holding the validation token (e.g., Jito validation or Marinade validation). Because you are leveraged, you earn this underlying staking return across your entire expanded position size.
* **Kamino Supply APY**
  The baseline interest rate Kamino pays you simply for depositing your LST into their collateral supply vaults.
* **Mining Reward APY**
  Extra token bonus distributions distributed by Kamino or partner foundations (such as bonus \$KMNO tokens) to incentivize providing depth to that specific vault.
* **SOL Debt Cost**
  The interest fee accumulation you owe to the protocol for borrowing native SOL to fund your extra loop purchases. This scales based on your debt footprint $(\\text{{Leverage}} - 1)$.
* **Available Liquidity vs Vault Capacity Limit**
  Shows how much physical room is left in the strategy vault before it locks. If available liquidity reaches zero, you cannot withdraw or borrow additional amounts until matching pool liquidity changes.
""")
