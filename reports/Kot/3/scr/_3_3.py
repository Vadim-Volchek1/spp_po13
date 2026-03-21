from abc import ABC, abstractmethod


class ATM:
    def __init__(self, atm_id: str, initial_balance: float):
        self.atm_id = atm_id
        self.total_cash = initial_balance
        self._state = None
        self._authenticated_user = None

        # Initialize with Idle state
        self.change_state(IdleState())
        print(
            f"[ATM:{self.atm_id}] System started. Balance: ${initial_balance:.2f}. State: IDLE"
        )

    def change_state(self, new_state):
        self._state = new_state
        self._state.set_atm(self)
        print(
            f"[ATM:{self.atm_id}] -> State changed to: {new_state.__class__.__name__}"
        )

    def insert_card(self):
        self._state.insert_card()

    def enter_pin(self, pin):
        self._state.enter_pin(pin)

    def withdraw(self, amount):
        self._state.withdraw(amount)

    def end_session(self):
        self._state.end_session()

    # Getters and setters for context data
    def get_cash(self):
        return self.total_cash

    def set_cash(self, amount):
        self.total_cash = amount
        print(f"[ATM:{self.atm_id}] Cash balance updated: ${self.total_cash:.2f}")

    def is_cash_available(self, amount):
        return self.total_cash >= amount

    def authenticate_user(self, pin):
        # Dummy authentication: any PIN except 0000 is valid
        if pin == "0000":
            print("[AUTH] Invalid PIN code.")
            return False
        self._authenticated_user = "Customer"
        print("[AUTH] User authenticated successfully.")
        return True

    def clear_auth(self):
        self._authenticated_user = None
        print("[AUTH] User logged out.")


# Абстрактное состояние
class State(ABC):
    def __init__(self):
        self._atm = None

    def set_atm(self, atm):
        self._atm = atm

    @abstractmethod
    def insert_card(self):
        pass

    @abstractmethod
    def enter_pin(self, pin):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def end_session(self):
        pass


# Конкретные состояния
class IdleState(State):
    def insert_card(self):
        print("[ACTION] Card inserted. Please enter PIN.")
        self._atm.change_state(AuthenticatingState())

    def enter_pin(self, pin):
        print("[ERROR] No card inserted. Please insert card first.")

    def withdraw(self, amount):
        print("[ERROR] No session active. Please insert card.")

    def end_session(self):
        print("[INFO] No active session to end.")


class AuthenticatingState(State):
    def insert_card(self):
        print("[WARN] Card already detected. Please enter PIN.")

    def enter_pin(self, pin):
        if self._atm.authenticate_user(pin):
            print("[ACTION] Authentication successful. Select operation.")
            self._atm.change_state(OperationState())
        else:
            print("[ERROR] Authentication failed. Ejecting card.")
            self._atm.change_state(IdleState())

    def withdraw(self, amount):
        print("[ERROR] Please complete authentication first.")

    def end_session(self):
        print("[INFO] Session cancelled by user. Ejecting card.")
        self._atm.change_state(IdleState())


class OperationState(State):
    def insert_card(self):
        print("[INFO] Card already in session.")

    def enter_pin(self, pin):
        print("[INFO] Already authenticated.")

    def withdraw(self, amount):
        if amount <= 0:
            print("[ERROR] Invalid amount.")
            return

        if not self._atm.is_cash_available(amount):
            print(
                f"[ERROR] Insufficient funds in ATM. Available: ${self._atm.get_cash():.2f}"
            )
            print("[BLOCK] ATM is out of cash. Entering BLOCKED mode.")
            self._atm.change_state(BlockedState())
            return

        print(f"[TRANSACTION] Dispensing ${amount:.2f}...")
        self._atm.set_cash(self._atm.get_cash() - amount)
        print(
            f"[SUCCESS] Please take your cash. Remaining balance in ATM: ${self._atm.get_cash():.2f}"
        )
        self.end_session()

    def end_session(self):
        print("[SESSION] Ending session. Thank you for using our ATM.")
        self._atm.clear_auth()
        self._atm.change_state(IdleState())


class BlockedState(State):
    def insert_card(self):
        print("[BLOCKED] ATM is out of service. Please contact support.")

    def enter_pin(self, pin):
        print("[BLOCKED] Operation unavailable.")

    def withdraw(self, amount):
        print("[BLOCKED] No cash available.")

    def end_session(self):
        print("[BLOCKED] Forced session end.")
        self._atm.change_state(IdleState())


# Клиентский код
if __name__ == "__main__":
    test_atm_id = "ATM-001"
    test_atm = ATM(test_atm_id, 500.00)

    print("\n=== Scenario 1: Normal operation ===")
    test_atm.insert_card()
    test_atm.enter_pin("1234")
    test_atm.withdraw(200.00)

    print("\n=== Scenario 2: Wrong PIN ===")
    test_atm.insert_card()
    test_atm.enter_pin("0000")

    print("\n=== Scenario 3: Withdraw more than available (trigger BLOCKED) ===")
    test_atm.insert_card()
    test_atm.enter_pin("1111")
    test_atm.withdraw(600.00)

    print("\n=== Scenario 4: Try to use blocked ATM ===")
    test_atm.insert_card()
