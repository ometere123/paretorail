"""Windows compatibility for genlayer-test 0.29.2 Direct Mode.

The pinned runner keeps fd 0 open on the temporary message file until the VM
context is torn down.  Windows rejects unlinking that file during import,
although POSIX permits it.  Keep the file name until teardown on Windows;
contract execution, calldata, mocks, and assertions remain unchanged.
"""

import os
import tempfile

import pytest


@pytest.fixture(scope="session", autouse=True)
def _windows_direct_mode_loader_compatibility():
    if os.name != "nt":
        yield
        return

    import gltest.direct.loader as loader
    from gltest.direct.vm import VMContext

    original_inject = loader._inject_message_to_fd0
    original_cleanup = VMContext._cleanup_after_deactivate

    def inject_without_early_unlink(vm):
        try:
            from genlayer.py import calldata
            from genlayer.py.types import Address
        except ImportError:
            return original_inject(vm)

        sender = vm.sender
        if isinstance(sender, bytes):
            sender = Address(sender)
        contract = vm._contract_address
        if isinstance(contract, bytes):
            contract = Address(contract)
        origin = vm.origin
        if isinstance(origin, bytes):
            origin = Address(origin)

        message_data = {
            "contract_address": contract,
            "sender_address": sender,
            "origin_address": origin,
            "stack": [],
            "value": vm._value,
            "datetime": vm._datetime,
            "is_init": False,
            "chain_id": vm._chain_id,
            "entry_kind": 0,
            "entry_data": b"",
            "entry_stage_data": None,
        }
        encoded = calldata.encode(message_data)
        fd, path = tempfile.mkstemp()
        try:
            os.write(fd, encoded)
            os.lseek(fd, 0, os.SEEK_SET)
            vm._original_stdin_fd = os.dup(0)
            os.dup2(fd, 0)
            vm._paretorail_message_path = path
        finally:
            os.close(fd)

    def cleanup_after_deactivate(vm):
        path = getattr(vm, "_paretorail_message_path", None)
        try:
            original_cleanup(vm)
        finally:
            if path:
                try:
                    os.unlink(path)
                except FileNotFoundError:
                    pass
                vm._paretorail_message_path = None

    loader._inject_message_to_fd0 = inject_without_early_unlink
    VMContext._cleanup_after_deactivate = cleanup_after_deactivate
    try:
        yield
    finally:
        loader._inject_message_to_fd0 = original_inject
        VMContext._cleanup_after_deactivate = original_cleanup
