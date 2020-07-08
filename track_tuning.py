import os
import pickle
from pathlib import Path
import numpy as np

from track_dataset import run_tracker
from options import select_algorithms
from datasets.got10kdataset import GOT10KDatasetVal
from evaluations.ope_benchmark import OPEBenchmark
from evaluations.offline_benchmark import OfflineBenchmark


def main(eval_dir, algorithm_name, experts, thresholds, **kwargs):
    algorithms = []
    dataset = GOT10KDatasetVal()
    dataset_name = "GOT10K"

    for threshold in thresholds:
        kwargs["feature_threshold"] = threshold
        algorithm = select_algorithms(algorithm_name, experts, **kwargs)

        run_tracker(algorithm, dataset, experts=experts)
        algorithms.append(algorithm.name)

    eval_save = eval_dir / "eval.pkl"
    if eval_save.exists():
        successes, precisions, anchor_frames, anchor_successes, anchor_precisions, offline_successes, offline_precisions = pickle.loads(
            eval_save.read_bytes()
        )
    else:
        # algorithms' performance
        ope = OPEBenchmark(dataset)
        successes = {dataset_name: ope.eval_success(algorithms)}
        precisions = {dataset_name: ope.eval_precision(algorithms)}

        # offline trackers' performance
        if algorithm_name.startswith("AAA"):
            offline = OfflineBenchmark(dataset)
            anchor_frames = {dataset_name: {}}
            anchor_successes = {dataset_name: {}}
            anchor_precisions = {dataset_name: {}}
            offline_successes = {dataset_name: {}}
            offline_precisions = {dataset_name: {}}
            for algorithm in algorithms:
                anchor_frame, anchor_success, anchor_precision = offline.eval_anchor_frame(
                    algorithm, experts
                )
                offline_success, offline_precision = offline.eval_offline_tracker(
                    algorithm, experts
                )

                anchor_frames[dataset_name][algorithm] = anchor_frame
                anchor_successes[dataset_name][algorithm] = anchor_success[algorithm]
                anchor_precisions[dataset_name][algorithm] = anchor_precision[algorithm]
                offline_successes[dataset_name][algorithm] = offline_success[algorithm]
                offline_precisions[dataset_name][algorithm] = offline_precision[
                    algorithm
                ]
        else:
            anchor_frames = None
            anchor_successes = None
            anchor_precisions = None
            offline_successes = None
            offline_precisions = None

        eval_save.write_bytes(
            pickle.dumps(
                (
                    successes,
                    precisions,
                    anchor_frames,
                    anchor_successes,
                    anchor_precisions,
                    offline_successes,
                    offline_precisions,
                )
            )
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithm", default="AAA", type=str)
    parser.add_argument("-e", "--experts", default=list(), nargs="+")
    parser.add_argument("-n", "--mode", default="Expert", type=str)
    parser.add_argument("-s", "--reset_target", action="store_true")
    parser.add_argument("-m", "--only_max", action="store_true")
    parser.add_argument("-i", "--use_iou", action="store_true")
    parser.add_argument("-f", "--use_feature", action="store_false")
    parser.add_argument("-x", "--cost_iou", action="store_false")
    parser.add_argument("-y", "--cost_feature", action="store_false")
    parser.add_argument("-z", "--cost_score", action="store_false")
    args = parser.parse_args()

    start_point = 0.6
    end_point = 0.9
    thresholds = np.arange(start_point, end_point, 0.01)

    eval_dir = Path(f"./tuning_results/{args.algorithm}/{args.mode}")
    os.makedirs(eval_dir, exist_ok=True)

    main(
        eval_dir,
        args.algorithm,
        args.experts,
        thresholds,
        mode=args.mode,
        reset_target=args.reset_target,
        only_max=args.only_max,
        use_iou=args.use_iou,
        use_feature=args.use_feature,
        cost_iou=args.cost_iou,
        cost_feature=args.cost_feature,
        cost_score=args.cost_score,
    )
