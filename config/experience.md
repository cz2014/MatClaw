# Experience Notes

Operational lessons learned from past runs. Auto-injected into every prompt.
Both humans and the agent (via write_experience tool) can add notes.

## 1. Do NOT define custom @job functions in the agent sandbox

The @job decorator transforms a function into a jobflow Job factory -- calling
it returns an OutputReference placeholder, not a computed result. The function
body never executes locally; it would only run on the remote worker, where
sandbox-defined functions don't exist. Instead, use the provided tools
(train_deepmd, batch_static_eval, wait_for_jobflow) which are pre-registered
as remote jobs. For data merging, pass a list of sources to train_deepmd's
data_source parameter.

## 2. MongoDB has a 16 MB document size limit

train_deepmd pre-check rejects inline dicts above ~10 MB (~800 frames of
90-atom structures). To bypass: write data locally, use remote_put to upload,
and pass the remote path string instead of inline data. Both train_deepmd and
batch_static_eval accept remote path strings.

Default upload directory: /pscratch/sd/c/cz2014/agent_tmp_dir
(avoid /tmp -- node-local and periodically cleaned).

## 3. Use a separate MD trajectory for held-out evaluation

When constructing a held-out test set from MD trajectories, generate a SEPARATE
MD trajectory for evaluation. Do NOT split frames from the training trajectories
(e.g., every Nth frame). Adjacent frames in an MD trajectory are highly
correlated and do not constitute an independent test.


## 4. Avoid explicit repr() calls in sandbox code

The restricted interpreter may reject explicit repr(...) as a forbidden function call, especially inside exception handlers. Prefer f-strings like f'{exc}' or just print the object directly instead of calling repr explicitly.


## 5. Avoid accessing dunder attributes directly in sandbox inspection

The restricted interpreter may block direct access to dunder attributes like __init__. When inspecting classes, prefer inspect.signature(ClassName) for the constructor signature, inspect.signature(ClassName.make) for regular methods, and inspect.getsource(ClassName) instead of referencing ClassName.__init__.
