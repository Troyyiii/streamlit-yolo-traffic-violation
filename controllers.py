import cv2
import cvzone
import streamlit as st
import const_settings as settings
from detect_line_violation import DetectLineViolation

def static_input_controller():
    static_source = st.sidebar.selectbox('Choose a video', settings.VIDEOS_DICT)
    
    with open(settings.VIDEOS_DICT.get(static_source), 'rb') as video_file:
        video_bytes = video_file.read()
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            st.text(settings.INPUT_VIDEO)
            if video_bytes:
                with st.spinner('Loading video...'):
                    st.video(video_bytes)
            else:
                st.info('Please select a static video')
        except Exception as e:
            st.exception(f'Error occured: {e}')
    
    # TODO: implement output video
    with col2:
        st.text(settings.OUTPUT_VIDEO)

def upload_input_controller():
    upload_source = st.sidebar.file_uploader('Choose a file', type=['mp4'], accept_multiple_files=False)
    
    if upload_source is None:
        st.info('Please upload a video')
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.text(settings.INPUT_VIDEO)
            try:
                with st.spinner('Loading video...'):
                    video_bytes = upload_source
                    if video_bytes:
                        st.video(video_bytes)
            except Exception as e:
                st.exception(f'Error occured: {e}')
        
        # TODO: implement output video
        with col2:
            st.text(settings.OUTPUT_VIDEO)

def link_input_controller():
    link_source = st.sidebar.text_input('Enter url:')
    st.sidebar.caption('Example URL: __test_url__')
    
    if not link_source:
        st.info('Please enter a url')
    
    if st.sidebar.button('Start detect'):
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                st.text(settings.INPUT_VIDEO)
                
                capture = cv2.VideoCapture(link_source)
                st_frame = st.empty()
                
                if not capture.isOpened():
                    capture.release()
                    st.error('Error: Failed to open video source.', icon='😟')
                else:
                    while True:
                        ret, frame = capture.read()
                        
                        if not ret:
                            capture.release()
                            st.error('Error: Cannot read frame.')
                            break
                    
                        st_frame.image(frame, channels='BGR', use_container_width=True)
                    capture.release()
            except Exception as e:
                capture.release()
                st.exception(f'Error occured: {e}')
        
        # TODO: implement output video
        with col2:
            st.text(settings.OUTPUT_VIDEO)

def webcam_input_controller(line_model, crosswalk_model):
    st.sidebar.caption('Please allow access to your webcam')
    
    if st.sidebar.button('Activate'):
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                st.text(settings.INPUT_VIDEO)
                
                webcam_source = settings.WEBCAM_PATH
                capture = cv2.VideoCapture(webcam_source)
                st_frame_input = st.empty()
                
                if not capture.isOpened():
                    capture.release()
                    st.error('Error: Cannot open webcam.', icon='😟')
                else:
                    with col2:
                        st.text(settings.OUTPUT_VIDEO)
                        st_frame_output = st.empty()
                        
                        detect_violation = DetectLineViolation(line_model, crosswalk_model)
                        
                        while True:
                            ret, frame = capture.read()
                            
                            if not ret:
                                st.error('Error: Cannot read frame.')
                                break
                            
                            frame = cv2.resize(frame, (1280, int(1280 * (9/16))))
                            processed_frame = detect_violation.start_detect(frame)
                            draw_detected_areas(processed_frame, detect_violation.area)
                            
                            if detect_violation.crosswalk_dir_check:
                                if detect_violation.traffic_light_status == "Red":
                                    box_color = (0, 0, 255)
                                elif detect_violation.traffic_light_status == "Green":
                                    box_color = (0, 255, 0)
                                else:
                                    box_color = (0, 0, 0)
                                cvzone.putTextRect(processed_frame, f"Traffic light status: {detect_violation.traffic_light_status}, L: {detect_violation.traffic_light_violator_counter}, W: {detect_violation.wrong_way_violator_counter}", (25, 60), scale=1, thickness=1, offset=3, colorR=box_color)
                            
                            st_frame_input.image(frame, channels='BGR', use_container_width=True)
                            st_frame_output.image(processed_frame, channels='BGR', use_container_width=True)
                        capture.release()
            except Exception as e:
                capture.release()
                st.exception(f'Error occured: {e}')
    
def draw_detected_areas(frame, areas):
    if areas:
        for area in areas:
            coords = area["coords"]
            north_count = area["north_count"]
            south_count = area["south_count"]
            status_dir = area["status_dir"]
            
            if len(coords) > 1:
                for i in range(len(coords) - 1):
                    cv2.line(frame, (coords[i][0], coords[i][1]), (coords[i + 1][0], coords[i + 1][1]), (255, 255, 255), 2)
            
            cvzone.putTextRect(frame, f"{north_count} {south_count} {status_dir}", (coords[0][0], coords[0][1] - 10), scale=0.8, thickness=1, offset=3)