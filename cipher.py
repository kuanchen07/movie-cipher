import streamlit as st
import json
import os

# Function to load the key from an uploaded file
def load_key(uploaded_file):
    if uploaded_file is not None:
        return uploaded_file.getvalue().decode().strip()
    return None

# Vigenère cipher function (unchanged)
def vigenere_cipher(text, key, mode='encrypt'):
    result = []
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - 65
            if mode == 'decrypt':
                shift = -shift
            if char.isupper():
                result.append(chr((ord(char) - 65 + shift) % 26 + 65))
            else:
                result.append(chr((ord(char) - 97 + shift) % 26 + 97))
        else:
            result.append(char)
    return ''.join(result)

# Function to load history
def load_history():
    if os.path.exists('movie_titles.json'):
        with open('movie_titles.json', 'r') as file:
            return json.load(file)
    return {"encrypted": [], "decrypted": []}

# Function to save history
def save_history(history):
    with open('movie_titles.json', 'w') as file:
        json.dump(history, file)

# Streamlit app
def main():
    st.title("Vigenère Cipher - Movie Title Encoder/Decoder")

    # File uploader for key
    uploaded_file = st.file_uploader("Upload key file", type="txt")
    key = load_key(uploaded_file)

    if key is None:
        st.error("Please upload a key file to proceed.")
        return

    # Load history
    history = load_history()

    # Tabs for Encrypt and Decrypt
    tab1, tab2, tab3 = st.tabs(["Encrypt", "Decrypt", "History"])

    with tab1:
        st.header("Encrypt a Movie Title")
        title_to_encrypt = st.text_input("Enter the movie title to encrypt:")
        if st.button("Encrypt"):
            if title_to_encrypt:
                encrypted = vigenere_cipher(title_to_encrypt, key, 'encrypt')
                st.success(f"Encrypted title: {encrypted}")
                history["encrypted"].append({"original": title_to_encrypt, "encrypted": encrypted})
                save_history(history)
            else:
                st.warning("Please enter a movie title to encrypt.")

    with tab2:
        st.header("Decrypt a Movie Title")
        title_to_decrypt = st.text_input("Enter the movie title to decrypt:")
        if st.button("Decrypt"):
            if title_to_decrypt:
                decrypted = vigenere_cipher(title_to_decrypt, key, 'decrypt')
                st.success(f"Decrypted title: {decrypted}")
                history["decrypted"].append({"encrypted": title_to_decrypt, "decrypted": decrypted})
                save_history(history)
            else:
                st.warning("Please enter a movie title to decrypt.")

    with tab3:
        st.header("Encryption/Decryption History")
        st.subheader("Encrypted Titles")
        for item in history["encrypted"]:
            st.write(f"Original: {item['original']} | Encrypted: {item['encrypted']}")
        st.subheader("Decrypted Titles")
        for item in history["decrypted"]:
            st.write(f"Encrypted: {item['encrypted']} | Decrypted: {item['decrypted']}")

if __name__ == "__main__":
    main()
