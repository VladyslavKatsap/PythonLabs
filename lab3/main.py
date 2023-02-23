class RadioModule:
    def handle_message(self):
        return "Радіомодуль"


class Buttons:
    def handle_message(self):
        return "Кнопки"


class Battery:
    def handle_message(self):
        return "Батарея"


class Screen:
    def handle_message(self):
        return "Екран"


class Processor:
    def handle_message(self):
        return "Процесор"


class Sensor:
    def handle_message(self):
        return "Сенсор"


class Radio(RadioModule, Battery, Buttons):
    def __init__(self):
        self.radio_module = RadioModule()
        self.buttons = Buttons()
        self.battery = Battery()

class Phone(RadioModule, Battery, Buttons, Screen, Processor):
    def __init__(self):
        self.radio_module = RadioModule()
        self.buttons = Buttons()
        self.battery = Battery()
        self.screen = Screen()
        self.processor = Processor()

class Computer(Buttons, Screen, Processor):
    def __init__(self):
        self.buttons = Buttons()
        self.screen = Screen()
        self.processor = Processor()

class Tablet(Battery, Screen, Processor, Sensor):
    def __init__(self):
        self.battery = Battery()
        self.screen = Screen()
        self.processor = Processor()
        self.sensor = Sensor()

    def handle_message(self):
        return self.screen.handle_message(), self.sensor.handle_message(), self.processor.handle_message(), self.battery.handle_message()


tablet = Tablet()
print(tablet.handle_message())