"""
The parent class for all agents.
"""

from llama_cpp import Llama
import config
from logger_config import log
from collections import deque
import numpy as np

from agents.utilities.confidence import calculate_average_confidence, calculate_lowest_group_confidence, calculate_lowest_single_token_confidence


class BaseAgent:
    def __init__(self, system_prompt=""):
        self.system_prompt = system_prompt
        self.llm = None  # Initialize llm as None
        try:
            self.llm = Llama(
                model_path=config.MODEL_PATH,
                n_ctx=config.N_CTX,
                n_gpu_layers=config.N_GPU_LAYERS,
                verbose=False,
                logits_all=True,  # Enable logits for logprobs support
                n_threads=config.N_THREADS  # Use the configured number of threads
            )
            log.info(
                "Model loaded for agent with persona: %s",
                self.__class__.__name__,
            )
        except Exception:
            log.error("Failed to load model", exc_info=True)

    def invoke(self, prompt, history=None):
        if not self.llm:
            log.warning("Invoke called but model is not loaded.")
            return "Model not loaded. Please check the logs for errors."

        full_prompt = (
            f"<|system|>\n{self.system_prompt}<|end|>\n"
            f"<|user|>\n{prompt}<|end|>\n"
            "<|im_start|>assistant\n"
        )

        log.info(f"Invoking model with streaming for {self.__class__.__name__}...")

        # --- Enable Streaming ---
        stream = self.llm.create_completion(
            full_prompt,
            max_tokens=1024,
            stop=["<|end|>", "<|im_end|>"],
            temperature=0.1,
            logprobs=True,
            stream=True  # <-- This enables the token-by-token stream
        )

        # --- Real-time confidence Checking Logic ---
        final_response = ""
        window_size = 32 # The size of our confidence window
        confidences = deque(maxlen=window_size)
        stopped_early = False

        for output in stream:
            token_text = output['choices'][0]['text']
            final_response += token_text

            logprobs = output['choices'][0]['logprobs']
            if logprobs and logprobs['token_logprobs']:
                # Calculate and add this token's confidence to our window
                confidence = -logprobs['token_logprobs'][0]
                confidences.append(confidence)

                # Check for early stopping only after our confidence window is full
                if len(confidences) == window_size:
                    current_group_confidence = np.mean(list(confidences))

                    # Core DeepConf Logic
                    if current_group_confidence < config.CONFIDENCE_THRESHOLD:
                        log.warning(f"Stopping early! Group confidence {current_group_confidence:.4f} fell below threshold {config.CONFIDENCE_THRESHOLD}")
                        stopped_early = True
                        break # Exit the generation loop

        if stopped_early:
            final_response += "..." # Indicate the response was cut off
        
        log.info("Model inference complete.")
        return final_response 
