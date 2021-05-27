CUDA_DEVICE_ID="0"

CUDA_VISIBLE_DEVICES=$CUDA_DEVICE_ID \
  python run_infer.py --model_type bert \
  --model_name_or_path models/ \
  --output_dir models \
  --data_dir data \
  --train_file KorQuAD_v1.0_train.json \
  --predict_file KorQuAD_v1.0_dev.json \
  --per_gpu_train_batch_size 8 \
  --per_gpu_eval_batch_size 8 \
  --max_seq_length 512 \
  --logging_steps 4000 \
  --save_steps 4000 \
  --fp16 \
  --do_eval

#    --evaluate_during_training \
