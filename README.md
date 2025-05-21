Cài Python, làm sao chạy được lệnh python và pip (thường sẽ phải add path/variable bằng tay)

Cài đặt các thư viện: pip install -r requirements.txt
Chạy ứng dụng: uvicorn app.main:app --reload
Truy cập http://127.0.0.1:8000/docs để xem API documentation và thử nghiệm. Bạn sẽ thấy các endpoints cho /api/v1/items/.