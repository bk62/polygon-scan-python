from .base import Base


class Block(Base):
    """Helper class containing all block module methods."""

    params = {"module": "block"}

    def get_block_rewards_by_block_number(self, blockno):
        params = self.get_params(action="getblockreward", blockno=blockno)
        return self.request(params)

    def get_estimated_block_countdown(self, blockno):
        params = self.get_params(action="getblockcountdown", blockno=blockno)
        return self.request(params)

    def get_block_number_by_timestamp(self, timestamp, closest="before"):
        params = self.get_params(
            action="getblocknobytime", timestamp=timestamp, closest=closest
        )
        return self.request(params)

    # TODO
    # Pro tier endpoints
