# Python RQ失败了的任务怎么办？

我们使用 RQ执行任务的时候，有的时候任务会失败，这个任务就会进入 failed_job_registry。你可以通过他找到所有失败的任务。

我们可以启动个 python，逐条输入脚本：

```python
from redis import Redis
redis_conn = Redis()
q = Queue(connection=redis_conn)
len(q.failed_job_registry)
```

我们就可以看到有多少失败的 job。

如果我们希望重新执行他们的话，我们可以执行下面这段把 job 重新放入队列：

```python
 for job_id in q.failed_job_registry.get_job_ids():
     job = q.failed_job_registry.requeue(job_id)
```

如果我们想要清理掉他们的话，可以删除他们：

```python
for job in q.failed_job_registry:
   print(job)
```

