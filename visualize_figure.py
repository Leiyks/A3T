import os
from pathlib import Path
import pickle
import seaborn as sns
from datasets.otbdataset import OTBDataset
from datasets.votdataset import VOTDataset
from datasets.tpldataset import TPLDataset
from visualize_result import draw_graph, draw_result
from visualize_eval import (
    name2color,
    draw_rank_both,
    draw_pie,
    draw_score_with_ratio,
    make_score_table,
    make_regret_table,
)


def get_tuning_results(tune_dir):
    dataset_name = "GOT10K"
    modes = ["High", "Low", "Mix", "SiamDW", "SiamRPN++"]

    threshold_successes = {mode: {} for mode in modes}
    threshold_precisions = {mode: {} for mode in modes}
    threshold_anchor_successes = {mode: {} for mode in modes}
    threshold_anchor_precisions = {mode: {} for mode in modes}
    threshold_offline_successes = {mode: {} for mode in modes}
    threshold_offline_precisions = {mode: {} for mode in modes}
    threshold_anchors = {mode: {} for mode in modes}

    for mode in modes:
        eval_save = tune_dir / mode / "eval.pkl"
        successes, precisions, anchor_frames, anchor_successes, anchor_precisions, offline_successes, offline_precisions = pickle.loads(
            eval_save.read_bytes()
        )

        for algorithm in successes[dataset_name].keys():
            algorithm_split_name = algorithm.split("_")[3]

            threshold_successes[mode][algorithm_split_name] = successes[dataset_name][
                algorithm
            ]
            threshold_precisions[mode][algorithm_split_name] = precisions[dataset_name][
                algorithm
            ]
            threshold_anchor_successes[mode][algorithm_split_name] = anchor_successes[
                dataset_name
            ][algorithm]
            threshold_anchor_precisions[mode][algorithm_split_name] = anchor_precisions[
                dataset_name
            ][algorithm]
            threshold_offline_successes[mode][algorithm_split_name] = offline_successes[
                dataset_name
            ][algorithm]
            threshold_offline_precisions[mode][
                algorithm_split_name
            ] = offline_precisions[dataset_name][algorithm]
            threshold_anchors[mode][algorithm_split_name] = anchor_frames[dataset_name][
                algorithm
            ]

    return (
        threshold_successes,
        threshold_precisions,
        threshold_anchor_successes,
        threshold_anchor_precisions,
        threshold_offline_successes,
        threshold_offline_precisions,
        threshold_anchors,
    )


def figure1(datasets_name, all_experts, all_experts_name, all_successes, save_dir):
    figsize = (10, 5)
    colors = name2color(all_experts)
    sns.set_palette(colors)
    draw_pie(
        datasets_name,
        all_experts,
        all_experts_name,
        all_successes,
        figsize,
        save_dir,
        legend=True,
        file_name="Figure1",
    )


def figure2(vot_dataset, high_algorithm, high_experts, save_dir):
    target_seqs = ["fish1", "nature"]
    vis_trackers = high_experts + [high_algorithm]
    draw_result(
        vot_dataset,
        high_algorithm,
        high_experts,
        name2color(vis_trackers),
        save_dir / "Figure2",
        target_seqs,
        show=["frame"],
        gt=True,
        best=True,
    )


def figure4(datasets_name, high_algorithm, high_experts, high_successes, save_dir):
    figsize = (20, 5)
    vis_trackers = high_experts + [high_algorithm]
    colors = name2color(vis_trackers)
    sns.set_palette(colors)
    draw_rank_both(
        datasets_name,
        vis_trackers,
        high_successes,
        figsize,
        save_dir,
        legend=True,
        file_name="Figure4",
    )


def figure5(otb_dataset, tpl_dataset, high_algorithm, high_experts, save_dir):
    vis_trackers = high_experts + [high_algorithm]

    otb_seqs = ["Girl2"]
    draw_graph(
        otb_dataset,
        high_algorithm,
        high_experts,
        name2color(vis_trackers),
        save_dir / "Figure5",
        otb_seqs,
        iserror=True,
        legend=True,
    )
    draw_graph(
        otb_dataset,
        high_algorithm,
        high_experts,
        name2color(vis_trackers),
        save_dir / "Figure5",
        otb_seqs,
        iserror=False,
        legend=False,
    )
    draw_result(
        otb_dataset,
        high_algorithm,
        high_experts,
        name2color(vis_trackers),
        save_dir / "Figure5",
        otb_seqs,
        show=["frame"],
    )

    tpl_seqs = ["tpl_Yo_yos_ce1"]
    draw_graph(
        tpl_dataset,
        high_algorithm,
        high_experts,
        name2color(vis_trackers),
        save_dir / "Figure5",
        tpl_seqs,
        iserror=True,
        legend=True,
    )
    draw_graph(
        tpl_dataset,
        high_algorithm,
        high_experts,
        name2color(vis_trackers),
        save_dir / "Figure5",
        tpl_seqs,
        iserror=False,
        legend=False,
    )
    draw_result(
        tpl_dataset,
        high_algorithm,
        high_experts,
        name2color(vis_trackers),
        save_dir / "Figure5",
        tpl_seqs,
        show=["frame"],
    )


def figure6(threshold_successes, threshold_anchors, save_dir):
    figsize = (20, 5)
    thresholds = sorted(list(threshold_successes.values())[0].keys())
    modes = threshold_successes.keys()
    draw_score_with_ratio(
        modes,
        thresholds,
        threshold_successes,
        threshold_anchors,
        figsize,
        save_dir,
        "Figure6",
    )


def figure7(otb_dataset, high_mcct_algorithm, high_experts, save_dir):
    target_seqs = ["Bird1", "Tiger1"]
    vis_trackers = high_experts + [high_mcct_algorithm]
    draw_result(
        otb_dataset,
        high_mcct_algorithm,
        high_experts,
        name2color(vis_trackers),
        save_dir / "Figure7",
        target_seqs,
        show=["frame"],
    )


def table1(
    datasets_name,
    high_algorithm,
    high_baselines,
    high_experts,
    high_successes,
    high_precisions,
    save_dir,
):
    eval_trackers = high_experts + high_baselines + [high_algorithm]
    make_score_table(
        datasets_name,
        eval_trackers,
        len(high_experts),
        high_successes,
        high_precisions,
        save_dir,
        "Table1",
        isvot=True,
    )


def table2(
    datasets_name,
    low_algorithm,
    low_baselines,
    low_experts,
    low_successes,
    low_precisions,
    save_dir,
):
    eval_trackers = low_experts + low_baselines + [low_algorithm]
    make_score_table(
        datasets_name,
        eval_trackers,
        len(low_experts),
        low_successes,
        low_precisions,
        save_dir,
        "Table2",
        isvot=True,
    )


def table3(
    datasets_name,
    mix_algorithm,
    mix_baselines,
    mix_experts,
    mix_successes,
    mix_precisions,
    save_dir,
):
    eval_trackers = mix_experts + mix_baselines + [mix_algorithm]
    make_score_table(
        datasets_name,
        eval_trackers,
        len(mix_experts),
        mix_successes,
        mix_precisions,
        save_dir,
        "Table3",
        isvot=True,
    )


def table4(
    datasets_name,
    mix_algorithm,
    mix_experts,
    mix_offline_successes,
    mix_offline_precisions,
    save_dir,
):
    eval_trackers = mix_experts + [mix_algorithm]
    make_score_table(
        datasets_name,
        eval_trackers,
        len(mix_experts),
        mix_offline_successes,
        mix_offline_precisions,
        save_dir,
        "Table4",
        isvot=True,
    )


def table5(datasets_name, mix_algorithm, mix_experts, mix_regrets, save_dir):
    eval_trackers = mix_experts + [mix_algorithm]
    make_regret_table(
        datasets_name, eval_trackers, len(mix_experts), mix_regrets, save_dir, "Table5"
    )


def table6(
    datasets_name,
    siamdw_algorithm,
    siamdw_baselines,
    siamdw_experts,
    siamdw_successes,
    siamdw_precisions,
    save_dir,
):
    eval_trackers = siamdw_experts + siamdw_baselines + [siamdw_algorithm]
    make_score_table(
        datasets_name,
        eval_trackers,
        len(siamdw_experts),
        siamdw_successes,
        siamdw_precisions,
        save_dir,
        "Table6",
        isvot=True,
    )


def table7(
    datasets_name,
    siamrpn_algorithm,
    siamrpn_baselines,
    siamrpn_experts,
    siamrpn_successes,
    siamrpn_precisions,
    save_dir,
):
    eval_trackers = siamrpn_experts + siamrpn_baselines + [siamrpn_algorithm]
    make_score_table(
        datasets_name,
        eval_trackers,
        len(siamrpn_experts),
        siamrpn_successes,
        siamrpn_precisions,
        save_dir,
        "Table7",
        isvot=True,
    )


def table8(
    datasets_name,
    high_algorithm,
    high_experts,
    high_anchor_successes,
    high_anchor_precisions,
    save_dir,
):
    eval_trackers = high_experts + [high_algorithm]
    make_score_table(
        datasets_name,
        eval_trackers,
        len(high_experts),
        high_anchor_successes,
        high_anchor_precisions,
        save_dir,
        "Table8",
        isvot=True,
    )


def main(experiments, all_experts, all_experts_name, save_dir, eval_dir, tune_dir):
    otb = OTBDataset()
    tpl = TPLDataset()
    vot = VOTDataset()

    datasets_name = ["OTB2015", "TColor128", "UAV123", "NFS", "LaSOT", "VOT2018"]

    # All
    eval_save = eval_dir / "All" / "eval.pkl"
    all_successes, _, _, _, _, _, _, _, _ = pickle.loads(eval_save.read_bytes())
    figure1(datasets_name, all_experts, all_experts_name, all_successes, save_dir)

    # High
    high_algorithm, high_baselines, high_experts = experiments["High"]
    eval_save = eval_dir / "High" / "eval.pkl"
    high_successes, high_precisions, high_anchor_frames, high_anchor_successes, high_anchor_precisions, high_offline_successes, high_offline_precisions, high_regret_gts, high_regret_offlines = pickle.loads(
        eval_save.read_bytes()
    )
    table1(
        datasets_name,
        high_algorithm,
        high_baselines,
        high_experts,
        high_successes,
        high_precisions,
        save_dir,
    )
    table8(
        datasets_name,
        high_algorithm,
        high_experts,
        high_anchor_successes,
        high_anchor_precisions,
        save_dir,
    )
    figure2(vot, high_algorithm, high_experts, save_dir)
    figure4(datasets_name, high_algorithm, high_experts, high_successes, save_dir)
    figure5(otb, tpl, high_algorithm, high_experts, save_dir)
    figure7(otb, high_baselines[0], high_experts, save_dir)

    # Low
    low_algorithm, low_baselines, low_experts = experiments["Low"]
    eval_save = eval_dir / "Low" / "eval.pkl"
    low_successes, low_precisions, low_anchor_frames, low_anchor_successes, low_anchor_precisions, low_offline_successes, low_offline_precisions, low_regret_gts, low_regret_offlines = pickle.loads(
        eval_save.read_bytes()
    )
    table2(
        datasets_name,
        low_algorithm,
        low_baselines,
        low_experts,
        low_successes,
        low_precisions,
        save_dir,
    )

    # Mix
    mix_algorithm, mix_baselines, mix_experts = experiments["Mix"]
    eval_save = eval_dir / "Mix" / "eval.pkl"
    mix_successes, mix_precisions, mix_anchor_frames, mix_anchor_successes, mix_anchor_precisions, mix_offline_successes, mix_offline_precisions, mix_regret_gts, mix_regret_offlines = pickle.loads(
        eval_save.read_bytes()
    )
    table3(
        datasets_name,
        mix_algorithm,
        mix_baselines,
        mix_experts,
        mix_successes,
        mix_precisions,
        save_dir,
    )
    table4(
        datasets_name,
        mix_algorithm,
        mix_experts,
        mix_offline_successes,
        mix_offline_precisions,
        save_dir,
    )
    table5(datasets_name, mix_algorithm, mix_experts, mix_regret_offlines, save_dir)

    # SiamDW
    siamdw_algorithm, siamdw_baselines, siamdw_experts = experiments["SiamDW"]
    eval_save = eval_dir / "SiamDW" / "eval.pkl"
    siamdw_successes, siamdw_precisions, siamdw_anchor_frames, siamdw_anchor_successes, siamdw_anchor_precisions, siamdw_offline_successes, siamdw_offline_precisions, siamdw_regret_gts, siamdw_regret_offlines = pickle.loads(
        eval_save.read_bytes()
    )
    table6(
        datasets_name,
        siamdw_algorithm,
        siamdw_baselines,
        siamdw_experts,
        siamdw_successes,
        siamdw_precisions,
        save_dir,
    )

    # SiamRPN++
    siamrpn_algorithm, siamrpn_baselines, siamrpn_experts = experiments["SiamRPN++"]
    eval_save = eval_dir / "SiamRPN++" / "eval.pkl"
    siamrpn_successes, siamrpn_precisions, siamrpn_anchor_frames, siamrpn_anchor_successes, siamrpn_anchor_precisions, siamrpn_offline_successes, siamrpn_offline_precisions, siamrpn_regret_gts, siamrpn_regret_offlines = pickle.loads(
        eval_save.read_bytes()
    )
    table7(
        datasets_name,
        siamrpn_algorithm,
        siamrpn_baselines,
        siamrpn_experts,
        siamrpn_successes,
        siamrpn_precisions,
        save_dir,
    )

    # Tuning
    threshold_successes, _, _, _, _, _, threshold_anchors = get_tuning_results(tune_dir)
    figure6(threshold_successes, threshold_anchors, save_dir)


if __name__ == "__main__":
    high_algorithm = "AAA_High_0.00_0.69_False_False_False_True_True_True_True"
    low_algorithm = "AAA_Low_0.00_0.60_False_False_False_True_True_True_True"
    mix_algorithm = "AAA_Mix_0.00_0.65_False_False_False_True_True_True_True"
    siamdw_algorithm = "AAA_SiamDW_0.00_0.67_False_False_False_True_True_True_True"
    siamrpn_algorithm = "AAA_SiamRPN++_0.00_0.61_False_False_False_True_True_True_True"

    high_baselines = ["MCCT_High_0.10", "Random_High", "Max_High"]
    low_baselines = ["MCCT_Low_0.10", "Random_Low", "Max_Low"]
    mix_baselines = ["MCCT_Mix_0.10", "Random_Mix", "Max_Mix"]
    siamdw_baselines = ["MCCT_SiamDW_0.10", "Random_SiamDW", "Max_SiamDW"]
    siamrpn_baselines = ["MCCT_SiamRPN++_0.10", "Random_SiamRPN++", "Max_SiamRPN++"]

    all_experts = [
        "ATOM",
        "DaSiamRPN",
        "GradNet",
        "MemTrack",
        "SiamDW",
        "SiamFC",
        "SiamMCF",
        "SiamRPN",
        "SiamRPN++",
        "SPM",
        "Staple",
        "THOR",
    ]
    all_experts_name = [
        "ATOM[26]",
        "DaSiamRPN[27]",
        "GradNet[34]",
        "MemTrack[35]",
        "SiamDW[32]",
        "SiamFC[36]",
        "SiamMCF[28]",
        "SiamRPN[33]",
        "SiamRPN++[29]",
        "SPM[30]",
        "Staple[37]",
        "THOR[31]",
    ]
    high_experts = ["ATOM", "DaSiamRPN", "SiamMCF", "SiamRPN++", "SPM", "THOR"]
    low_experts = ["GradNet", "MemTrack", "SiamDW", "SiamFC", "SiamRPN", "Staple"]
    mix_experts = ["ATOM", "SiamRPN++", "SPM", "MemTrack", "SiamFC", "Staple"]
    siamdw_experts = [
        "SiamDW_SiamFCRes22",
        "SiamDW_SiamFCIncep22",
        "SiamDW_SiamFCNext22",
        "SiamDW_SiamRPNRes22",
        "SiamDW_SiamFCRes22_VOT",
        "SiamDW_SiamFCIncep22_VOT",
        "SiamDW_SiamFCNext22_VOT",
        "SiamDW_SiamRPNRes22_VOT",
    ]
    siamrpn_experts = [
        "SiamRPN++_AlexNet",
        "SiamRPN++_AlexNet_OTB",
        "SiamRPN++_ResNet-50",
        "SiamRPN++_ResNet-50_OTB",
        "SiamRPN++_ResNet-50_LT",
        "SiamRPN++_MobileNetV2",
        "SiamRPN++_SiamMask",
    ]

    experiments = {
        "High": (high_algorithm, high_baselines, high_experts),
        "Low": (low_algorithm, low_baselines, low_experts),
        "Mix": (mix_algorithm, mix_baselines, mix_experts),
        "SiamDW": (siamdw_algorithm, siamdw_baselines, siamdw_experts),
        "SiamRPN++": (siamrpn_algorithm, siamrpn_baselines, siamrpn_experts),
    }

    save_dir = Path("./visualization_results")
    os.makedirs(save_dir, exist_ok=True)

    eval_dir = Path(f"./evaluation_results")
    tune_dir = Path(f"./tuning_results/AAA")
    main(experiments, all_experts, all_experts_name, save_dir, eval_dir, tune_dir)
