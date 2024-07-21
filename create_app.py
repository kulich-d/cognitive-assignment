import streamlit as st
import requests

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


# Заголовок приложения
st.title("Image Uploader to API")

# Загрузка первой картинки
uploaded_file1 = st.file_uploader("Upload first image", type=["jpg", "jpeg", "png"])
# Загрузка второй картинки
uploaded_file2 = st.file_uploader("Upload second image", type=["jpg", "jpeg", "png"])

if uploaded_file1 and uploaded_file2:
    # Отображение загруженных изображений
    st.image(uploaded_file1, caption='First Image', use_column_width=True)
    st.image(uploaded_file2, caption='Second Image', use_column_width=True)

    # Преобразование загруженных файлов в формат, пригодный для отправки через API
    image1 = uploaded_file1.read()
    image2 = uploaded_file2.read()

    # Кнопка для отправки изображений на API
    if st.button("Send to API"):
        with st.spinner("Sending images to API..."):
            result = send_images_to_api(io.BytesIO(image1), io.BytesIO(image2))
            st.success("Images sent successfully!")
            st.json(result)
