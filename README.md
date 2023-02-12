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
  ![Liberty](examples/Liberty.png?raw=true)

 has3dkx
  ![has3dkx](examples/has3dkx.png?raw=true)

 Weighted Sum merge (liberty + has3dkx)
  ![ws05](examples/ws05.png?raw=true)

 LossLessMix (colorful + liberty + has3dkx)
  ![mindif](examples/mindif.png?raw=true)

 Colorful model (created wthout merging, only with mixing)

https://civitai.com/models/7279/colorful

 ## Credits

Also implemented the maxdiff algorithm proposed by https://www.reddit.com/user/Another__one/ here https://www.reddit.com/r/StableDiffusion/comments/1012lto/comment/j7aoyso/?context=3


Can be applied to mix models oriented for different tasks (landscapes + 3d), when mixing similar models it can lead to unexpected results

MaxDiffMix (colorful + liberty + has3dkx)


But it work well then merge redshiftdiffusion with landscape model, try "Ford mustang at night forest"

## PS

Unfortunately I am limited in the speed of algorithm development (macbook air m1), I would be happy if you find this algorithm useful. My Doge Wallet: 