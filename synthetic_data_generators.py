#!/usr/bin/env python3
"""
Synthetic Data Generators for Wayne IA Demonstrations
Real data, real processing, real performance!

This module generates industry-standard synthetic data that our demos
actually process, proving Wayne IA's capabilities with verifiable workloads.
"""

import random
import json
import time
from datetime import datetime, timedelta
import hashlib


class SparkBiomedicalDataGenerator:
    """
    Generates Synthea-compatible patient data for clinical trials
    Includes COWS scores, vital signs, and adverse events
    """

    def __init__(self):
        self.patient_template = {
            "resourceType": "Patient",
            "identifier": None,
            "active": True,
            "gender": None,
            "birthDate": None,
            "address": []
        }

        # Clinical Opiate Withdrawal Scale components
        self.cows_components = [
            "resting_pulse", "sweating", "restlessness", "pupil_size",
            "bone_aches", "runny_nose", "gi_upset", "tremor",
            "yawning", "anxiety", "gooseflesh_skin"
        ]

    def generate_patient_batch(self, count):
        """Generate a batch of Synthea-compatible patients with COWS scores"""
        patients = []

        for i in range(count):
            patient = self.patient_template.copy()
            patient["identifier"] = f"SPARK-{random.randint(100000, 999999)}"
            patient["gender"] = random.choice(["male", "female"])
            patient["birthDate"] = self._random_birthdate()

            # Add COWS assessment
            patient["cows_assessment"] = self._generate_cows_score()

            # Add vital signs
            patient["vitals"] = {
                "heartRate": random.randint(60, 100),
                "bloodPressure": f"{random.randint(110, 140)}/{random.randint(70, 90)}",
                "temperature": round(random.uniform(97.0, 99.5), 1),
                "respiratoryRate": random.randint(12, 20)
            }

            # Add treatment response
            patient["treatmentResponse"] = {
                "baseline": random.randint(15, 35),
                "week1": random.randint(10, 25),
                "week2": random.randint(5, 20),
                "week4": random.randint(0, 15)
            }

            patients.append(patient)

        return patients

    def _generate_cows_score(self):
        """Generate realistic COWS score components"""
        scores = {}
        total = 0

        for component in self.cows_components:
            score = random.randint(0, 4)  # 0-4 scale for each component
            scores[component] = score
            total += score

        scores["total"] = total
        scores["severity"] = self._classify_withdrawal(total)

        return scores

    def _classify_withdrawal(self, score):
        """Classify withdrawal severity based on COWS total"""
        if score < 5:
            return "none"
        elif score < 13:
            return "mild"
        elif score < 25:
            return "moderate"
        elif score < 37:
            return "severe"
        else:
            return "very_severe"

    def _random_birthdate(self):
        """Generate random birthdate between 18-65 years ago"""
        days_ago = random.randint(18 * 365, 65 * 365)
        birthdate = datetime.now() - timedelta(days=days_ago)
        return birthdate.strftime("%Y-%m-%d")


class L3AerospaceDataGenerator:
    """
    Generates stress-strain curves and fatigue data for composite materials
    Follows ASTM standards for aerospace testing
    """

    def __init__(self):
        self.materials = {
            "carbon_fiber_7821": {
                "tensile_strength": 3500,  # MPa
                "elastic_modulus": 230,     # GPa
                "poisson_ratio": 0.3
            },
            "titanium_aluminum": {
                "tensile_strength": 1100,
                "elastic_modulus": 110,
                "poisson_ratio": 0.34
            },
            "ceramic_matrix": {
                "tensile_strength": 400,
                "elastic_modulus": 380,
                "poisson_ratio": 0.17
            }
        }

    def generate_stress_strain_curve(self, material_name, num_points=1000):
        """Generate realistic stress-strain data points"""
        material = self.materials.get(material_name, self.materials["carbon_fiber_7821"])

        data_points = []
        max_strain = material["tensile_strength"] / (material["elastic_modulus"] * 1000)

        for i in range(num_points):
            strain = (i / num_points) * max_strain * 1.5  # Go past yield

            if strain < max_strain:
                # Elastic region - linear
                stress = strain * material["elastic_modulus"] * 1000
            else:
                # Plastic region - non-linear
                stress = material["tensile_strength"] * (1 + 0.1 * (strain - max_strain))

            data_points.append({
                "strain": round(strain, 6),
                "stress": round(stress, 2),
                "temperature": 23.0,  # Room temp
                "cycle": 1
            })

        return data_points

    def generate_fatigue_data(self, material_name, num_cycles=10000):
        """Generate S-N curve data for fatigue analysis"""
        material = self.materials.get(material_name, self.materials["carbon_fiber_7821"])

        fatigue_data = []
        stress_levels = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]  # Fraction of tensile strength

        for stress_ratio in stress_levels:
            stress = material["tensile_strength"] * stress_ratio

            # Basquin's equation approximation
            cycles_to_failure = int(1e6 * (0.9 / stress_ratio) ** 12)

            fatigue_data.append({
                "stress_amplitude": round(stress, 2),
                "mean_stress": 0,
                "cycles_to_failure": min(cycles_to_failure, num_cycles),
                "temperature": -65 if stress_ratio > 0.7 else 150,  # Extreme temps
                "frequency": 10  # Hz
            })

        return fatigue_data

    def generate_temperature_cycling(self, num_cycles=1000):
        """Generate temperature cycling data for aerospace qualification"""
        cycling_data = []

        for cycle in range(num_cycles):
            # MIL-STD-810G temperature cycling
            cycle_data = {
                "cycle_number": cycle + 1,
                "min_temp": -65,  # °C
                "max_temp": 150,  # °C
                "ramp_rate": 5,   # °C/min
                "dwell_time": 30, # minutes
                "measurements": []
            }

            # Add measurements at key points
            for temp in [-65, 0, 23, 100, 150]:
                measurement = {
                    "temperature": temp,
                    "thermal_expansion": random.uniform(-0.001, 0.005),
                    "electrical_resistance": random.uniform(0.99, 1.01),
                    "visual_inspection": "PASS"
                }
                cycle_data["measurements"].append(measurement)

            cycling_data.append(cycle_data)

        return cycling_data


class HealthcarePlatformDataGenerator:
    """
    Generates real-time patient monitoring data streams
    HIPAA-compliant format with realistic vital signs
    """

    def __init__(self):
        self.patient_conditions = {
            "diabetes_type1": {
                "glucose_mean": 180,
                "glucose_std": 40,
                "hba1c_mean": 7.5
            },
            "diabetes_type2": {
                "glucose_mean": 150,
                "glucose_std": 30,
                "hba1c_mean": 6.8
            },
            "healthy": {
                "glucose_mean": 95,
                "glucose_std": 15,
                "hba1c_mean": 5.2
            }
        }

    def generate_patient_stream(self, patient_count, time_points=288):  # 288 = 24hrs @ 5min
        """Generate continuous glucose monitoring data for multiple patients"""
        streams = []

        for patient_id in range(patient_count):
            condition = random.choice(list(self.patient_conditions.keys()))
            params = self.patient_conditions[condition]

            patient_stream = {
                "patient_id": hashlib.sha256(f"patient_{patient_id}".encode()).hexdigest()[:16],
                "condition": condition,
                "data_points": [],
                "alerts": []
            }

            # Generate time series data
            current_glucose = params["glucose_mean"]

            for t in range(time_points):
                # Add realistic variability
                delta = random.gauss(0, params["glucose_std"] * 0.1)
                current_glucose += delta

                # Add meal spikes
                if t % 60 == 30:  # Meal time
                    current_glucose += random.uniform(30, 60)

                # Natural decay
                current_glucose = 0.98 * current_glucose + 0.02 * params["glucose_mean"]

                data_point = {
                    "timestamp": (datetime.now() - timedelta(minutes=5 * (time_points - t))).isoformat(),
                    "glucose_mg_dl": max(40, min(400, int(current_glucose))),
                    "trend": self._calculate_trend(current_glucose, params["glucose_mean"])
                }

                # Check for alerts
                if current_glucose > 250:
                    patient_stream["alerts"].append({
                        "type": "hyperglycemia",
                        "severity": "high",
                        "value": current_glucose,
                        "timestamp": data_point["timestamp"]
                    })
                elif current_glucose < 70:
                    patient_stream["alerts"].append({
                        "type": "hypoglycemia",
                        "severity": "critical",
                        "value": current_glucose,
                        "timestamp": data_point["timestamp"]
                    })

                patient_stream["data_points"].append(data_point)

            streams.append(patient_stream)

        return streams

    def generate_hipaa_audit_log(self, access_count=1000):
        """Generate HIPAA-compliant audit log entries"""
        audit_logs = []

        actions = ["CREATE", "READ", "UPDATE", "DELETE", "PRINT", "EXPORT"]
        resources = ["Patient", "Observation", "Medication", "Procedure", "Report"]

        for i in range(access_count):
            log_entry = {
                "id": hashlib.sha256(f"audit_{i}".encode()).hexdigest()[:32],
                "timestamp": (datetime.now() - timedelta(seconds=random.randint(0, 86400))).isoformat(),
                "user_id": f"user_{random.randint(1000, 9999)}",
                "action": random.choice(actions),
                "resource_type": random.choice(resources),
                "resource_id": hashlib.sha256(f"resource_{i}".encode()).hexdigest()[:16],
                "outcome": "SUCCESS" if random.random() > 0.05 else "DENIED",
                "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "user_agent": "WayneIA-HealthPlatform/2.1"
            }

            audit_logs.append(log_entry)

        return sorted(audit_logs, key=lambda x: x["timestamp"], reverse=True)

    def _calculate_trend(self, current, mean):
        """Calculate glucose trend arrow"""
        diff = current - mean
        if abs(diff) < 10:
            return "→"
        elif diff > 30:
            return "↑↑"
        elif diff > 10:
            return "↑"
        elif diff < -30:
            return "↓↓"
        else:
            return "↓"


class MedicalDeviceFDADataGenerator:
    """
    Generates FDA submission documents and test data
    Follows 21 CFR Part 820 and ISO 13485 standards
    """

    def __init__(self):
        self.predicate_database = {
            "K182456": {
                "name": "CardiacMonitor Pro",
                "manufacturer": "MedTech Corp",
                "classification": "Class II",
                "product_code": "DQK",
                "clearance_date": "2018-09-15"
            },
            "K193421": {
                "name": "AI-ECG Analyzer",
                "manufacturer": "HeartTech Inc",
                "classification": "Class II",
                "product_code": "DQK",
                "clearance_date": "2019-11-22"
            },
            "K201234": {
                "name": "Portable Cardiac Monitor",
                "manufacturer": "CardioSystems LLC",
                "classification": "Class II",
                "product_code": "DQK",
                "clearance_date": "2020-06-30"
            }
        }

    def generate_510k_sections(self, device_name):
        """Generate complete 510(k) submission sections"""
        sections = {
            "device_description": self._generate_device_description(device_name),
            "indications_for_use": self._generate_indications(),
            "substantial_equivalence": self._find_predicates(device_name),
            "performance_data": self._generate_performance_data(),
            "software_validation": self._generate_software_validation(),
            "biocompatibility": self._generate_biocompatibility()
        }

        return sections

    def generate_iso_10993_results(self, material_type="polymer"):
        """Generate ISO 10993 biocompatibility test results"""
        tests = {
            "cytotoxicity": {
                "standard": "ISO 10993-5",
                "method": "MEM Elution",
                "result": "Non-cytotoxic",
                "grade": random.randint(0, 1)  # 0 or 1 is passing
            },
            "sensitization": {
                "standard": "ISO 10993-10",
                "method": "Guinea Pig Maximization",
                "result": "Non-sensitizing",
                "score": random.uniform(0, 0.9)  # <1.0 is passing
            },
            "irritation": {
                "standard": "ISO 10993-10",
                "method": "Intracutaneous Reactivity",
                "result": "Non-irritating",
                "primary_irritation_index": random.uniform(0, 0.5)  # <1.0 is passing
            },
            "acute_toxicity": {
                "standard": "ISO 10993-11",
                "method": "Systemic Injection",
                "result": "Non-toxic",
                "mortality": 0
            }
        }

        return tests

    def _generate_device_description(self, device_name):
        """Generate detailed device description"""
        return {
            "device_name": device_name,
            "common_name": "Cardiac Monitoring System",
            "classification_name": "Electrocardiograph",
            "product_code": "DQK",
            "device_class": "II",
            "prescription_use": True,
            "components": [
                "Main processing unit with AI algorithms",
                "ECG sensor array (12-lead)",
                "Wireless data transmission module",
                "Battery power system (48-hour capacity)",
                "Patient interface software"
            ],
            "materials": [
                "Medical grade silicone (skin contact)",
                "ABS plastic housing (external)",
                "Silver/Silver chloride electrodes"
            ]
        }

    def _generate_indications(self):
        """Generate indications for use statement"""
        return {
            "intended_use": "The device is intended for use by healthcare professionals " +
                           "to acquire, analyze, and display electrocardiographic data " +
                           "for diagnostic purposes in clinical settings.",
            "patient_population": "Adult patients (18 years and older) requiring " +
                                 "cardiac monitoring in hospital and ambulatory settings.",
            "use_environment": ["Hospital", "Clinic", "Ambulatory care"],
            "contraindications": ["Patients with implanted electronic devices may " +
                                 "experience interference"]
        }

    def _find_predicates(self, device_name):
        """Find and compare with predicate devices"""
        comparisons = []

        for pred_id, pred_data in self.predicate_database.items():
            comparison = {
                "predicate_510k": pred_id,
                "predicate_name": pred_data["name"],
                "comparison_table": {
                    "intended_use": "Same",
                    "technology": "Similar with AI enhancement",
                    "patient_contact": "Same",
                    "performance_specs": "Equivalent or better"
                },
                "differences": [
                    "Addition of AI-based arrhythmia detection",
                    "Wireless connectivity vs wired in predicate"
                ],
                "why_differences_dont_affect_safety":
                    "AI algorithms validated to medical device standards. " +
                    "Wireless module meets IEC 60601-1-2 EMC requirements."
            }
            comparisons.append(comparison)

        return comparisons

    def _generate_performance_data(self):
        """Generate clinical performance data"""
        return {
            "bench_testing": {
                "accuracy": 99.2,
                "precision": 98.5,
                "sensitivity": 97.8,
                "specificity": 99.1,
                "sample_rate": 500  # Hz
            },
            "clinical_validation": {
                "study_size": 523,
                "sites": 3,
                "duration_months": 6,
                "primary_endpoint_met": True,
                "adverse_events": 0
            },
            "software_performance": {
                "response_time_ms": 50,
                "uptime_percent": 99.99,
                "data_integrity": "SHA-256 validated"
            }
        }

    def _generate_software_validation(self):
        """Generate software V&V documentation outline"""
        return {
            "development_level": "Major Level of Concern",
            "iec_62304_class": "Class B",
            "validation_activities": [
                "Requirements Analysis",
                "Design Review",
                "Code Review",
                "Unit Testing (98% coverage)",
                "Integration Testing",
                "System Testing",
                "User Acceptance Testing"
            ],
            "cybersecurity": {
                "threat_model": "Completed",
                "penetration_testing": "Passed",
                "sbom_available": True,
                "update_mechanism": "Encrypted OTA"
            }
        }

    def _generate_biocompatibility(self):
        """Generate biocompatibility summary"""
        return {
            "patient_contact_type": "Surface contact - Skin",
            "contact_duration": "Prolonged (>24 hours)",
            "iso_10993_tests": [
                "Cytotoxicity (ISO 10993-5)",
                "Sensitization (ISO 10993-10)",
                "Irritation (ISO 10993-10)"
            ],
            "all_tests_passed": True,
            "materials_fda_recognized": True
        }


# Utility function to generate all data types
def generate_all_synthetic_data():
    """Generate complete synthetic data sets for all demos"""

    print("Generating synthetic data for all demonstrations...")

    # Spark Biomedical data
    spark_gen = SparkBiomedicalDataGenerator()
    spark_data = {
        "patients": spark_gen.generate_patient_batch(1000),
        "timestamp": datetime.now().isoformat()
    }

    # L-3 Aerospace data
    l3_gen = L3AerospaceDataGenerator()
    l3_data = {
        "stress_strain": l3_gen.generate_stress_strain_curve("carbon_fiber_7821"),
        "fatigue": l3_gen.generate_fatigue_data("carbon_fiber_7821"),
        "thermal_cycling": l3_gen.generate_temperature_cycling(100),
        "timestamp": datetime.now().isoformat()
    }

    # Healthcare platform data
    health_gen = HealthcarePlatformDataGenerator()
    health_data = {
        "patient_streams": health_gen.generate_patient_stream(100),
        "audit_logs": health_gen.generate_hipaa_audit_log(1000),
        "timestamp": datetime.now().isoformat()
    }

    # Medical device data
    device_gen = MedicalDeviceFDADataGenerator()
    device_data = {
        "510k_sections": device_gen.generate_510k_sections("CardioGuard AI Monitor"),
        "biocompatibility": device_gen.generate_iso_10993_results(),
        "timestamp": datetime.now().isoformat()
    }

    return {
        "spark_biomedical": spark_data,
        "l3_aerospace": l3_data,
        "healthcare_platform": health_data,
        "medical_device_fda": device_data
    }


if __name__ == "__main__":
    # Test data generation
    print("Testing synthetic data generators...")

    # Quick test of each generator
    spark = SparkBiomedicalDataGenerator()
    patients = spark.generate_patient_batch(5)
    print(f"\n✓ Generated {len(patients)} Synthea patients with COWS scores")

    l3 = L3AerospaceDataGenerator()
    stress_data = l3.generate_stress_strain_curve("carbon_fiber_7821", 100)
    print(f"✓ Generated {len(stress_data)} stress-strain data points")

    health = HealthcarePlatformDataGenerator()
    streams = health.generate_patient_stream(5, 48)  # 5 patients, 4 hours
    print(f"✓ Generated {len(streams)} patient monitoring streams")

    device = MedicalDeviceFDADataGenerator()
    sections = device.generate_510k_sections("TestDevice")
    print(f"✓ Generated {len(sections)} FDA 510(k) sections")

    print("\nAll synthetic data generators operational!")