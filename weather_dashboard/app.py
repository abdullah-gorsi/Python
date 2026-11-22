
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from datetime import datetime, timedelta, timezone
from atmosphere import WeatherAPI


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Atmosphere | Weather",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* Global */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f7f9fc;
    color: #172033;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Headings */
h1, h2, h3 {
    color: #172033 !important;
    letter-spacing: -0.7px;
}

p {
    color: #64748b;
}

/* Header */
.app-brand {
    font-size: 25px;
    font-weight: 800;
    color: #172033;
    letter-spacing: -1px;
}

.app-subtitle {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 3px;
}

/* Cards */
.weather-card {
    background: #ffffff;
    border: 1px solid #e9eef5;
    border-radius: 18px;
    padding: 23px;
    height: 100%;
    box-shadow: 0 3px 15px rgba(15, 23, 42, 0.025);
}

.hero-card {
    background: linear-gradient(135deg, #eaf3ff 0%, #f5f8ff 100%);
    border: 1px solid #dceaff;
    border-radius: 22px;
    padding: 30px;
    min-height: 255px;
}

.hero-temp {
    font-size: 64px;
    font-weight: 700;
    color: #172033;
    letter-spacing: -4px;
    line-height: 1.2;
}

.hero-condition {
    font-size: 16px;
    color: #64748b;
    margin-top: 8px;
}

.hero-location {
    font-size: 14px;
    color: #64748b;
    font-weight: 500;
}

.hero-icon {
    font-size: 75px;
    text-align: center;
}

/* Metric cards */
.metric-label {
    font-size: 12px;
    color: #94a3b8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.metric-value {
    font-size: 25px;
    font-weight: 700;
    color: #172033;
    margin-top: 9px;
}

.metric-icon {
    font-size: 22px;
    margin-bottom: 14px;
}

/* Section headings */
.section-heading {
    font-size: 19px;
    font-weight: 700;
    color: #172033;
    margin-top: 30px;
    margin-bottom: 16px;
    letter-spacing: -0.5px;
}

.section-caption {
    font-size: 12px;
    color: #94a3b8;
    margin-top: -12px;
    margin-bottom: 18px;
}

/* Forecast cards */
.forecast-card {
    background: #ffffff;
    border: 1px solid #e9eef5;
    border-radius: 15px;
    padding: 16px 8px;
    text-align: center;
    min-height: 150px;
}

.forecast-day {
    font-size: 12px;
    color: #94a3b8;
    font-weight: 600;
}

.forecast-icon {
    font-size: 27px;
    margin: 12px 0;
}

.forecast-temp {
    font-size: 15px;
    color: #172033;
    font-weight: 700;
}

.forecast-low {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 4px;
}

/* Search */
.stTextInput input {
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    background: #ffffff;
    height: 45px;
}

.stButton button {
    border-radius: 11px;
    border: 1px solid #e2e8f0;
    background: #ffffff;
    color: #334155;
    font-weight: 600;
    height: 43px;
    transition: 0.2s;
}

.stButton button:hover {
    border-color: #93b9f5;
    color: #2563eb;
}

/* Divider */
hr {
    border-color: #e9eef5 !important;
    margin-top: 27px;
    margin-bottom: 27px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e9eef5;
}

/* Footer */
.app-footer {
    color: #94a3b8;
    font-size: 12px;
    text-align: center;
    padding: 25px 0;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e9eef5;
    padding: 15px;
    border-radius: 14px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8;
}

[data-testid="stMetricValue"] {
    color: #172033;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-temp {
        font-size: 48px;
    }

    .hero-card {
        padding: 20px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SESSION STATE
# =====================================================

if "city" not in st.session_state:
    st.session_state.city = "Bahawalpur"

if "favorites" not in st.session_state:
    st.session_state.favorites = ["Bahawalpur"]

if "unit" not in st.session_state:
    st.session_state.unit = "Celsius"


# =====================================================
# API INITIALIZATION
# =====================================================

@st.cache_resource
def initialize_api():
    return WeatherAPI()


api = initialize_api()


# =====================================================
# CACHED API REQUESTS
# =====================================================

@st.cache_data(ttl=600, show_spinner=False)
def load_weather(city):

    location = api.get_coordinates(city)

    lat = location["lat"]
    lon = location["lon"]

    current = api.get_current_weather(lat, lon)
    forecast = api.get_forecast(lat, lon)

    try:
        air = api.get_air_quality(lat, lon)
    except Exception:
        air = None

    return location, current, forecast, air


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def convert_temp(value):

    if st.session_state.unit == "Fahrenheit":
        return (value * 9 / 5) + 32

    return value


def temp_symbol():

    return "°F" if st.session_state.unit == "Fahrenheit" else "°C"


def get_local_time(timestamp, offset):

    local_tz = timezone(timedelta(seconds=offset))

    return datetime.fromtimestamp(
        timestamp,
        tz=local_tz
    ).strftime("%I:%M %p")


def get_local_datetime(timestamp, offset):

    local_tz = timezone(timedelta(seconds=offset))

    return datetime.fromtimestamp(
        timestamp,
        tz=local_tz
    )


def get_icon(condition):

    icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Fog": "🌫️",
        "Haze": "🌫️",
        "Smoke": "🌫️",
        "Dust": "🌪️",
        "Sand": "🌪️"
    }

    return icons.get(condition, "🌤️")


def get_aqi_label(value):

    labels = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }

    return labels.get(value, "Unavailable")


# =====================================================
# HEADER
# =====================================================

header_left, header_right = st.columns([3, 1])

with header_left:

    st.markdown(
        '<div class="app-brand">◉ atmosphere.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="app-subtitle">'
        'Your personal weather intelligence dashboard'
        '</div>',
        unsafe_allow_html=True
    )

with header_right:

    st.selectbox(
        "Temperature",
        ["Celsius", "Fahrenheit"],
        key="unit"
    )


st.divider()


# =====================================================
# SEARCH BAR
# =====================================================

search_col, button_col = st.columns([5, 1])

with search_col:

    search_city = st.text_input(
        "Search location",
        value=st.session_state.city,
        placeholder="Search city..."
    )

with button_col:

    st.write("")

    search_clicked = st.button(
        "Search →",
        use_container_width=True
    )


if search_clicked:

    if search_city.strip():

        st.session_state.city = search_city.strip()
        st.rerun()

    else:

        st.warning("Please enter a city name.")


city = st.session_state.city


# =====================================================
# LOAD WEATHER DATA
# =====================================================

try:

    with st.spinner("Loading weather information..."):

        location, current, forecast, air = load_weather(city)

except Exception as error:

    st.error(f"Unable to load weather information: {error}")

    st.info(
        "Check your API key, internet connection, "
        "and location name."
    )

    if st.button("Retry"):

        load_weather.clear()
        st.rerun()

    st.stop()


# =====================================================
# EXTRACT DATA
# =====================================================

city_name = location["name"]
country = location["country"]

main = current["main"]
weather = current["weather"][0]
wind = current["wind"]

condition = weather["main"]
icon = get_icon(condition)

timezone_offset = current["timezone"]

temperature = convert_temp(main["temp"])
feels_like = convert_temp(main["feels_like"])


# =====================================================
# LOCATION BAR
# =====================================================

location_col, favorite_col = st.columns([4, 1])

with location_col:

    st.markdown(
        f"### 📍 {city_name}, {country}"
    )

    st.caption(
        f"Last observation: "
        f"{get_local_time(current['dt'], timezone_offset)}"
    )

with favorite_col:

    if city_name not in st.session_state.favorites:

        if st.button("☆ Save location", use_container_width=True):

            st.session_state.favorites.append(city_name)
            st.rerun()

    else:

        st.markdown(
            "<div style='text-align:right;color:#2563eb;"
            "font-size:13px;padding-top:10px;'>"
            "★ Saved location"
            "</div>",
            unsafe_allow_html=True
        )


# =====================================================
# MAIN WEATHER SECTION
# =====================================================

st.markdown(
    '<div class="section-heading">Current weather</div>',
    unsafe_allow_html=True
)

hero_left, hero_right = st.columns([2, 1])

with hero_left:

    st.markdown(
        f"""
        <div class="hero-card">

            <div class="hero-location">
                CURRENT CONDITIONS
            </div>

            <div style="display:flex;
                        align-items:center;
                        justify-content:space-between;
                        margin-top:20px;">

                <div>

                    <div class="hero-temp">
                        {temperature:.1f}{temp_symbol()}
                    </div>

                    <div class="hero-condition">
                        {weather['description'].title()}
                    </div>

                    <div style="margin-top:16px;
                                color:#64748b;
                                font-size:13px;">
                        Feels like {feels_like:.1f}{temp_symbol()}
                    </div>

                </div>

                <div class="hero-icon">
                    {icon}
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with hero_right:

    st.markdown(
        """
        <div class="weather-card">
            <div class="metric-icon">🌡️</div>
            <div class="metric-label">Temperature Range</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.metric(
        "Maximum",
        f"{convert_temp(main['temp_max']):.1f}{temp_symbol()}"
    )

    st.metric(
        "Minimum",
        f"{convert_temp(main['temp_min']):.1f}{temp_symbol()}"
    )


# =====================================================
# WEATHER METRICS
# =====================================================

st.markdown(
    '<div class="section-heading">Weather details</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown(
        """
        <div class="weather-card">
            <div class="metric-icon">💧</div>
            <div class="metric-label">Humidity</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.metric(" ", f"{main['humidity']}%")

with m2:

    st.markdown(
        """
        <div class="weather-card">
            <div class="metric-icon">💨</div>
            <div class="metric-label">Wind Speed</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.metric("  ", f"{wind['speed']} m/s")

with m3:

    st.markdown(
        """
        <div class="weather-card">
            <div class="metric-icon">🌫️</div>
            <div class="metric-label">Visibility</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.metric(
        "   ",
        f"{current.get('visibility', 0) / 1000:.1f} km"
    )

with m4:

    st.markdown(
        """
        <div class="weather-card">
            <div class="metric-icon">☁️</div>
            <div class="metric-label">Cloud Coverage</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.metric("    ", f"{current['clouds']['all']}%")


# =====================================================
# SUNRISE AND SUNSET
# =====================================================

st.markdown(
    '<div class="section-heading">Sunrise & sunset</div>',
    unsafe_allow_html=True
)

sun1, sun2 = st.columns(2)

with sun1:

    st.markdown(
        """
        <div class="weather-card">
            <div class="metric-icon">🌅</div>
            <div class="metric-label">Sunrise</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.metric(
        " ",
        get_local_time(
            current["sys"]["sunrise"],
            timezone_offset
        )
    )

with sun2:

    st.markdown(
        """
        <div class="weather-card">
            <div class="metric-icon">🌇</div>
            <div class="metric-label">Sunset</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.metric(
        " ",
        get_local_time(
            current["sys"]["sunset"],
            timezone_offset
        )
    )


# =====================================================
# HOURLY FORECAST
# =====================================================

st.markdown(
    '<div class="section-heading">Temperature forecast</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-caption">'
    'Upcoming forecast · 3-hour intervals'
    '</div>',
    unsafe_allow_html=True
)

forecast_list = forecast["list"]

hourly_data = []

for item in forecast_list[:8]:

    hourly_data.append({

        "Time": get_local_datetime(
            item["dt"],
            timezone_offset
        ),

        "Temperature": convert_temp(
            item["main"]["temp"]
        ),

        "Rain": item.get("pop", 0) * 100

    })


df_hourly = pd.DataFrame(hourly_data)


fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df_hourly["Time"],
        y=df_hourly["Temperature"],
        mode="lines+markers",
        name="Temperature",
        line=dict(
            color="#3b82f6",
            width=3,
            shape="spline"
        ),
        marker=dict(size=7),
        fill="tozeroy",
        fillcolor="rgba(59,130,246,0.07)"
    )
)

fig.update_layout(
    height=320,
    margin=dict(l=10, r=10, t=20, b=10),
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(
        family="Inter",
        color="#64748b"
    ),
    xaxis=dict(
        showgrid=False,
        title=None
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#edf1f7",
        title=f"Temperature ({temp_symbol()})"
    ),
    showlegend=False,
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================================
# FIVE-DAY FORECAST
# =====================================================

st.markdown(
    '<div class="section-heading">5-day forecast</div>',
    unsafe_allow_html=True
)

forecast_data = []

for item in forecast_list:

    local_date = get_local_datetime(
        item["dt"],
        timezone_offset
    ).date()

    forecast_data.append({

        "Date": local_date,

        "Temperature": convert_temp(
            item["main"]["temp"]
        ),

        "Condition": item["weather"][0]["main"],

        "Rain": item.get("pop", 0) * 100

    })


df_forecast = pd.DataFrame(forecast_data)

daily = df_forecast.groupby("Date").agg(
    Min=("Temperature", "min"),
    Max=("Temperature", "max"),
    Rain=("Rain", "max")
).reset_index()


forecast_columns = st.columns(5)

for index, row in daily.head(5).iterrows():

    with forecast_columns[index]:

        day_name = row["Date"].strftime("%a")
        date_name = row["Date"].strftime("%d %b")

        st.markdown(
            f"""
            <div class="forecast-card">

                <div class="forecast-day">
                    {day_name}, {date_name}
                </div>

                <div class="forecast-icon">
                    🌤️
                </div>

                <div class="forecast-temp">
                    {row['Max']:.0f}°
                    <span style="color:#94a3b8;">
                        {row['Min']:.0f}°
                    </span>
                </div>

                <div class="forecast-low">
                    Rain {row['Rain']:.0f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# PRECIPITATION CHART
# =====================================================

st.markdown(
    '<div class="section-heading">Rain probability</div>',
    unsafe_allow_html=True
)

fig_rain = go.Figure()

fig_rain.add_trace(
    go.Bar(
        x=df_hourly["Time"],
        y=df_hourly["Rain"],
        marker_color="#60a5fa",
        marker_line_width=0,
        name="Rain probability"
    )
)

fig_rain.update_layout(
    height=280,
    margin=dict(l=10, r=10, t=15, b=10),
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(
        family="Inter",
        color="#64748b"
    ),
    xaxis=dict(
        showgrid=False,
        title=None
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#edf1f7",
        title="Probability (%)",
        range=[0, 100]
    ),
    showlegend=False
)

st.plotly_chart(
    fig_rain,
    use_container_width=True
)


# =====================================================
# AIR QUALITY
# =====================================================

st.markdown(
    '<div class="section-heading">Air quality</div>',
    unsafe_allow_html=True
)

if air and air.get("list"):

    air_data = air["list"][0]

    aqi = air_data["main"]["aqi"]

    pollutants = air_data["components"]

    aq1, aq2, aq3, aq4 = st.columns(4)

    with aq1:
        st.metric(
            "Air Quality Index",
            f"{aqi}/5",
            get_aqi_label(aqi)
        )

    with aq2:
        st.metric(
            "PM2.5",
            f"{pollutants['pm2_5']:.1f} µg/m³"
        )

    with aq3:
        st.metric(
            "PM10",
            f"{pollutants['pm10']:.1f} µg/m³"
        )

    with aq4:
        st.metric(
            "NO₂",
            f"{pollutants['no2']:.1f} µg/m³"
        )

else:

    st.info("Air quality data is currently unavailable.")


# =====================================================
# MAP
# =====================================================

st.markdown(
    '<div class="section-heading">Location</div>',
    unsafe_allow_html=True
)

map_data = pd.DataFrame({
    "latitude": [location["lat"]],
    "longitude": [location["lon"]]
})

st.map(
    map_data,
    zoom=9,
    use_container_width=True
)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## ◉ atmosphere.")

    st.caption("Weather Dashboard")

    st.divider()

    st.markdown("### Saved locations")

    if st.session_state.favorites:

        for favorite in st.session_state.favorites:

            col1, col2 = st.columns([4, 1])

            with col1:

                if st.button(
                    f"📍 {favorite}",
                    key=f"select_{favorite}",
                    use_container_width=True
                ):

                    st.session_state.city = favorite
                    st.rerun()

            with col2:

                if st.button(
                    "×",
                    key=f"remove_{favorite}"
                ):

                    st.session_state.favorites.remove(favorite)

                    if not st.session_state.favorites:
                        st.session_state.favorites.append("Bahawalpur")

                    st.rerun()

    else:

        st.caption("No saved locations yet.")

    st.divider()

    st.markdown("### Data source")

    st.caption("OpenWeatherMap API")

    st.caption("Weather data may be delayed or vary from local observations.")


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class="app-footer">
        ◉ atmosphere. &nbsp; | &nbsp;
        Built with Python, Streamlit & Plotly
        <br><br>
        Weather information is provided by OpenWeatherMap.
        <br>
        Forecasts are estimates and actual conditions may vary.
    </div>
    """,
    unsafe_allow_html=True
)
