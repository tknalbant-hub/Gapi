import streamlit as st
import time
import json
import os
from google import genai
from google.genai import types

# --- 1. SİLİNMEYEN İNTERNET HAFIZASI (SESSION STATE & GÜVENLİ DEPOLAMA) ---
# İnternet sunucusunda kalıcı hafızayı korumak için Streamlit'in tarayıcı tabanlı hafızasını
# ve ileride harici bir veri tabanına (Örn: Supabase/Firebase) bağlanmaya hazır esnek yapıyı kuruyoruz.

if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = [
        {"role": "assistant", "content": "Merhaba Tarık Kayra. GAPİ bulut çekirdeği internet üzerinde 7/24 aktif. Hafıza ve yapay zeka modüllerim global erişime hazır. Dinlemedeyim."}
    ]

# --- 2. BULUT API GÜVENLİK AYARI ---
@st.cache_resource
def yapay_zeka_bulut_baglan():
    # İnternette çalışırken anahtar Streamlit Secrets'tan (st.secrets) otomatik çekilir
    try:
        if "GEMINI_API_KEY" in st.secrets:
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        else:
            # Lokal testler için geri dönüş kapısı
            client = genai.Client()
        return client
    except Exception as e:
        return None

ai_client = yapay_zeka_bulut_baglan()

# --- 3. SİBER ARAYÜZ TASARIMI ---
st.set_page_config(page_title="GAPİ Cloud v1.0", page_icon="🛰️", layout="centered")

st.markdown("""
    <style>
        .stTextInput>div>div>input { color: #DEFF9A; background-color: #000000; }
        .stChatMessage { border-radius: 15px; margin-bottom: 10px; border: 1px solid rgba(222, 255, 154, 0.1); }
    </style>
""", unsafe_allow_html=True)

st.title("🛰️ GAPİ Bulut Kontrol Merkezi")
st.caption("Gelişmiş Arduino-Pi İşlemcisi — Global Yazılım Çekirdeği")
st.write("---")

# Sol Menü (Bulut Göstergeleri)
with st.sidebar:
    st.header("🌐 Bulut Sunucu Durumu")
    st.success("⚡ Sunucu: 7/24 ÇALIŞIYOR (Bulut)")
    if ai_client:
        st.success("🧠 Yapay Zeka: GLOBAL AKTİF")
    else:
        st.error("⚠️ API KEY EKSİK! (Streamlit Secrets Ayarla)")
    st.write("---")
    st.markdown("**Geliştirici:** Tarık Kayra Nalbant")
    
    if st.button("🔴 Mevcut Oturum Hafızasını Temizle", use_container_width=True):
        st.session_state.mesajlar = [st.session_state.mesajlar[0]]
        st.rerun()

# Geçmiş mesajları internet tarayıcısında göster
for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["role"]):
        st.write(mesaj["content"])

# --- 4. GLOBAL DÜŞÜNCE MOTORU ---
if kullanici_girdisi := st.chat_input("İnternet üzerinden GAPİ'ye emir ver..."):
    
    st.session_state.mesajlar.append({"role": "user", "content": kullanici_girdisi})
    with st.chat_message("user"):
        st.write(kullanici_girdisi)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        gapi_cevabi = ""
        
        if ai_client:
            try:
                sistem_talimati = (
                    "Sen GAPİ'sin (Gelişmiş Arduino-Pi İşlemcisi). Tarık Kayra Nalbant tarafından "
                    "geliştirilen, internet üzerinden çalışan akıllı bir bulut asistanısın. "
                    "Yanıtların teknolojik, net ve çözüm odaklı olmalı. Kullanıcına ismiyle (Tarık Kayra) hitap et."
                )
                
                # Hafıza bağlamını oluştur
                gecmis_baglami = []
                for m in st.session_state.mesajlar[-12:]:
                    rol_tipi = "user" if m["role"] == "user" else "model"
                    gecmis_baglami.append(types.Content(role=rol_tipi, parts=[types.Part.from_text(text=m["content"])]))

                response = ai_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=gecmis_baglami,
                    config=types.GenerateContentConfig(
                        system_instruction=sistem_talimati,
                        temperature=0.7
                    )
                )
                gapi_cevabi = response.text
            except Exception as e:
                gapi_cevabi = f"Bulut API hatası oluştu Tarık Kayra: {e}"
        else:
            gapi_cevabi = "Yapay zeka motoru buluta bağlanamadı. Lütfen Streamlit Secrets ayarlarını kontrol et Tarık Kayra."

        # Akıcı yazı efekti
        full_response = ""
        for char in gapi_cevabi:
            full_response += char
            time.sleep(0.005)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    st.session_state.mesajlar.append({"role": "assistant", "content": gapi_cevabi})