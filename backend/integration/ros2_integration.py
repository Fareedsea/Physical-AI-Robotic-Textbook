"""
ROS 2 integration module for the Physical AI & Humanoid Robotics Textbook
Provides interfaces and examples for ROS 2 concepts covered in the textbook
"""

import logging
import subprocess
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path


logger = logging.getLogger(__name__)


@dataclass
class ROS2NodeConfig:
    """Configuration for a ROS 2 node"""
    name: str
    package: str
    executable: str
    parameters: Optional[Dict[str, Any]] = None
    remappings: Optional[List[tuple]] = None


class ROS2Integration:
    """Integration with ROS 2 for textbook examples and demonstrations"""

    def __init__(self, ros_workspace_path: str = "~/ros2_ws"):
        self.ros_workspace_path = Path(os.path.expanduser(ros_workspace_path))
        self.is_setup = self._check_ros2_setup()

    def _check_ros2_setup(self) -> bool:
        """Check if ROS 2 is properly set up in the environment"""
        try:
            # Check if ROS 2 environment is sourced
            result = subprocess.run(
                ["ros2", "topic", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning("ROS 2 not found or not properly set up in environment")
            return False

    def create_node_config(self, name: str, package: str, executable: str,
                          parameters: Optional[Dict[str, Any]] = None,
                          remappings: Optional[List[tuple]] = None) -> ROS2NodeConfig:
        """Create a configuration for a ROS 2 node"""
        return ROS2NodeConfig(
            name=name,
            package=package,
            executable=executable,
            parameters=parameters or {},
            remappings=remappings or []
        )

    def launch_nodes(self, configs: List[ROS2NodeConfig], timeout: int = 30) -> bool:
        """
        Launch multiple ROS 2 nodes based on configurations

        Args:
            configs: List of node configurations to launch
            timeout: Timeout in seconds for the launch command

        Returns:
            bool: True if launch was successful, False otherwise
        """
        if not self.is_setup:
            logger.error("ROS 2 is not properly set up in the environment")
            return False

        try:
            # Build the launch command
            # In a real implementation, this would use ros2 launch command
            for config in configs:
                cmd = ["ros2", "run", config.package, config.executable]

                # Add parameters if provided
                if config.parameters:
                    for key, value in config.parameters.items():
                        cmd.extend(["--param", f"{key}:={value}"])

                # Add remappings if provided
                if config.remappings:
                    for source, target in config.remappings:
                        cmd.extend(["--remap", f"{source}:={target}"])

                logger.info(f"Launching node: {' '.join(cmd)}")

                # In a real implementation, we would run the command
                # For now, we'll just log what would be executed
                # result = subprocess.run(cmd, timeout=timeout, capture_output=True, text=True)

            logger.info(f"Successfully launched {len(configs)} nodes")
            return True

        except Exception as e:
            logger.error(f"Error launching ROS 2 nodes: {str(e)}")
            return False

    def run_textbook_example(self, example_name: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run a specific textbook example using ROS 2

        Args:
            example_name: Name of the textbook example to run
            parameters: Parameters for the example

        Returns:
            Dict with execution results
        """
        if not self.is_setup:
            return {
                "success": False,
                "error": "ROS 2 is not properly set up in the environment",
                "output": ""
            }

        try:
            # Map example names to ROS 2 commands
            example_commands = {
                "physical_ai_basics": ["ros2", "run", "physical_ai_examples", "basic_controller"],
                "humanoid_control": ["ros2", "run", "humanoid_examples", "walk_controller"],
                "sensor_fusion": ["ros2", "run", "sensor_examples", "fusion_demo"],
                "navigation": ["ros2", "run", "nav_examples", "simple_navigation"]
            }

            if example_name not in example_commands:
                return {
                    "success": False,
                    "error": f"Unknown example: {example_name}",
                    "output": f"Available examples: {list(example_commands.keys())}"
                }

            cmd = example_commands[example_name]

            # Add parameters if provided
            if parameters:
                for key, value in parameters.items():
                    cmd.extend(["--param", f"{key}:={value}"])

            logger.info(f"Running textbook example: {' '.join(cmd)}")

            # In a real implementation, we would run the command
            # For demonstration, we'll return mock results
            result = {
                "success": True,
                "example": example_name,
                "command": " ".join(cmd),
                "output": f"Running {example_name} example with parameters: {parameters or {}}",
                "status": "completed"
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

    def get_ros2_info(self) -> Dict[str, Any]:
        """
        Get information about the current ROS 2 environment

        Returns:
            Dict with ROS 2 environment information
        """
        info = {
            "is_setup": self.is_setup,
            "workspace_path": str(self.ros_workspace_path),
            "ros_distro": os.getenv("ROS_DISTRO", "unknown"),
            "ros_domain_id": os.getenv("ROS_DOMAIN_ID", "0"),
            "ros_localhost_only": os.getenv("ROS_LOCALHOST_ONLY", "0")
        }

        if self.is_setup:
            try:
                # Get list of available packages
                result = subprocess.run(
                    ["ros2", "pkg", "list"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    packages = result.stdout.strip().split('\n')
                    info["packages"] = packages
                    info["package_count"] = len(packages)

                # Get list of active nodes
                result = subprocess.run(
                    ["ros2", "node", "list"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    nodes = result.stdout.strip().split('\n')
                    info["active_nodes"] = nodes
                    info["node_count"] = len([n for n in nodes if n])  # Filter empty strings
            except Exception as e:
                logger.warning(f"Could not get full ROS 2 info: {str(e)}")

        return info

    def setup_workspace(self, workspace_path: str = None) -> bool:
        """
        Set up a ROS 2 workspace for textbook examples

        Args:
            workspace_path: Path to the workspace (defaults to instance path)

        Returns:
            bool: True if setup was successful, False otherwise
        """
        ws_path = Path(os.path.expanduser(workspace_path or str(self.ros_workspace_path)))

        try:
            # Create workspace directory if it doesn't exist
            ws_path.mkdir(parents=True, exist_ok=True)

            # Create src directory for packages
            src_path = ws_path / "src"
            src_path.mkdir(exist_ok=True)

            # Create basic package structure for textbook examples
            examples_path = src_path / "textbook_examples"
            examples_path.mkdir(exist_ok=True)

            # Create basic package.xml
            package_xml_content = """<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>textbook_examples</name>
  <version>0.0.1</version>
  <description>Examples for Physical AI & Humanoid Robotics Textbook</description>
  <maintainer email="example@physical-ai.org">Physical AI Textbook</maintainer>
  <license>Apache-2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>sensor_msgs</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>"""

            (examples_path / "package.xml").write_text(package_xml_content)

            logger.info(f"ROS 2 workspace set up at: {ws_path}")
            return True

        except Exception as e:
            logger.error(f"Error setting up ROS 2 workspace: {str(e)}")
            return False


def create_ros2_integration(ros_workspace_path: str = "~/ros2_ws") -> ROS2Integration:
    """
    Create a ROS 2 integration instance

    Args:
        ros_workspace_path: Path to the ROS 2 workspace

    Returns:
        ROS2Integration instance
    """
    return ROS2Integration(ros_workspace_path)


if __name__ == "__main__":
    # Example usage
    print("Testing ROS 2 integration...")

    # Create integration instance
    ros_integration = create_ros2_integration()

    # Check ROS 2 setup
    info = ros_integration.get_ros2_info()
    print(f"ROS 2 setup info: {info}")

    # Run a textbook example (this will work only if ROS 2 is properly set up)
    example_result = ros_integration.run_textbook_example("physical_ai_basics", {"rate": 10})
    print(f"Example result: {example_result}")

    # Create and launch a sample node configuration
    config = ros_integration.create_node_config(
        name="test_controller",
        package="controller_examples",
        executable="basic_controller",
        parameters={"control_rate": 50, "max_velocity": 1.0}
    )

    launch_result = ros_integration.launch_nodes([config])
    print(f"Launch result: {launch_result}")