from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI-Based Road Accident Risk Prediction"
    app_env: str = "development"
    weather_timeout_seconds: float = 8.0
    geocoding_timeout_seconds: float = 8.0
    nominatim_user_agent: str = "ai-road-risk-college-project/1.0 (educational prototype)"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
