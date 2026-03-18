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

