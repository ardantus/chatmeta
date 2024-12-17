from flask import Flask, request, jsonify, render_template
from meta_ai_api import MetaAI

app = Flask(__name__)

# Inisialisasi MetaAI
ai = MetaAI()

@app.route('/')
def index():
    # Render halaman index.html
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Ambil pesan input dari user
    user_message = request.json.get("message")
    
    try:
        # Dapatkan respons dari MetaAI
        meta_ai_response = ai.prompt(message=user_message)

        # Debug: Cetak respons untuk memastikan formatnya
        print("DEBUG: MetaAI Response:", meta_ai_response)

        # Pastikan respons berupa string atau ekstrak dari objek
        if isinstance(meta_ai_response, dict):
            # Coba ambil kunci 'response', 'text', atau 'message' jika respons adalah dictionary
            response_text = meta_ai_response.get("response") or meta_ai_response.get("text") or meta_ai_response.get("message") or "Respons tidak tersedia."
        else:
            # Jika bukan dictionary, konversi langsung ke string
            response_text = str(meta_ai_response)

        # Return respons ke frontend dalam format JSON
        return jsonify({"response": response_text})

    except Exception as e:
        # Tangani error jika ada masalah saat memanggil MetaAI
        print("Error:", e)  # Cetak error ke terminal
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Jalankan aplikasi Flask di port 8081
    app.run(debug=True, host='0.0.0.0', port=8081)
