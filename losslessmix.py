import os
import argparse
import torch
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Merge three models with max diff")
parser.add_argument("a", type=str, help="Path to model 0")
parser.add_argument("b", type=str, help="Path to model 1")
parser.add_argument("c", type=str, help="Path to model 2")
parser.add_argument("--out", type=str, help="Output file name, without extension", default="merged", required=False)
parser.add_argument("--device", type=str, help="Device to use, defaults to cpu", default="cpu", required=False)
parser.add_argument("--without_vae", action="store_false", help="Do not merge VAE", required=False)
parser.add_argument("--dry", action="store_true", help="dry_run", default=False, required=False)
parser.add_argument("--alpha", type=float, help="multiply model b", default=1.0, required=False)
parser.add_argument("--beta", type=float, help="multiply model c", default=1.0, required=False)
parser.add_argument("--maxdiff", action="store_true", help="max diff", default=False, required=False)

args = parser.parse_args()


def loadModelWeights(mPath):
	model = torch.load(mPath, map_location=args.device)
	try: theta = model["state_dict"]
	except: theta = model
	return theta


output_file = f'{args.out}.ckpt'

step = 0
a, b, c = loadModelWeights(args.a), loadModelWeights(args.b), loadModelWeights(args.c)

for key in tqdm(a.keys(), desc="Stage 1/3"):
    # skip VAE model parameters to get better results
    if args.without_vae and "first_stage_model" in key: continue
    if "model" in key and key in b and key in c:
        if step == 1 or step == 2:
            print(f'step:{step}')
            print(f'a:{1000*a[key]}')
            print(f'b:{1000*b[key]}')
            print(f'c:{1000*c[key]}')
        step+=1
        if args.maxdiff == 1:
            a[key] = b[key] * (abs(a[key] - args.alpha*b[key]) > abs(a[key] - args.beta*c[key])) + c[key] * (abs(a[key] - args.alpha*b[key]) <= abs(a[key] - args.beta*c[key]))
        else:
            a[key] = c[key] * (abs(a[key] - args.alpha*b[key]) > abs(a[key] - args.beta*c[key])) + b[key] * (abs(a[key] - args.alpha*b[key]) <= abs(a[key] - args.beta*c[key]))
for key in tqdm(b.keys(), desc="Stage 2/3"):
	if "model" in key and key not in a: a[key] = b[key]
for key in tqdm(c.keys(), desc="Stage 3/3"):
	if "model" in key and key not in a: a[key] = c[key]

if args.dry == 0:
    print("Saving...")
    torch.save({"state_dict": a}, output_file)

print("Done!")