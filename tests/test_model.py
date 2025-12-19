# AdaptiveMind Framework
# Copyright (c) 2025 Jimmy De Jesus
# Licensed under CC-BY 4.0
#
# AdaptiveMind - Intelligent AI Routing & Context Engine
# More info: https://github.com/[username]/adaptivemind
# License: https://creativecommons.org/licenses/by/4.0/



# test_model.py
import os
import time

from apps.AdaptiveMind_Local.settings import get_active_model_path

# Resolve absolute path to model
model_path = get_active_model_path()
# Resolve absolute path safely: the `get_active_model_path` may return an absolute path,
# a path relative to the package, or a model name. Try a few fallbacks.
if os.path.isabs(model_path) or os.path.exists(model_path):
    abs_path = os.path.abspath(model_path)
else:
    candidate = os.path.abspath(os.path.join("apps", "AdaptiveMind_Local", model_path))
    if os.path.exists(candidate):
        abs_path = candidate
    else:
        # Fallback to interpreting the value as-is (may be a model id, not a file path)
        abs_path = os.path.abspath(model_path)

# Try loading model
try:
    from llama_cpp import Llama
    start_time = time.time()
    model = Llama(model_path=abs_path, n_ctx=2048, n_gpu_layers=-1)
    load_time = time.time() - start_time

    # Try generating a simple response
    output = model.create_completion(
        "Who won the Battle of Waterloo?",
        max_tokens=128,
        temperature=0.1
    )
    response = output["choices"][0]["text"]
except Exception:
    pass
