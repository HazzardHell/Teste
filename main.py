from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

# Configuration (Using env variables with defaults)
DEFAULT_COVERAGE_PERCENTAGE = float(os.getenv("COVERAGE_PERCENTAGE", 1.0))  # 100%
GIS_ADJUSTMENT = float(os.getenv("GIS_ADJUSTMENT", 0.0))  # Default 0% adjustment

# Domain Models
class CarDetails(BaseModel):
    make: str
    model: str
    year: int
    value: float
    deductible_percentage: float
    broker_fee: float
    registration_location: Optional[str] = None

class InsuranceResult(BaseModel):
    applied_rate: float
    policy_limit: float
    calculated_premium: float
    deductible_value: float

# Calculation Service
def calculate_insurance(car: CarDetails) -> InsuranceResult:
    # Calculate rate based on age and value
    age_based_rate = (2024 - car.year) * 0.005
    value_based_rate = (car.value // 10000) * 0.005
    
    applied_rate = age_based_rate + value_based_rate + GIS_ADJUSTMENT
    
    base_premium = car.value * applied_rate
    deductible_value = base_premium * car.deductible_percentage
    final_premium = base_premium - deductible_value + car.broker_fee
    
    base_policy_limit = car.value * DEFAULT_COVERAGE_PERCENTAGE
    deductible_value = base_policy_limit * car.deductible_percentage
    final_policy_limit = base_policy_limit - deductible_value
    
    return InsuranceResult(
        applied_rate=applied_rate,
        policy_limit=final_policy_limit,
        calculated_premium=final_premium,
        deductible_value=deductible_value
    )

@app.post("/calculate-premium", response_model=InsuranceResult)
def get_premium(car: CarDetails):
    return calculate_insurance(car)