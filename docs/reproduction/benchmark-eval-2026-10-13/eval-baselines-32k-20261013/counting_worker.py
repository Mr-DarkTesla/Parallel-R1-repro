from vllm.worker.worker import Worker
import torch
class CountingWorker(Worker):
    def load_model(self):
        super().load_model()
        self.physical_counter=torch.zeros((),dtype=torch.int64,device=self.device)
        self.counter_events=[]
        def tick(module,args):self.physical_counter.add_(1)
        self.model_runner.model.register_forward_pre_hook(tick)
    def execute_model(self,execute_model_req=None):
        output=super().execute_model(execute_model_req)
        if execute_model_req is not None and execute_model_req.seq_group_metadata_list:
            self.counter_events.append(dict(request_ids=[g.request_id for g in execute_model_req.seq_group_metadata_list],is_prompt=[g.is_prompt for g in execute_model_req.seq_group_metadata_list]))
        return output
    def reset_physical_counter(self):
        self.physical_counter.zero_();self.counter_events=[]
    def read_physical_counter(self):
        return dict(actual_global_model_forwards=int(self.physical_counter.item()),events=self.counter_events)
