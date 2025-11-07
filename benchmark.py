import time, json, torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --- CONFIG ---
with open("config.json") as f:
    config = json.load(f)

# --- LOAD MODEL ---
load_args = {"device_map": "auto"}
if config.get("quantization") == "4bit":
    load_args["load_in_4bit"] = True
if config.get("torch_dtype"):
    load_args["torch_dtype"] = getattr(torch, config["torch_dtype"])

print("\033[96m" + "="*60)
print(f"🚀 BENCHMARKING MODEL: {config['model_name']}")
print("="*60 + "\033[0m")

tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
model = AutoModelForCausalLM.from_pretrained(config["model_name"], **load_args)

prompt = "Jelaskan teori relativitas secara singkat dan padat."
inputs = tokenizer(prompt, return_tensors="pt").to(config["device"])

# --- BENCHMARK LOOP ---
runs = 3
results = []
for i in range(runs):
    torch.cuda.synchronize()
    start = time.time()
    output = model.generate(**inputs, max_new_tokens=config["max_new_tokens"])
    torch.cuda.synchronize()
    end = time.time()

    input_tokens = inputs["input_ids"].shape[-1]
    output_tokens = output[0].shape[-1] - input_tokens
    total_time = end - start
    tps = output_tokens / total_time
    results.append(tps)
    print(f"\033[93mRun {i+1}: {output_tokens} tokens in {total_time:.2f}s  →  {tps:.2f} tok/s\033[0m")

# --- SUMMARY ---
avg_tps = sum(results) / len(results)
used = torch.cuda.memory_allocated() / 1e9
resv = torch.cuda.memory_reserved() / 1e9

print("\033[92m" + "\n" + "-"*60)
print("📊 GPU PERFORMANCE SUMMARY")
print("-"*60)
print(f" Model:         {config['model_name']}")
print(f" Quantization:  {config.get('quantization','none')}")
print(f" Device:        {config['device']}")
print(f" Avg Speed:     {avg_tps:.2f} tokens/s")
print(f" VRAM Used:     {used:.2f} GB")
print(f" VRAM Reserved: {resv:.2f} GB")
print("-"*60 + "\033[0m")
