
import os
import sys
from collections import defaultdict

def main():
    audio_file = sys.argv[1] if len(sys.argv) > 1 else "/app/bird_test.mp3.mp3"

    if not os.path.isfile(audio_file):
        print("ERROR: Audio file not found:", audio_file, flush=True)
        return

    import birdnet
    import numpy as np

    print("Loading BirdNET model...", flush=True)

    model = birdnet.load(
        "acoustic",
        "2.4",
        "tf",
        library="litert"
    )

    print("Analyzing audio...", flush=True)

    result = model.predict(
        audio_file,
        top_k=5,
        n_workers=1,
        n_producers=1
    )

    ids = np.asarray(result.species_ids).squeeze()
    scores = np.asarray(result.species_probs).squeeze()
    species_list = result.species_list

    if ids.ndim != 2 or scores.ndim != 2:
        print("Unexpected prediction shape:", ids.shape, scores.shape)
        return

    # Collect the highest score for each species ID.
    best_scores = {}

    for segment in range(min(ids.shape[0], scores.shape[0])):
        for rank in range(min(ids.shape[1], scores.shape[1])):
            species_id = int(ids[segment, rank])
            score = float(scores[segment, rank])

            if 0 <= species_id < len(species_list):
                best_scores[species_id] = max(
                    best_scores.get(species_id, 0.0),
                    score
                )

    ranked = sorted(
        best_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )[:5]

    print("\n===== TOP 5 BIRD CANDIDATES =====", flush=True)

    for species_id, score in ranked:
        print(
            f"{species_list[species_id]} — {score * 100:.2f}%",
            flush=True
        )

    print("\nAnalysis complete.", flush=True)


if __name__ == "__main__":
    main()
