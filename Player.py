class Player:
    def __init__(self, name, hit_points, attack_damage, starting_location):
        self.name = name
        self.hit_points = hit_points
        self.attack_damage = attack_damage
        self.starting_location = starting_location

    def attack(self):
        return self.attack_damage