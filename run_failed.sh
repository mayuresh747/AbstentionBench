#!/bin/bash
source venv/bin/activate
pip install hydra-core datasets jsonlines pydantic pandas torch transformers gdown loguru wget -q
python main.py -m mode=local model=gpt51-rationalist abstention_detector=llm_judge_sonnet45_normal dataset_indices_subset="[0,1,2,3,4]" dataset_indices_path=null run_single_job_for_inference_and_judge=True "dataset=alcuna,bbq,big_bench_disambiguate,big_bench_known_unknowns,falseqa,gpqa,mediq,qasper,situated_qa,worldsense"
python aggregate_results.py
