from streamlit_drawable_canvas import st_canvas
import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from pathlib import Path

def signiture():
    
    st.write("Signiture")
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=2,
        stroke_color='black',
        background_color="#eee",
        # background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=True,
        height=150,
        drawing_mode="freedraw",
        # point_display_radius=point_display_radius if drawing_mode == "point" else 0,
        display_toolbar=True,
        key="full_app",
    )
    file_path = "./signiture.png"
    # Do something interesting with the image data and paths
    if canvas_result.image_data is not None:
        # st.image(canvas_result.image_data)
        img_data = canvas_result.image_data
        im = Image.fromarray(img_data.astype("uint8"), mode="RGBA")
        im.save(file_path, "PNG")

        buffered = BytesIO()
        im.save(buffered, format="PNG")
        img_data = buffered.getvalue()
        
