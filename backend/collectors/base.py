from abc import ABC, abstractmethod


class BaseCollector(ABC):
    def __init__(self, symbol: str):
        self.symbol = symbol

    @abstractmethod
    async def fetch_snapshot(self) -> dict:
        """
        Снимает один «снэпшот» текущего стакана через REST API.
        """
        pass
    

    @abstractmethod
    async def listen_stream(self, on_message):
        """
        Слушает WebSocket, вызывает on_message(normalized_data) при каждом обновлении.
        """
        pass