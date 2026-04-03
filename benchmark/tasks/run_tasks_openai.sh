#!/usr/bin/env bash
# Production OpenAI task runs: 2 models x 1 config = 2 runs
# Run in Terminal 2 alongside run_tasks_gemini.sh in Terminal 1
set -euo pipefail
cd "$(dirname "$0")/../.."

MODELS="gpt-4.1 gpt-5.4"
RUN=0

echo "=== OpenAI task benchmark (2 runs) ==="
echo "Started: $(date)"
echo ""

for model in $MODELS; do
  RUN=$((RUN + 1))
  echo ""
  echo "===== [$RUN/2] $model ====="
  echo "Time: $(date)"

  python benchmark/tasks/run_tasks_all.py --model "$model" --provider openai
done

echo ""
echo "=== OpenAI task benchmark complete ==="
echo "Finished: $(date)"
