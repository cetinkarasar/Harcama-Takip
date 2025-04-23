from flask import Flask, render_template, request, redirect, flash
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Flash mesajları için gerekli

dosya_adi = "harcamalar.csv"

def verileri_yukle():
    harcamalar = []
    try:
        with open(dosya_adi, mode="r", newline='', encoding="utf-8") as dosya:
            okuyucu = csv.DictReader(dosya)
            for satir in okuyucu:
                satir["tutar"] = float(satir["tutar"])
                harcamalar.append(satir)
    except FileNotFoundError:
        pass
    return harcamalar

def veriyi_kaydet(harcama):
    dosya_var = False
    try:
        open(dosya_adi).close()
        dosya_var = True
    except FileNotFoundError:
        pass

    with open(dosya_adi, mode="a", newline='', encoding="utf-8") as dosya:
        alanlar = ["tarih", "tutar", "kategori", "aciklama"]
        yazici = csv.DictWriter(dosya, fieldnames=alanlar)

        if not dosya_var:
            yazici.writeheader()
        yazici.writerow(harcama)

def veriyi_sil(sil_tarih, sil_tutar, sil_kategori, sil_aciklama):
    yeni_veriler = []
    with open(dosya_adi, mode="r", newline='', encoding="utf-8") as dosya:
        okuyucu = csv.DictReader(dosya)
        for satir in okuyucu:
            if not (satir["tarih"] == sil_tarih and
                    satir["tutar"] == sil_tutar and
                    satir["kategori"] == sil_kategori and
                    satir["aciklama"] == sil_aciklama):
                yeni_veriler.append(satir)

    with open(dosya_adi, mode="w", newline='', encoding="utf-8") as dosya:
        alanlar = ["tarih", "tutar", "kategori", "aciklama"]
        yazici = csv.DictWriter(dosya, fieldnames=alanlar)
        yazici.writeheader()
        yazici.writerows(yeni_veriler)

@app.route('/sil', methods=["POST"])
def sil():
    tarih = request.form.get("tarih")
    tutar = request.form.get("tutar")
    kategori = request.form.get("kategori")
    aciklama = request.form.get("aciklama")

    veriyi_sil(tarih, tutar, kategori, aciklama)
    flash('Harcama başarıyla silindi!', 'success')  # Başarı mesajı
    return redirect('/')

@app.route('/')
def index():
    harcamalar = verileri_yukle()
    toplam = sum(h["tutar"] for h in harcamalar)
    return render_template("index.html", harcamalar=harcamalar, toplam=toplam)

@app.route('/ekle', methods=["POST"])
def ekle():
    tarih = request.form.get("tarih") or datetime.today().strftime('%Y-%m-%d')
    tutar = float(request.form.get("tutar"))
    kategori = request.form.get("kategori")
    aciklama = request.form.get("aciklama")

    harcama = {
        "tarih": tarih,
        "tutar": tutar,
        "kategori": kategori,
        "aciklama": aciklama
    }

    veriyi_kaydet(harcama)
    flash('Harcama başarıyla eklendi!', 'success')  # Başarı mesajı
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
