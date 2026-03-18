#!/usr/bin/env node
/**
 * Code-chunk wrapper for MatClaw RAG.
 * Uses tree-sitter to produce contextualizedText with scope chain.
 *
 * Usage: node chunk_with_context.mjs <sources_dir> <output_jsonl> <max_chunk_bytes> [packages...]
 */
import { readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { chunkBatch } from "code-chunk";

const EXT_OK = new Set([".py", ".pyi"]);
const IGNORE_DIRS = new Set([".git", "__pycache__", ".venv", "node_modules", ".tox", ".eggs"]);

async function walk(rootDir) {
  const out = [];
  async function rec(dir) {
    let entries;
    try {
      entries = await readdir(dir, { withFileTypes: true });
    } catch (e) {
      // Skip unreadable directories
      return;
    }
    for (const e of entries) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) {
        if (IGNORE_DIRS.has(e.name)) continue;
        await rec(p);
      } else if (e.isFile()) {
        if (EXT_OK.has(path.extname(e.name))) out.push(p);
      }
    }
  }
  await rec(rootDir);
  return out;
}

// Parse CLI args
const sourcesDir = process.argv[2];
const outPath = process.argv[3];
const maxChunkBytes = parseInt(process.argv[4] || "3200", 10);
const packages = process.argv.slice(5);

if (!sourcesDir || !outPath || packages.length === 0) {
  console.error("Usage: node chunk_with_context.mjs <sources_dir> <output.jsonl> <max_bytes> pkg1 pkg2 ...");
  process.exit(1);
}

let jsonl = "";
let totalChunks = 0;

for (const pkg of packages) {
  const pkgDir = path.join(sourcesDir, pkg);
  let files;
  try {
    files = await walk(pkgDir);
  } catch (e) {
    console.log(`  ${pkg}: directory not found, skipping`);
    continue;
  }

  if (files.length === 0) {
    console.log(`  ${pkg}: no .py files found`);
    continue;
  }

  const batchInputs = [];
  for (const fp of files) {
    try {
      const code = await readFile(fp, "utf8");
      batchInputs.push({ filepath: fp, code });
    } catch (e) {
      // Skip unreadable files
    }
  }

  if (batchInputs.length === 0) {
    console.log(`  ${pkg}: no readable files`);
    continue;
  }

  let results;
  try {
    results = await chunkBatch(batchInputs, {
      maxChunkSize: maxChunkBytes,
      contextMode: "full",
      siblingDetail: "signatures",
      overlapLines: 3,
      concurrency: 10,
    });
  } catch (e) {
    console.error(`  ${pkg}: chunkBatch failed: ${e.message}`);
    continue;
  }

  let chunkCount = 0;
  for (const r of results) {
    if (r.error) continue;
    for (const c of r.chunks) {
      const relPath = path.relative(sourcesDir, r.filepath);
      jsonl += JSON.stringify({
        software: pkg,
        filepath: relPath,
        index: c.index,
        lineRange: c.lineRange,
        contextualizedText: c.contextualizedText,
        text: c.text,
        context: c.context,
      }) + "\n";
      chunkCount++;
    }
  }
  console.log(`  ${pkg}: ${chunkCount} chunks from ${batchInputs.length} files`);
  totalChunks += chunkCount;
}

await writeFile(outPath, jsonl, "utf8");
console.log(`Wrote ${totalChunks} total chunks to ${outPath}`);
