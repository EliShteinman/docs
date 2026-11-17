import logging
from pathlib import Path

from airgap_mirrors.exceptions import TransferError
from airgap_mirrors.models import ExportLedger, ImportReceipt
from airgap_mirrors.storage import JsonModelStore, LedgerLocator
from airgap_mirrors.transfer import TransferLayout

logger: logging.Logger = logging.getLogger(__name__)


class ReceiptConfirmer:
    """Online side. Reads the receipt the import wrote and marks those states as GitLab's,
    so the next export only carries what came after them."""

    def __init__(self, ledgers: LedgerLocator, layout: TransferLayout, store: JsonModelStore) -> None:
        self._ledgers: LedgerLocator = ledgers
        self._layout: TransferLayout = layout
        self._store: JsonModelStore = store

    def confirm(self) -> int:
        receipt: ImportReceipt | None = self._store.load(self._layout.receipt_path, ImportReceipt)
        if receipt is None:
            raise TransferError(f"no receipt at {self._layout.receipt_path}: copy it back from the import machine")
        confirmed: int = 0
        for entry in receipt.entries:
            ledger_path: Path = self._ledgers.export_ledger(entry.name)
            ledger: ExportLedger | None = self._store.load(ledger_path, ExportLedger)
            if ledger is not None and entry.state_id in ledger.pending:
                self._store.save(ledger_path, ledger.with_confirmed(entry.state_id))
                logger.info("%s: confirmed", entry.name)
                confirmed += 1
            elif ledger is not None and ledger.confirmed and ledger.confirmed.state_id == entry.state_id:
                logger.debug("%s: already confirmed", entry.name)
            else:
                logger.warning("%s: the receipt names a transfer this machine did not export; ignored", entry.name)
        return confirmed
