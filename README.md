## Algorithm that allows you to mix models without loss of quality. 

**TLDR;** When mixing, the weights closest to the weights of the original model are chosen. When combining three models (a,b,c), the algorithm takes the nearest weights from models b or c (mixes them (b and c)). The new weights are added.

## Algorithm

```
a[key] = c[key] * (abs(a[key] - args.alpha*b[key]) > abs(a[key] - args.beta*c[key])) + b[key] * (abs(a[key] - args.alpha*b[key]) <= abs(a[key] - args.beta*c[key]))
```
example:
```
a[0.2,-.02]

b[0.25,-0.06]

c[0.3,-.03]

result tensor [0.25,-0.03]
```

## Usage

```
python3 losslessmix.py colorful_v12_RC1.ckpt liberty.ckpt has3dkx.ckpt --out tst

```

## Two models merging

 - merge models a + b with classic weighted sum
 - it will be your reference, "average" model ab
 - now merge models with lossless,  ab =  a || b: `losslessmix.py ab a b --out bestfrom_a_or_b`
 - ...
 - profit

## Hints

 - merging fp32 with fp16 probably bad idea, use prune
 - if model b matrix [0.001,-0.001] very different from c [0.005,-0.005] - use alpha/beta, or find more similar model

## Disadvantages

 - Models must have a similar order of weights 
 - Use --dry mode for estimates of the similarity of the weights

## Advantages

 - Blending without loss of quality
 - More variety of mix
 - More colorful

## Example

 [Colorful](https://civitai.com/models/7279/colorful)
 ![Colorful](examples/colorful.png?raw=true)

 [Liberty](https://civitai.com/models/5935/liberty)
  ![Liberty](examples/liberty.png?raw=true)

 [has3dkx](https://civitai.com/models/2504/handas-3dkx-11)
  ![has3dkx](examples/has3dkx.png?raw=true)

 Weighted Sum merge (liberty + has3dkx)
  ![ws05](examples/ws05.png?raw=true)

 **LossLessMix (colorful + liberty + has3dkx)**
  ![mindif](examples/mindif.png?raw=true)

## Playing with alpha/beta

Take a look to the root level tenzors:
```
a:tensor([-17.9531,   7.5273,   9.1172,  ...,  -2.1504, -15.6719,  17.5625],
       dtype=torch.float16)
b:tensor([-18.7969,   8.0000,   9.6016,  ...,  -2.3867, -16.4219,  18.5000],
       dtype=torch.float16)
c:tensor([-17.9688,   7.3828,   9.6328,  ...,  -2.3691, -15.4766,  17.6719],
       dtype=torch.float16)
```
a & c in same space, but b - not, let's try to normalize, add some alpha 0.95
```
python3 losslessmix.py colorful_v11.ckpt liberty.ckpt has3dkx.ckpt --out tst --beta 1.0 --dry --alpha 0.95
```
root tenzors
```
step:1
a:tensor([-17.9531,   7.5273,   9.1172,  ...,  -2.1504, -15.6719,  17.5625],
       dtype=torch.float16)
b:tensor([-17.8594,   7.6016,   9.1172,  ...,  -2.2676, -15.5938,  17.5625],
       dtype=torch.float16)
c:tensor([-17.9688,   7.3828,   9.6328,  ...,  -2.3691, -15.4766,  17.6719],
       dtype=torch.float16)
```
 **LossLessMix (liberty * 0.95)**
```
python3 losslessmix.py colorful_v11.ckpt liberty.ckpt has3dkx.ckpt --out tst --alpha 0.95 
```
  ![alpha](examples/alpha.png?raw=true)

Lets play with beta (just for fun)

```
python3 losslessmix.py colorful_v11.ckpt liberty.ckpt has3dkx.ckpt --out tst4 --beta 1.1
```
 **LossLessMix (has3dkx * 1.2)**

  ![beta](examples/beta.png?raw=true)
# Prompt:
```
modelshoot style, (extremely detailed CG unity 8k wallpaper), full shot body photo of the most beautiful artwork in the world, medieval armor, professional majestic oil painting by Ed Blinkey, Atey Ghailan, Studio Ghibli, by Jeremy Mann, Greg Manchess, Antonio Moro, trending on ArtStation, trending on CGSociety, Intricate, High Detail, Sharp focus, dramatic, photorealistic painting art by midjourney and greg rutkowski
Negative prompt: deformed, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, ugly, disgusting, poorly drawn hands, missing limb, floating limbs, disconnected limbs, malformed hands, blurry, ((((mutated hands and fingers)))), watermark, watermarked, oversaturated, censored, distorted hands, amputation, missing hands, obese, doubled face, double hands, b&w, black and white, sepia
Steps: 28, Sampler: DPM++ 2M Karras, CFG scale: 7, Seed: 0, Size: 576x832, Model hash: 277a582c32, ENSD: 31337, Script: X/Y/Z plot, X Type: Seed, X Values: "0,1,10000,393076097", Fixed X Values: "0, 1, 10000, 393076097"
```
 Colorful model (created wthout merging, only with mixing)

https://civitai.com/models/7279/colorful

 ## Credits

Also implemented the maxdiff algorithm proposed by https://www.reddit.com/user/Another__one/ here https://www.reddit.com/r/StableDiffusion/comments/1012lto/comment/j7aoyso/?context=3


Can be applied to mix models oriented for different tasks (landscapes + 3d), when mixing similar models it can lead to unexpected (but fun!) results

MaxDifMix (colorful + liberty + has3dkx)
![maxdif](examples/maxdiff.png?raw=true)

But it work well then merge redshiftdiffusion with landscape model, try "Ford mustang at night forest"

## PS

Unfortunately I am limited in the speed of algorithm development (macbook air m1), I would be happy if you find this algorithm useful. My Doge Wallet: DEw2DR8C7BnF8GgcrfTzUjSnGkuMeJhg83