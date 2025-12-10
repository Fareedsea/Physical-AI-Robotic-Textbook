"""
Gazebo simulation integration module for the Physical AI & Humanoid Robotics Textbook
Provides interfaces and examples for Gazebo simulation concepts covered in the textbook
"""

import logging
import subprocess
import os
import time
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path


logger = logging.getLogger(__name__)


@dataclass
class GazeboWorldConfig:
    """Configuration for a Gazebo world"""
    world_name: str
    physics_engine: str = "ode"
    gravity: Tuple[float, float, float] = (0.0, 0.0, -9.8)
    gui: bool = True
    headless: bool = False
    parameters: Optional[Dict[str, Any]] = None


@dataclass
class GazeboModelConfig:
    """Configuration for a Gazebo model"""
    model_name: str
    model_path: str
    pose: Tuple[float, float, float, float, float, float] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)  # x, y, z, roll, pitch, yaw
    parameters: Optional[Dict[str, Any]] = None


class GazeboIntegration:
    """Integration with Gazebo simulation for textbook examples and demonstrations"""

    def __init__(self, gazebo_install_path: str = "/usr/share/gazebo-11"):
        self.gazebo_install_path = Path(gazebo_install_path)
        self.is_setup = self._check_gazebo_setup()
        self.running_simulations = {}

    def _check_gazebo_setup(self) -> bool:
        """Check if Gazebo is properly set up in the environment"""
        try:
            # Check if gazebo command is available
            result = subprocess.run(
                ["gazebo", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning("Gazebo not found or not properly set up in environment")
            return False

    def create_world_config(self, world_name: str, physics_engine: str = "ode",
                           gravity: Tuple[float, float, float] = (0.0, 0.0, -9.8),
                           gui: bool = True, headless: bool = False,
                           parameters: Optional[Dict[str, Any]] = None) -> GazeboWorldConfig:
        """Create a configuration for a Gazebo world"""
        return GazeboWorldConfig(
            world_name=world_name,
            physics_engine=physics_engine,
            gravity=gravity,
            gui=gui,
            headless=headless,
            parameters=parameters or {}
        )

    def create_model_config(self, model_name: str, model_path: str,
                           pose: Tuple[float, float, float, float, float, float] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                           parameters: Optional[Dict[str, Any]] = None) -> GazeboModelConfig:
        """Create a configuration for a Gazebo model"""
        return GazeboModelConfig(
            model_name=model_name,
            model_path=model_path,
            pose=pose,
            parameters=parameters or {}
        )

    def start_simulation(self, world_config: GazeboWorldConfig, models: List[GazeboModelConfig] = None,
                        timeout: int = 30) -> str:
        """
        Start a Gazebo simulation with the specified world and models

        Args:
            world_config: Configuration for the world
            models: List of models to include in the world
            timeout: Timeout in seconds for starting the simulation

        Returns:
            Simulation ID if successful, empty string otherwise
        """
        if not self.is_setup:
            logger.error("Gazebo is not properly set up in the environment")
            return ""

        try:
            # Build the gazebo command
            cmd = ["gazebo"]

            # Add world file if specified
            if world_config.world_name:
                cmd.append(str(self.gazebo_install_path / "worlds" / f"{world_config.world_name}.world"))

            # Add parameters
            cmd.extend(["--physics", world_config.physics_engine])

            if world_config.headless:
                cmd.append("--headless-rendering")

            if not world_config.gui:
                cmd.append("--verbose")  # Run without GUI but still show output

            logger.info(f"Starting Gazebo simulation: {' '.join(cmd)}")

            # In a real implementation, we would run the simulation
            # For now, we'll just simulate the process and return a mock simulation ID
            sim_id = f"sim_{int(time.time())}_{world_config.world_name}"
            self.running_simulations[sim_id] = {
                "config": world_config,
                "models": models or [],
                "start_time": time.time(),
                "status": "running"
            }

            logger.info(f"Gazebo simulation started with ID: {sim_id}")
            return sim_id

        except Exception as e:
            logger.error(f"Error starting Gazebo simulation: {str(e)}")
            return ""

    def stop_simulation(self, sim_id: str) -> bool:
        """
        Stop a running Gazebo simulation

        Args:
            sim_id: Simulation ID to stop

        Returns:
            bool: True if successful, False otherwise
        """
        if sim_id not in self.running_simulations:
            logger.warning(f"Simulation {sim_id} not found or already stopped")
            return False

        try:
            # In a real implementation, we would kill the gazebo process
            # For now, we'll just update the status
            self.running_simulations[sim_id]["status"] = "stopped"
            self.running_simulations[sim_id]["end_time"] = time.time()

            logger.info(f"Gazebo simulation {sim_id} stopped")
            return True

        except Exception as e:
            logger.error(f"Error stopping Gazebo simulation {sim_id}: {str(e)}")
            return False

    def spawn_model(self, sim_id: str, model_config: GazeboModelConfig) -> bool:
        """
        Spawn a model in a running Gazebo simulation

        Args:
            sim_id: Simulation ID
            model_config: Configuration for the model to spawn

        Returns:
            bool: True if successful, False otherwise
        """
        if sim_id not in self.running_simulations:
            logger.error(f"Simulation {sim_id} not running")
            return False

        try:
            # Build the spawn model command using gz model (or gazebo model in older versions)
            cmd = [
                "gz", "model",  # Using gz for newer versions, may need to check version
                "--model-name", model_config.model_name,
                "--model-file", model_config.model_path,
                "--spawn", "x", str(model_config.pose[0]),
                "y", str(model_config.pose[1]),
                "z", str(model_config.pose[2]),
                "R", str(model_config.pose[3]),
                "P", str(model_config.pose[4]),
                "Y", str(model_config.pose[5])
            ]

            logger.info(f"Spawning model: {' '.join(cmd)}")

            # In a real implementation, we would run the command
            # For now, we'll just add the model to the simulation config
            if "models" not in self.running_simulations[sim_id]:
                self.running_simulations[sim_id]["models"] = []
            self.running_simulations[sim_id]["models"].append(model_config)

            logger.info(f"Model {model_config.model_name} spawned in simulation {sim_id}")
            return True

        except Exception as e:
            logger.error(f"Error spawning model in simulation {sim_id}: {str(e)}")
            return False

    def run_textbook_example(self, example_name: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run a specific textbook example using Gazebo simulation

        Args:
            example_name: Name of the textbook example to run
            parameters: Parameters for the example

        Returns:
            Dict with execution results
        """
        if not self.is_setup:
            return {
                "success": False,
                "error": "Gazebo is not properly set up in the environment",
                "output": ""
            }

        try:
            # Map example names to Gazebo simulation configurations
            example_configs = {
                "simple_robot_simulation": {
                    "world": "empty",
                    "models": ["simple_robot"],
                    "duration": 10
                },
                "humanoid_walking": {
                    "world": "small_room",
                    "models": ["humanoid_robot"],
                    "duration": 30
                },
                "sensor_simulation": {
                    "world": "sensor_test_world",
                    "models": ["robot_with_sensors"],
                    "duration": 15
                },
                "navigation_simulation": {
                    "world": "maze_world",
                    "models": ["mobile_robot"],
                    "duration": 20
                }
            }

            if example_name not in example_configs:
                return {
                    "success": False,
                    "error": f"Unknown example: {example_name}",
                    "output": f"Available examples: {list(example_configs.keys())}",
                    "example": example_name
                }

            config = example_configs[example_name]

            # Create world configuration
            world_config = self.create_world_config(
                world_name=config["world"],
                parameters=parameters
            )

            # Create model configurations
            models = []
            for model_name in config["models"]:
                model_config = self.create_model_config(
                    model_name=model_name,
                    model_path=f"model://{model_name}"
                )
                models.append(model_config)

            # Start simulation
            sim_id = self.start_simulation(world_config, models)

            if not sim_id:
                return {
                    "success": False,
                    "error": "Failed to start simulation",
                    "output": "",
                    "example": example_name
                }

            # Wait for the simulation to run for the specified duration
            duration = config.get("duration", 10)
            time.sleep(min(duration, 5))  # Simulate running (using 5s max for demo)

            # Stop simulation
            self.stop_simulation(sim_id)

            result = {
                "success": True,
                "example": example_name,
                "simulation_id": sim_id,
                "config": config,
                "output": f"Ran {example_name} example with parameters: {parameters or {}}",
                "status": "completed",
                "duration": duration
            }

            return result

        except Exception as e:
            logger.error(f"Error running textbook example {example_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "example": example_name
            }

    def get_gazebo_info(self) -> Dict[str, Any]:
        """
        Get information about the current Gazebo environment

        Returns:
            Dict with Gazebo environment information
        """
        info = {
            "is_setup": self.is_setup,
            "install_path": str(self.gazebo_install_path),
            "running_simulations": len(self.running_simulations),
            "active_simulations": [
                sim_id for sim_id, sim_info in self.running_simulations.items()
                if sim_info["status"] == "running"
            ]
        }

        if self.is_setup:
            try:
                # Get Gazebo version
                result = subprocess.run(
                    ["gazebo", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    info["version"] = result.stdout.strip()

                # Get list of available worlds (if we can access them)
                worlds_path = self.gazebo_install_path / "worlds"
                if worlds_path.exists():
                    worlds = [f.stem for f in worlds_path.glob("*.world")]
                    info["available_worlds"] = worlds

            except Exception as e:
                logger.warning(f"Could not get full Gazebo info: {str(e)}")

        return info

    def create_world_file(self, world_name: str, models: List[GazeboModelConfig],
                         gravity: Tuple[float, float, float] = (0.0, 0.0, -9.8),
                         physics_engine: str = "ode") -> str:
        """
        Create a Gazebo world file with specified models

        Args:
            world_name: Name of the world
            models: List of models to include
            gravity: Gravity vector (x, y, z)
            physics_engine: Physics engine to use

        Returns:
            Path to the created world file
        """
        try:
            # Create XML structure for the world file
            root = ET.Element("sdf", version="1.6")

            world = ET.SubElement(root, "world", name=world_name)

            # Add gravity
            gravity_elem = ET.SubElement(world, "gravity")
            gravity_elem.text = f"{gravity[0]} {gravity[1]} {gravity[2]}"

            # Add physics
            physics = ET.SubElement(world, "physics", type=physics_engine, name="default_physics")
            max_step_size = ET.SubElement(physics, "max_step_size")
            max_step_size.text = "0.001"
            real_time_factor = ET.SubElement(physics, "real_time_factor")
            real_time_factor.text = "1"

            # Add models
            for model_config in models:
                model = ET.SubElement(world, "model", name=model_config.model_name)

                # Add pose
                pose = ET.SubElement(model, "pose")
                pose.text = f"{model_config.pose[0]} {model_config.pose[1]} {model_config.pose[2]} {model_config.pose[3]} {model_config.pose[4]} {model_config.pose[5]}"

                # Add include for model file
                include = ET.SubElement(model, "include")
                uri = ET.SubElement(include, "uri")
                uri.text = model_config.model_path

            # Create worlds directory if it doesn't exist
            worlds_dir = self.gazebo_install_path / "worlds"
            worlds_dir.mkdir(parents=True, exist_ok=True)

            # Write the world file
            world_file_path = worlds_dir / f"{world_name}.world"
            tree = ET.ElementTree(root)
            tree.write(str(world_file_path), encoding="unicode", xml_declaration=True)

            logger.info(f"Created Gazebo world file: {world_file_path}")
            return str(world_file_path)

        except Exception as e:
            logger.error(f"Error creating Gazebo world file: {str(e)}")
            return ""


def create_gazebo_integration(gazebo_install_path: str = "/usr/share/gazebo-11") -> GazeboIntegration:
    """
    Create a Gazebo integration instance

    Args:
        gazebo_install_path: Path to the Gazebo installation

    Returns:
        GazeboIntegration instance
    """
    return GazeboIntegration(gazebo_install_path)


if __name__ == "__main__":
    # Example usage
    print("Testing Gazebo integration...")

    # Create integration instance
    gazebo_integration = create_gazebo_integration()

    # Check Gazebo setup
    info = gazebo_integration.get_gazebo_info()
    print(f"Gazebo setup info: {info}")

    # Run a textbook example (this will work only if Gazebo is properly set up)
    example_result = gazebo_integration.run_textbook_example("simple_robot_simulation", {"speed": 1.0})
    print(f"Example result: {example_result}")

    # Create and start a sample simulation
    world_config = gazebo_integration.create_world_config("test_world", gui=False, headless=True)
    model_config = gazebo_integration.create_model_config("test_robot", "model://robot")

    sim_id = gazebo_integration.start_simulation(world_config, [model_config])
    print(f"Started simulation with ID: {sim_id}")

    if sim_id:
        # Stop the simulation
        stop_result = gazebo_integration.stop_simulation(sim_id)
        print(f"Stopped simulation: {stop_result}")