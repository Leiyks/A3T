datasets=("OTB" "NFS" "UAV" "TPL" "VOT" "LaSOT")
baselines=("MCCT" "Random" "Max")

high_experts=("ATOM" "DaSiamRPN" "SiamMCF" "SiamRPN++" "SPM" "THOR")
threshold=0.1
for (( j=0; j<${#datasets[@]}; j++ )); do    
    for (( i=0; i<${#baselines[@]}; i++ )); do
        python ./track_algorithm.py -a ${baselines[$i]} -n High -d ${datasets[$j]} -e ${high_experts[@]} -r $threshold
    done
done

low_experts=("GradNet" "MemTrack" "SiamDW" "SiamFC" "SiamRPN" "Staple")
threshold=0.1
for (( j=0; j<${#datasets[@]}; j++ )); do    
    for (( i=0; i<${#baselines[@]}; i++ )); do
        python ./track_algorithm.py -a ${baselines[$i]} -n Low -d ${datasets[$j]} -e ${low_experts[@]} -r $threshold
    done
done

mix_experts=("ATOM" "SiamRPN++" "SPM" "MemTrack" "SiamFC" "Staple")
threshold=0.1
for (( j=0; j<${#datasets[@]}; j++ )); do    
    for (( i=0; i<${#baselines[@]}; i++ )); do
        python ./track_algorithm.py -a ${baselines[$i]} -n Mix -d ${datasets[$j]} -e ${mix_experts[@]} -r $threshold
    done
done

siamdw_experts=("SiamDW_SiamFCRes22" "SiamDW_SiamFCIncep22" "SiamDW_SiamFCNext22" "SiamDW_SiamRPNRes22" "SiamDW_SiamFCRes22_VOT" "SiamDW_SiamFCIncep22_VOT" "SiamDW_SiamFCNext22_VOT" "SiamDW_SiamRPNRes22_VOT")
threshold=0.1
for (( j=0; j<${#datasets[@]}; j++ )); do    
    for (( i=0; i<${#baselines[@]}; i++ )); do
        python ./track_algorithm.py -a ${baselines[$i]} -n SiamDW -d ${datasets[$j]} -e ${siamdw_experts[@]} -r $threshold
    done
done

siamrpn_experts=("SiamRPN++_AlexNet" "SiamRPN++_AlexNet_OTB" "SiamRPN++_ResNet-50" "SiamRPN++_ResNet-50_OTB" "SiamRPN++_ResNet-50_LT" "SiamRPN++_MobileNetV2" "SiamRPN++_SiamMask")
threshold=0.1
for (( j=0; j<${#datasets[@]}; j++ )); do    
    for (( i=0; i<${#baselines[@]}; i++ )); do
        python ./track_algorithm.py -a ${baselines[$i]} -n SiamRPN++ -d ${datasets[$j]} -e ${siamrpn_experts[@]} -r $threshold
    done
done