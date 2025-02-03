import streamlit as st
import const_settings as settings
import controllers as controller
import model as model

st.set_page_config(
    page_title='Travio',
    page_icon="🚦",
    layout='wide',
    initial_sidebar_state='expanded'
)

# sidebar header
st.sidebar.title('Travio Menu', anchor=False)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# sidebar input option
st.sidebar.subheader('Input Configuration', divider='grey')
input_radio = st.sidebar.radio('Select input source', settings.SOURCE_LIST)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# content header
st.title('YOLOv5 - Traffic Violation Detection', anchor=False)
st.divider()

# load model
@st.cache_resource
def load_models():
    try:
        line_model = model.load_model(settings.LINE_MODEL_PATH)
        helmet_model = model.load_model(settings.HELMET_MODEL_PATH)
        crosswalk_model = model.load_model(settings.CROSSWALK_MODEL_PATH)
        return line_model, helmet_model, crosswalk_model
    except Exception as e:
        st.exception(f'Unable to load model. Error occurred: {e}')
        return None, None, None

line_model, helmet_model, crosswalk_model = load_models()

# static video source
if input_radio == settings.STATIC:
    controller.static_input_controller()

# upload video source
elif input_radio == settings.UPLOAD:
    controller.upload_input_controller()

# link video source
elif input_radio == settings.LINK:
    controller.link_input_controller()

# webcam video source
elif input_radio == settings.WEBCAM:
    controller.webcam_input_controller(line_model, crosswalk_model)