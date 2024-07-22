import streamlit as st
import requests
from PIL import Image
import io


# Функция для отправки изображений на API
def send_images_to_api(image1, image2):
    url = "http://127.0.0.1:8000/congnitiv-analysis"
    files = {
        'advertisement_image': ('advert_image.jpg', image1, 'image/jpeg'),
        'advertisement_heatmap_image': ('heatmap_image.jpg', image2, 'image/jpeg')
    }
    response = requests.post(url, files=files)
    return response.json()

def resize_image(image, scale_factor):
    image = Image.open(image)
    image = image.convert("RGB") # to reduce buf length
    width, height = image.size
    new_width = width // scale_factor
    new_height = height // scale_factor
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    return resized_image


st.title("Image Uploader to API")

uploaded_file1 = st.file_uploader("Upload first image", type=["jpg", "jpeg", "png"])
uploaded_file2 = st.file_uploader("Upload second image", type=["jpg", "jpeg", "png"])



if uploaded_file1 and uploaded_file2:
    st.image(uploaded_file1, caption='First Image', use_column_width=True)
    st.image(uploaded_file2, caption='Second Image', use_column_width=True)

    image1 = uploaded_file1.read()
    image2 = uploaded_file2.read()

    resized_image1 = resize_image(io.BytesIO(image1), 4)
    resized_image2 = resize_image(io.BytesIO(image2), 4)


    buffered1 = io.BytesIO()
    resized_image1.save(buffered1, format="JPEG")
    buffered1.seek(0)

    buffered2 = io.BytesIO()
    resized_image2.save(buffered2, format="JPEG")
    buffered2.seek(0)


    if st.button("Send to API"):
        with st.spinner("Sending images to API..."):


            result = send_images_to_api(buffered1, buffered2)
            st.success("Images sent successfully!")
            st.json(result)
