# Built from https://www.jetbrains.com/help/pycharm/2018.1/meet-pycharm.html

class Car:
    def __init__(self):
        self.speed = 0
        self.odometer = 0
        self.time = 0
        self.max_speed = 250

    def say_state(self):
        print("I'm going {} kph!".format(self.speed))

    def accelerate(self):
        self.speed += 5
        if self.speed > self.max_speed: self.speed = self.max_speed
        print("Faster!")

    def brake(self):
        self.speed -= 5
        print("Slow down!")

    def step(self):
        self.odometer += abs(self.speed)
        self.time += 1

    def avg_speed(self):
        if self.time != 0:
            return(self.odometer / self.time)
        else:
            return(0)

    def report(self):
        print("Total km traveled: {}".format(self.odometer))
        print("I reached {} kph".format(self.max_speed))
        print("Fuel burned: {} liters.".format(0))

class Moped(Car):
    def __init__(self):
        self.speed = 0
        self.odometer = 0
        self.time = 0
        self.max_speed = 15

if __name__ == '__main__':
    my_car = Moped()

    print("I'm a Tesla Model S (tm)!")

    _q = True
    while _q:
        action = input("What should I do? [A]ccelerate, [B]rake, "
                       "show [O]dometer, show average [S]peed,"
                       "[R]eport or [Q]uit? ").upper()

        if action not in "ABOSRQ" or len(action) != 1:
            print("I don't know how to do that")
            continue
        if action == 'A':
            my_car.accelerate()
        elif action == 'B':
            my_car.brake()
        elif action == 'O':
            print("I have driven {} kilometers.".format(my_car.odometer))
        elif action == 'S':
            print("My average speed was {} kph".format(my_car.avg_speed()))
        elif action == 'R':
            my_car.report()
        elif action == 'Q':
            _q = False
            continue

        my_car.step()
        my_car.say_state()

    my_car.report()
