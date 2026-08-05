import json
from PIL import Image
import streamlit as st
from ultralytics import YOLO
import csv
from datetime import datetime
import pandas as pd


# Atur layout menjadi wide (lebar penuh)
st.set_page_config(
    page_title="Pastry Shop Deteksi",
    layout="wide"  
)

# Judul
st.markdown("Pastry Shop")

# Load Model YOLO
model = YOLO("best.onnx", task="detect")


# 1. Inisialisasi session untuk cart dan gambar hasil deteksi
if "cart" not in st.session_state:
  st.session_state.cart = {}

if "processed_image" not in st.session_state:
  st.session_state.processed_image = None

# 2. Daftar Produk Utama (Pastikan ini ada di atas sebelum dipanggil)
produk_list = {
    "croissant": {
        "nama": "Croissant Original",
        "harga": 25000,
        "gambar": "images/croissant.jpg",
    },
    "baklava": {
        "nama": "Baklava",
        "harga": 30000,
        "gambar": "images/baklava.jpg",
    },
    "pain au chocolat": {
            "nama": "Pain au chocolate",
            "harga": 30000,
            "gambar": "images/pain au chocolate.jpg",
    },
    "Canele": {
            "nama": "Canele",
            "harga": 30000,
            "gambar": "images/canele.jpg",
    },
    "tebirkes": {
            "nama": "Tebirkes",
            "harga": 30000,
            "gambar": "images/tebirkes.jpg",
    },
}

# Mapping dari nama label YOLO ke prod_id produk_list
label_to_prod_id = {
    "croissant": "croissant",
    "baklava": "baklava",
    "pain au chocolat" : "pain au chocolat",
    "Canele" : "Canele",
    "tebirkes" : "tebirkes"
}

# --- FORM UPLOAD GAMBAR ---
# with st.form("upload_form"):
#   uploaded_files = st.file_uploader(
#       "Upload images", accept_multiple_files=False, type=["jpg", "png", "jpeg"]
#   )
#   submitted = st.form_submit_button("Proses Gambar")


# web camera
cam, kasir = st.columns(2)

with cam:
  toggle = st.toggle("camera active")
  if toggle :
    picture = st.camera_input("Take a picture")
    if picture is not None:

      # if submitted and uploaded_files is not None:
        image = Image.open(picture)
        results = model(image)

        # Ambil hasil plot YOLO dan ubah ke RGB PIL Image
        for r in results:
          im_bgr = r.plot()
          im_rgb = Image.fromarray(im_bgr[..., ::-1])
          st.session_state.processed_image = im_rgb

        # Proses data prediksi untuk dimasukkan ke cart
        list_pastry = []
        for r in results:
          convert_json = r.to_json()
          list_json = json.loads(convert_json)
          for item in list_json:
            list_pastry.append(item["name"])

        total_pesanan = {}
        for pesanan in list_pastry:
          total_pesanan[pesanan] = total_pesanan.get(pesanan, 0) + 1

        # Masukkan hasil YOLO ke cart menggunakan prod_id
        for nama_yolo, qty in total_pesanan.items():
          prod_id = label_to_prod_id.get(
              nama_yolo, "croissant"
          )  # Default fallback jika tidak ada
          info = produk_list.get(
              prod_id, {"nama": nama_yolo, "harga": 25000}
          )

          if prod_id in st.session_state.cart:
            st.session_state.cart[prod_id]["qty"] += qty
          else:
            st.session_state.cart[prod_id] = {
                "nama": info["nama"],
                "harga": info["harga"],
                "qty": qty,
            }

      # --- TAMPILKAN GAMBAR JIKA ADA DI SESSION ---
    if st.session_state.processed_image is not None:
        st.image(st.session_state.processed_image, caption="Hasil Deteksi Model")


# ==========================================
# Bagian Edit Manual (Grid Produk)
# ==========================================
st.markdown("---")
st.subheader("🥐 Pilih Produk Manual")
col1, col2, col3, col4 = st.columns(4)

# --- Produk 1 ---
with col1:
  with st.container(border=True):
    st.image(
        produk_list["croissant"]["gambar"], use_container_width=True
    )  # Perbaikan parameter width
    st.markdown(
        f"<h4 style='text-align: center;'>{produk_list['croissant']['nama']}</h4>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center;'>Rp {produk_list['croissant']['harga']:,}</p>",
        unsafe_allow_html=True,
    )

    if st.button("Pesan", key="btn_c1"):
      prod_id = "croissant"
      if prod_id in st.session_state.cart:
        st.session_state.cart[prod_id]["qty"] += 1
      else:
        st.session_state.cart[prod_id] = {
            "nama": produk_list[prod_id]["nama"],
            "harga": produk_list[prod_id]["harga"],
            "qty": 1,
        }
      st.rerun()

# --- Produk 2 ---
with col2:
  with st.container(border=True):
    st.image(produk_list["baklava"]["gambar"], use_container_width=True)
    st.markdown(
        f"<h4 style='text-align: center;'>{produk_list['baklava']['nama']}</h4>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center;'>Rp {produk_list['baklava']['harga']:,}</p>",
        unsafe_allow_html=True,
    )

    if st.button("Pesan", key="btn_c2"):
      prod_id = "baklava"
      if prod_id in st.session_state.cart:
        st.session_state.cart[prod_id]["qty"] += 1
      else:
        st.session_state.cart[prod_id] = {
            "nama": produk_list[prod_id]["nama"],
            "harga": produk_list[prod_id]["harga"],
            "qty": 1,
        }
      st.rerun()


# --- Produk 3 ---
with col3:
  with st.container(border=True):
    st.image(produk_list["pain au chocolat"]["gambar"], use_container_width=True)
    st.markdown(
        f"<h4 style='text-align: center;'>{produk_list['pain au chocolat']['nama']}</h4>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center;'>Rp {produk_list['pain au chocolat']['harga']:,}</p>",
        unsafe_allow_html=True,
    )

    if st.button("Pesan", key="btn_c3"):
      prod_id = "pain au chocolat"
      if prod_id in st.session_state.cart:
        st.session_state.cart[prod_id]["qty"] += 1
      else:
        st.session_state.cart[prod_id] = {
            "nama": produk_list[prod_id]["nama"],
            "harga": produk_list[prod_id]["harga"],
            "qty": 1,
        }
      st.rerun()


# --- Produk 4 ---
with col4:
  with st.container(border=True):
    st.image(produk_list["Canele"]["gambar"], use_container_width=True)
    st.markdown(
        f"<h4 style='text-align: center;'>{produk_list['Canele']['nama']}</h4>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center;'>Rp {produk_list['Canele']['harga']:,}</p>",
        unsafe_allow_html=True,
    )

    if st.button("Pesan", key="btn_c4"):
      prod_id = "Canele"
      if prod_id in st.session_state.cart:
        st.session_state.cart[prod_id]["qty"] += 1
      else:
        st.session_state.cart[prod_id] = {
            "nama": produk_list[prod_id]["nama"],
            "harga": produk_list[prod_id]["harga"],
            "qty": 1,
        }
      st.rerun()


# --- Produk 5 ---
col5,col6, col7, col8 = st.columns(4)
with col5:
  with st.container(border=True):
    st.image(produk_list["tebirkes"]["gambar"], use_container_width=True)
    st.markdown(
        f"<h4 style='text-align: center;'>{produk_list['tebirkes']['nama']}</h4>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center;'>Rp {produk_list['tebirkes']['harga']:,}</p>",
        unsafe_allow_html=True,
    )

    if st.button("Pesan", key="btn_c5"):
      prod_id = "tebirkes"
      if prod_id in st.session_state.cart:
        st.session_state.cart[prod_id]["qty"] += 1
      else:
        st.session_state.cart[prod_id] = {
            "nama": produk_list[prod_id]["nama"],
            "harga": produk_list[prod_id]["harga"],
            "qty": 1,
        }
      st.rerun()

# ==========================================
# Bagian Daftar Pesanan / Invoice (Cart)
# ==========================================

with kasir :
  st.subheader("📋 Daftar Pesanan Anda (Invoice)")
  if not st.session_state.cart:
    st.info("Belum ada pesanan yang dipilih.")
  else:
    total_keseluruhan = 0

    for prod_id, item in list(st.session_state.cart.items()):
      subtotal = item["harga"] * item["qty"]
      total_keseluruhan += subtotal

      col_name, col_qty, col_minus,  col_plus, col_delete, col_sub= st.columns(
          [2, 1, 0.8, 0.8, 1.2, 0.8]
      )

      col_name.write(item["nama"])
      col_qty.write(f"x{item['qty']}")

      # Tombol Kurang (-)
      if col_minus.button("➖", key=f"min_{prod_id}"):
        if item["qty"] > 1:
          st.session_state.cart[prod_id]["qty"] -= 1
        else:
          del st.session_state.cart[prod_id]
        st.rerun()

      # Tombol Kurang (+)
      if col_plus.button("+", key=f"max_{prod_id}"):
        st.session_state.cart[prod_id]["qty"] += 1   
        st.rerun()

      # Tombol Hapus (🗑️)
      if col_delete.button("🗑️", key=f"del_{prod_id}"):
        del st.session_state.cart[prod_id]
        st.rerun()

      col_sub.write(f"Rp {subtotal:,}")

    st.write("---")
    st.write(f"**Total Pembayaran: Rp {total_keseluruhan:,}**")

    if st.button("Checkout Sekarang", type="primary"):
      waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      # mengumpulkan data dari keranjang kedalam list
      data_transaksi = []
      for prod_id, item in st.session_state.cart.items():
        subtotal = item["harga"] * item["qty"]
        data_transaksi.append({
                    "Waktu": waktu,
                    "Produk": item["nama"],
                    "Harga Satuan": item["harga"],
                    "Quantity": item["qty"],
                    "Subtotal": subtotal,
                    "Total Keseluruhan": total_keseluruhan
        })

      # ubah ke pandas
      df_baru = pd.DataFrame(data_transaksi)

      # simpan file
      try:
        # Jika file sudah ada, append (tambah di bawah). Jika belum, buat baru dengan header.
        df_baru.to_csv("pastry.csv", mode='a', index=False, header=not pd.io.common.file_exists("pastry.csv"))
      except Exception as e:
        st.error(f"Gagal menyimpan: {e}")

      
      st.success("Pesanan berhasil diproses!")
      st.session_state.cart = {}
      st.session_state.processed_image = None
      st.rerun()

