import os
import requests
from dotenv import load_dotenv
import streamlit as st

# Carrega as variáveis do arquivo .env
load_dotenv()

# Função para obter o token do Azure AD
def obter_token_azure():
    url = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("AZURE_CLIENT_ID"),
        "client_secret": os.getenv("AZURE_CLIENT_SECRET"),
        "scope": "https://management.azure.com/.default"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        st.error(f"Erro ao obter token do Azure AD: {response.status_code}, {response.text}")
        return None

# Função para obter o token do Video Indexer
def obter_token_video_indexer(subscription_id, resource_group, account_name, access_token):
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.VideoIndexer/accounts/{account_name}/generateAccessToken?api-version=2024-01-01"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    body = {
        "permissionType": "Contributor",
        "scope": "Account"
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        token = response.json().get("accessToken")
        return token
    else:
        st.error(f"Erro ao obter token do Video Indexer: {response.status_code}, {response.text}")
        return None

# Função para fazer upload de vídeo para o Azure Video Indexer
def upload_video_azure(access_token, location, account_id, uploaded_file, video_name, description, privacy):
    url = f"https://api.videoindexer.ai/{location}/Accounts/{account_id}/Videos"
    params = {
        'accessToken': access_token,
        'name': video_name,
        'description': description,
        'privacy': privacy
    }

    # Envio como multipart/form-data
    files = {
        'file': (uploaded_file.name, uploaded_file, uploaded_file.type)
    }

    response = requests.post(url, params=params, files=files)

    if response.status_code == 200:
        video_id = response.json().get("id")  # ID do vídeo retornado
        video_url = response.json().get("accountUrl")
        return video_id, video_url
    else:
        st.error(f"Erro ao fazer upload do vídeo: {response.status_code}, Detalhes: {response.text}")
        return None, None

# Função que será usada no frontend para fazer o upload do vídeo
def processar_upload(uploaded_file, video_name, description, privacy):
    subscription_id = os.getenv('subscriptionId')
    resource_group = os.getenv('resourceGroupName')
    account_name = os.getenv('accountname')
    location = os.getenv('location')
    account_id = os.getenv('accountId')

    azure_access_token = obter_token_azure()
    if azure_access_token:
        video_indexer_token = obter_token_video_indexer(subscription_id, resource_group, account_name, azure_access_token)
        if video_indexer_token:
            video_id, video_url = upload_video_azure(video_indexer_token, location, account_id, uploaded_file, video_name, description, privacy)
            if video_id:
                return video_id, video_url
            else:
                return None, None
