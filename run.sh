dataset=Got10K

experts=("ATOM" "DaSiamRPN" "DiMP18" "DiMP50" "ECO" "SiamDW" "SiamFC" "SiamRPN" "SiamRPN++" "Staple" "STRCF" "TADT")
len=${#experts[@]}
for (( i=0; i<$len; i++ )); do
    python ./run_expert.py -e ${experts[$i]} -d $dataset
done

baselines=("Average" "Max" "MCCT")
len=${#baselines[@]}
for (( i=0; i<$len; i++ )); do
    python ./run_baseline.py -a ${baselines[$i]} -d $dataset -e $experts
done