from .base import Base


class Contract(Base):
    """Helper class containing all contract module methods."""

    params = {"module": "contract"}

    def get_contract_abi(self, address):
        """Get the Application Binary Interface (ABI) of verified smart contracts."""
        params = self.get_params(action="getabi", address=address)
        return self.request(params)

    def get_contract_source(self, address):
        """Get the Solidity contract source code of verified smart contracts."""
        params = self.get_params(action="getsourcecode", address=address)
        return self.request(params)

    # TODO
    def verify_source_code(self):
        pass

    def verify_proxy_contract(self):
        pass
