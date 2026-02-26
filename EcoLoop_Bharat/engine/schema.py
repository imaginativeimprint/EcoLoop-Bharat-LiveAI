"""
Digital Twin Schemas for EcoLoop Bharat
Defines the data structures for tracking India's circular economy
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict
import pathway as pw
import enum

class MaterialCategory(enum.Enum):
    """Indian waste classification as per CPCB guidelines"""
    PLASTIC = "plastic"
    E_WASTE = "e_waste"
    METAL = "metal"
    PAPER = "paper"
    GLASS = "glass"
    ORGANIC = "organic"
    HAZARDOUS = "hazardous"

class WasteSource(enum.Enum):
    """Source of waste generation"""
    MANUFACTURING = "manufacturing"
    POST_CONSUMER = "post_consumer"
    INDUSTRIAL = "industrial"
    ELECTRONIC = "electronic"
    PACKAGING = "packaging"

# Pathway Schema for Real-time Stream Processing
class ProductStream(pw.Schema):
    """Digital Twin schema for manufactured products"""
    product_id: str
    batch_number: str
    manufacturer_id: str
    manufacturer_name: str
    material_type: str
    material_category: str
    weight_kg: float
    carbon_footprint: float
    recyclable_percentage: float
    gst_hsn_code: str
    manufacturing_date: float  # timestamp
    expiry_date: Optional[float]
    qr_code_hash: str
    gps_lat: float
    gps_lon: float
    source: str

class RecoveryStream(pw.Schema):
    """Digital Twin schema for waste recovery/returns"""
    recovery_id: str
    product_id: str
    recovery_center_id: str
    recovery_center_name: str
    recovery_date: float
    material_type: str
    weight_recovered: float
    condition: str  # excellent, good, damaged, end_of_life
    recycling_method: str
    recovered_by: str
    circular_credit_amount: float
    gps_lat: float
    gps_lon: float
    verification_hash: str

class AlertStream(pw.Schema):
    """Real-time alert schema"""
    alert_id: str
    alert_type: str  # leakage, delay, violation, opportunity
    severity: str  # low, medium, high, critical
    product_id: str
    material_type: str
    description: str
    days_in_transit: float
    recommended_action: str
    timestamp: float
    location: str