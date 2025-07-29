
---

# 📊 **Bitcoin Trading Analytics Report**

### Powered by Greed & Fear Index Sentiment Classification

📅 *Date Range: 2023-03-28 to 2025-02-19*

---

## 🧾 **1. Executive Summary**

This report presents a comprehensive exploration of Bitcoin trading behavior using sentiment-driven analysis derived from the **Greed & Fear Index**. It analyzes over **184,000 trades** spanning various sentiment classifications, order types, and trading directions to develop a robust strategy.

---

## 📁 **2. Dataset Overview**

| Metric                     | Value            |
| -------------------------- | ---------------- |
| Dataset Size               | 184,263 trades   |
| Total Trading Volume (USD) | \$880,912,169.43 |
| Total Fees Paid            | \$184,908.74     |
| Net PnL                    | \$10,225,249.60  |
| Most Active Classification | Fear             |
| Preferred Trading Side     | Sell             |

---

## 💰 **3. PnL Behavior by Sentiment**

| Classification    | Total PnL | ROI (%)  | Win Rate (%) | Avg PnL | Profit Factor |
| ----------------- | --------- | -------- | ------------ | ------- | ------------- |
| **Fear**          | \$6.69M   | 0.95     | 41.51        | 50.04   | 5.97          |
| **Greed**         | \$3.19M   | **2.76** | 44.65        | 87.89   | **7.22**      |
| **Extreme Greed** | \$176.9K  | 0.45     | **49.01**    | 25.42   | 3.21          |
| **Neutral**       | \$158.7K  | 0.72     | 31.72        | 22.22   | 1.96          |

### 🔍 Key Insights:

* **Best Total PnL**: Fear
* **Best ROI**: Greed
* **Best Win Rate**: Extreme Greed

---

## 🔄 **4. Buy/Sell Behavior Analysis**

| Classification | Avg Buy Price | Avg Sell Price | Price Spread |
| -------------- | ------------- | -------------- | ------------ |
| Neutral        | **\$2788.39** | \$2542.39      | N/A          |
| Fear           | \$12,494.39   | \$9,744.83     | \$-2,749.56  |
| Greed          | \$6,966.71    | \$4,439.98     | \$-2,526.73  |
| Extreme Greed  | \$9,769.03    | **\$9,774.59** | **\$5.56**   |

### 🔍 Key Insights:

* **Buy at**: Neutral (lowest entry price)
* **Sell at**: Extreme Greed (highest exit price)
* **Largest Spread**: Extreme Greed → \$5.56

---

## 🏷 **5. Order Type Analysis (Market vs Limit)**

| Order Type | Total PnL   | Avg PnL | Win Rate (%) | Total Fees Paid |
| ---------- | ----------- | ------- | ------------ | --------------- |
| **Limit**  | **\$5.59M** | 66.67   | 49.6         | \$16,694.52     |
| **Market** | \$4.63M     | 29.89   | 37.2         | \$168,214.31    |

### 🔍 Key Insights:

* **Better Order Type**: Limit Orders
* Lower fees & higher ROI observed with limit orders

---

## 📊 **6. Greed/Fear Index Value Analysis**

| Index Value | Total PnL   | Avg PnL | Win Rate (%) | Avg Price   |
| ----------- | ----------- | ------- | ------------ | ----------- |
| 44.0        | **\$6.69M** | 50.04   | 41.51        | \$11,102.06 |
| 74.0        | \$3.19M     | 90.50   | 45.16        | \$5,367.50  |
| 84.0        | \$176.9K    | 25.42   | **49.01**    | \$9,771.90  |

### 🔍 Key Insights:

* **Most Profitable Index**: 44.0
* **Highest Win Rate**: 84.0
* **Value–PnL Correlation**: 0.0111 (weak)

---

## 📈 **7. Directional Trading Performance**

| Strategy  | Total PnL   | Trade Count | Win Rate (%) |
| --------- | ----------- | ----------- | ------------ |
| **Short** | **\$7.04M** | 78,842      | **48.11%**   |
| Long      | \$3.11M     | 105,156     | 37.49%       |

### 🔍 Key Insights:

* **Best Direction**: Short
* Most profitable direction: **Close Short**

---

## 💲 **8. Execution Price Volatility**

| Classification | Avg Price  | Std Dev  | CV (Volatility) |
| -------------- | ---------- | -------- | --------------- |
| Neutral        | \$2663.13  | \$10,895 | **4.09**        |
| Greed          | \$5513.71  | \$20,927 | 3.80            |
| Fear           | \$11102.05 | \$29,350 | 2.64            |
| Extreme Greed  | \$9771.89  | \$17,267 | **1.77**        |

### 🔍 Key Insights:

* **Most Volatile**: Neutral
* **Stable Price**: Extreme Greed

---

## 📋 **9. Strategy Matrix & Rankings**

| Classification | Total PnL   | ROI (%)  | Win Rate (%) | Avg Price  | Volatility |
| -------------- | ----------- | -------- | ------------ | ---------- | ---------- |
| Greed          | \$3.19M     | **2.76** | 44.65        | \$5513.71  | 3.80       |
| Fear           | **\$6.70M** | 0.95     | 41.51        | \$11102.05 | 2.64       |
| Extreme Greed  | \$176.9K    | 0.45     | **49.01**    | \$9771.89  | **1.77**   |
| Neutral        | \$158.7K    | 0.72     | 31.72        | \$2663.13  | 4.09       |

---

## 💼 **10. Strategic Recommendations**

### ✅ Entry Strategy:

* **Buy during Neutral**: Lowest entry prices
* **Go Long in Fear**: High volume + upward reversal
* **Use Limit Orders**: Reduce costs, improve ROI

### ✅ Exit Strategy:

* **Sell in Extreme Greed**: Maximize profits
* **Exit Longs in Greed**: Euphoria marks peak
* **Monitor sentiment trends** to time exits

### ⚠️ Risk Management:

* Use **stop-losses based on volatility**
* **Diversify** across sentiment conditions
* Track **PnL vs Index value correlation**

---

## 🧪 **11. Strategy Simulation Results**

**Simulated Strategy:**
Buy during `Neutral` → Sell during `Greed` or `Extreme Greed`

| Metric                  | Value         |
| ----------------------- | ------------- |
| Avg Buy Price (Neutral) | \$2789.89     |
| Avg Sell Price (Greed)  | \$5271.13     |
| Potential Profit/Token  | **\$2481.24** |
| Potential ROI           | **88.94%**    |

---

## 🧭 **12. Conclusion**

This analysis supports a **mean-reversion strategy** centered around **neutral entry (buy)** and **greedy exit (sell)**, supplemented by short positions during market peaks. The **Greed/Fear index** enhances trade timing precision and helps construct a **risk-aware sentiment-driven strategy**.

---

## 🛠 Built With

* 📈 Streamlit + Plotly Dashboard
* 🧠 Pandas, NumPy, EDA Techniques
* 📅 Greed/Fear Index Classification


Here is a **professional README.md** for your Bitcoin Fear-Greed Streamlit dashboard project, based on your provided structure and deployment details.

---




## 📁 Project Structure

```bash
Bitcoin-analysis/
│
├── 📂 Charts/                             # Saved visualizations (PNL, Heatmaps, etc.)
├── 📂 Csv/                             # Saved visualizations (PNL, Heatmaps, etc.)
├──  bitcoin_app.py                      # Streamlit app entry point
├── 📄 Bitcoin_Analysis (2).ipynb          # Jupyter notebook 
├── 📄 Report.pdf                          # Report
├── 📄 requirements.txt                    # Python dependencies
├── 📄 .gitignore
├── 📄 LICENSE
└── 📄 README.md                           # Project report (this file)
```

---

## 🧠 Project Overview

### 📌 Objective

To analyze how public sentiment (Fear & Greed Index) correlates with trading behaviors and visualize:

* Classification of market sentiment
* Buy/Sell signals under emotional triggers
* Strategy simulation based on sentiment
* Profit & Loss patterns

### 📈 Data Sources

* **Fear-Greed Index**: Measures market emotion on a scale from 0 (Extreme Fear) to 100 (Extreme Greed).
* **Trade Logs**: Contains trade timestamps, price, volume, and sides (BUY/SELL).
* **Merged Dataset**: Combined above sources by timestamp into: `merged_bitcoin_trades_sentiment (2).csv`

---

## 💻 How to Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/ManavChauhan123/Bitcoin-analysis.git
cd Bitcoin-analysis
```

### 2️⃣ Create & activate virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Launch the app

```bash
streamlit run bitcoin_app.py
```

---

## 📦 Requirements

Contents of `requirements.txt`:

```txt
streamlit
pandas
numpy
plotly
```

You may update it with:

```bash
pip freeze > requirements.txt
```

---

## 🧪 Features in the Dashboard

✅ Filter by **classification** (Fear, Greed, etc.)
✅ Filter by **side** (BUY/SELL)
✅ View **sentiment timeline & histogram**
✅ View **PNL simulation** based on strategy
✅ View **raw data table** with classification
✅ Dark-themed minimalist UI with Plotly graphs

---

## 🚀 Deployment

This project is deployed using **Streamlit Cloud**:

### Deployment Steps

1. Push code to a public GitHub repository
2. Login to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click **New App**
4. Connect your repo → Set `bitcoin_app.py` as the main file
5. Add `requirements.txt` for dependency installation
6. Deploy!

---

---

## 🔗 Live Demo

👉 **[Click to View the Deployed App](https://bitcoin-fear-greed-app.streamlit.app/)**
📄 Uploaded Dataset: `merged_bitcoin_trades_sentiment (2).csv`

---
## 📚 Key Files Explained

| File                                      | Description                                    |
| ----------------------------------------- | ---------------------------------------------- |
| `bitcoin_app.py`                          | Core Streamlit app logic                       |
| `Bitcoin_Analysis (2).ipynb`              | Full analysis, EDA, data merging               |
| `merged_bitcoin_trades_sentiment (2).csv` | Final dataset with sentiment-classified trades |
| `Charts/`                                 | Visual output images used in app/report        |
| `requirements.txt`                        | Project dependencies                           |
| `README.md`                               | Project summary and usage guide                |

---

## 📈 Strategy Logic (Simplified)

The app supports a naive strategy simulation:

> **BUY during Fear** → **SELL during Greed**

This uses filtered trade data based on sentiment classification and shows hypothetical profits based on these entry/exit conditions.

---

## 🙌 Acknowledgements

* [Streamlit](https://streamlit.io/) for app framework
* [Plotly](https://plotly.com/) for interactive charts
* [Alternative.me](https://alternative.me/crypto/fear-and-greed-index/) for sentiment data



