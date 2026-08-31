# Framework Pengujian API Playwright-Python

[English](README.md) | [Bahasa Indonesia](README.id.md)

Proyek ini adalah framework pengujian API yang ringan, dibuat dengan Python, pytest, dan Playwright API request client. Framework ini dirancang untuk konfigurasi berbasis environment, test case yang dapat digunakan kembali, skenario berbasis Excel, serta laporan HTML untuk validasi smoke.

## Ringkasan

Framework ini mendukung:

- Switching environment melalui `--env`
- Fixture `api` yang berbagi context request Playwright
- Modul test case reusable di dalam `test_case/`
- Eksekusi berbasis data dari file Excel
- Validasi response berdasarkan status dan body yang diharapkan
- Laporan HTML suite yang tersimpan di `reports/`

## Persyaratan

- Python 3.13 atau versi Python 3 yang kompatibel
- Akses internet ke API yang dikonfigurasi
- PowerShell di Windows, atau shell yang serupa

## Struktur Proyek

```text
config/                 File konfigurasi YAML environment
core/                   Logika inti framework
  api_client.py         Wrapper API Playwright
  body_builder.py       Helper pembuatan request body
  context.py           Helper context
  data_driven.py       Merge data + eksekusi validasi
  header_builder.py    Helper pembuatan header
  report_manager.py    Penghasil laporan HTML
  report_helper.py     Builder template HTML
  response_validator.py Validasi assert response
  suite_helper.py      Runner suite berbasis Excel
  test_executor.py     Alur eksekusi reusable
  test_loader.py       Helper pemuat test
  test_logger.py       Helper logging

data/                   File skenario Excel
  test_excel_contoh.xlsx
reports/                Laporan HTML hasil eksekusi
  YYYY-MM-DD/
    test_smoke/
      test_smoke_<timestamp>.html
test_case/              Modul test case reusable
  booking/
    test_create_booking.py
    test_get_booking.py
test_suite/             Entry point suite
  smoke/
    suite_smoke.py
utils/                  Utility bersama
  config.py             Loader environment YAML
  excel_utils.py       Pembaca file Excel
conftest.py             Fixture pytest dan opsi CLI
requirements.txt        Daftar dependency
README.md               Dokumentasi bahasa Inggris
README.id.md            Dokumentasi bahasa Indonesia
```

## Konfigurasi Environment

Framework membaca konfigurasi dari `config/<environment>.yaml`.

File yang tersedia saat ini:

- `config/staging.yaml` dengan URL default Restful Booker
- `config/dev.yaml`
- `config/uat.yaml`

Contoh isi file:

```yaml
base_url: https://restful-booker.herokuapp.com
```

Environment default adalah `staging`, seperti yang ditetapkan di `conftest.py`:

```python
parser.addoption(
    "--env",
    action="store",
    default="staging",
    help="Environment: dev, staging, uat"
)
```

Untuk menjalankan suite pada environment tertentu:

```powershell
pytest -v --env dev .\test_suite\smoke\suite_smoke.py
pytest -v --env staging .\test_suite\smoke\suite_smoke.py
pytest -v --env uat .\test_suite\smoke\suite_smoke.py
```

## Instalasi

Buat dan aktifkan virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependency:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Jika nanti ditambahkan test berbasis browser, install browser Playwright dengan:

```powershell
playwright install
```

## Cara Kerja Framework

1. `conftest.py` membaca flag `--env` dan memuat konfigurasi YAML yang sesuai melalui `utils/config.py`.
2. Fixture `api` membuat request context Playwright dengan `base_url` dari konfigurasi environment.
3. Modul test mengekspor fungsi `run(api, data=None)` dan mengembalikan hasil dari `DataDriven.run(...)`.
4. `SuiteHelper.run(...)` membaca lembar Excel, memfilter baris dengan `execute = Y`, mengimpor modul test yang cocok, lalu menjalankannya.
5. `ReportManager.generate()` menulis file HTML di `reports/YYYY-MM-DD/<suite_name>/`.

## Menjalankan Test

Jalankan satu test booking secara langsung:

```powershell
pytest -v .\test_case\booking\test_create_booking.py
pytest -v .\test_case\booking\test_get_booking.py
```

Jalankan smoke suite:

```powershell
pytest -v .\test_suite\smoke\suite_smoke.py
```

Jalankan semua test di proyek:

```powershell
pytest -v
```

Jalankan test tertentu berdasarkan keyword:

```powershell
pytest -v .\test_case\booking\test_create_booking.py -k test_create_booking
```

Tampilkan apa yang akan dikumpulkan pytest tanpa menjalankan:

```powershell
pytest --collect-only -q
```

## Smoke Suite dan Data Excel

Smoke suite membaca data dari `data/test_excel_contoh.xlsx` dan mengambil sheet `API_TEST`.

Setiap baris diperlakukan sebagai satu skenario dengan field seperti:

- `execute`
- `test_case`
- override request tambahan
- nilai expected result

Suite helper mengimpor modul dengan pola `test_case.<test_case>`, misalnya:

```python
module = importlib.import_module(f"test_case.{test_case}")
result = module.run(api, data)
```

## Laporan

Saat smoke suite dijalankan, file HTML dibuat dalam struktur berikut:

```text
reports/2026-08-31/test_smoke/test_smoke_20260831_082812.html
```

Laporan yang dihasilkan berisi ringkasan suite, status setiap test, detail request, detail response, serta durasi eksekusi.

## Menambahkan Test Case Baru

1. Buat atau perbarui modul di `test_case/`.
2. Sediakan fungsi `run(api, data=None)`.
3. Letakkan request default dan expected value di dalam modul.
4. Tambahkan atau perbarui baris skenario di `data/test_excel_contoh.xlsx`.
5. Jalankan test secara spesifik, lalu jalankan smoke suite.

Contoh pola:

```python
def run(api, data=None):
    return DataDriven.run(api=api, default_data=DEFAULT_DATA, data=data)
```

## Troubleshooting

- Jika pytest menimbulkan error konfigurasi, pastikan `config/<environment>.yaml` ada dan berisi `base_url`.
- Jika suite berbasis Excel gagal dimuat, pastikan `data/test_excel_contoh.xlsx` ada dan memiliki worksheet `API_TEST`.
- Jika panggilan API gagal, cek environment yang dipilih, akses internet, serta base URL yang dikonfigurasi.
- Jika modul test tidak bisa diimpor, pastikan nilai `test_case` di Excel sesuai dengan path modul tanpa ekstensi `.py`.

## Catatan

Repositori ini saat ini menggunakan API Restful Booker sebagai target service untuk validasi smoke dan skenario booking.
