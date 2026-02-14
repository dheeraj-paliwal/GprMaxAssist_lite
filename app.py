
import re

class GprMaxChatbot:
    def __init__(self):
        self.knowledge_base = self.load_knowledge()
        self.simulation_setup = {} # To store the user's defined simulation

    def load_knowledge(self):
        """Loads basic gprMax command knowledge."""
        return {
            "domain": {
                "description": "Defines the simulation domain size.",
                "syntax": "#domain: <size_x> <size_y> <size_z>",
                "parameters": ["size_x (float, meters)", "size_y (float, meters)", "size_z (float, meters)"],
                "keywords": ["domain size", "simulation area", "extent"]
            },
            "material": {
                "description": "Defines a material with its electromagnetic properties.",
                "syntax": "#material: <name> <epsilon_r> <sigma> <mu_r> <loss_tan_e> <loss_tan_m>",
                "parameters": ["name (string)", "epsilon_r (float, relative permittivity)", "sigma (float, conductivity S/m)", "mu_r (float, relative permeability)", "loss_tan_e (float)", "loss_tan_m (float)"],
                "keywords": ["add material", "define property", "create medium"]
            },
            "geometry_box": {
                "description": "Creates a rectangular block geometry.",
                "syntax": "#geometry: box (<x1>, <y1>, <z1>) (<x2>, <y2>, <z2>) <material_name>",
                "parameters": ["(x1, y1, z1) (tuple of floats, meters)", "(x2, y2, z2) (tuple of floats, meters)", "material_name (string)"],
                "keywords": ["create block", "add rectangle", "make box"]
            },
            "source_dipole": {
                "description": "Adds a Hertzian dipole source.",
                "syntax": "#source: dipole <orientation> <frequency> <x> <y> <z>",
                "parameters": ["orientation (string: x, y, or z)", "frequency (float, Hz)", "x (float, meters)", "y (float, meters)", "z (float, meters)"],
                "keywords": ["add source", "create emitter", "place dipole"]
            },
            "receiver": {
                "description": "Adds a receiver to record electromagnetic fields.",
                "syntax": "#rx: <x> <y> <z>",
                "parameters": ["x (float, meters)", "y (float, meters)", "z (float, meters)"],
                "keywords": ["add receiver", "place sensor", "record field"]
            }
            # if further it requires any commands then they will ve added here !!
        }

    def process_input(self, user_input):
        """Processes the user's natural language input."""
        user_input = user_input.lower()

        # --- Intent Recognition (Basic Keyword Matching) ---
        if any(keyword in user_input for keyword in self.knowledge_base["domain"]["keywords"]):
            return "domain"
        elif any(keyword in user_input for keyword in self.knowledge_base["material"]["keywords"]):
            return "material"
        elif any(keyword in user_input for keyword in self.knowledge_base["geometry_box"]["keywords"]):
            return "geometry_box"
        elif any(keyword in user_input for keyword in self.knowledge_base["source_dipole"]["keywords"]):
            return "source_dipole"
        elif any(keyword in user_input for keyword in self.knowledge_base["receiver"]["keywords"]):
            return "receiver"
        elif user_input in ["help", "commands", "what can you do"]:
            return "help"
        elif user_input in ["show setup", "current simulation"]:
            return "show_setup"
        elif user_input == "done":
            return "done"
        else:
            return "unknown"

    def handle_domain(self, user_input):
        """Handles user input related to domain definition."""
        match = re.search(r"domain size is (\d+(\.\d*)?) by (\d+(\.\d*)?) by (\d+(\.\d*)?) (meters|m)", user_input, re.IGNORECASE)
        if match:
            self.simulation_setup["domain"] = {
                "size_x": float(match.group(1)),
                "size_y": float(match.group(3)),
                "size_z": float(match.group(5))
            }
            return f"Domain size set to {self.simulation_setup['domain']['size_x']}x{self.simulation_setup['domain']['size_y']}x{self.simulation_setup['domain']['size_z']} meters."
        else:
            return "Please specify the domain size in the format 'domain size is X by Y by Z meters'."

    def handle_material(self, user_input):
        """Handles user input related to material definition."""
        match = re.search(r"add a material named (\w+) with relative permittivity (\d+(\.\d*)?), conductivity (\d+(\.\d*)?), relative permeability (\d+(\.\d*)?)", user_input, re.IGNORECASE)
        if match:
            material_name = match.group(1)
            self.simulation_setup.setdefault("materials", {})[material_name] = {
                "epsilon_r": float(match.group(2)),
                "sigma": float(match.group(4)),
                "mu_r": float(match.group(6)),
                "loss_tan_e": 0.0,
                "loss_tan_m": 0.0
            }
            return f"Material '{material_name}' added."
        else:
            return "Please specify the material properties like 'add a material named [name] with relative permittivity [er], conductivity [sigma], relative permeability [mr]'."

    def handle_geometry_box(self, user_input):
        """Handles user input related to creating a box geometry."""
        match = re.search(r"create a block of material (\w+) from \((\d+(\.\d*)?), (\d+(\.\d*)?), (\d+(\.\d*)?)\) to \((\d+(\.\d*)?), (\d+(\.\d*)?), (\d+(\.\d*)?)\)", user_input, re.IGNORECASE)
        if match:
            material_name = match.group(1)
            self.simulation_setup.setdefault("geometries", []).append({
                "type": "box",
                "material": material_name,
                "start": (float(match.group(2)), float(match.group(4)), float(match.group(6))),
                "end": (float(match.group(8)), float(match.group(10)), float(match.group(12)))
            })
            return f"Box geometry of material '{material_name}' created."
        else:
            return "Please specify the block geometry like 'create a block of material [name] from (x1, y1, z1) to (x2, y2, z2)'."

    def handle_source_dipole(self, user_input):
        """Handles user input related to adding a dipole source."""
        match = re.search(r"add a source with type dipole and orientation (\w) at position \((\d+(\.\d*)?), (\d+(\.\d*)?), (\d+(\.\d*)?)\)", user_input, re.IGNORECASE)
        if match:
            orientation = match.group(1).lower()
            self.simulation_setup.setdefault("sources", []).append({
                "type": "dipole",
                "orientation": orientation,
                "position": (float(match.group(2)), float(match.group(4)), float(match.group(6)))
            })
            return f"Dipole source with orientation '{orientation}' added at {self.simulation_setup['sources'][-1]['position']}."
        else:
            return "Please specify the dipole source like 'add a source with type dipole and orientation [x/y/z] at position (x, y, z)'."

    def handle_receiver(self, user_input):
        """Handles user input related to adding a receiver."""
        match = re.search(r"add a receiver at position \((\d+(\.\d*)?), (\d+(\.\d*)?), (\d+(\.\d*)?)\)", user_input, re.IGNORECASE)
        if match:
            self.simulation_setup.setdefault("receivers", []).append({
                "position": (float(match.group(1)), float(match.group(3)), float(match.group(5)))
            })
            return f"Receiver added at {self.simulation_setup['receivers'][-1]['position']}."
        else:
            return "Please specify the receiver position like 'add a receiver at position (x, y, z)'."

    def generate_gprmax_commands(self):
        """Generates gprMax input file commands based on the setup."""
        commands = []
        if "domain" in self.simulation_setup:
            domain = self.simulation_setup["domain"]
            commands.append(f"#domain: {domain['size_x']} {domain['size_y']} {domain['size_z']}")
        if "materials" in self.simulation_setup:
            for name, props in self.simulation_setup["materials"].items():
                commands.append(f"#material: {name} {props['epsilon_r']} {props['sigma']} {props['mu_r']} {props['loss_tan_e']} {props['loss_tan_m']}")
        if "geometries" in self.simulation_setup:
            for geom in self.simulation_setup["geometries"]:
                if geom["type"] == "box":
                    commands.append(f"#geometry: box ({geom['start'][0]}, {geom['start'][1]}, {geom['start'][2]}) ({geom['end'][0]}, {geom['end'][1]}, {geom['end'][2]}) {geom['material']}")
        if "sources" in self.simulation_setup:
            for source in self.simulation_setup["sources"]:
                if source["type"] == "dipole":
                    commands.append(f"#source: dipole {source['orientation']} 1e9 {source['position'][0]} {source['position'][1]} {source['position'][2]}") # Assuming a default frequency
        if "receivers" in self.simulation_setup:
            for rx in self.simulation_setup["receivers"]:
                commands.append(f"#rx: {rx['position'][0]} {rx['position'][1]} {rx['position'][2]}")
        return "\n".join(commands)

    def run(self):
        """Runs the chatbot."""
        print("Welcome to the gprMax Simulation Builder Chatbot!")
        print("Type 'help' for available commands, 'show setup' to see your current simulation, or 'done' to generate the gprMax input.")

        while True:
            user_input = input("> ").strip()
            intent = self.process_input(user_input)

            if intent == "domain":
                response = self.handle_domain(user_input)
                print(response)
            elif intent == "material":
                response = self.handle_material(user_input)
                print(response)
            elif intent == "geometry_box":
                response = self.handle_geometry_box(user_input)
                print(response)
            elif intent == "source_dipole":
                response = self.handle_source_dipole(user_input)
                print(response)
            elif intent == "receiver":
                response = self.handle_receiver(user_input)
                print(response)
            elif intent == "help":
                print("\nAvailable commands:")
                for command, info in self.knowledge_base.items():
                    print(f"- {', '.join(info['keywords'])}: {info['description']}")
                print("- show setup: Display the current simulation setup.")
                print("- done: Generate the gprMax input file commands.")
                print("- exit: Exit the chatbot.")
                print()
            elif intent == "show_setup":
                print("\nCurrent Simulation Setup:")
                for key, value in self.simulation_setup.items():
                    print(f"- {key}: {value}")
                print()
            elif intent == "done":
                commands = self.generate_gprmax_commands()
                print("\nGenerated gprMax Input File Commands:")
                print(commands)
                break
            elif user_input.lower() == "exit":
                break
            else:
                print("Sorry, I didn't understand that. Type 'help' for available commands.")

if __name__ == "__main__":
    chatbot = GprMaxChatbot()
    chatbot.run()
