from distribrewed_core.base.master import BaseMaster

from masters.signals import worker_registered, handle_pong, worker_de_registered


# noinspection SpellCheckingInspection
class DistribrewedMaster(BaseMaster):
    def register_worker(self, worker_id, worker_info, worker_methods, reload_queues=False):
        super(DistribrewedMaster, self).register_worker(
            worker_id,
            worker_info,
            worker_methods,
            reload_queues=reload_queues
        )
        worker_registered.send(
            sender=self.__class__,
            worker_id=worker_id,
            worker_info=worker_info,
            worker_methods=worker_methods
        )
        self.ping_worker(worker_id)

    def de_register_worker(self, worker_id, worker_info):
        super(DistribrewedMaster, self).de_register_worker(
            worker_id,
            worker_info,
        )
        worker_de_registered.send(
            sender=self.__class__,
            worker_id=worker_id,
            worker_info=worker_info,
        )

    def handle_pong(self, worker_id):
        super(DistribrewedMaster, self).handle_pong(worker_id)
        handle_pong.send(
            sender=self.__class__,
            worker_id=worker_id,
        )

    def send_telgram_message(self, message):
        self._call_worker_method(
            worker_id='pi_telegram',
            method='telegram_bot_send_message',
            args=[message]
        )
