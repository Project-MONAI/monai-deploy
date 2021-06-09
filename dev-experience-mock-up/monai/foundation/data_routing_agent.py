from abc import ABC, abstractmethod
from timeloop import Timeloop
from datetime import timedelta, datetime


from monai.routing import DataRoutingService


class DataRoutingAgent:
    """
    Base class of Data routing agent that polls newly received dataset from the Data Routing Server
    """
    
    _timeloop = Timeloop()

    def __init__(self, name) -> None:
        """
        Sets up polling with DataRoutingService
        """
        self._agent_name = name
        self._interval = load_from_config()
        self._last_poll = datetime.now()
        self._api = DataRoutingService()

        if not _dev_mode():
            _timeloop.start(block=false)
        
    @_timeloop.job(interval=timedelta(seconds=1))
    def execute(self) -> None:
        """
        Polls any newly received instances from Data Routing Service
        """
        new_dataset = super.poll()
        result = self._api.get_since(self._last_poll)
        self._last_poll = datetime.now()
        self.execute(result)

    def _dev_mode(self) -> bool:
        """
        Returns if routing agent is running in development mode
        """
        return True

    @abstractmethod
    def execute(self, data):
        pass