import logging

from airgap_mirrors.exceptions import AirgapMirrorError
from airgap_mirrors.external import ReceiptConfirmer

logger: logging.Logger = logging.getLogger(__name__)


class ConfirmCommand:
    def __init__(self, confirmer: ReceiptConfirmer) -> None:
        self._confirmer: ReceiptConfirmer = confirmer

    def run(self) -> list[str]:
        try:
            confirmed: int = self._confirmer.confirm()
        except AirgapMirrorError as failure:
            logger.error("confirm failed: %s", failure)
            return ["confirm"]
        logger.info("%d repositories confirmed; the next export starts from them", confirmed)
        return []
