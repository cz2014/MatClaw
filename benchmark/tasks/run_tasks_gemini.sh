#!/usr/bin/env bash
# Production Gemini task runs: 3 models x 1 config = 3 runs
# Run in Terminal 1 alongside run_tasks_openai.sh in Terminal 2
set -euo pipefail
cd "$(dirname "$0")/../.."

MODELS="gemini/gemini-2.0-flash gemini/gemini-2.5-flash gemini/gemini-3-flash-preview"
RUN=0

echo "=== Gemini task benchmark (3 runs) ==="
echo "Started: $(date)"
echo ""

for model in $MODELS; do
  RUN=$((RUN + 1))
  tag="${model##*/}"
  echo ""
  echo "===== [$RUN/3] $tag ====="
  echo "Time: $(date)"

  # Use --delay 1.0 for deprecated gemini-2.0-flash (conservative rate limit)
  delay_flag=""
  if [ "$model" = "gemini/gemini-2.0-flash" ]; then
    delay_flag="--delay 1.0"
  fi

  python benchmark/tasks/run_tasks_all.py --model "$model" --provider gemini $delay_flag
done

echo ""
echo "=== Gemini task benchmark complete ==="
echo "Finished: $(date)"
