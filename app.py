import streamlit as st
import pandas as pd
import time
import pickle
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html
from sqlalchemy import text

# --- Streamlit Page Config ---
st.set_page_config(page_title="Milkqu - Predict Milk Quality", page_icon="🎓", layout="wide", initial_sidebar_state="auto")


def login_screen():

    # def login_screen():
    st.markdown("<div style='text-align: center; font-size: 3.5rem; font-weight: bold; color: white; text-shadow: -1px -1px 0 #84BAE8, 1px -1px 0 #84BAE8, -1px 1px 0 #84BAE8, 1px 1px 0 #84BAE8, -2px 0 0 #84BAE8, 2px 0 0 #84BAE8, 0 -2px 0 #84BAE8, 0 2px 0 #84BAE8;'>👋 Welcome to MilkQu</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Predict your milk quality easily with AI</p>", unsafe_allow_html=True)
    # st.header("This app is private.")
    
    st.markdown("---")

    # Centered Image
    st.markdown("""
        <div style="
            display: flex; 
            justify-content: center; 
            margin: 30px auto;
            position: relative;
            max-width: 550px;
        ">
            <img src="https://raw.githubusercontent.com/jidan24/asset/refs/heads/master/image_fx%20(7).jpg"  alt="logo Milkqu login"
                style="
                    width: 100%;
                    border-radius: 12px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                "
                onmouseover="this.style.transform='scale(1.02)'; this.style.boxShadow='0 15px 40px rgba(0, 0, 0, 0.3)';"
                onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 10px 30px rgba(0, 0, 0, 0.25)';"
            >
        </div>
        
        <style>
            @media (max-width: 768px) {
                img {
                    width: 90% !important;
                }
            }
        </style>
        """, unsafe_allow_html=True)

    # Styling dan UI login MilkQu
    st.markdown("""
    <style>
    /* Body style */
    body {
        background-color: #ffffff;
        color: #333333;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* Button style */
    .stButton>button {
        background-color: #f0f4f8;
        color: #2c3e50;
        border: 1px solid #d1dbe8;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-size: 1rem;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        width: auto;
        min-width: 180px;
    }

    .stButton>button:hover {
        background-color: #e6eef7;
        border-color: #a3b8cc;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 2px rgba(0, 0, 0, 0.1);
    }

    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

    st.button("Log in with Google", on_click=st.login)
    st.markdown("---")

# --- Apply style & script configurations ---
style_configurations = """
<style>
    #MainMenu {visibility: hidden;}
    div[data-testid="collapsedControl"] {top: 1rem !important;}
    div[class="css-1nm2qww e1fqkh3o2"] {top: 1rem !important;}
    footer {visibility: hidden;}
    .stApp {top: 1.5px !important;}
    section[data-testid="stSidebar"] div {gap: 0rem !important;}
    section[data-testid="stSidebar"] {
        box-shadow: rgba(0, 0, 0, 0.16) 0px 2rem 2rem !important;
        background-color: white !important;
    }
    .stProgress > div > div > div > div {background-color: green;}
    button[title="View fullscreen"] {visibility: hidden;}
    iframe[title="st.iframe"] {display: none;}
    .t_over:nth-child(8):hover ~ .tilt-box{transform: rotateX(20deg) rotateY(0deg);}
    .t_over:nth-child(9):hover ~ .tilt-box{transform: rotateX(20deg) rotateY(-20deg);}
</style>
"""
script_configurations = """
<script>
    console.log("Welcome To Milkqu Version 0.0.1");
</script>
"""

st.markdown(style_configurations, unsafe_allow_html=True)
html(script_configurations)


# --- Declare global function ---
@st.cache_data
def load_default_milk_data():
    return pd.DataFrame({"pH": ["6.6"], "Temprature": ["35"], "Taste": ["1"], "Odor": ["0"], "Fat ": ["1"], "Turbidity": ["0"], "Colour": ["254"]}, index=[0])


@st.cache_data
def load_milk_data(ph, temprature, taste, odor, fat, turbidity, colour):
    return pd.DataFrame({"pH": [ph], "Temprature": [temprature], "Taste": [taste], "Odor": [odor], "Fat ": [fat], "Turbidity": [turbidity], "Colour": [colour]}, index=[0])


@st.cache_data
def load_encoded_milk_data(ph, temprature, taste, odor, fat, turbidity, colour, _list_column):
    return pd.DataFrame({"pH": ph, "Temprature": temprature, "Taste": taste, "Odor": odor, "Fat ": fat, "Turbidity": turbidity, "Colour": colour}, index=[0], columns=_list_column)


@st.cache_resource
def init_model():
    return pickle.load(open("milk_model.pickle", "rb"))


# Function for parcing
def safe_get_float(source, key, default=0.0):
    try:
        return float(source.get(key, [default])[0])
    except ValueError:
        return default


def safe_get_int(source, key, default=0):
    try:
        return int(source.get(key, [default])[0])
    except ValueError:
        return default


# --- Declare global variables ---
current_url = st.query_params.to_dict()
direct_menu = int(current_url["redirect"][0]) if "redirect" in current_url else 0

tilt_effect = """
<div class="contaienr">
    <div class="tilt-box-wrap">
        <span class="t_over"></span>
        <span class="t_over"></span>
        <span class="t_over"></span>
        <span class="t_over"></span>
        <span class="t_over"></span>
        <span class="t_over"></span>
        <span class="t_over"></span>
        <span class="t_over"></span>
        <span class="t_over"></span>
        <div class="tilt-box">
            <img src="https://raw.githubusercontent.com/jidan24/asset/refs/heads/master/image_fx%20(7).jpg" alt="Milkqu Header" style="width: 100%;"/>
        </div>
    </div>
</div>
<br/>
"""

# CORE
if not st.user.is_logged_in:
    login_screen()
else:

    # --- Sidebar ---
    with st.sidebar:
        # st.success(f"👋 Welcome {st.session_state.user_info['name']}")
        st.markdown("---")
        # st.caption(f"📧 {st.session_state.user_info['email']}")
        st.markdown(tilt_effect, unsafe_allow_html=True)

        # --- Menu ---
        menu = option_menu(None, ["Documentations", "Milkqu Prediction", "Prediction History"],
                           icons=["journal-text", "ui-checks", "receipt", "clock-history"],
                           default_index=int(direct_menu),
                           styles={
                               "container": {
                                   "padding": "0px !important",
                                   "padding-right": "2px"
                               },
                               "nav-item": {
                                   "background": "#fff"
                               },
                               "nav-link": {
                                   "font-size": "13px",
                                   "text-align": "left",
                                   "background-color": "#F8F9FB"
                               },
                               "nav-link-selected": {
                                   "background-color": "#E8B840"
                               },
                           })

        # github repo button
        st.write("""
        <style>
        .custom-button {
            background-color: rgb(248, 249, 251);
            color: #31333f;
            border: none;
            width: 100%;
            height: 40px;
            border-radius: 10px;
            font-family: Avenir, Helvetica, Arial, sans-serif;
            font-size: 13px;
            text-align: left;
            padding-left: 10px;
            cursor: pointer;
            margin-bottom: 10px;
        }
        .custom-button:hover {
            background-color: #f2f2f2;
        }
        </style>

        <div style='margin-top: -3px; margin-bottom: 25px;'>
        <a href="https://github.com/bimbingan-skripsi-jidan/prediction-milkqu" target="_blank">
            <button class="custom-button">GitHub Repository</button>
        </a>
        <a href="https://www.kaggle.com/datasets/jidanhaviarsaviola/milk-quality" target="_blank">
            <button class="custom-button">Explore Dataset</button>
        </a>
        </div>
        """,
                 unsafe_allow_html=True)
        
        st.button("Log out", on_click=st.logout)
        st.markdown("---")
        st.success(f"Welcome to MilkQu App, {st.user.name}!")

    if menu == "Documentations":

        # declare variable
        st.markdown(
            """
            <style>
                .stApp > header {visibility: hidden;}
                .title {font-family: 'Helvetica Neue', sans-serif; color: #333;}
                .section-title {color: #444; margin-top: 30px; margin-bottom: 10px;}
                .info-box {background-color: #f0f2f6; padding: 15px; border-radius: 8px; border-left: 4px solid #2c3e50;}
            </style>
            """,
            unsafe_allow_html=True,
        )

        # ─── PAGE TITLE ────────────────────────────────────────────────────────────────
        st.markdown("""
            <div style='display: flex; align-items: center; gap: 10px;'>
                <img src='https://raw.githubusercontent.com/jidan24/asset/refs/heads/master/logo-milk.png' alt='MilkQu Logo' width='40'/>
                <h1 style='margin: 0;' class='title'>MilkQu Docs</h1>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ─── WHAT IS MILKQU? ───────────────────────────────────────────────────────────
        st.markdown("<h2 class='section-title'>🥛 What is MilkQu?</h2>", unsafe_allow_html=True)
        st.info(
            """
            MilkQu (Milk Quality) adalah web app berbasis machine learning
            untuk mengklasifikasikan kualitas susu berdasarkan beberapa parameter seperti:
            keasaman, suhu, kejernihan, bau, kandungan lemak, tingkat keruh, dan warna.
            Dataset diambil dari Kaggle untuk memahami karakteristik fisika & kimia susu.Melalui antarmuka yang intuitif dan dapat mengunduh laporan prediksi history dengan format CSV, atau langsung mengekspor dataset ke format CSV untuk analisis lebih dalam. Model kami dilatih menggunakan Milk Quality Dataset dari Kaggle memberikan jaminan bahwa setiap prediksi lahir dari data real beragam kondisi susu.Dengan MilkQu, analisis kualitas susu menjadi lebih efisien, terpercaya, dan mudah diakses di mana saja—cukup buka browser, unggah data, dan biarkan algoritma cerdas kami bekerja untuk Anda!
            """
        )

        # ─── ABOUT DATASETS ────────────────────────────────────────────────────────────
        st.markdown("<h2 class='section-title'>📊 About Datasets</h2>", unsafe_allow_html=True)
        with st.expander("Detail Dataset (Kaggle: Milk Quality Dataset)"):
            st.markdown(
                """
                - **Jumlah baris:** 1000+  
                - **Fitur utama:** pH, Temperature, Taste, Odor, Fat, Turbidity, Colour and Grade  
                """
            )

        # ─── HOW MILKQU WORKS ──────────────────────────────────────────────────────────
        st.markdown("<h2 class='section-title'>⚙️ How MilkQu Works</h2>", unsafe_allow_html=True)
        st.markdown(
            """
            1. User mengunggah data parameter susu  
            2. Model ML melakukan prediksi kualitas  
            3. Hasil ditampilkan sebagai **High**, **Medium**, atau **Low**
            """
        )
        code = '''def predict():
        """
        this is code
        for processing
        the machine learning
        """
        print(f"your milk quality is {predict_result}")'''
        st.code(code, language="python")

        # ─── FOOTER ───────────────────────────────────────────────────────────────────
        st.markdown("---")
        st.caption("© 2025 MilkQu • built with Streamlit")

    elif menu == "Milkqu Prediction":
        # declare variable
        identity_value = current_url.get("identity", [""])[0]
        ph_value = safe_get_float(current_url, "pH")
        temprature_value = safe_get_int(current_url, "Temprature")
        taste_value = safe_get_int(current_url, "Taste")
        odor_value = safe_get_int(current_url, "Odor")
        fat = safe_get_int(current_url, "Fat ")
        turbidity = safe_get_int(current_url, "Turbidity")
        colour_value = safe_get_int(current_url, "Colour")

        prediction_result = ""
        default_milkqu_df = load_default_milk_data()
        clusters = init_model()

        # sub header and caption
        st.subheader("Milkqu default template")
        st.caption("", unsafe_allow_html=False)

        st.dataframe(default_milkqu_df, use_container_width=True)

        st.caption(":blue[pH] = Mengukur tingkat keasaman susu, yang bisa mempengaruhi kesegarannya.", unsafe_allow_html=False)
        st.caption(":blue[Temperature] = Suhu susu saat diukur, yang berpengaruh terhadap pertumbuhan bakteri.", unsafe_allow_html=False)
        st.caption(":blue[Taste] = Apakah susu terasa normal atau asam.", unsafe_allow_html=False)
        st.caption(":blue[Odor] = Bau susu, apakah masih segar atau sudah menunjukkan tanda-tanda pembusukan.", unsafe_allow_html=False)
        st.caption(":blue[Fat] = Kandungan lemak dalam susu.", unsafe_allow_html=False)
        st.caption(":blue[Turbidity] = Seberapa keruh susu tersebut.", unsafe_allow_html=False)
        st.caption(":blue[Colour] = Warna susu yang bisa menunjukkan perubahan kualitas.", unsafe_allow_html=False)
        st.caption(":blue[Grade] = Label hasil kualitas susu berdasarkan fitur-fitur di atas (high, medium, low).", unsafe_allow_html=False)

        # category one : predict milkqu answer
        st.subheader("Milk Quality Prediction")

        with st.form(key="prediction_form"):

            identity = st.text_input("Your Name", value=identity_value)
            ph = st.number_input("pH", value=ph_value)
            temprature = st.number_input("Temprature", value=temprature_value)
            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)
            colour = st.number_input("Colour", value=colour_value)

            with c1:
                taste = st.number_input("Taste", value=taste_value)
            with c2:
                odor = st.number_input("Odor", value=odor_value)
            with c3:
                fat = st.number_input("Fat ", value=fat)
            with c4:
                turbidity = st.number_input("Turbidity", value=turbidity)

            progress_text = "STATUS : IDLE"
            progress_bar = st.progress(0, text=progress_text)

            delivered_results = st.form_submit_button("Predict Milk Quality", use_container_width=True)

            if delivered_results:
                st.session_state["milkqu_answer_state"] = identity

        # save result as state
        if "milkqu_answer_state" not in st.session_state:
            st.info("Please fill parameters above and submit predict to see the result !")
            st.caption("© 2025 MilkQu • built with Streamlit")

        # execute
        else:

            # handle error
            try:

                if delivered_results:
                    for percent_complete in range(100):
                        df_predict = load_milk_data(ph, temprature, taste, odor, fat, turbidity, colour)
                        encoded_df = load_encoded_milk_data(ph, temprature, taste, odor, fat, turbidity, colour, df_predict.columns)
                        predictions = clusters.predict(encoded_df)
                        if df_predict is not None and percent_complete == 20:
                            progress_bar.progress(percent_complete + 1, text="STATUS : GATHERING DATASET")
                            time.sleep(2)
                            st.dataframe(df_predict, use_container_width=True)
                        if encoded_df is not None and percent_complete == 40:
                            progress_bar.progress(percent_complete + 1, text="STATUS : PREPROCESSING DATA")
                            time.sleep(2)
                            st.dataframe(encoded_df, use_container_width=True)
                        if predictions is not None and percent_complete == 80:
                            progress_bar.progress(percent_complete + 1, text="STATUS : PREDICTING DATA")
                            time.sleep(2)
                            st.dataframe(predictions, use_container_width=True)
                    progress_bar.progress(percent_complete + 1, text="STATUS : PREDICTION COMPLETE")

                    prediction_label = {0: "High", 1: "Low", 2: "Medium"}
                    # history_prediction_label = {"High": "rocket", "Low": "walking", "Medium": "bicyclist"}

                    # conn.query("INSERT INTO histories VALUES ('Belly', 'rocket');")
                    # Perform query.

                    conn = st.connection("postgresql", type="sql")

                    with conn.session as session:
                        session.execute(text("INSERT INTO histories (name, quality) VALUES (:name, :quality)"), {"name": identity, "quality": prediction_label[int(predictions)]})
                        session.commit()

                    st.success(identity + " Milk Grade Is " + prediction_label[int(predictions)])

            except:
                print(st.error)
                st.error("Invalid parameters, please [follow](#milkqu-default-template) default template above !")

    elif menu == "Prediction History":

            # Warna tema utama
        PRIMARY_COLOR = "#2E86C1"     # Biru cerah
        SECONDARY_COLOR = "#5DADE2"   # Biru muda
        ACCENT_COLOR = "#FF9800"      # Oranye
        SUCCESS_COLOR = "#00C853"     # Hijau
        WARNING_COLOR = "#FFB74D"     # Oranye muda
        DANGER_COLOR = "#F44336"      # Merah
        BG_COLOR = "#F5F7F9"          # Latar belakang abu-abu terang

        st.markdown (
            f"""
                <style>
            .metric-card {{
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 15px;
                border-left: 5px solid {PRIMARY_COLOR};
            }}
            .metric-value {{
                font-size: 24px;
                font-weight: bold;
                color: {PRIMARY_COLOR};
            }}
            .metric-label {{
                font-size: 14px;
                color: #666;
            }}
            </style>
            """,
        unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="text-align: center; padding: 10px 0;">
                <h1 style="margin: 0; font-family: 'Helvetica Neue', sans-serif; color: #333;">
                    📈 Milk Quality History Prediction
                </h1>
                <p style="color: #666; font-size: 16px;">
                    Ringkasan riwayat prediksi kualitas.  
                    Gunakan filter untuk menelusuri data lebih detail!
                </p>
            </div>
            <hr>
            """,
            unsafe_allow_html=True,
        )

        # ─── DATABASE & DATAFRAME ────────────────────────────────────────────────────
        conn = st.connection("postgresql", type="sql")
        df = conn.query('SELECT name, quality AS grade FROM histories;', ttl=0)

        # ubah label jadi pakai ikon
        label_map = {
            "High":   "🚀 High",
            "Medium": "🚴 Medium",
            "Low":    "🚶 Low"
        }
        df["grade"] = df["grade"].map(label_map)

        # ─── SUMMARY METRICS ──────────────────────────────────────────────────────────
        total_pred = len(df)
        high_count   = df["grade"].str.contains("High").sum()
        medium_count = df["grade"].str.contains("Medium").sum()
        low_count    = df["grade"].str.contains("Low").sum()

        st.markdown("<div style='display: flex; gap: 15px;'>", unsafe_allow_html=True)
        
        metrics = [
            {"label": "Total Predictions", "value": total_pred, "color": PRIMARY_COLOR, "percentage": ""},
            {"label": "High 🚀", "value": high_count, "color": SUCCESS_COLOR, "percentage": f"{high_count/total_pred:.0%}"},
            {"label": "Medium 🚴", "value": medium_count, "color": WARNING_COLOR, "percentage": f"{medium_count/total_pred:.0%}"},
            {"label": "Low 🚶", "value": low_count, "color": DANGER_COLOR, "percentage": f"{low_count/total_pred:.0%}"}
        ]
        
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        
        for i, (col, metric) in enumerate(zip(cols, metrics)):
            with col:
                st.markdown(
                    f"""
                    <div class="metric-card" style="border-left: 5px solid {metric['color']}">
                        <div class="metric-value" style="color: {metric['color']}">{metric['value']}</div>
                        <div class="metric-label">{metric['label']}</div>
                        <div style="color: {metric['color']}; font-size: 12px; font-weight: bold;">{metric['percentage']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ─── DISTRIBUTION CHART ───────────────────────────────────────────────────────
        st.markdown("### 📊 Grade Distribution")
        dist = df["grade"].value_counts()
        st.bar_chart(dist)

        # ─── FILTER PANEL ─────────────────────────────────────────────────────────────
        with st.expander("🔍 Filter & Search"):
            with st.form("filter_form"):
                selected_grades = st.multiselect(
                    "Pilih Grade", options=df["grade"].unique(), default=df["grade"].unique()
                )
                name_query = st.text_input("Cari berdasarkan Nama")
                cari = st.form_submit_button("🔍 Cari")

            if cari:
                mask = df["grade"].isin(selected_grades)
                if name_query:
                    mask &= df["name"].str.contains(name_query, case=False)
                df_filtered = df[mask]
            else:
                df_filtered = df.copy()

        # ─── FILTERED RESULTS ─────────────────────────────────────────────────────────
        st.markdown("### 📋 Hasil Filter")
        st.dataframe(df_filtered, use_container_width=True,)

        # ─── DOWNLOAD BUTTON ──────────────────────────────────────────────────────────
        csv = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="milkqu_prediction_history.csv",
            mime="text/csv"
        )
        st.caption("© 2025 MilkQu • built with Streamlit")
