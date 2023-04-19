## Please use supermerger project: https://github.com/hako-mikan/sd-webui-supermerger
It has improved  version of cosine similarity with awesome UI

## Algorithm that allows you to mix models without loss of quality. 

**TLDR;** Mixing models by cosine similarity

## Usage

```
python3 weightedsim.py openjourney-v2.ckpt EimisAnimeDiffusion_1-0v.ckpt

```

## Example

#### openjourney-v2
![openjourney](examples/openjourney-v2.png?raw=true)

#### eimisanimediffusion_1-0v
![eimisanime](examples/eimisanimediffusion_1-0v.png?raw=true)

#### weighted sum merge
![open_eimis_sum_05](examples/open_eimis_sum_05.png?raw=true)

#### weighted sim merge 
![open_eimis_sim_05](examples/open_eimis_sim_05.png?raw=true)

#### Prompt
```
25 year old woman, white top, blue shorts, adorable face, piercing eyes, resting mouth, intricate necklace, short hair, looking away, standing next to beach, sunset, palm tree

Negative prompt: deformed, bad anatomy, disfigured, mutation, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, malformed hands, blurry, ((((mutated hands and fingers)))), distorted hands, amputation, missing hands, double hands, watermark, censored, black and white, sepia, zombie
Steps: 28, Sampler: DPM++ 2M Karras, CFG scale: 7, Seed: 0, Size: 576x832, Model hash: 628090e8bb, Model: merged-0.5, ENSD: 31337
```


## The list of models that used this script to create them:

- [ReV Animated](https://civitai.com/models/7371/rev-animated)

- [animatrix](https://civitai.com/models/21916/animatrix)

- [Colorful](https://civitai.com/models/7279/colorful)


## PS

### Please stop asking me how to run this and how to work with it. I wrote it without knowing Python. This is my second and hopefully last Python script.


## My Doge Wallet

DEw2DR8C7BnF8GgcrfTzUjSnGkuMeJhg83

## Have fun!

![fun](examples/1.jpeg?raw=true)
