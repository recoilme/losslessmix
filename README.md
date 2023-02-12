## An experimental algorithm that allows you to mix models without loss of quality. 

When mixing, the weights closest to the weights of the original model are chosen

## Algorithm

```
a[key] = c[key] * (abs(a[key] - args.alpha*b[key]) > abs(a[key] - args.beta*c[key])) + b[key] * (abs(a[key] - args.alpha*b[key]) <= abs(a[key] - args.beta*c[key]))
```

## Disadvantages

 - Models must have a similar order of weights 
 - Use --dry mode for estimates of the similarity of the weights

## Advantages

 - Blending without loss of quality
 - More variety of mix
 - More colorful

## Example

 Colorful
 ![Colorful](examples/colorful.png?raw=true)

 Liberty
  ![Liberty](examples/liberty.png?raw=true)

 has3dkx
  ![has3dkx](examples/has3dkx.png?raw=true)

 Weighted Sum merge (liberty + has3dkx)
  ![ws05](examples/ws05.png?raw=true)

 LossLessMix (colorful + liberty + has3dkx)
  ![mindif](examples/mindif.png?raw=true)

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


Can be applied to mix models oriented for different tasks (landscapes + 3d), when mixing similar models it can lead to unexpected results

MaxDifMix (colorful + liberty + has3dkx)
![maxdif](examples/maxdif.png?raw=true)

But it work well then merge redshiftdiffusion with landscape model, try "Ford mustang at night forest"

## PS

Unfortunately I am limited in the speed of algorithm development (macbook air m1), I would be happy if you find this algorithm useful. My Doge Wallet: 