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
parser.add_argument("--s", type=float, help="share of model a", default=.5, required=False)
args = parser.parse_args()


def loadModelWeights(mPath):
	model = torch.load(mPath, map_location=args.device)
	try: theta = model["state_dict"]
	except: theta = model
	return theta


output_file = f'{args.out}-{args.s}.ckpt'

a, b = loadModelWeights(args.a), loadModelWeights(args.b)
sim = torch.nn.CosineSimilarity(dim=0)

for key in tqdm(a.keys(), desc="Stage 1/1"):
    # prune vae
    if "first_stage_model" in key:
        a[key] = a[key].to(torch.float16)
        continue
    # not in b
    if not key in b:
        continue
    # merge not mergeble (2.0 with 1.5)?
    if (a[key].size() != b[key].size()):
        continue
    # unet merge
    if "model.diffusion_model" in key and key in b:
        sims = np.array([], dtype=np.float32)
        simab = sim(a[key].to(torch.float32), b[key].to(torch.float32))
        sims = np.append(sims,simab.detach().numpy())
        sims = sims[~np.isnan(sims)]
        sims = np.delete(sims, np.where(sims<np.percentile(sims, 1 ,method = 'midpoint')))
        sims = np.delete(sims, np.where(sims>np.percentile(sims, 99 ,method = 'midpoint')))
        if len(sims)!=1 and sims.min()!=sims.max():
            k = (simab - sims.min())/(sims.max() - sims.min())
            k = k - args.s
            k = k.clip(min=.0,max=1.)
            a[key] = a[key] * k + b[key] * (1 - k)
            a[key] = a[key].to(torch.float16)
            if args.dry == 1:
                print(len(sims),sims.min(),sims.max(),key)

if args.dry == 0:
    print("Saving...")
    torch.save({"state_dict": a}, output_file)

print("Done!")