import os
import argparse
import torch
import numpy as np
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Merge models with weighted similarity")
parser.add_argument("a", type=str, help="Path to model a")
parser.add_argument("b", type=str, help="Path to model b")
parser.add_argument("--out", type=str, help="Output file name, without extension", default="merged", required=False)
parser.add_argument("--device", type=str, help="Device to use, defaults to cpu", default="cpu", required=False)
parser.add_argument("--without_vae", action="store_false", help="Do not merge VAE", required=False)
parser.add_argument("--dry", action="store_true", help="dry_run", default=False, required=False)
parser.add_argument("--soft", action="store_true", help="soft", default=False, required=False)
parser.add_argument("--s", type=float, help="share a b", default=.5, required=False)
args = parser.parse_args()


def loadModelWeights(mPath):
	model = torch.load(mPath, map_location=args.device)
	try: theta = model["state_dict"]
	except: theta = model
	return theta


output_file = f'{args.out}-{args.s}.ckpt'

step = 0
a, b = loadModelWeights(args.a), loadModelWeights(args.b)
sim = torch.nn.CosineSimilarity(dim=0)
sims = np.array([], dtype=np.float64)

for key in tqdm(a.keys(), desc="Stage 1/3"):
    # skip VAE model parameters to get better results
    if args.without_vae and "first_stage_model" in key: continue
    if "model" in key and key in b:
        simab = sim(a[key].to(torch.float64), b[key].to(torch.float64))
        sims = np.append(sims,simab.numpy())
sims = sims[~np.isnan(sims)]
#print(len(sims),sims.min(),sims.max())
sims = np.delete(sims, np.where(sims<np.percentile(sims, 1 ,method = 'midpoint')))
sims = np.delete(sims, np.where(sims>np.percentile(sims, 99 ,method = 'midpoint')))
print(len(sims),sims.min(),sims.max())
#sims = np.delete(sims, np.where(sims<sims.mean() - 3 * sims.std()))
#sims = np.delete(sims, np.where(sims>sims.mean() + 3 * sims.std()))
#print(len(sims),sims.min(),sims.max())


i = -1
for key in tqdm(a.keys(), desc="Stage 2/3"):
    # skip VAE model parameters to get better results
    if args.without_vae and "first_stage_model" in key: continue
    if "model" in key and key in b:
        i+=1
        simab = sim(a[key].to(torch.float32), b[key].to(torch.float32))
        k = (simab - sims.min())/(sims.max() - sims.min())
        k = k - args.s
        k = k.clip(min=.0,max=1.)
        if args.soft:
            a[key] = a[key] * (1 - k) + b[key] * k
        else:
            a[key] = a[key] * k + b[key] * (1 - k)
        a[key] = a[key].to(torch.float16)
for key in tqdm(b.keys(), desc="Stage 3/3"):
	if "model" in key and key not in a: a[key] = b[key]

if args.dry == 0:
    print("Saving...")
    torch.save({"state_dict": a}, output_file)

print("Done!")