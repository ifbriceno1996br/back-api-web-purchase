from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"

    # Database Configuration
    SQL_SERVER: str = "MSI\\SQLEXPRESS"
    SQL_DATABASE: str = "WebApiPurchase"
    SQLALCHEMY_DATABASE_URI: str = f"mssql+pyodbc://{SQL_SERVER}/{SQL_DATABASE}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = 'WebApiPurchase'
    VERSION: str = '1.0.0'
    DESCRIPTION: str = "Web API for Purchase"

settings = Settings()
