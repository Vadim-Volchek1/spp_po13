from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class PrescriptionType(Enum):
    """Type of prescription."""

    PROCEDURE = "procedure"
    MEDICINE = "medicine"
    OPERATION = "operation"


class DischargeReason(Enum):
    """Reason for discharge."""

    RECOVERED = "treatment completed"
    REGIME_VIOLATION = "regime violation"
    OTHER = "other circumstances"


class PrescriptionExecutor(ABC):
    """Interface: someone who can execute a prescription (Doctor or Nurse)."""

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def execute_prescription(self, prescription: Prescription) -> str:
        pass


class Prescription:
    """Prescription: procedures, medicines, operations."""

    def __init__(self, prescription_type: PrescriptionType, description: str, patient: Patient, prescribed_by: Doctor):
        self.type = prescription_type
        self.description = description
        self.patient = patient
        self.prescribed_by = prescribed_by
        self._executed_by: Optional[PrescriptionExecutor] = None
        self._executed = False

    def assign_executor(self, executor: PrescriptionExecutor) -> None:
        self._executed_by = executor

    def perform(self) -> str:
        if self._executed:
            return "Prescription already executed."
        if not self._executed_by:
            return "No executor assigned."
        msg = self._executed_by.execute_prescription(self)
        self._executed = True
        return msg

    def __str__(self) -> str:
        status = "executed" if self._executed else "not executed"
        return f"{self.type.value}: {self.description} ({status})"


class Doctor(PrescriptionExecutor):
    """Doctor: prescribes for patient and can execute prescriptions (or another doctor/nurse)."""

    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty

    def get_title(self) -> str:
        return f"Doctor {self.name} ({self.specialty})"

    def make_prescription(self, patient: Patient, ptype: PrescriptionType, description: str) -> Prescription:
        return Prescription(ptype, description, patient, self)

    def execute_prescription(self, prescription: Prescription) -> str:
        return f"{self.get_title()} executed: {prescription.description}"

    def __str__(self) -> str:
        return self.get_title()


class Nurse(PrescriptionExecutor):
    """Nurse: executes prescriptions (procedures, medicines)."""

    def __init__(self, name: str):
        self.name = name

    def get_title(self) -> str:
        return f"Nurse {self.name}"

    def execute_prescription(self, prescription: Prescription) -> str:
        return f"{self.get_title()} executed: {prescription.description}"

    def __str__(self) -> str:
        return self.get_title()


class Patient:
    """Patient: has attending doctor, list of prescriptions, can be discharged."""

    def __init__(self, name: str, attending_doctor: Optional[Doctor] = None):
        self.name = name
        self.attending_doctor = attending_doctor
        self.prescriptions: list[Prescription] = []
        self._discharged = False
        self._discharge_reason: Optional[DischargeReason] = None

    def set_attending_doctor(self, doctor: Doctor) -> None:
        self.attending_doctor = doctor

    def add_prescription(self, prescription: Prescription) -> None:
        self.prescriptions.append(prescription)

    def discharge(self, reason: DischargeReason) -> None:
        self._discharged = True
        self._discharge_reason = reason

    @property
    def is_discharged(self) -> bool:
        return self._discharged

    @property
    def discharge_reason(self) -> Optional[DischargeReason]:
        return self._discharge_reason

    def __str__(self) -> str:
        status = "discharged" if self._discharged else "in treatment"
        reason = f" ({self._discharge_reason.value})" if self._discharge_reason else ""
        doc = self.attending_doctor.name if self.attending_doctor else "not assigned"
        return f"Patient {self.name}, attending doctor: {doc}, status: {status}{reason}"


class Hospital:
    """Hospital: collection of patients, doctors and nurses."""

    def __init__(self, name: str):
        self.name = name
        self._patients: list[Patient] = []
        self._doctors: list[Doctor] = []
        self._nurses: list[Nurse] = []

    def add_patient(self, patient: Patient) -> None:
        if patient not in self._patients:
            self._patients.append(patient)

    def add_doctor(self, doctor: Doctor) -> None:
        if doctor not in self._doctors:
            self._doctors.append(doctor)

    def add_nurse(self, nurse: Nurse) -> None:
        if nurse not in self._nurses:
            self._nurses.append(nurse)

    def discharge_patient(self, patient: Patient, reason: DischargeReason) -> None:
        patient.discharge(reason)

    def get_patients(self) -> list[Patient]:
        return self._patients.copy()

    def get_doctors(self) -> list[Doctor]:
        return self._doctors.copy()

    def get_nurses(self) -> list[Nurse]:
        return self._nurses.copy()

    def __str__(self) -> str:
        return (
            f"Hospital «{self.name}»: "
            f"{len(self._patients)} patients, "
            f"{len(self._doctors)} doctors, "
            f"{len(self._nurses)} nurses."
        )


def main() -> None:
    """Demonstration of the Hospital system."""
    print("=== Hospital System ===\n")
    hospital = Hospital("City Hospital No. 1")
    doctor1 = Doctor("Ivanova", "therapist")
    doctor2 = Doctor("Petrov", "surgeon")
    nurse = Nurse("Sidorova")
    hospital.add_doctor(doctor1)
    hospital.add_doctor(doctor2)
    hospital.add_nurse(nurse)
    patient = Patient("Kozlov")
    patient.set_attending_doctor(doctor1)
    hospital.add_patient(patient)
    print(hospital)
    print(patient)
    print()
    p1 = doctor1.make_prescription(patient, PrescriptionType.PROCEDURE, "Physiotherapy")
    p2 = doctor1.make_prescription(patient, PrescriptionType.MEDICINE, "Antibiotic 7 days")
    p3 = doctor2.make_prescription(patient, PrescriptionType.OPERATION, "Appendectomy")

    patient.add_prescription(p1)
    patient.add_prescription(p2)
    patient.add_prescription(p3)

    print("Prescriptions:")
    for pr in patient.prescriptions:
        print(f"  - {pr}")
    print()

    p1.assign_executor(nurse)
    p2.assign_executor(nurse)
    p3.assign_executor(doctor2)

    print("Executing prescriptions:")
    print(f"  {p1.perform()}")
    print(f"  {p2.perform()}")
    print(f"  {p3.perform()}")
    print()
    print(p1.perform())
    print()
    hospital.discharge_patient(patient, DischargeReason.RECOVERED)
    print(patient)
    print()
    patient2 = Patient("Novikov", doctor1)
    hospital.add_patient(patient2)
    hospital.discharge_patient(patient2, DischargeReason.REGIME_VIOLATION)
    print(patient2)


if __name__ == "__main__":
    main()
