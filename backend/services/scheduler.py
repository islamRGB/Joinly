import schedule
import threading
import time

class SchedulerService:
    def __init__(self):
        self.active = False
        self.thread = None
        self.jobs = []
    
    def start(self):
        self.active = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.active = False
        if self.thread:
            self.thread.join()
    
    def _run_scheduler(self):
        while self.active:
            schedule.run_pending()
            time.sleep(1)
    
    def add_job(self, interval_seconds: int, func, *args, **kwargs):
        job = schedule.every(interval_seconds).seconds.do(func, *args, **kwargs)
        self.jobs.append(job)
        return job
    
    def add_job_minutes(self, interval_minutes: int, func, *args, **kwargs):
        job = schedule.every(interval_minutes).minutes.do(func, *args, **kwargs)
        self.jobs.append(job)
        return job
    
    def remove_job(self, job):
        schedule.cancel_job(job)
        if job in self.jobs:
            self.jobs.remove(job)
    
    def clear_jobs(self):
        schedule.clear()
        self.jobs.clear()