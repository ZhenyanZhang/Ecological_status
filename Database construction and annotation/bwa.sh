#!/bin/bash

input_path=$1
output_path=$2
database=$3
num_jobs=$4

mkdir BWA_DONE

# Check if the correct number of arguments is provided
if [ $# -ne 4 ]; then
echo "Usage: $0 <source_path> <target_path><database> <num_jobs>"
exit 1
fi

# Function to process a single gzip file
process_bwa() {
local F="$1"

R=${F%_*}_2.fastq
BASE=${F##*/}
SAMPLE=${BASE%_*}
echo $SAMPLE

if [ -e $output_path/${SAMPLE}.stat ]; then
    echo "$SAMPLE SKIP"
    mv $F BWA_DONE
    mv $R BWA_DONE
else
    bwa mem -t 20 $database $F $R|samtools view -t 20 -bS /dev/stdin -o $output_path/$SAMPLE.bam && samtools view -bF 4 $output_path/$SAMPLE.bam >$output_path/$SAMPLE.mapped.bam && samtools sort --threads 20 $output_path/$SAMPLE.mapped.bam -o $output_path/$SAMPLE.sort.mapped.bam && samtools index $output_path/$SAMPLE.sort.mapped.bam && samtools idxstats $output_path/$SAMPLE.sort.mapped.bam >$output_path/$SAMPLE.stat && rm $output_path/$SAMPLE.bam $output_path/$SAMPLE.mapped.bam
    echo "$SAMPLE bwa DONE"
    mv $F BWA_DONE
    mv $R BWA_DONE
fi

}

# Use parallel to process gzip files in parallel with specified number of jobs
for F in $input_path/*_1.fastq; do
process_bwa "$F" &
((++processed_files))
[ $((processed_files % num_jobs)) -eq 0 ] && wait
done

