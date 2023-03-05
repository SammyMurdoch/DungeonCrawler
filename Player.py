class Player:
    def __init__(self, name, hit_points, attack_damage, starting_location: list, texture):
        self.name = name
        self.hit_points = hit_points
        self.attack_damage = attack_damage
        self.coords = starting_location
        self.texture = texture

    def move_x(self, step):
        self.coords[0] += step

    def move_y(self, step):
        self.coords[1] += step

    def attack(self):
        return self.attack_damage
