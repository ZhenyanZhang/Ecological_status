#!/bin/bash

bwa_path=$1
ags_path=$2
num_jobs=$3
if_group=$4
functional_group=$5



# Check if the correct number of arguments is provided
if [ $# -ne 5 ]; then
echo "Usage: $0 <bwa_path> <ags_path> <num_jobs> <if functional group, YES or NO> <if YES for functional group, provide your functional group file; if NO, enter whatever you like>"
exit 1
fi

# Function to process a single file
process_bwa_result() {
local stat="$1"
#echo $stat

#added sample name into stat file of bwa
name=$(basename "$stat" | cut -d. -f1)
echo $name
name_file=$name.name
awk -v col_name="$name" 'BEGIN{OFS="\t"} {print col_name, $0}' $stat > $name_file  && mv $name_file $stat

#add genome_equivalent
ge_file=$name.ge
while IFS=$'\t' read -r sample gene length reads_count rest; do
	if [[ -n $sample ]]; then
		genome_equivalent="${map_dict_ge[$sample]}"
		#echo $genome_equivalent
		if [[ -n $genome_equivalent ]]; then
			echo -e "$sample\t$gene\t$length\t$reads_count\t$genome_equivalent" >> $ge_file
		fi
	fi
done < $stat

awk 'BEGIN { FS=OFS="\t" } $3 != 0 { $6 = $4 / ($3/1000) / $5; print $1"\t"$2"\t"$6}' $ge_file > $stat

rm $ge_file
}

# Function for functional group
process_functional_group() {
local stat="$1"
#echo $stat

name=$(basename "$stat" | cut -d. -f1)
echo $name
fg_file=$name.fg

#added functional group info into stat file of bwa
while IFS=$'\t' read -r sample gene RPKG; do
	if [[ -n $gene ]]; then
		functional_group="${map_dict[$gene]}"
		if [[ -n $functional_group ]]; then
			echo -e "$sample\t$functional_group\t$RPKG" >> $fg_file
		fi
	fi
done < $stat

awk 'BEGIN { FS = "\t" } { sum[$2] += $3; lines[$2] = $1"\t"$2"\t" } END { for (key in sum) print lines[key] sum[key] }' $fg_file > $stat

rm $fg_file
}

#merge ags results
for ags in $ags_path/*.tsv; do
	name=$(basename $ags | cut -d. -f1)
	echo $name
	GE=$(awk -F'\t' '$1=="genome_equivalents:"{print $2; exit}' $ags)
	echo -e "${name}\t${GE}" >> genome_equivalent.txt
done

# add sample name and genome_equivalents into bwa results
map_file_ge="genome_equivalent.txt"
declare -A map_dict_ge
	
while IFS=$'\t' read -r sample genome_equivalent; do
		map_dict_ge[$sample]=$genome_equivalent
done < $map_file_ge

for stat in $bwa_path/*.stat; do
	process_bwa_result "$stat" &
	((++processed_files))
	[ $((processed_files % num_jobs)) -eq 0 ] && wait
done

wait

#merge all stat file
cat $bwa_path/*.stat > stat_all
awk 'BEGIN { print "sample\tgene\tRPKG" } { print }' stat_all > gene_abundance_rpkg.tsv

rm stat_all

#calculated as functional group
if [ $if_group = "YES" ]; then

	#add functional_group
	map_file=$functional_group
	declare -A map_dict
	
	while IFS=$'\t' read -r functional_group gene; do
		map_dict[$gene]=$functional_group
	done < "$map_file"
	
	for stat in $bwa_path/*.stat; do
		process_functional_group "$stat" &
		((++processed_files))
		[ $((processed_files % num_jobs)) -eq 0 ] && wait
	done
	wait
	cat $bwa_path/*.stat > function_all
	awk 'BEGIN { print "sample\tfunction\tRPKG" } { print }' function_all > function_abundance_rpkg.tsv

	rm function_all
elif [ "$if_group" = "NO" ]; then
	echo "Skipping kegg"
else
	echo "Invalid choice. Please provide YES or NO for functional group. If you choose YES, please provide your group file"
	exit 1
fi




