class Hospital:
    def __init__(self, title):
        self.title = title
        self.doctors = []
        self.patients = []

    def manage(self):
        print(f"--- Работа больницы '{self.title}' ---")


class MedicalStaff:
    def __init__(self, name):
        self.name = name

class Doctor(MedicalStaff):

    def __init__(self, name, specializacia):
        super().__init__(name)
        self.specializacia = specializacia

    def creatNaznachenie(self, pacient, typeNazn, nameNazn):
        print(f"Врач {self.name} назначил {typeNazn}: {nameNazn} для {pacient.name}")
        pacient.addPrescription(typeNazn, nameNazn)

    def doOperation(self, pacient):
        if "operation" in pacient.prescriptions and pacient.prescriptions["operation"]:
            opName = pacient.prescriptions["operation"].pop(0)
            print(f"Врач {self.name} проводит операцию: {opName} пациенту {pacient.name}")
        else:
            print(f"У пациента {pacient.name} нет назначенных операций.")

class Pacient:
    def __init__(self, name):
        self.name = name
        self.prescriptions = {"procedur": [], "lekcarstvo": [], "operation": []}
        self.isDischarged = False
        self.lechaushiyVarch = None

    def addPrescription(self, category, name):
        if category in self.prescriptions:
            self.prescriptions[category].append(name)

    def setDoctor(self, doctor):
        self.lechaushiyVarch = doctor
        print(f"Пациенту {self.name} назначен лечащий врач: {doctor.name}")

    def discharge(self, reason):
        self.isDischarged = True
        print(f"Пациент {self.name} выписан. Причина: {reason}")

class Medsister(MedicalStaff):
    def giveLeckarstvo(self, pacient):
        if "lekcarstvo" in pacient.prescriptions and pacient.prescriptions["lekcarstvo"]:
            med = pacient.prescriptions["lekcarstvo"].pop(0)
            print(f"Медсестра {self.name} выдала лекарство {med} пациенту {pacient.name}")
        else:
            print(f"Для пациента {pacient.name} нет лекарств.")

    def doProcedur(self, pacient):
        if "procedur" in pacient.prescriptions and pacient.prescriptions["procedur"]:
            proc = pacient.prescriptions["procedur"].pop(0)
            print(f"Медсестра {self.name} выполнила процедуру {proc} пациенту {pacient.name}")
        else:
            print(f"Для пациента {pacient.name} нет процедур.")

# Создаем персонал
doctor1 = Doctor("Фолитарик", "Хирург")
medSister1 = Medsister("Яна")

# Создаем пациента
pacient1 = Pacient("Шрамук")

# Назначаем лечащего врача (Ассоциация)
pacient1.setDoctor(doctor1)

# Врач делает назначения
doctor1.creatNaznachenie(pacient1, "lekcarstvo", "Аспирин")
doctor1.creatNaznachenie(pacient1, "procedur", "Прогревание")
doctor1.creatNaznachenie(pacient1, "operation", "Удаление аппендицита")

print("*" * 30)

# Медсестра выполняет назначения
medSister1.giveLeckarstvo(pacient1)
medSister1.doProcedur(pacient1)

# Врач выполняет операцию
doctor1.doOperation(pacient1)

# Выписка пациента
print("*" * 30)
pacient1.discharge("Завершение лечения")
