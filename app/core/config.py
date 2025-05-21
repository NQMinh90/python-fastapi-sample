from typing import Optional, Dict, Any, Union, List # Thêm Union và List
from pydantic_settings import BaseSettings
from pydantic import EmailStr, AnyHttpUrl, model_validator, PostgresDsn # Thêm model_validator và PostgresDsn (nếu bạn có kế hoạch dùng)

class Settings(BaseSettings):
    PROJECT_NAME: str = "3-Tier FastAPI Project"
    API_V1_STR: str = "/api/v1"

    APP_ENV: str = "Development"
    DEV_TENANT_CODE: Optional[str] = None # Sẽ đọc từ .env nếu APP_ENV là Development

    # Biến cho CORS
    SERVER_NAME: str = "localhost"
    SERVER_HOST: str = "http://localhost"

    # BACKEND_CORS_ORIGINS có thể là một list các string hoặc một string được phân tách bằng dấu phẩy
    BACKEND_CORS_ORIGINS: Union[List[AnyHttpUrl], str] = []

    # Central Database URL (đã đổi tên từ SQLALCHEMY_DATABASE_URL)
    CENTRAL_DATABASE_URL: str = ""
    # Logging Database URL
    LOGGING_DATABASE_URL: str = ""

    # First Superuser
    FIRST_SUPERUSER_EMAIL: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethispassword"

    # JWT Settings
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE_CHANGE_ME" # << RẤT QUAN TRỌNG: Thay đổi key này!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days

    # Ví dụ nếu bạn muốn hỗ trợ cả PostgreSQL cho một số trường hợp
    # POSTGRES_SERVER: Optional[str] = None
    # POSTGRES_USER: Optional[str] = None
    # POSTGRES_PASSWORD: Optional[str] = None
    # POSTGRES_DB: Optional[str] = None
    # ASSEMBLED_POSTGRES_URL: Optional[PostgresDsn] = None

    @model_validator(mode="after")
    def assemble_settings(self) -> "Settings":
        # Xây dựng BACKEND_CORS_ORIGINS nếu nó là list rỗng và SERVER_NAME/SERVER_HOST có giá trị
        if isinstance(self.BACKEND_CORS_ORIGINS, list) and not self.BACKEND_CORS_ORIGINS:
            if self.SERVER_NAME and self.SERVER_HOST:
                origins = [
                    f"http://{self.SERVER_NAME}",
                    f"https://{self.SERVER_NAME}",
                    self.SERVER_HOST, # Thường là http://localhost hoặc https://yourdomain.com
                    # Thêm các port phổ biến nếu cần cho môi trường dev
                    f"http://{self.SERVER_NAME}:3000", # Ví dụ React dev
                    f"http://{self.SERVER_NAME}:8080", # Ví dụ Vue dev
                    f"http://localhost:3000", # Cho dev local
                    f"http://localhost:8080", # Cho dev local
                ]
                # Loại bỏ các giá trị None hoặc rỗng và các giá trị trùng lặp
                self.BACKEND_CORS_ORIGINS = [str(origin) for origin in set(filter(None, origins))]
        elif isinstance(self.BACKEND_CORS_ORIGINS, str) and self.BACKEND_CORS_ORIGINS:
            # Nếu là string, tách thành list
            self.BACKEND_CORS_ORIGINS = [s.strip() for s in self.BACKEND_CORS_ORIGINS.split(",")]

        # Kiểm tra các URL database bắt buộc
        if not self.CENTRAL_DATABASE_URL:
            raise ValueError("CENTRAL_DATABASE_URL must be set in the environment variables.")
        if not self.LOGGING_DATABASE_URL:
            raise ValueError("LOGGING_DATABASE_URL must be set in the environment variables.")

        # Ví dụ logic để build URL PostgreSQL nếu các thành phần được cung cấp
        # if self.POSTGRES_USER and self.POSTGRES_PASSWORD and self.POSTGRES_SERVER and self.POSTGRES_DB:
        #     self.ASSEMBLED_POSTGRES_URL = PostgresDsn.build(
        #         scheme="postgresql", username=self.POSTGRES_USER, password=self.POSTGRES_PASSWORD, host=self.POSTGRES_SERVER, path=f"/{self.POSTGRES_DB}"
        #     )
        return self

    class Config:
        case_sensitive = True
        env_file = ".env" # Tải biến môi trường từ file .env

settings = Settings()