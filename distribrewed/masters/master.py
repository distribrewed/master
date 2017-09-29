from distribrewed_core.base.master import ScheduleMaster

from masters.signals import worker_registered, handle_pong, worker_de_registered, schedule_finished
# noinspection SpellCheckingInspection
from workers.models import Worker


class DistribrewedMaster(ScheduleMaster):
    def _register_worker(self, worker_id, worker_info, worker_methods, reload_queues=False):
        super(DistribrewedMaster, self)._register_worker(
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

    def _de_register_worker(self, worker_id, worker_info):
        super(DistribrewedMaster, self)._de_register_worker(
            worker_id,
            worker_info,
        )
        worker_de_registered.send(
            sender=self.__class__,
            worker_id=worker_id,
            worker_info=worker_info,
        )

    def _handle_pong(self, worker_id):
        super(DistribrewedMaster, self)._handle_pong(worker_id)
        handle_pong.send(
            sender=self.__class__,
            worker_id=worker_id,
        )

    def _handle_worker_finished(self, worker_id, schedule_id):
        schedule_finished.send(
            sender=self.__class__,
            worker_id=worker_id,
            schedule_id=schedule_id
        )

    def send_telgram_message(self, message):
        available_workers = Worker.objects.filter(type='TelegramWorker')
        assert len(available_workers) > 0, 'No Telegram workers available'
        self._call_worker_method(
            worker_id=available_workers[0].id,
            method='send_message',
            args=[message]
        )
