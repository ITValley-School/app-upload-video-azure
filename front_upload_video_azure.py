import streamlit as st
from service_upload_video_azure import processar_upload
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Título principal
st.markdown("<h1 style='text-align: center;'>scripto.ai</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Upload Your Video to Azure Video Indexer</h2>", unsafe_allow_html=True)

# Carregar o logo no sidebar
logo_path = "it_valley.png"
st.sidebar.image(logo_path, use_column_width=True)

# Seção de upload na área principal
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mkv", "avi", "mpeg4"])

# Se um arquivo foi carregado, usar o nome do arquivo como nome padrão
if uploaded_file is not None:
    video_name = st.text_input("Video Name", value=uploaded_file.name.split(".")[0])
    description = st.text_input("Description", value="Uploaded via IAConversacional")
else:
    video_name = st.text_input("Video Name", value="My Video")
    description = st.text_input("Description", value="Description of the video")

privacy = st.selectbox("Privacy", options=["Private", "Public"])

# Botão para enviar o vídeo
if st.button("Upload Video"):
    if uploaded_file:
        # Exibir spinner na área principal durante o processamento
        with st.spinner("Uploading video... Please wait."):
            video_id, video_url = processar_upload(uploaded_file, video_name, description, privacy)
        
        # Mensagem de sucesso ou erro na área principal
        if video_id:
            st.success(f"Video uploaded successfully! ID: {video_id}")
            st.markdown(f"[Click here to access the video on Azure Video Indexer](https://www.videoindexer.ai/media/library)")
        else:
            st.error("Failed to upload the video.")
    else:
        st.error("Please select a video file.")

