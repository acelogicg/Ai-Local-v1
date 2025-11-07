@echo off
echo Mengaktifkan environment conda: deepseek...
CALL C:\ProgramData\Miniconda3\Scripts\activate.bat deepseek

echo Menginstal dependensi...
pip install -r requirements.txt

echo Menjalankan aplikasi...
python main.py

pause
