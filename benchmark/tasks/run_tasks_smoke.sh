#!/usr/bin/env bash
# Smoke test: 5 models x 2 tasks = 10 runs
set -euo pipefail
cd "$(dirname "$0")/../.."

GEMINI_MODELS="gemini/gemini-2.0-flash gemini/gemini-2.5-flash gemini/gemini-3-flash-preview"
OPENAI_MODELS="gpt-4.1 gpt-5.4"
LIMIT=2
PASSED=0
FAILED=0

echo "=== Task smoke test: all models, --limit $LIMIT ==="
for model in $GEMINI_MODELS; do
    tag="${model##*/}"
    echo "--- $tag ---"
    if python benchmark/tasks/run_tasks_all.py --model "$model" --provider gemini \
        --limit $LIMIT; then
      PASSED=$((PASSED + 1))
    else
      echo "FAILED: $tag"
      FAILED=$((FAILED + 1))
    fi
done

for model in $OPENAI_MODELS; do
    tag="$model"
    echo "--- $tag ---"
    if python benchmark/tasks/run_tasks_all.py --model "$model" --provider openai \
        --limit $LIMIT; then
      PASSED=$((PASSED + 1))
    else
      echo "FAILED: $tag"
      FAILED=$((FAILED + 1))
    fi
done
echo "=== Smoke test done: $PASSED passed, $FAILED failed ==="
