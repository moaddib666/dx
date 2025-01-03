class BalanceSkillCalculator:
    def __init__(self):
        # Base attributes
        self.base_character_attributes = {
            "Charisma": 10,
            "Concentration": 10,
            "Flow Connection": 10,
            "Flow Manipulation": 10,
            "Flow Resonance": 10,
            "Knowledge": 10,
            "Luck": 10,
            "Mental Strength": 10,
            "Physical Strength": 10,
            "Speed": 10
        }

        # Derived stats
        self.base_stats = {
            "Health": 75,
            "Energy": 155,
            "Action Points": 5
        }

        # Conversion rates
        self.damage_per_ap = 3
        self.healing_per_ap = 3
        self.energy_per_ap = 6

    def calculate_damage(self, ap):
        return ap * self.damage_per_ap

    def calculate_healing(self, ap):
        return ap * self.healing_per_ap

    def calculate_energy(self, ap):
        return ap * self.energy_per_ap

    def calculate_ap(self, value, conversion_rate):
        return value / conversion_rate

    def calculate(self, ap=None, damage=None, heal=None, energy=None):
        """
        Calculate the results based on provided parameters. At least one parameter is required.

        :param ap: Action Points (AP) spent
        :param damage: Damage output
        :param heal: Healing output
        :param energy: Energy consumption
        :return: A dictionary of calculated values
        """
        if not (ap or damage or heal or energy):
            raise ValueError("At least one parameter (ap, damage, heal, energy) must be provided.")

        results = {
            "Damage": 0,
            "Healing": 0,
            "Energy": 0,
            "AP Used": 0
        }

        if ap is not None:
            results["Damage"] = self.calculate_damage(ap)
            results["Healing"] = self.calculate_healing(ap)
            results["Energy"] = self.calculate_energy(ap)
            results["AP Used"] = ap

        if damage is not None:
            results["AP Used"] = self.calculate_ap(damage, self.damage_per_ap)
            results["Damage"] = damage
            results["Healing"] = self.calculate_healing(results["AP Used"])
            results["Energy"] = self.calculate_energy(results["AP Used"])

        if heal is not None:
            results["AP Used"] = self.calculate_ap(heal, self.healing_per_ap)
            results["Healing"] = heal
            results["Damage"] = self.calculate_damage(results["AP Used"])
            results["Energy"] = self.calculate_energy(results["AP Used"])

        if energy is not None:
            results["AP Used"] = self.calculate_ap(energy, self.energy_per_ap)
            results["Energy"] = energy
            results["Damage"] = self.calculate_damage(results["AP Used"])
            results["Healing"] = self.calculate_healing(results["AP Used"])

        return results


# Example Usage
if __name__ == "__main__":
    calculator = BalanceSkillCalculator()

    # Calculate based on Action Points
    result_ap = calculator.calculate(ap=5)
    print("Calculation for AP:", result_ap)
