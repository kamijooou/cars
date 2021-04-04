import csv
import os

class CarBase:

    def __init__(self, brand, photo_file_name, carrying):
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]

class Car(CarBase):

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'car'
        self.passenger_seats_count = int(passenger_seats_count)

class Truck(CarBase):

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        split_body_whl = body_whl.split('x')
        self.car_type = 'truck'
        if len(split_body_whl) == 3:
            try:
                self.body_width = float(split_body_whl[1])
                self.body_height = float(split_body_whl[2])
                self.body_length = float(split_body_whl[0])
            except (ValueError, IndexError):
                self.body_width = 0.0
                self.body_height = 0.0
                self.body_length = 0.0
        else:
            self.body_width = 0.0
            self.body_height = 0.0
            self.body_length = 0.0

    def get_body_volume(self):
        return self.body_length*self.body_width*self.body_height

class SpecMachine(CarBase):

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'spec_machine'
        self.extra = extra


##################

def converter_to_cl_inst(row):
    extender_car_list = []
    photo_ext_tuple = ('.jpg', '.jpeg', '.png', '.gif')
    try:
        float(row[5])
    except ValueError:
        return []
    else:
        if row[1] and os.path.splitext(row[3])[1] in photo_ext_tuple:
            if row[0] == 'car':
                try:
                    int(row[2])
                except ValueError:
                    return []
                else:
                    car = Car(row[1], row[3], row[5], row[2])
                    extender_car_list.append(car)
                    return extender_car_list
            if row[0] == 'truck':
                truck = Truck(row[1], row[3], row[5], row[4])
                extender_car_list.append(truck)
                return extender_car_list
            if row[0] == 'spec_machine' and row[6]:
                try:
                    str(row[6])
                except ValueError:
                    return []
                else:
                    spec = SpecMachine(row[1], row[3], row[5], row[6])
                    extender_car_list.append(spec)
                    return extender_car_list
        else: return []
    return extender_car_list

##################

def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as fin:
        reader = csv.reader(fin, delimiter=';')
        next(reader)
        for row in reader:
            if len(row) == 7:
                car_list.extend(converter_to_cl_inst(row))
            else: continue
    return car_list