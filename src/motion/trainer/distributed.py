from torch.utils.data import DistributedSampler

from trainer.base import Trainer
from trainer.formatter import TrainingMessageFormatter


class DistributedTrainer(Trainer):
    def __init__(
            self,
            model,
            training_set,
            batch_size,
            learning_rate,
            rank,
            world_size,
            validation_set=None,
            test_set=None,
            checkpoint_dir=None,
    ):
        sampler = DistributedSampler(
            training_set,
            num_replicas=world_size,
            rank=rank,
            shuffle=True
        )
        if rank != 0:
            test_set = None
            validation_set = None

        super().__init__(
            model=model,
            training_set=training_set,
            validation_set=validation_set,
            test_set=test_set,
            batch_size=batch_size,
            learning_rate=learning_rate,
            checkpoint_dir=checkpoint_dir,
            sampler=sampler
        )

        self.rank = rank

    def _get_formatter(self, epochs):
        return TrainingMessageFormatter(epochs, self.rank)

    def _save_checkpoint(self, epoch, loss, best=False):
        if self.rank == 0:
            super()._save_checkpoint(epoch, loss, best=best)