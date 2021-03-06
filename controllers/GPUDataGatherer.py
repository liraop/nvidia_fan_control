from abc import ABC, abstractmethod
from utils.parsers import command_parser

class GPUDataFetcher(ABC):
    """
    A class/interface/metaclass to gather data from GPU.

    This design choice was made to promote the use both nvidia-smi and nvidia-settings commands
    as well any other agent to gather data from the actual hardware GPU.
    """

    @abstractmethod
    def get_gpu_count(self):
        """
        Get local machine total attached gpu devices

        Returns:
            Total attached GPU count

        """
        pass

    @abstractmethod
    def get_gpu_info(self, slot):
        """
        Get identification from GPU in `slot`

        Returns:
            (slot,name) tuple

        """
        pass

    @abstractmethod
    def get_gpu_temperature(self, slot):
        """
        Get core temperature from GPU in `slot`

        Returns:
            Temperature in Celcius
        """
        pass

    @abstractmethod
    def get_gpu_fanspeed(self, slot):
        """
        Get fan speed from GPU in `slot`

        Returns:
            Fan speed in percentage
        """

    @abstractmethod
    def get_gpu_pm(self, slot):
        """
        Get persistence mode status from GPU in `slot`

        Returns:
            Boolean
        """
class SMIFetcher(GPUDataFetcher):
    """
    Fetching data using NVIDIA SMI commands
    """

    def get_gpu_count(self):

        return int(command_parser("nvidia-smi --query-gpu=count --format=csv,noheader"))


    def get_gpu_info(self, slot):

        command = "nvidia-smi -i %d --query-gpu=name --format=csv,noheader" % slot
        gpu_data = (slot, command_parser(command).strip())

        return gpu_data

    def get_gpu_temperature(self, slot):

        command = "nvidia-smi -i %d --query-gpu=temperature.gpu --format=csv,noheader" % slot
        temperature = command_parser(command).strip()

        return temperature

    def get_gpu_fanspeed(self, slot):

        command = "nvidia-smi -i %d --query-gpu=fan.speed --format=csv,noheader,nounits" % slot
        fanspeed = command_parser(command).strip()

        return fanspeed

    def get_gpu_pm(self, slot):

        command = "nvidia-smi -i %d --query-gpu=persistence_mode --format=csv,nohead,nounits" % slot
        pm = command_parser(command)

        return pm
