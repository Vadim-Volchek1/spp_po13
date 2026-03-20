from abc import ABC

class TV(ABC):
    def __init__(self):
        self.power = False [cite: 113]
        self.volume = 10 [cite: 114]
        self.channel = 1 [cite: 114]

    def turn_on(self):
        self.power = True
        print("TV is ON") [cite: 116]

    def turn_off(self):
        self.power = False
        print("TV is OFF") [cite: 118]

    def volume_up(self):
        if self.volume < 100:
            self.volume += 1
            print(f"Volume: {self.volume}") [cite: 122]

    def volume_down(self):
        if self.volume > 0:
            self.volume -= 1
            print(f"Volume: {self.volume}") [cite: 126]

    def channel_up(self):
        self.channel += 1
        if self.channel > 999:
            self.channel = 1
        print(f"Channel: {self.channel}") [cite: 131]

    def channel_down(self):
        self.channel -= 1
        if self.channel < 1:
            self.channel = 999
        print(f"Channel: {self.channel}") [cite: 136]

class SonyTV(TV):
    def __init__(self):
        super().__init__()
        print("Sony TV created") [cite: 140]

class SamsungTV(TV):
    def __init__(self):
        super().__init__()
        print("Samsung TV created") [cite: 144]

class RemoteControl:
    def __init__(self, tv):
        self.tv = tv [cite: 146]

    def toggle_power(self):
        if self.tv.power:
            self.tv.turn_off() [cite: 148]
        else:
            self.tv.turn_on() [cite: 150]

    def volume_up(self):
        self.tv.volume_up()

    def volume_down(self):
        self.tv.volume_down()

    def channel_up(self):
        self.tv.channel_up()

    def channel_down(self):
        self.tv.channel_down()

class BasicRemote(RemoteControl):
    def mute(self):
        self.tv.volume = 0 [cite: 157]
        print("Muted") [cite: 157]

class AdvancedRemote(RemoteControl):
    def set_channel(self, number):
        if 1 <= number <= 999:
            self.tv.channel = number [cite: 159]
            print(f"Channel set to {number}") [cite: 159]
        else:
            print("Invalid channel number") [cite: 161]

def main():
    print("Bridge pattern demo\n") [cite: 163]
    tv = SonyTV() [cite: 164]
    remote = BasicRemote(tv) [cite: 167]
    remote.toggle_power()
    remote.volume_up()
    remote.mute()
    remote.toggle_power()

    print("-" * 50)
    tv2 = SamsungTV() [cite: 175]
    adv_remote = AdvancedRemote(tv2) [cite: 177]
    adv_remote.toggle_power()
    adv_remote.set_channel(42) [cite: 178]
    adv_remote.toggle_power()

if __name__ == "__main__":
    main()
