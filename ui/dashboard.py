"""
AI Cost Observatory Dashboard
Open-source observability layer for agentic systems
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Configuration
# When running in Docker, use internal network hostname
# When running locally, use localhost
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Show connection info in sidebar
def show_api_info():
    """Display API connection info"""
    st.sidebar.info(f"API: {API_URL}")

st.set_page_config(
    page_title="AI Cost Observatory",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


def fetch_data(endpoint, params=None):
    """Fetch data from API"""
    try:
        response = requests.get(f"{API_URL}/{endpoint}", params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error(f"Request timed out while fetching {endpoint}. The API may be processing a large dataset.")
        return None
    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to API at {API_URL}. Make sure the API is running.")
        return None
    except Exception as e:
        st.error(f"Error fetching data from {endpoint}: {str(e)}")
        return None


def main():
    """Main dashboard"""
    
    # Header
    st.title("🔭 AI Cost Observatory")
    st.markdown("Open-source observability layer for agentic systems")
    
    # Sidebar
    st.sidebar.title("Filters")
    
    # Show API connection info
    show_api_info()
    
    project_filter = st.sidebar.text_input("Project", "")
    
    # Date range
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
    )
    
    # Navigation
    page = st.sidebar.radio(
        "Navigate",
        ["Overview", "Agent Breakdown", "Request Explorer", "Forecast", "Optimization"]
    )
    
    # Route to pages
    if page == "Overview":
        show_overview(project_filter)
    elif page == "Agent Breakdown":
        show_agent_breakdown(project_filter, date_range)
    elif page == "Request Explorer":
        show_request_explorer(project_filter, date_range)
    elif page == "Forecast":
        show_forecast(project_filter)
    elif page == "Optimization":
        show_optimization(project_filter)


def show_overview(project_filter):
    """Show overview dashboard"""
    st.header("📊 Overview")
    
    # Fetch overview data
    params = {"project": project_filter} if project_filter else {}
    data = fetch_data("dashboard/overview", params)
    
    if not data:
        st.warning("No data available. Start tracking LLM calls to see metrics.")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Today's Cost",
            value=f"${data['today_cost']:.4f}",
            delta=None,
        )
    
    with col2:
        st.metric(
            label="Month's Cost",
            value=f"${data['month_cost']:.2f}",
            delta=None,
        )
    
    with col3:
        st.metric(
            label="Total Tokens",
            value=f"{data['total_tokens']:,}",
            delta=None,
        )
    
    with col4:
        st.metric(
            label="Avg Cost/Request",
            value=f"${data['avg_cost_per_request']:.6f}",
            delta=None,
        )
    
    # Cost over time chart
    st.subheader("💰 Cost Over Time")
    if data.get('cost_over_time'):
        df_cost = pd.DataFrame(data['cost_over_time'])
        df_cost['timestamp'] = pd.to_datetime(df_cost['timestamp'])
        
        fig = px.line(
            df_cost,
            x='timestamp',
            y='value',
            title='Daily Cost Trend',
            labels={'value': 'Cost (USD)', 'timestamp': 'Date'},
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Two columns for models and agents
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Top Models")
        if data.get('top_models'):
            df_models = pd.DataFrame(data['top_models'])
            
            fig = px.bar(
                df_models,
                x='model',
                y='cost',
                title='Cost by Model',
                labels={'cost': 'Cost (USD)', 'model': 'Model'},
                color='cost',
                color_continuous_scale='Viridis',
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show table
            st.dataframe(
                df_models[['model', 'requests', 'tokens', 'cost']],
                hide_index=True,
                use_container_width=True,
            )
    
    with col2:
        st.subheader("🎯 Top Agents")
        if data.get('top_agents'):
            df_agents = pd.DataFrame(data['top_agents'])
            
            fig = px.bar(
                df_agents,
                x='agent',
                y='cost',
                title='Cost by Agent',
                labels={'cost': 'Cost (USD)', 'agent': 'Agent'},
                color='cost',
                color_continuous_scale='Blues',
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show table
            st.dataframe(
                df_agents[['agent', 'requests', 'tokens', 'cost']],
                hide_index=True,
                use_container_width=True,
            )


def show_agent_breakdown(project_filter, date_range):
    """Show agent breakdown"""
    st.header("🎯 Agent Breakdown")
    
    params = {
        "project": project_filter if project_filter else None,
    }
    
    # Add date range if available
    if len(date_range) > 0:
        # Convert date to datetime string with time component
        start_datetime = datetime.combine(date_range[0], datetime.min.time())
        params["start_date"] = start_datetime.isoformat()
    
    if len(date_range) > 1:
        # Convert date to datetime string with time component (end of day)
        end_datetime = datetime.combine(date_range[1], datetime.max.time())
        params["end_date"] = end_datetime.isoformat()
    
    params = {k: v for k, v in params.items() if v is not None}
    
    data = fetch_data("stats/agents", params)
    
    if not data:
        st.warning("No agent data available.")
        return
    
    df = pd.DataFrame(data)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Agents", len(df))
    
    with col2:
        st.metric("Total Requests", df['requests'].sum())
    
    with col3:
        st.metric("Total Cost", f"${df['cost'].sum():.4f}")
    
    # Agent comparison
    st.subheader("Agent Comparison")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Requests',
        x=df['agent'],
        y=df['requests'],
        yaxis='y',
        offsetgroup=1,
    ))
    
    fig.add_trace(go.Bar(
        name='Cost ($)',
        x=df['agent'],
        y=df['cost'],
        yaxis='y2',
        offsetgroup=2,
    ))
    
    fig.update_layout(
        title='Agent Requests and Cost',
        xaxis=dict(title='Agent'),
        yaxis=dict(title='Requests'),
        yaxis2=dict(title='Cost (USD)', overlaying='y', side='right'),
        barmode='group',
        height=500,
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.subheader("Agent Details")
    st.dataframe(
        df.sort_values('cost', ascending=False),
        hide_index=True,
        use_container_width=True,
    )


def show_request_explorer(project_filter, date_range):
    """Show request explorer"""
    st.header("🔍 Request Explorer")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        agent_filter = st.text_input("Agent", "")
    
    with col2:
        model_filter = st.text_input("Model", "")
    
    with col3:
        limit = st.number_input("Limit", min_value=10, max_value=1000, value=100)
    
    # Fetch events
    params = {
        "project": project_filter if project_filter else None,
        "agent": agent_filter if agent_filter else None,
        "model": model_filter if model_filter else None,
        "limit": limit,
    }
    
    # Add date range if available
    if len(date_range) > 0:
        # Convert date to datetime string with time component
        start_datetime = datetime.combine(date_range[0], datetime.min.time())
        params["start_date"] = start_datetime.isoformat()
    
    if len(date_range) > 1:
        # Convert date to datetime string with time component (end of day)
        end_datetime = datetime.combine(date_range[1], datetime.max.time())
        params["end_date"] = end_datetime.isoformat()
    
    params = {k: v for k, v in params.items() if v is not None}
    
    data = fetch_data("events", params)
    
    if not data:
        st.warning("No events found.")
        return
    
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Summary
    st.subheader("Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Requests", len(df))
    
    with col2:
        st.metric("Total Tokens", df['total_tokens'].sum())
    
    with col3:
        st.metric("Total Cost", f"${df['total_cost'].sum():.4f}")
    
    with col4:
        st.metric("Avg Latency", f"{df['latency_ms'].mean():.0f}ms")
    
    # Events table
    st.subheader("Recent Events")
    
    display_df = df[[
        'timestamp', 'project', 'agent', 'model',
        'prompt_tokens', 'completion_tokens', 'total_cost', 'latency_ms'
    ]].copy()
    
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    display_df['total_cost'] = display_df['total_cost'].apply(lambda x: f"${x:.6f}")
    
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
        height=400,
    )


def show_forecast(project_filter):
    """Show cost forecast"""
    st.header("📈 Cost Forecast")
    
    params = {"project": project_filter} if project_filter else {}
    data = fetch_data("forecast", params)
    
    if not data:
        st.warning("No forecast data available.")
        return
    
    # Display forecast
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Monthly Projection",
            value=f"${data['monthly_projection']:.2f}",
        )
    
    with col2:
        st.metric(
            label="Daily Average",
            value=f"${data['daily_average']:.4f}",
        )
    
    with col3:
        trend_emoji = "📈" if data['trend'] == "increasing" else "📉" if data['trend'] == "decreasing" else "➡️"
        st.metric(
            label="Trend",
            value=f"{trend_emoji} {data['trend'].title()}",
        )
    
    # Forecast details
    st.subheader("Forecast Details")
    
    st.info(f"""
    **Confidence Level:** {data['confidence'].title()}
    
    **Analysis:**
    - At the current rate, your projected monthly spend is **${data['monthly_projection']:.2f}**
    - Daily average cost: **${data['daily_average']:.4f}**
    - Trend: **{data['trend'].title()}**
    
    {"⚠️ Your costs are increasing. Consider reviewing the optimization suggestions." if data['trend'] == 'increasing' else ""}
    """)
    
    # Projection visualization
    st.subheader("30-Day Projection")
    
    days = list(range(1, 31))
    projected_costs = [data['daily_average'] * i for i in days]
    
    df_projection = pd.DataFrame({
        'Day': days,
        'Projected Cumulative Cost': projected_costs,
    })
    
    fig = px.line(
        df_projection,
        x='Day',
        y='Projected Cumulative Cost',
        title='30-Day Cost Projection',
        labels={'Projected Cumulative Cost': 'Cost (USD)', 'Day': 'Days from Now'},
    )
    fig.add_hline(
        y=data['monthly_projection'],
        line_dash="dash",
        line_color="red",
        annotation_text=f"Monthly Projection: ${data['monthly_projection']:.2f}",
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def show_optimization(project_filter):
    """Show optimization suggestions"""
    st.header("💡 Optimization Suggestions")
    
    params = {"project": project_filter} if project_filter else {}
    data = fetch_data("optimize", params)
    
    if not data:
        st.success("✅ No optimization suggestions at this time. Your setup looks efficient!")
        return
    
    st.info(f"Found {len(data)} optimization opportunities")
    
    # Calculate total potential savings
    total_savings = sum(s['estimated_savings'] for s in data)
    st.metric(
        label="Total Potential Savings (30 days)",
        value=f"${total_savings:.2f}",
    )
    
    # Show suggestions
    for i, suggestion in enumerate(data, 1):
        with st.expander(
            f"💰 Suggestion {i}: {suggestion['type'].title()} - Save ${suggestion['estimated_savings']:.2f} ({suggestion['estimated_savings_percent']:.0f}%)",
            expanded=True,
        ):
            st.markdown(f"**Type:** {suggestion['type'].title()}")
            st.markdown(f"**Current:** {suggestion['current']}")
            st.markdown(f"**Suggested:** {suggestion['suggested']}")
            st.markdown(f"**Estimated Savings:** ${suggestion['estimated_savings']:.2f} ({suggestion['estimated_savings_percent']:.0f}%)")
            st.markdown(f"**Reason:** {suggestion['reason']}")


if __name__ == "__main__":
    main()
