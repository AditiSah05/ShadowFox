"""1. Create inheritance using MobilePhone as base class and Apple &
Samsung as child class
1. The base class should have properties:
1. ScreenType = Touch Screen
2. NetworkType = 4G/5G
3. DualSim = True or False
4. FrontCamera = (5MP/8MP/12MP/16MP)
5. rearCamera = (8MP/12MP/16MP/32MP/48MP)
6. RAM = (2GB/3GB/4GB)
7. Storage = (16GB/32GB/64GB)"""

class MobilePhone:
    def __init__(self, screen_type, network_type, dual_sim, front_camera, rear_camera, ram, storage):
        self.screen_type = screen_type
        self.network_type = network_type
        self.dual_sim = dual_sim
        self.front_camera = front_camera
        self.rear_camera = rear_camera
        self.ram = ram
        self.storage = storage
    
    def display_specs(self):
        print(f"Screen Type: {self.screen_type}")
        print(f"Network Type: {self.network_type}")
        print(f"Dual SIM: {self.dual_sim}")
        print(f"Front Camera: {self.front_camera}")
        print(f"Rear Camera: {self.rear_camera}")
        print(f"RAM: {self.ram}")
        print(f"Storage: {self.storage}")
    
    def make_call(self, number):
        print(f"Calling {number}...")
    
    def receive_call(self, number):
        print(f"Receiving call from {number}...")
    
    def take_a_picture(self):
        print(f"Taking picture with {self.rear_camera} rear camera")
    
    def send_message(self, number, message):
        print(f"Sending message to {number}: {message}")

class Apple(MobilePhone):
    def __init__(self, screen_type, network_type, dual_sim, front_camera, rear_camera, ram, storage, model):
        super().__init__(screen_type, network_type, dual_sim, front_camera, rear_camera, ram, storage)
        self.model = model
        self.brand = "Apple"
    
    def display_specs(self):
        print(f"\n{self.brand} {self.model} Specifications:")
        super().display_specs()

class Samsung(MobilePhone):
    def __init__(self, screen_type, network_type, dual_sim, front_camera, rear_camera, ram, storage, model):
        super().__init__(screen_type, network_type, dual_sim, front_camera, rear_camera, ram, storage)
        self.model = model
        self.brand = "Samsung"
    
    def display_specs(self):
        print(f"\n{self.brand} {self.model} Specifications:")
        super().display_specs()

iphone = Apple("Touch Screen", "5G", False, "12MP", "48MP", "4GB", "64GB", "iPhone 14")
iphone.display_specs()

galaxy = Samsung("Touch Screen", "5G", True, "16MP", "48MP", "4GB", "64GB", "Galaxy S23")
galaxy.display_specs()

"""2. Create basic mobile phone functionalities in the classes like:
make_call, recieve_call, take_a_picture, etc."""



print("\n--- Testing Mobile Phone Functionalities ---")
iphone.make_call("123-456-7890")
iphone.receive_call("987-654-3210")
iphone.take_a_picture()
iphone.send_message("123-456-7890", "Hello from iPhone!")

galaxy.make_call("555-123-4567")
galaxy.receive_call("555-987-6543")
galaxy.take_a_picture()
galaxy.send_message("555-123-4567", "Hello from Samsung!")

#3. Use super() constructor for calling parent class’s constructor


print("\n--- Question 3: super() constructor is already used ---")
print("In both Apple and Samsung classes, we use:")
print("super().__init__(screen_type, network_type, dual_sim, front_camera, rear_camera, ram, storage)")
print("This calls the parent MobilePhone class's constructor to initialize inherited properties.")

#4. Make some objects of Apple class with different properties


print("\n--- Question 4: Creating multiple Apple objects ---")

iphone_13 = Apple("Touch Screen", "5G", False, "12MP", "12MP", "4GB", "128GB", "iPhone 13")
iphone_13.display_specs()

iphone_14_pro = Apple("Touch Screen", "5G", True, "12MP", "48MP", "6GB", "256GB", "iPhone 14 Pro")
iphone_14_pro.display_specs()

iphone_se = Apple("Touch Screen", "4G", False, "7MP", "12MP", "3GB", "64GB", "iPhone SE")
iphone_se.display_specs()

#5. Make some objects of Samsung class with different properties


print("\n--- Question 5: Creating multiple Samsung objects ---")

galaxy_s22 = Samsung("Touch Screen", "5G", True, "10MP", "50MP", "8GB", "128GB", "Galaxy S22")
galaxy_s22.display_specs()

galaxy_a54 = Samsung("Touch Screen", "5G", True, "32MP", "50MP", "6GB", "128GB", "Galaxy A54")
galaxy_a54.display_specs()

galaxy_z_fold = Samsung("Touch Screen", "5G", True, "10MP", "50MP", "12GB", "512GB", "Galaxy Z Fold 5")
galaxy_z_fold.display_specs()
