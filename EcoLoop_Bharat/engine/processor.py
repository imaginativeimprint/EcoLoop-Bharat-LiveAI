"""
EcoLoop Bharat Core Processing Engine
Pathway-powered real-time circular economy tracking
"""
import pathway as pw
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import json
import hashlib
from schema import ProductStream, RecoveryStream, AlertStream, MaterialCategory

class EcoLoopProcessor:
    """
    Main processing engine using Pathway's Rust-powered streaming
    """
    def __init__(self):
        self.start_time = datetime.now()
        self.leakage_threshold_hours = 48  # CPCB standard
        self.recovery_target_percentage = 0.75  # Swachh Bharat target
        
    def setup_streams(self):
        """Initialize data streams from multiple sources"""
        
        # 1. Production Stream (Simulating IoT/ERP integration)
        self.production_stream = pw.io.csv.read(
            "data/factory_output.csv",
            schema=ProductStream,
            mode="streaming",
            csv_settings=pw.io.CsvParserSettings(
                delimiter=",",
                quote_char='"',
                double_quote=True,
                escape_char="\\"
            )
        )
        
        # 2. Recovery Stream (Simulating QR scan data from recycling centers)
        self.recovery_stream = pw.io.csv.read(
            "data/return_logs.csv",
            schema=RecoveryStream,
            mode="streaming",
            csv_settings=pw.io.CsvParserSettings(
                delimiter=",",
                quote_char='"'
            )
        )
        
        # 3. Real-time Kafka Stream (For live demo)
        try:
            self.kafka_stream = pw.io.kafka.read(
                rdkafka_settings={
                    "bootstrap.servers": "localhost:9092",
                    "group.id": "ecoloop-processor",
                    "auto.offset.reset": "latest"
                },
                topic="waste-stream",
                schema=ProductStream,
                format="json"
            )
            print("✅ Connected to Kafka stream")
        except:
            print("⚠️ Kafka not available, using CSV streams only")
        
        return self

    def create_circular_ledger(self):
        """
        Real-time join of production vs recovery
        This is Pathway's magic - sub-second joins at scale
        """
        # Left join to find unmatched products (potential leakage)
        self.circular_ledger = self.production_stream.join_left(
            self.recovery_stream,
            pw.left.product_id == pw.right.product_id
        ).select(
            # Product Information
            product_id=pw.left.product_id,
            material_type=pw.left.material_type,
            material_category=pw.left.material_category,
            manufacturer=pw.left.manufacturer_name,
            weight_kg=pw.left.weight_kg,
            
            # Recovery Information (null if not recovered)
            recovered=pw.if_else(
                pw.right.product_id.is_not_none(),
                True,
                False
            ),
            recovery_center=pw.right.recovery_center_name,
            recovery_date=pw.right.recovery_date,
            circular_credit=pw.right.circular_credit_amount,
            
            # Time Calculations
            days_since_production=(
                pw.this.timestamp_utc() - pw.left.manufacturing_date
            ) / 86400.0,  # Convert to days
            
            # Leakage Status
            status=pw.if_else(
                pw.right.product_id.is_not_none(),
                "RECOVERED",
                pw.if_else(
                    (pw.this.timestamp_utc() - pw.left.manufacturing_date) > 
                    (self.leakage_threshold_hours * 3600),
                    "LEAKED_CRITICAL",
                    "IN_TRANSIT"
                )
            ),
            
            # Environmental Impact
            carbon_saved=pw.if_else(
                pw.right.product_id.is_not_none(),
                pw.left.carbon_footprint * 0.7,  # 70% carbon saving through recycling
                0.0
            )
        )
        
        return self

    def detect_leakage_patterns(self):
        """
        Advanced anomaly detection for waste leakage
        Demonstrates Pathway's windowing and pattern matching
        """
        
        # Time-windowed analysis (7-day rolling window)
        window_size = timedelta(days=7)
        
        # Calculate recovery rates by region
        regional_recovery = self.recovery_stream.windowby(
            pw.this.recovery_date,
            window=window_size
        ).reduce(
            region=pw.this.recovery_center_id,
            recovery_count=pw.reducers.count(),
            total_weight=pw.reducers.sum(pw.this.weight_recovered),
            avg_credit=pw.reducers.avg(pw.this.circular_credit_amount)
        )
        
        # Identify leakage hotspots (products >48hrs unrecovered)
        self.critical_leaks = self.circular_ledger.filter(
            (pw.this.status == "LEAKED_CRITICAL")
        ).select(
            alert_id=pw.this.uuid(),
            alert_type="WASTE_LEAKAGE",
            severity="critical",
            product_id=pw.this.product_id,
            material_type=pw.this.material_type,
            description="Product exceeds 48hr recovery window",
            days_in_transit=pw.this.days_since_production,
            recommended_action="Immediate trace & recovery",
            timestamp=pw.this.timestamp_utc(),
            location="Unknown"
        )
        
        return self

    def calculate_epr_compliance(self):
        """
        Extended Producer Responsibility (EPR) compliance
        Auto-generate reports for CPCB
        """
        
        # Group by manufacturer for compliance tracking
        manufacturer_compliance = self.circular_ledger.groupby(
            pw.this.manufacturer
        ).reduce(
            manufacturer=pw.this.manufacturer,
            total_products=pw.reducers.count(),
            recovered_products=pw.reducers.sum(pw.this.recovered.cast(int)),
            recovery_rate=(
                pw.reducers.sum(pw.this.recovered.cast(int)) / 
                pw.reducers.count() * 100
            ),
            total_carbon_saved=pw.reducers.sum(pw.this.carbon_saved)
        )
        
        # Flag non-compliant manufacturers
        self.compliance_alerts = manufacturer_compliance.filter(
            pw.this.recovery_rate < (self.recovery_target_percentage * 100)
        ).select(
            alert_id=pw.this.uuid(),
            alert_type="EPR_NON_COMPLIANCE",
            severity="high",
            product_id="N/A",
            material_type="ALL",
            description=(
                "Manufacturer below " +
                f"{self.recovery_target_percentage*100}% recovery target"
            ),
            days_in_transit=0.0,
            recommended_action="Immediate compliance review",
            timestamp=pw.this.timestamp_utc(),
            location=pw.this.manufacturer
        )
        
        return self

    def predict_future_leakage(self):
        """
        ML-powered leakage prediction
        Integrated directly into Pathway stream
        """
        
        # Create features for ML model
        features = self.production_stream.select(
            product_id=pw.this.product_id,
            weight_kg=pw.this.weight_kg,
            recyclable_percentage=pw.this.recyclable_percentage,
            material_category=pw.this.material_category,
            # Time-based features
            hour_of_day=pw.this.hour(pw.this.manufacturing_date),
            day_of_week=pw.this.day_of_week(pw.this.manufacturing_date)
        )
        
        # In real implementation, you'd load a pre-trained XGBoost model
        # and apply it to the stream. For MVP, we'll simulate predictions
        self.leakage_predictions = features.select(
            product_id=pw.this.product_id,
            leakage_probability=0.3,  # Simulated prediction
            risk_level=pw.if_else(
                0.3 > 0.7,
                "HIGH",
                pw.if_else(0.3 > 0.4, "MEDIUM", "LOW")
            )
        )
        
        return self

    def run_pipeline(self):
        """
        Execute the complete Pathway pipeline
        """
        print("🚀 Starting EcoLoop Bharat Processing Engine...")
        print(f"📊 Leakage threshold: {self.leakage_threshold_hours} hours")
        print(f"🎯 Recovery target: {self.recovery_target_percentage*100}%")
        
        # Chain all processing steps
        (self.setup_streams()
         .create_circular_ledger()
         .detect_leakage_patterns()
         .calculate_epr_compliance()
         .predict_future_leakage())
        
        # Output streams for dashboard
        pw.io.csv.write(
            self.circular_ledger,
            "data/live/live_inventory.csv"
        )
        
        pw.io.csv.write(
            self.critical_leaks,
            "data/live/critical_leaks.csv"
        )
        
        pw.io.csv.write(
            self.compliance_alerts,
            "data/live/compliance_alerts.csv"
        )
        
        # JSON output for real-time dashboard
        pw.io.jsonlines.write(
            self.circular_ledger,
            "data/live/streaming_output.jsonl"
        )
        
        # WebSocket output for live updates
        pw.io.websocket.connect(
            self.circular_ledger,
            host="0.0.0.0",
            port=8765,
            route="/ws/updates"
        )
        
        print("✅ Pipeline configured. Running Pathway engine...")
        
        # Run the engine (this blocks)
        pw.run(monitoring_level=pw.MonitoringLevel.ALL)
        
        return self

# Entry point
if __name__ == "__main__":
    processor = EcoLoopProcessor()
    processor.run_pipeline()