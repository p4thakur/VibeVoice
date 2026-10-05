"""Bulk-generate audio for every .txt script in a folder using one voice sample.

Usage:
  .venv313/bin/python batch_generate.py --scripts_dir scripts --output_dir output_audio --voice prateek_1

Scripts may be plain text or use "Speaker 1: ..." lines (only Speaker 1's voice is used).
Files whose output WAV already exists are skipped, so an interrupted run can be resumed.
"""
import argparse
import os
import re
import time

import torch

from vibevoice.modular.modeling_vibevoice_inference import VibeVoiceForConditionalGenerationInference
from vibevoice.processor.vibevoice_processor import VibeVoiceProcessor

HERE = os.path.dirname(os.path.abspath(__file__))


def normalize_script(text: str) -> str:
    """Return the script as 'Speaker 1: ...' lines (single-voice)."""
    text = text.replace("’", "'").strip()
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    out, cur = [], None
    for line in lines:
        m = re.match(r"^Speaker\s+\d+:\s*(.*)$", line, re.IGNORECASE)
        if m:
            if cur:
                out.append(cur)
            cur = m.group(1).strip()
        else:
            cur = f"{cur} {line}" if cur else line
    if cur:
        out.append(cur)
    return "\n".join(f"Speaker 1: {t}" for t in out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model_path", default="vibevoice/VibeVoice-1.5B")
    p.add_argument("--scripts_dir", default=os.path.join(HERE, "scripts"))
    p.add_argument("--output_dir", default=os.path.join(HERE, "output_audio"))
    p.add_argument("--voice", default="prateek_1", help="file name (no extension) in demo/voices")
    p.add_argument("--cfg_scale", type=float, default=1.3)
    p.add_argument("--steps", type=int, default=10)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--min_num", type=int, default=None,
                   help="only process scripts whose leading number (e.g. 14_name.txt) is >= this")
    args = p.parse_args()

    voice_path = os.path.join(HERE, "demo", "voices", f"{args.voice}.wav")
    if not os.path.exists(voice_path):
        raise SystemExit(f"Voice sample not found: {voice_path}")
    os.makedirs(args.output_dir, exist_ok=True)

    files = sorted(f for f in os.listdir(args.scripts_dir) if f.lower().endswith(".txt"))
    if args.min_num is not None:
        files = [f for f in files
                 if (m := re.match(r"^(\d+)", f)) and int(m.group(1)) >= args.min_num]
    todo = [f for f in files
            if not os.path.exists(os.path.join(args.output_dir, os.path.splitext(f)[0] + ".wav"))]
    print(f"{len(files)} scripts found, {len(todo)} to generate, voice={args.voice}")
    if not todo:
        return

    device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
    dtype = {"cuda": torch.bfloat16, "mps": torch.float16, "cpu": torch.float32}[device]
    processor = VibeVoiceProcessor.from_pretrained(args.model_path)
    model = VibeVoiceForConditionalGenerationInference.from_pretrained(
        args.model_path, torch_dtype=dtype, attn_implementation="sdpa", device_map=None)
    model.to(device)
    model.eval()
    model.set_ddpm_inference_steps(num_steps=args.steps)

    for i, f in enumerate(todo, 1):
        name = os.path.splitext(f)[0]
        out_path = os.path.join(args.output_dir, name + ".wav")
        script = normalize_script(open(os.path.join(args.scripts_dir, f), encoding="utf-8").read())
        if not script:
            print(f"[{i}/{len(todo)}] {f}: empty, skipped")
            continue
        if args.seed is not None:
            torch.manual_seed(args.seed)
        print(f"[{i}/{len(todo)}] {f} ...", flush=True)
        try:
            inputs = processor(text=[script], voice_samples=[[voice_path]], padding=True,
                               return_tensors="pt", return_attention_mask=True)
            inputs = {k: (v.to(device) if torch.is_tensor(v) else v) for k, v in inputs.items()}
            t0 = time.time()
            outputs = model.generate(**inputs, max_new_tokens=None, cfg_scale=args.cfg_scale,
                                     tokenizer=processor.tokenizer,
                                     generation_config={"do_sample": False},
                                     verbose=False, is_prefill=True)
            processor.save_audio(outputs.speech_outputs[0], output_path=out_path)
            dur = outputs.speech_outputs[0].shape[-1] / 24000
            print(f"    saved {out_path} ({dur:.1f}s audio in {time.time() - t0:.0f}s)", flush=True)
        except Exception as e:
            print(f"    FAILED {f}: {type(e).__name__}: {e}", flush=True)
        if device == "mps":
            torch.mps.empty_cache()


if __name__ == "__main__":
    main()
