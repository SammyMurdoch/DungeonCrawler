class Player:
    def __init__(self, name, hit_points, attack_damage, starting_location: tuple):
        self.name = name
        self.hit_points = hit_points
        self.attack_damage = attack_damage
        self.x_coord, self.y_coord = starting_location[0], starting_location[1]

    def move_x(self, step):
        self.x_coord += step

    def move_y(self, step):
        self.y_coord += step

    def attack(self):
        return self.attack_damage


player = Player('Bob', 10, 10, (0, 1))

player.move_x(10)

print(player.x_coord)
