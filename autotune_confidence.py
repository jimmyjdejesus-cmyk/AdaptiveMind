# autotune_confidence.py
import config
from evaluation import run_evaluation # <-- Import our harness
from logger_config import log

def find_optimal_threshold():
    # Define the range of thresholds to test
    # We'll test from 1.0 up to 15.0, in steps of 0.5
    threshold_range = [i * 0.5 for i in range(2, 31)] 

    successful_thresholds = []
    log.info("--- STARTING CONFIDENCE AUTO-TUNER ---")
    log.info(f"Testing {len(threshold_range)} different thresholds from {threshold_range[0]} to {threshold_range[-1]}...")

    for threshold in threshold_range:
        # Temporarily set the config value for this run
        config.CONFIDENCE_THRESHOLD = threshold
        log.info(f"--- Testing threshold: {threshold:.2f} ---")

        # Run the full evaluation
        results = run_evaluation()

        # Check if all tests passed
        if results["passed"] == results["total"]:
            log.info(f"SUCCESS: All tests passed with threshold {threshold:.2f}")
            successful_thresholds.append(threshold)
        else:
            log.warning(f"FAILURE: {len(results['failed_tests'])} test(s) failed with threshold {threshold:.2f}")
            # Optional: break here to speed it up, as higher thresholds will also fail
            # break 

    log.info("--- AUTO-TUNER COMPLETE ---")

    if successful_thresholds:
        optimal_threshold = max(successful_thresholds)
        log.info(f"Optimal threshold found: {optimal_threshold:.2f}")
        log.info("Update your config.py with this value for the best balance.")
    else:
        log.warning("No threshold resulted in a perfect score. The model may need a better prompt or the tests may be too difficult.")

if __name__ == "__main__":
    find_optimal_threshold()