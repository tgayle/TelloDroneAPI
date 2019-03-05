from typing import Optional
from abc import ABC, abstractmethod

DroneResponse: Optional[str] = Optional[str]
"""
Wrapper for the expected responses from any calls to the drone. Either a string should be returned
in case of direct responses from the drone, or None if there was an issue getting a response at all.
"""


class Drone(ABC):
    def __init__(self):
        self.connected = False
        self.silent_errors = False
        """
        If this is set to true, then any commands send to the drone while not connected will fail silently.
        """

        self.control = None
        self.connection = None
        self.drone_response = None

    """
    A base class representing a drone. Implementations of Drones should be subclasses of this class.
    """
    @abstractmethod
    async def connect(self) -> bool:
        """
        Attempts to connect to a drone device.
        :return: True if successfully connected, otherwise False
        """
        pass

    def send_command(self, message: str, ignore_error=False) -> None:
        """
        Sends a message to a drone device.
        :param ignore_error: bool True if drone should be sent a message regardless of connection
            status.
        :param message: str The message or command to send to the drone.
        :return: None
        """
        if not self.silent_errors and not self.connected and not ignore_error:
            raise RuntimeError("This drone is not connected.")

    @abstractmethod
    async def await_drone_response(self, timeout: int) -> DroneResponse:
        """
        Waits for a response from the drone to verify a command has been received, optionally timing
        out if there's no response.
        :param timeout: int The amount of time, in seconds to wait before considering this a timeout
        :return: The string response from the drone, or None if there is no response.
        """
        pass

    @abstractmethod
    async def send_command_and_await(self, message: str, timeout: int = None) -> DroneResponse:
        """
        Combines send_command and await_drone_response into one method, accepting a timeout length
        if one is provided.
        :param message: The command to send to the device
        :param timeout: int The amount of time, in seconds to wait before timing out, or None if
            the command should block until there's a response.
        :return: The string response from the drone or None if there is no response
        """
        pass
