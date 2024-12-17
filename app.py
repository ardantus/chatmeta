import os
from flask import Flask, request, jsonify, render_template
from meta_ai_api import MetaAI

app = Flask(__name__)

# Ambil kredensial dari environment atau set langsung
FB_EMAIL = os.getenv("META_FB_EMAIL", "your_fb_email")
FB_PASSWORD = os.getenv("META_FB_PASSWORD", "your_fb_password")

# Inisialisasi MetaAI
ai = None
ai_with_login = None

def initialize_metaai():
    """Fungsi untuk memastikan MetaAI login."""
    global ai_with_login
    try:
        print("DEBUG: Mencoba login ke MetaAI...")
        ai_with_login = MetaAI(fb_email=FB_EMAIL, fb_password=FB_PASSWORD)
        print("DEBUG: Login MetaAI berhasil.")
    except Exception as e:
        print("ERROR: Gagal login ke MetaAI:", e)
        ai_with_login = None

try:
    # Inisialisasi untuk teks
    print("DEBUG: Inisialisasi MetaAI untuk teks...")
    ai = MetaAI()
    print("DEBUG: MetaAI berhasil diinisialisasi untuk teks.")
except Exception as e:
    print("ERROR: MetaAI tidak dapat diinisialisasi:", e)
    ai = None

# Login untuk fitur gambar
initialize_metaai()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Route untuk menangani teks."""
    user_message = request.json.get("message", "")

    try:
        if not ai:
            raise Exception("MetaAI tidak dapat diinisialisasi.")

        print(f"DEBUG: Permintaan teks: {user_message}")
        response = ai.prompt(message=user_message)

        if isinstance(response, dict):
            response_text = response.get("message", "Respons tidak tersedia.")
        else:
            response_text = response.strip() if response else "Respons tidak tersedia."

        return jsonify({"response": response_text})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"response": "Error: Tidak dapat memproses permintaan."}), 500

@app.route('/generate-image', methods=['POST'])
def generate_image():
    """Route untuk menangani generate gambar."""
    user_message = request.json.get("message", "")

    try:
        if not ai_with_login:
            initialize_metaai()  # Coba login ulang
            if not ai_with_login:
                return jsonify({"response": "Error: Gagal login. Pastikan kredensial benar."}), 403

        print(f"DEBUG: Permintaan generate image: {user_message}")
        response = ai_with_login.prompt(message=user_message)

        # Debug respons
        print("DEBUG: Raw Image Response:", response)

        if isinstance(response, dict) and "image_url" in response:
            return jsonify({"image_url": response["image_url"], "response": "Gambar berhasil dibuat."})
        else:
            return jsonify({"response": "Gambar tidak tersedia.", "image_url": None})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"response": "Error: Gagal menghasilkan gambar.", "image_url": None}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
