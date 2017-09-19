from distribrewed_core.base.master import BaseMaster


class DistribrewedMaster(BaseMaster):
    def send_telgram_message(self, message):
        self._call_worker_method(
            worker_id='worker.pi_telegram',
            method='telegram_bot_send_message',
            args=[message]
        )
