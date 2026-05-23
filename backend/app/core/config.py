from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "Plataforma Integral de Gestión Gastronómica"
    version: str = "0.1.0"

    # Configuración de base de datos (hardcodeada)
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "$FrankO80365"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "gestion_gastronomica"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()
