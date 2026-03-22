import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # adding streamlit-app to sys.path to import utils
import streamlit as st
from utils.aqi import get_multiple_cities, aqi_color, get_aqi
import pandas as pd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Vayu AQI Dashboard", page_icon="🔰")
st.title("🔰Vayu AQI Dashboard")
st.caption("Real time AQI Dashboard for selected cities")
major_cities = sorted(["Bangalore", "Mumbai", "Pune", "Jakarta", "Washington", "New York", "Chennai", "Hyderabad", "London", "Bejing", "Paris", "Lyon", "Delhi","Salem", "Ahmedabad", "Kolkata", "Jaipur", "Gurgaon"])

cities = st.multiselect(label = "Select one or more cities", options = major_cities) # select multiple

if st.button("🔃 Fetch Live Data"):
    if cities:
        with st.spinner("Fetching.."):
            data = get_multiple_cities(cities)

        if not data:
            st.error("Check your API token")
            st.stop()


        df = pd.DataFrame(data)
        df = df.replace("N/A", None)

        # Multi City View
        if len(cities)>1:

            # Metrics
            cols = st.columns(len(data))
            for i, row in enumerate(data): # i is the index and row contains a dict of data
                color, label = aqi_color(row["aqi"])
                with cols[i]:
                    st.metric(row["city"], row["aqi"], label, delta_color = color[1])
                    #st.markdown(f"<p style='text-align: center; font-size: 12px;'>Source: {row["name"]}</p>", unsafe_allow_html=True)
            st.divider()

            # Bar Chart 
            fig = px.bar(
            df, x="city", y="aqi",
            color="aqi",
            color_continuous_scale=["#00e400","#ffff00","#ff7e00","#ff0000","#8f3f97", "#1e1e1e"],
            range_color=[0, 300], # smoothens out colors
            labels={"aqi": "AQI", "city": "City"},
            title="AQI Comparison"
            )
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

        else:
            
            col1, col2 = st.columns(2)

            with col1:
                #st.markdown("<p style='text-align: center;font-weight: bold;'>AQI</p>", unsafe_allow_html=True)
                aqi_val = df["aqi"][0]
                color, label = aqi_color(aqi_val)
                # gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=aqi_val,
                    gauge={
                        "axis":{"range":[0,300]},
                        "bar":{"color":"rgba(0,0,0,0.8)"},
                        "steps":[
                            {"range":[0,50], "color":"#00e400"},
                            {"range":[51,100], "color":"#ffff00"},
                            {"range":[101,150], "color":"#ff7e00"},
                            {"range":[151,200], "color":"#ff0000"},
                            {"range":[201,300], "color":"#8f3f97"}
                        ]
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig)
            
            with col2:
                #st.markdown("<p style='text-align: center;font-weight: bold;'>Pollutants</p>", unsafe_allow_html=True)
                pollutants = ["pm25","pm10","so2","no2","o3","co"]
                values = [data[0].get(p) or 0 for p in pollutants] # pulls live pollutant data and replaces None with 0
                who_limits = [25, 50, 20, 40, 60, 10] # FROM WHO
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar( # Reality
                    r=values, theta = pollutants, fill="toself",name=cities[0],line_color="#d85a30"
                ))
                fig_radar.add_trace(go.Scatterpolar( # WHO limits
                    r=who_limits, theta = pollutants, fill="toself",name="WHO Limit",line_color="#639922",
                    line_dash = "dash", opacity=0.8
                ))
                fig_radar.update_layout(height=300, showlegend=True)
                st.plotly_chart(fig_radar, use_container_width=True)

            # horizontal bar chart
            fig_hbar = go.Figure()
            fig_hbar.add_trace(go.Bar( # Actual
                y = pollutants, x = values, orientation='h',name=cities[0],marker_color = "#d85a30"
            ))
            fig_hbar.add_trace(go.Bar( # WHO limits
                y = pollutants, x = who_limits, orientation='h',name="WHO Safe Limit",marker_color = "#2ec816", opacity=0.4
            ))
            fig_hbar.update_layout(
                title="Real-time Pollutants vs WHO Safe Limits",
                barmode = "overlay", # overlays WHO safe limits and reality hbar plots
                height = 300 # keep it uniform
            )
            st.plotly_chart(fig_hbar, use_container_width=True) # stretvh to full container width
    else:
        st.toast("Select one or more city!")



