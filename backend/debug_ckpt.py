import torch

ckpt = torch.load(r'E:\model train\train\backend\weights\best.pt', map_location='cpu', weights_only=False)
print("Checkpoint keys:", list(ckpt.keys()))

model_obj = ckpt.get('model')
print("\nModel object type:", type(model_obj))
print("Model object dir (sample):", [x for x in dir(model_obj) if not x.startswith('_')][:20])

if hasattr(model_obj, 'names'):
    names = model_obj.names
    print("\nmodel.names type:", type(names))
    print("model.names content:", names)
    if isinstance(names, dict):
        print("Dict keys:", list(names.keys()))
        print("Dict sample:", {k: names[k] for k in list(names.keys())[:8]})
