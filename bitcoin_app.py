import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Custom CSS for blackish-purplish theme
def load_custom_css():
    st.markdown("""
    <style>
    /* Main theme colors */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e6e6fa;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2d1b69 0%, #11998e 100%);
    }
    
    /* Metrics styling */
    .metric-container {
        background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #8b5cf6;
        margin: 0.5rem;
        box-shadow: 0 4px 6px rgba(139, 92, 246, 0.3);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e6e6fa !important;
        text-shadow: 2px 2px 4px rgba(139, 92, 246, 0.5);
    }
    
    /* Custom info boxes */
    .info-box {
        background: linear-gradient(135deg, #581c87 0%, #7c2d12 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #a855f7;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #a855f7 0%, #c084fc 100%);
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.4);
        transform: translateY(-2px);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #4c1d95 0%, #581c87 100%);
        border: 1px solid #8b5cf6;
    }
    
    /* Warning/Success boxes */
    .success-box {
        background: linear-gradient(135deg, #065f46 0%, #059669 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #92400e 0%, #d97706 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Color palette for plots
PURPLE_PALETTE = [
    '#8b5cf6', '#a855f7', '#c084fc', '#ddd6fe', '#ede9fe',
    '#7c3aed', '#6d28d9', '#5b21b6', '#4c1d95', '#3730a3'
]

def create_plotly_theme():
    """Create custom plotly theme"""
    return {
        'layout': {
            'paper_bgcolor': 'rgba(26, 26, 46, 0.9)',
            'plot_bgcolor': 'rgba(22, 33, 62, 0.8)',
            'font': {'color': '#e6e6fa', 'family': 'Arial'},
            'colorway': PURPLE_PALETTE,
            'xaxis': {
                'gridcolor': 'rgba(139, 92, 246, 0.3)',
                'linecolor': 'rgba(139, 92, 246, 0.5)',
                'tickcolor': 'rgba(230, 230, 250, 0.8)',
                'color': '#e6e6fa'
            },
            'yaxis': {
                'gridcolor': 'rgba(139, 92, 246, 0.3)',
                'linecolor': 'rgba(139, 92, 246, 0.5)',
                'tickcolor': 'rgba(230, 230, 250, 0.8)',
                'color': '#e6e6fa'
            }
        }
    }

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """Create styled metric cards"""
    delta_html = ""
    if delta is not None:
        color = "#10b981" if delta_color == "normal" and delta > 0 else "#ef4444" if delta < 0 else "#6b7280"
        delta_html = f'<p style="color: {color}; margin: 0; font-size: 0.9em;">{"↑" if delta > 0 else "↓"} {abs(delta):.2f}</p>'
    
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="margin: 0; color: #e6e6fa; font-size: 1.1em;">{title}</h3>
        <p style="margin: 0; font-size: 1.8em; font-weight: bold; color: #a855f7;">{value}</p>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def plot_pnl_by_classification(df):
    """Create PnL analysis by classification"""
    pnl_data = df.groupby('classification').agg({
        'Closed PnL': ['sum', 'mean', 'count'],
        'Size USD': 'sum'
    }).round(2)
    
    pnl_data.columns = ['Total_PnL', 'Avg_PnL', 'Trade_Count', 'Volume']
    pnl_data['Win_Rate'] = df.groupby('classification')['Closed PnL'].apply(lambda x: (x > 0).mean() * 100).round(2)
    pnl_data['ROI'] = (pnl_data['Total_PnL'] / pnl_data['Volume'] * 100).round(2)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Total PnL by Classification', 'Win Rate by Classification', 
                       'Average PnL per Trade', 'ROI Percentage'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    classifications = pnl_data.index.tolist()
    
    # Total PnL
    fig.add_trace(
        go.Bar(x=classifications, y=pnl_data['Total_PnL'], 
               name='Total PnL', marker_color=PURPLE_PALETTE[0],
               hovertemplate='%{x}<br>Total PnL: $%{y:,.2f}<extra></extra>'),
        row=1, col=1
    )
    
    # Win Rate
    fig.add_trace(
        go.Bar(x=classifications, y=pnl_data['Win_Rate'], 
               name='Win Rate', marker_color=PURPLE_PALETTE[1],
               hovertemplate='%{x}<br>Win Rate: %{y:.2f}%<extra></extra>'),
        row=1, col=2
    )
    
    # Average PnL
    fig.add_trace(
        go.Bar(x=classifications, y=pnl_data['Avg_PnL'], 
               name='Avg PnL', marker_color=PURPLE_PALETTE[2],
               hovertemplate='%{x}<br>Avg PnL: $%{y:.2f}<extra></extra>'),
        row=2, col=1
    )
    
    # ROI
    fig.add_trace(
        go.Bar(x=classifications, y=pnl_data['ROI'], 
               name='ROI', marker_color=PURPLE_PALETTE[3],
               hovertemplate='%{x}<br>ROI: %{y:.2f}%<extra></extra>'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        title_text="PnL Analysis by Greed/Fear Classification",
        title_x=0.5,
        **create_plotly_theme()['layout']
    )
    
    return fig, pnl_data

def plot_buy_sell_analysis(df):
    """Create buy/sell analysis visualization"""
    buy_trades = df[df['Side'] == 'BUY']
    sell_trades = df[df['Side'] == 'SELL']
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Avg Execution Price: Buy vs Sell', 'Trading Volume by Side',
                       'Price Spread Analysis', 'Trade Count by Side'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Average execution prices
    buy_avg = buy_trades.groupby('classification')['Execution Price'].mean()
    sell_avg = sell_trades.groupby('classification')['Execution Price'].mean()
    
    fig.add_trace(
        go.Bar(x=buy_avg.index, y=buy_avg.values, name='Buy', 
               marker_color='#10b981', opacity=0.8),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(x=sell_avg.index, y=sell_avg.values, name='Sell', 
               marker_color='#ef4444', opacity=0.8),
        row=1, col=1
    )
    
    # Volume by side
    volume_data = df.groupby(['classification', 'Side'])['Size USD'].sum().unstack(fill_value=0)
    
    fig.add_trace(
        go.Bar(x=volume_data.index, y=volume_data['BUY'], name='Buy Volume', 
               marker_color='#10b981', opacity=0.8),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(x=volume_data.index, y=volume_data['SELL'], name='Sell Volume', 
               marker_color='#ef4444', opacity=0.8),
        row=1, col=2
    )
    
    # Price spread
    price_spread = sell_avg - buy_avg
    fig.add_trace(
        go.Bar(x=price_spread.index, y=price_spread.values, name='Price Spread', 
               marker_color=PURPLE_PALETTE[4]),
        row=2, col=1
    )
    
    # Trade count
    trade_count = df.groupby(['classification', 'Side']).size().unstack(fill_value=0)
    fig.add_trace(
        go.Bar(x=trade_count.index, y=trade_count['BUY'], name='Buy Count', 
               marker_color='#10b981', opacity=0.8),
        row=2, col=2
    )
    fig.add_trace(
        go.Bar(x=trade_count.index, y=trade_count['SELL'], name='Sell Count', 
               marker_color='#ef4444', opacity=0.8),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text="Buy vs Sell Analysis by Classification",
        title_x=0.5,
        **create_plotly_theme()['layout']
    )
    
    return fig

def plot_order_type_analysis(df):
    """Create order type (crossed) analysis"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('PnL by Order Type', 'Win Rate Heatmap', 
                       'Average PnL Heatmap', 'Fee Analysis'),
        specs=[[{"secondary_y": False}, {"type": "heatmap"}],
               [{"type": "heatmap"}, {"secondary_y": False}]]
    )
    
    # PnL by order type
    order_pnl = df.groupby('Crossed')['Closed PnL'].sum()
    order_labels = ['Limit Order', 'Market Order']
    
    fig.add_trace(
        go.Bar(x=order_labels, y=order_pnl.values, 
               marker_color=[PURPLE_PALETTE[0], PURPLE_PALETTE[2]]),
        row=1, col=1
    )
    
    # Win rate heatmap
    win_rate_data = df.groupby(['Crossed', 'classification'])['Closed PnL'].apply(
        lambda x: (x > 0).mean() * 100
    ).unstack()
    
    fig.add_trace(
        go.Heatmap(
            z=win_rate_data.values,
            x=win_rate_data.columns,
            y=['Limit Order', 'Market Order'],
            colorscale='Viridis',
            showscale=True
        ),
        row=1, col=2
    )
    
    # Average PnL heatmap
    avg_pnl_data = df.groupby(['Crossed', 'classification'])['Closed PnL'].mean().unstack()
    
    fig.add_trace(
        go.Heatmap(
            z=avg_pnl_data.values,
            x=avg_pnl_data.columns,
            y=['Limit Order', 'Market Order'],
            colorscale='RdYlGn',
            showscale=True
        ),
        row=2, col=1
    )
    
    # Fee analysis
    fee_data = df.groupby(['Crossed', 'classification'])['Fee'].mean().unstack()
    
    for i, classification in enumerate(fee_data.columns):
        fig.add_trace(
            go.Bar(x=['Limit Order', 'Market Order'], y=fee_data[classification].values, 
                   name=classification, marker_color=PURPLE_PALETTE[i % len(PURPLE_PALETTE)]),
            row=2, col=2
        )
    
    fig.update_layout(
        height=600,
        title_text="Order Type Analysis (Market vs Limit Orders)",
        title_x=0.5,
        **create_plotly_theme()['layout']
    )
    
    return fig

def plot_value_analysis(df):
    """Create greed/fear index value analysis"""
    value_data = df.groupby('value').agg({
        'Closed PnL': ['sum', 'mean', 'count'],
        'Size USD': 'sum',
        'Execution Price': 'mean'
    }).round(2)
    
    value_data.columns = ['Total_PnL', 'Avg_PnL', 'Trade_Count', 'Volume', 'Avg_Price']
    value_data['Win_Rate'] = df.groupby('value')['Closed PnL'].apply(lambda x: (x > 0).mean() * 100).round(2)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Total PnL by Index Value', 'Win Rate by Index Value',
                       'Index Value vs PnL Scatter', 'Correlation Matrix'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"type": "heatmap"}]]
    )
    
    # Total PnL by value
    fig.add_trace(
        go.Bar(x=value_data.index, y=value_data['Total_PnL'], 
               marker_color=PURPLE_PALETTE[0]),
        row=1, col=1
    )
    
    # Win rate by value
    fig.add_trace(
        go.Bar(x=value_data.index, y=value_data['Win_Rate'], 
               marker_color=PURPLE_PALETTE[1]),
        row=1, col=2
    )
    
    # Scatter plot: Value vs PnL
    sample_df = df.sample(min(1000, len(df)))
    fig.add_trace(
        go.Scatter(x=sample_df['value'], y=sample_df['Closed PnL'], 
                   mode='markers', marker_color=PURPLE_PALETTE[2],
                   opacity=0.6, name='PnL vs Value'),
        row=2, col=1
    )
    
    # Correlation matrix
    corr_data = df[['value', 'Closed PnL', 'Execution Price', 'Size USD']].corr()
    fig.add_trace(
        go.Heatmap(
            z=corr_data.values,
            x=corr_data.columns,
            y=corr_data.columns,
            colorscale='RdBu',
            showscale=True,
            text=corr_data.values,
            texttemplate='%{text:.3f}'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text="Greed/Fear Index Value Analysis",
        title_x=0.5,
        **create_plotly_theme()['layout']
    )
    
    return fig, value_data

def plot_direction_analysis(df):
    """Create trading direction analysis"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('PnL by Direction', 'Direction Frequency',
                       'Long vs Short Performance', 'Direction PnL Heatmap'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"type": "heatmap"}]]
    )
    
    # PnL by direction
    direction_pnl = df.groupby('Direction')['Closed PnL'].sum().sort_values(ascending=False)
    
    fig.add_trace(
        go.Bar(y=direction_pnl.index, x=direction_pnl.values, 
               orientation='h', marker_color=PURPLE_PALETTE[0]),
        row=1, col=1
    )
    
    # Direction frequency
    direction_freq = df['Direction'].value_counts()
    fig.add_trace(
        go.Bar(x=direction_freq.index, y=direction_freq.values, 
               marker_color=PURPLE_PALETTE[1]),
        row=1, col=2
    )
    
    # Long vs Short comparison
    long_directions = ['Open Long', 'Close Long', 'Buy']
    short_directions = ['Open Short', 'Close Short', 'Sell']
    
    long_trades = df[df['Direction'].isin(long_directions)]
    short_trades = df[df['Direction'].isin(short_directions)]
    
    comparison_data = {
        'Strategy': ['Long', 'Short'],
        'Total_PnL': [long_trades['Closed PnL'].sum(), short_trades['Closed PnL'].sum()],
        'Win_Rate': [(long_trades['Closed PnL'] > 0).mean() * 100, 
                     (short_trades['Closed PnL'] > 0).mean() * 100]
    }
    
    fig.add_trace(
        go.Bar(x=comparison_data['Strategy'], y=comparison_data['Total_PnL'], 
               name='Total PnL', marker_color=PURPLE_PALETTE[2]),
        row=2, col=1
    )
    
    # Direction PnL heatmap
    direction_heatmap = df.groupby(['Direction', 'classification'])['Closed PnL'].mean().unstack()
    
    fig.add_trace(
        go.Heatmap(
            z=direction_heatmap.values,
            x=direction_heatmap.columns,
            y=direction_heatmap.index,
            colorscale='RdYlGn',
            showscale=True
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text="Trading Direction Analysis",
        title_x=0.5,
        **create_plotly_theme()['layout']
    )
    
    return fig, comparison_data

def plot_execution_price_analysis(df):
    """Create execution price analysis"""
    price_stats = df.groupby('classification')['Execution Price'].agg([
        'mean', 'std', 'min', 'max', 'median'
    ]).round(4)
    
    price_stats['CV'] = (price_stats['std'] / price_stats['mean']).round(4)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Price Distribution by Classification', 'Average Price by Classification',
                       'Price Volatility (CV)', 'Price Range Analysis'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Box plot for price distribution
    for i, classification in enumerate(df['classification'].unique()):
        subset = df[df['classification'] == classification]
        fig.add_trace(
            go.Box(y=subset['Execution Price'], name=classification,
                   marker_color=PURPLE_PALETTE[i % len(PURPLE_PALETTE)]),
            row=1, col=1
        )
    
    # Average price
    fig.add_trace(
        go.Bar(x=price_stats.index, y=price_stats['mean'], 
               marker_color=PURPLE_PALETTE[0]),
        row=1, col=2
    )
    
    # Price volatility (CV)
    fig.add_trace(
        go.Bar(x=price_stats.index, y=price_stats['CV'], 
               marker_color=PURPLE_PALETTE[1]),
        row=2, col=1
    )
    
    # Price range
    price_range = price_stats['max'] - price_stats['min']
    fig.add_trace(
        go.Bar(x=price_stats.index, y=price_range.values, 
               marker_color=PURPLE_PALETTE[2]),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text="Execution Price Analysis by Classification",
        title_x=0.5,
        showlegend=False,
        **create_plotly_theme()['layout']
    )
    
    return fig, price_stats

def main():
    # Load custom CSS
    load_custom_css()
    
    # App header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3em; margin-bottom: 0;">🚀 Bitcoin Trading Analytics</h1>
        <p style="font-size: 1.2em; color: #a855f7; margin-top: 0;">Greed & Fear Index Trading Strategy Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown("### 📊 Dashboard Controls")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload your CSV file", 
        type=['csv'],
        help="Upload your Bitcoin trading data CSV file"
    )
    
    # Check if file is uploaded
    if uploaded_file is None:
        st.sidebar.warning("⚠️ Please upload a CSV file to proceed.")
        st.markdown("""
        <div class="warning-box">
            <h3>⚠️ No Data Uploaded</h3>
            <p>Please upload a valid CSV file using the sidebar to view the analytics dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
        return  # Stop execution until a file is uploaded
    
    # Load and validate data
    try:
        df = pd.read_csv(uploaded_file)
        # Check if required columns exist
        required_columns = ['date_only', 'classification', 'Side', 'Closed PnL', 'Size USD', 'Execution Price', 'Crossed', 'Direction', 'value']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.sidebar.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
            st.markdown(f"""
            <div class="warning-box">
                <h3>❌ Invalid Data Format</h3>
                <p>The uploaded CSV file is missing the following required columns: {', '.join(missing_columns)}</p>
                <p>Please ensure your CSV contains all required columns: {', '.join(required_columns)}</p>
            </div>
            """, unsafe_allow_html=True)
            return  # Stop execution if required columns are missing
        
        # Convert date_only to datetime and set as index
        if 'date_only' in df.columns:
            df['date_only'] = pd.to_datetime(df['date_only'])
            df.set_index('date_only', inplace=True)
        st.sidebar.success("✅ Data loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading file: {str(e)}")
        st.markdown(f"""
        <div class="warning-box">
            <h3>❌ Error Loading File</h3>
            <p>An error occurred while loading the CSV file: {str(e)}</p>
            <p>Please upload a valid CSV file with the correct format.</p>
        </div>
        """, unsafe_allow_html=True)
        return  # Stop execution if file loading fails
    
    # Analysis options
    st.sidebar.markdown("### 🎯 Analysis Options")
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        ["📈 Overview", "💰 PnL Analysis", "🔄 Buy/Sell Analysis", 
         "📋 Order Type Analysis", "📊 Value Analysis", 
         "🎯 Direction Analysis", "💲 Price Analysis", "🚀 Strategy Recommendations"]
    )
    
    # Filter options
    st.sidebar.markdown("### 🔍 Filters")
    
    selected_classifications = st.sidebar.multiselect(
        "Select Classifications",
        options=df['classification'].unique(),
        default=df['classification'].unique()
    )
    
    selected_sides = st.sidebar.multiselect(
        "Select Trading Sides",
        options=df['Side'].unique(),
        default=df['Side'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['classification'].isin(selected_classifications)) &
        (df['Side'].isin(selected_sides))
    ]
    
    # Check if filtered data is empty
    if filtered_df.empty:
        st.markdown("""
        <div class="warning-box">
            <h3>⚠️ No Data Available</h3>
            <p>The selected filters result in no data. Please adjust the classification or side filters.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Main content based on analysis type
    if analysis_type == "📈 Overview":
        st.markdown("## 📊 Data Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_metric_card("Total Trades", f"{len(filtered_df):,}")
        
        with col2:
            total_pnl = filtered_df['Closed PnL'].sum()
            create_metric_card("Total PnL", f"${total_pnl:,.2f}")
        
        with col3:
            win_rate = (filtered_df['Closed PnL'] > 0).mean() * 100
            create_metric_card("Win Rate", f"{win_rate:.1f}%")
        
        with col4:
            total_volume = filtered_df['Size USD'].sum()
            create_metric_card("Total Volume", f"${total_volume:,.0f}")
        
        # Data summary
        st.markdown("### 📋 Data Summary")
        summary_data = {
            'Metric': ['Date Range', 'Most Active Classification', 'Preferred Side', 'Average Trade Size'],
            'Value': [
                f"{filtered_df.index.min().strftime('%Y-%m-%d')} to {filtered_df.index.max().strftime('%Y-%m-%d')}",
                filtered_df['classification'].value_counts().index[0],
                filtered_df['Side'].value_counts().index[0],
                f"${filtered_df['Size USD'].mean():,.2f}"
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True)
        
        # Quick insights
        st.markdown("""
        <div class="info-box">
            <h3>💡 Quick Insights</h3>
            <p>• Use the sidebar to filter data by classification and trading side</p>
            <p>• Navigate through different analysis sections to get detailed insights</p>
            <p>• All visualizations are interactive - hover for details</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif analysis_type == "💰 PnL Analysis":
        st.markdown("## 💰 PnL Analysis by Classification")
        
        fig, pnl_data = plot_pnl_by_classification(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        best_pnl = pnl_data['Total_PnL'].idxmax()
        best_roi = pnl_data['ROI'].idxmax()
        best_win_rate = pnl_data['Win_Rate'].idxmax()
        
        st.markdown(f"""
        <div class="success-box">
            <h3>🎯 Key Insights - PnL Analysis</h3>
            <p><strong>Best Total PnL:</strong> {best_pnl} (${pnl_data.loc[best_pnl, 'Total_PnL']:,.2f})</p>
            <p><strong>Best ROI:</strong> {best_roi} ({pnl_data.loc[best_roi, 'ROI']:.2f}%)</p>
            <p><strong>Highest Win Rate:</strong> {best_win_rate} ({pnl_data.loc[best_win_rate, 'Win_Rate']:.2f}%)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed table
        st.markdown("### 📊 Detailed PnL Statistics")
        st.dataframe(pnl_data.round(2), use_container_width=True)
    
    elif analysis_type == "🔄 Buy/Sell Analysis":
        st.markdown("## 🔄 Buy vs Sell Analysis")
        
        fig = plot_buy_sell_analysis(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Buy/Sell insights
        buy_trades = filtered_df[filtered_df['Side'] == 'BUY']
        sell_trades = filtered_df[filtered_df['Side'] == 'SELL']
        
        buy_avg_prices = buy_trades.groupby('classification')['Execution Price'].mean()
        sell_avg_prices = sell_trades.groupby('classification')['Execution Price'].mean()
        
        best_buy_classification = buy_avg_prices.idxmin() if not buy_avg_prices.empty else "N/A"
        best_sell_classification = sell_avg_prices.idxmax() if not sell_avg_prices.empty else "N/A"
        
        st.markdown(f"""
        <div class="success-box">
            <h3>🎯 Key Insights - Buy/Sell Analysis</h3>
            <p><strong>Best time to BUY:</strong> During '{best_buy_classification}' (Avg: ${buy_avg_prices.min():.4f if not buy_avg_prices.empty else 'N/A'})</p>
            <p><strong>Best time to SELL:</strong> During '{best_sell_classification}' (Avg: ${sell_avg_prices.max():.4f if not sell_avg_prices.empty else 'N/A'})</p>
            <p><strong>Price Spread:</strong> ${(sell_avg_prices.max() - buy_avg_prices.min()):.4f if not (buy_avg_prices.empty or sell_avg_prices.empty) else 'N/A'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Side-by-side comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🟢 Buy Trades Summary")
            buy_summary = buy_trades.groupby('classification').agg({
                'Execution Price': 'mean',
                'Size USD': 'sum',
                'Size Tokens': 'sum'
            }).round(4)
            st.dataframe(buy_summary, use_container_width=True)
        
        with col2:
            st.markdown("### 🔴 Sell Trades Summary")
            sell_summary = sell_trades.groupby('classification').agg({
                'Execution Price': 'mean',
                'Size USD': 'sum',
                'Closed PnL': 'sum'
            }).round(4)
            st.dataframe(sell_summary, use_container_width=True)
    
    elif analysis_type == "📋 Order Type Analysis":
        st.markdown("## 📋 Order Type Analysis (Market vs Limit)")
        
        fig = plot_order_type_analysis(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Order type insights
        market_pnl = filtered_df[filtered_df['Crossed'] == True]['Closed PnL'].sum()
        limit_pnl = filtered_df[filtered_df['Crossed'] == False]['Closed PnL'].sum()
        
        market_win_rate = (filtered_df[filtered_df['Crossed'] == True]['Closed PnL'] > 0).mean() * 100
        limit_win_rate = (filtered_df[filtered_df['Crossed'] == False]['Closed PnL'] > 0).mean() * 100
        
        better_order_type = "Market Orders" if market_pnl > limit_pnl else "Limit Orders"
        
        st.markdown(f"""
        <div class="success-box">
            <h3>🎯 Key Insights - Order Type Analysis</h3>
            <p><strong>Market Orders PnL:</strong> ${market_pnl:,.2f} (Win Rate: {market_win_rate:.2f}%)</p>
            <p><strong>Limit Orders PnL:</strong> ${limit_pnl:,.2f} (Win Rate: {limit_win_rate:.2f}%)</p>
            <p><strong>Recommended:</strong> {better_order_type}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed breakdown
        st.markdown("### 📊 Order Type Breakdown by Classification")
        order_breakdown = filtered_df.groupby(['Crossed', 'classification']).agg({
            'Closed PnL': ['sum', 'mean', 'count'],
            'Fee': 'mean'
        }).round(4)
        order_breakdown.columns = ['Total_PnL', 'Avg_PnL', 'Count', 'Avg_Fee']
        
        st.dataframe(order_breakdown, use_container_width=True)
    
    elif analysis_type == "📊 Value Analysis":
        st.markdown("## 📊 Greed/Fear Index Value Analysis")
        
        fig, value_data = plot_value_analysis(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Value insights
        best_value_pnl = value_data['Total_PnL'].idxmax()
        best_value_win_rate = value_data['Win_Rate'].idxmax()
        
        # Correlation insights
        correlation = filtered_df[['value', 'Closed PnL', 'Execution Price', 'Size USD']].corr()
        value_pnl_corr = correlation.loc['value', 'Closed PnL']
        
        st.markdown(f"""
        <div class="success-box">
            <h3>🎯 Key Insights - Index Value Analysis</h3>
            <p><strong>Most Profitable Value:</strong> {best_value_pnl} (PnL: ${value_data.loc[best_value_pnl, 'Total_PnL']:,.2f})</p>
            <p><strong>Highest Win Rate Value:</strong> {best_value_win_rate} ({value_data.loc[best_value_win_rate, 'Win_Rate']:.2f}%)</p>
            <p><strong>Value-PnL Correlation:</strong> {value_pnl_corr:.4f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Value mapping
        st.markdown("### 🎭 Index Value Mapping")
        value_mapping = filtered_df.groupby(['value', 'classification']).size().unstack(fill_value=0)
        st.dataframe(value_mapping, use_container_width=True)
        
        # Detailed value statistics
        st.markdown("### 📈 Detailed Value Statistics")
        st.dataframe(value_data.round(2), use_container_width=True)
    
    elif analysis_type == "🎯 Direction Analysis":
        st.markdown("## 🎯 Trading Direction Analysis")
        
        fig, comparison_data = plot_direction_analysis(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Direction insights
        long_directions = ['Open Long', 'Close Long', 'Buy']
        short_directions = ['Open Short', 'Close Short', 'Sell']
        
        long_trades = filtered_df[filtered_df['Direction'].isin(long_directions)]
        short_trades = filtered_df[filtered_df['Direction'].isin(short_directions)]
        
        long_pnl = long_trades['Closed PnL'].sum()
        short_pnl = short_trades['Closed PnL'].sum()
        
        better_strategy = "Long Strategy" if long_pnl > short_pnl else "Short Strategy"
        
        st.markdown(f"""
        <div class="success-box">
            <h3>🎯 Key Insights - Direction Analysis</h3>
            <p><strong>Long Strategy PnL:</strong> ${long_pnl:,.2f} ({len(long_trades):,} trades)</p>
            <p><strong>Short Strategy PnL:</strong> ${short_pnl:,.2f} ({len(short_trades):,} trades)</p>
            <p><strong>Recommended Strategy:</strong> {better_strategy}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Direction performance table
        st.markdown("### 📊 Direction Performance Summary")
        direction_summary = filtered_df.groupby('Direction').agg({
            'Closed PnL': ['sum', 'mean', 'count'],
            'Size USD': 'sum'
        }).round(2)
        direction_summary.columns = ['Total_PnL', 'Avg_PnL', 'Trade_Count', 'Volume']
        direction_summary['Win_Rate'] = filtered_df.groupby('Direction')['Closed PnL'].apply(
            lambda x: (x > 0).mean() * 100
        ).round(2)
        
        st.dataframe(direction_summary.sort_values('Total_PnL', ascending=False), use_container_width=True)
    
    elif analysis_type == "💲 Price Analysis":
        st.markdown("## 💲 Execution Price Analysis")
        
        fig, price_stats = plot_execution_price_analysis(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Price insights
        highest_avg_price = price_stats['mean'].idxmax()
        most_volatile = price_stats['CV'].idxmax()
        lowest_avg_price = price_stats['mean'].idxmin()
        
        st.markdown(f"""
        <div class="success-box">
            <h3>🎯 Key Insights - Price Analysis</h3>
            <p><strong>Highest Avg Price:</strong> {highest_avg_price} (${price_stats.loc[highest_avg_price, 'mean']:.4f})</p>
            <p><strong>Lowest Avg Price:</strong> {lowest_avg_price} (${price_stats.loc[lowest_avg_price, 'mean']:.4f})</p>
            <p><strong>Most Volatile:</strong> {most_volatile} (CV: {price_stats.loc[most_volatile, 'CV']:.4f})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Price statistics table
        st.markdown("### 📊 Price Statistics by Classification")
        st.dataframe(price_stats.round(4), use_container_width=True)
        
        # Price trend analysis
        st.markdown("### 📈 Price Trend Over Time")
        price_trend = filtered_df.groupby([filtered_df.index.date, 'classification'])['Execution Price'].mean().unstack()
        
        price_trend_fig = px.line(
            price_trend.reset_index(), 
            x='date_only', 
            y=price_trend.columns.tolist(),
            title="Average Execution Price Trend by Classification",
            color_discrete_sequence=PURPLE_PALETTE
        )
        price_trend_fig.update_layout(**create_plotly_theme()['layout'])
        st.plotly_chart(price_trend_fig, use_container_width=True)
    
    elif analysis_type == "🚀 Strategy Recommendations":
        st.markdown("## 🚀 Trading Strategy Recommendations")
        
        # Calculate strategy metrics
        strategy_metrics = {}
        
        for classification in filtered_df['classification'].unique():
            subset = filtered_df[filtered_df['classification'] == classification]
            
            strategy_metrics[classification] = {
                'total_pnl': subset['Closed PnL'].sum(),
                'win_rate': (subset['Closed PnL'] > 0).mean() * 100,
                'avg_pnl': subset['Closed PnL'].mean(),
                'roi': (subset['Closed PnL'].sum() / subset['Size USD'].sum()) * 100,
                'trade_count': len(subset),
                'avg_price': subset['Execution Price'].mean(),
                'price_volatility': subset['Execution Price'].std() / subset['Execution Price'].mean()
            }
        
        strategy_df = pd.DataFrame(strategy_metrics).T
        
        # Strategy performance matrix
        st.markdown("### 📊 Strategy Performance Matrix")
        st.dataframe(strategy_df.round(4), use_container_width=True)
        
        # Rankings
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏆 Performance Rankings")
            rankings = {
                'Best Total PnL': strategy_df['total_pnl'].idxmax(),
                'Best Win Rate': strategy_df['win_rate'].idxmax(),
                'Best ROI': strategy_df['roi'].idxmax(),
                'Most Active': strategy_df['trade_count'].idxmax()
            }
            
            for metric, classification in rankings.items():
                st.markdown(f"**{metric}:** {classification}")
        
        with col2:
            st.markdown("### 📈 Strategy Recommendations")
            
            # Buy strategy
            buy_trades = filtered_df[filtered_df['Side'] == 'BUY']
            buy_recommendations = buy_trades.groupby('classification')['Execution Price'].mean().sort_values()
            
            # Sell strategy
            sell_trades = filtered_df[filtered_df['Side'] == 'SELL']
            sell_recommendations = sell_trades.groupby('classification')['Execution Price'].mean().sort_values(ascending=False)
            
            st.markdown(f"**🟢 Best Buy Period:** {buy_recommendations.index[0] if not buy_recommendations.empty else 'N/A'}")
            st.markdown(f"**🔴 Best Sell Period:** {sell_recommendations.index[0] if not sell_recommendations.empty else 'N/A'}")
            
            # Order type recommendation
            market_pnl = filtered_df[filtered_df['Crossed'] == True]['Closed PnL'].sum()
            limit_pnl = filtered_df[filtered_df['Crossed'] == False]['Closed PnL'].sum()
            better_order = "Market Orders" if market_pnl > limit_pnl else "Limit Orders"
            st.markdown(f"**📋 Preferred Orders:** {better_order}")
        
        # Comprehensive strategy
        st.markdown("""
        <div class="info-box">
            <h3>🎯 Comprehensive Trading Strategy</h3>
            <p><strong>Entry Strategy:</strong></p>
            <ul>
                <li>Buy when sentiment is <strong>Neutral</strong> for lowest entry prices (mean-reversion setup)</li>
                <li>Go Long during "Fear" as the market shows strong buy-side interest and profit-taking from previous shorts</li>
                <li>Use limit orders if they show better performance</li>
                <li>Focus on high-volume classifications for better liquidity</li>
            </ul>
            <p><strong>Exit Strategy:</strong></p>
            <ul> 
                <li>For maximum profit, target <strong>"Extreme Greed"</strong> as the ideal exit (highest avg price)</li>
                <li>Initiate Shorts or Exit Longs during “Greed” as smart money is likely selling into buyer euphoria</li>
                <li>Sell when Win Rate and Profit Factor start dropping post-extreme sentiment spikes</li>
                <li>Monitor win rates by classification for optimal timing</li>
                <li>Consider market conditions and volatility</li>
            </ul>
            <p><strong>Risk Management:</strong></p>
            <ul>
                <li>Diversify across different market conditions</li>
                <li>Set stop-losses based on historical volatility</li>
                <li>Monitor correlation between index values and PnL</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Strategy backtesting simulation
        st.markdown("### 🧪 Strategy Simulation")
        
        if st.button("🚀 Run Strategy Simulation", help="Simulate the recommended strategy"):
            with st.spinner("Running simulation..."):
                # Simple simulation based on buy low (Fear) sell high (Greed) strategy
                fear_buys = filtered_df[(filtered_df['classification'] == 'Neutral') & (filtered_df['Side'] == 'BUY')]
                greed_sells = filtered_df[(filtered_df['classification'].isin(['Greed', 'Extreme Greed'])) & (filtered_df['Side'] == 'SELL')]
                
                if len(fear_buys) > 0 and len(greed_sells) > 0:
                    avg_buy_price = fear_buys['Execution Price'].mean()
                    avg_sell_price = greed_sells['Execution Price'].mean()
                    
                    potential_profit = avg_sell_price - avg_buy_price
                    roi_potential = (potential_profit / avg_buy_price) * 100
                    
                    st.success(f"""
                    📊 **Strategy Simulation Results:**
                    - Average Buy Price (Neutral): ${avg_buy_price:.4f}
                    - Average Sell Price (Greed): ${avg_sell_price:.4f}
                    - Potential Profit per Token: ${potential_profit:.4f}
                    - Potential ROI: {roi_potential:.2f}%
                    """)
                else:
                    st.warning("Insufficient data for simulation with current filters.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #a855f7;">
        <p>💜 Built with Streamlit & Plotly | Bitcoin Trading Analytics Dashboard</p>
        <p>📊 Navigate through different analysis sections to discover trading insights</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()