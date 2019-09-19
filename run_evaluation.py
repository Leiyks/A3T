from datasets.otbdataset import OTBDataset
from datasets.votdataset import VOTDataset
from datasets.tpldataset import TPLDataset
from datasets.uavdataset import UAVDataset
from datasets.nfsdataset import NFSDataset
from datasets.lasotdataset import LaSOTDataset
from evaluations.ope_benchmark import OPEBenchmark


def main(trackers, algorithms, dataset_name):
    if dataset_name == "OTB":
        dataset = OTBDataset()
    elif dataset_name == "NFS":
        dataset = NFSDataset()
    elif dataset_name == "UAV":
        dataset = UAVDataset()
    elif dataset_name == "TPL":
        dataset = TPLDataset()
    elif dataset_name == "VOT":
        dataset = VOTDataset()
    elif dataset_name == "LaSOT":
        dataset = LaSOTDataset()
    else:
        raise ValueError("Unknown dataset name")

    benchmark = OPEBenchmark(dataset)
    success = benchmark.eval_success(trackers + algorithms)
    precision = benchmark.eval_precision(trackers + algorithms)
    benchmark.show_result(success, precision, show_video_level=False)

    success_offline, overlap_anchor, anchor_ratio = benchmark.eval_success_offline(
        algorithms
    )
    precision_offline, dist_anchor, anchor_ratio = benchmark.eval_precision_offline(
        algorithms
    )
    benchmark.show_result_offline(
        success_offline, overlap_anchor, precision_offline, dist_anchor, anchor_ratio
    )


if __name__ == "__main__":
    trackers = [
        "ATOM",
        "DaSiamRPN",
        "DiMP",
        "ECO",
        "SiamDW",
        "SiamFC",
        "SiamRPN",
        "SiamRPN++",
        "Staple",
        "Average",
        "Max",
        "MCCT",
    ]
    algorithms = [""]

    dataset = "OTB"

    main(trackers, algorithms, dataset)
