
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Data absensi sementara
attendance_data = []

# Daftar mata kuliah
subjects = [
    "Algoritma dan Pemrograman",
    "Fisika",
    "Matematika",
    "Bahasa Indonesia"
]


# Halaman utama langsung membuka dashboard
@app.route("/")
def home():
    return redirect(url_for("dashboard"))


# Dashboard utama
@app.route("/dashboard")
def dashboard():

    total_attendance = len(attendance_data)

    total_subjects = len({
        item["subject"] for item in attendance_data
    })

    latest_attendance = (
        attendance_data[-1] if attendance_data else None
    )

    return render_template(
        "dashboard.html",
        username="Mahasiswa",
        role="Mahasiswa",
        total_attendance=total_attendance,
        total_subjects=total_subjects,
        latest_attendance=latest_attendance
    )


# Dashboard admin
@app.route("/admin")
def admin_dashboard():

    return render_template(
        "admin_dashboard.html",
        username="Admin"
    )


# Data absensi untuk halaman admin
@app.route("/admin/attendance")
def admin_attendance():

    return render_template(
        "admin_attendance.html",
        attendance_data=attendance_data
    )


# Halaman pengisian absensi
@app.route("/attendance")
def attendance():

    return render_template(
        "attendance.html",
        subjects=subjects
    )


# Proses pengiriman absensi
@app.route("/take-attendance", methods=["POST"])
def take_attendance():

    student_name = request.form.get(
        "student_name", ""
    ).strip()

    subject = request.form.get("subject", "")

    if not student_name or subject not in subjects:
        return redirect(url_for("attendance"))

    attendance = {
        "username": student_name,
        "subject": subject,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M")
    }

    attendance_data.append(attendance)

    return redirect(url_for("history"))


# Riwayat seluruh absensi
@app.route("/history")
def history():

    return render_template(
        "history.html",
        attendance_data=attendance_data
    )


if __name__ == "__main__":
    app.run(debug=True)
