from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/<page>")
def index(page="Grafik IPK"):
    # Pilih template berdasarkan halaman
    if page == "DataDiri":
        content_template = "data_diri.html"
    elif page == "DaftarNilai":
        content_template = "daftar_nilai.html"
    elif page == "LaporanNilai":
        content_template = "laporan_nilai.html"
    elif page == "GrafikIPK":
        content_template = "grafik_ipk.html"
    else:
        content_template = "grafik_ipk.html"  # Default

    return render_template("index.html", page=page, content_template=content_template)

if __name__ == "__main__":
    app.run(debug=True)
