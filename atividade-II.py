import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

st.set_page_config(layout="wide", page_title="Editor de Imagens")

st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
        color: #000;
    }
    .stButton > button {
        background-color: #006400;
        color: white;
    }
    .css-1v0mbdj, .css-1x8cf1d {
        background-color: #e0e0e0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🖼️ Editor de Imagens")
st.caption("Aplique transformações geométricas, ajustes de intensidade e filtros nas suas imagens.")

uploaded_file = st.file_uploader("📁 Faça upload da imagem", type=["jpg", "jpeg", "png"])
use_webcam = st.checkbox("📸 Usar webcam")

image = None
if use_webcam:
    camera_image = st.camera_input("Capture uma imagem")
    if camera_image:
        image = Image.open(camera_image)
elif uploaded_file:
    image = Image.open(uploaded_file)

def pil_to_cv2(img):
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def cv2_to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

if image:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Imagem Original")
        st.image(image, use_column_width=True)

    img_cv2 = pil_to_cv2(image)

    st.sidebar.subheader("Transformações Geométricas")
    angle = st.sidebar.slider("Rotação (graus)", -180, 180, 0)
    scale = st.sidebar.slider("Escala", 10, 300, 100) / 100
    shear_x = st.sidebar.slider("Cisalhamento X", -50, 50, 0)
    shear_y = st.sidebar.slider("Cisalhamento Y", -50, 50, 0)

    rows, cols = img_cv2.shape[:2]
    M_rot = cv2.getRotationMatrix2D((cols/2, rows/2), angle, scale)
    img_transformed = cv2.warpAffine(img_cv2, M_rot, (cols, rows))

    shear_matrix = np.float32([
        [1, shear_x / 100, 0],
        [shear_y / 100, 1, 0]
    ])
    img_transformed = cv2.warpAffine(img_transformed, shear_matrix, (cols, rows))

    st.sidebar.subheader("Ajustes de Intensidade")
    brightness = st.sidebar.slider("Brilho", -100, 100, 0)
    contrast = st.sidebar.slider("Contraste", 10, 300, 100)
    log_transform = st.sidebar.checkbox("Transformação Logarítmica")
    gamma = st.sidebar.slider("Gama (γ)", 0.1, 5.0, 1.0)

    img_transformed = cv2.convertScaleAbs(img_transformed, alpha=contrast/100, beta=brightness)

    if log_transform:
        img_transformed = np.uint8(255 * (np.log1p(img_transformed) / np.log1p(255)))

    img_transformed = np.clip(255 * ((img_transformed / 255) ** (1.0 / gamma)), 0, 255).astype('uint8')

    st.sidebar.subheader("Filtros")
    if st.sidebar.checkbox("🔄 Negativo"):
        img_transformed = cv2.bitwise_not(img_transformed)

    with col2:
        st.subheader("Imagem Editada")
        st.image(cv2_to_pil(img_transformed), use_column_width=True)

        # Botão para download
        buf = BytesIO()
        cv2_to_pil(img_transformed).save(buf, format="JPEG")
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 Baixar imagem editada",
            data=byte_im,
            file_name="imagem_editada.jpg",
            mime="image/jpeg"
        )