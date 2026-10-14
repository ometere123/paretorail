# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Optional consumer of ParetoRail head-pinned adopted amendments; no frontend."""
from genlayer import *

@gl.contract_interface
class IParetoRailView:
    class View:
        def is_adopted(self, proposal_id: u256, expected_head: str) -> bool: ...


class AmendedActionGate(gl.Contract):
    paretorail_address: Address
    proposal_id: u256
    approved_head_hash: str
    performed: bool

    def __init__(self, paretorail_address: Address, proposal_id: u256, approved_head_hash: str):
        self.paretorail_address = paretorail_address
        self.proposal_id = proposal_id
        self.approved_head_hash = approved_head_hash
        self.performed = False

    @gl.public.write
    def perform(self) -> None:
        if self.performed:
            raise gl.vm.UserError('ALREADY_PERFORMED')
        rail = IParetoRailView(self.paretorail_address)
        if not rail.view().is_adopted(self.proposal_id, self.approved_head_hash):
            raise gl.vm.UserError('AMENDMENT_NOT_CURRENTLY_ADOPTED')
        self.performed = True

    @gl.public.view
    def was_performed(self) -> bool:
        return self.performed
