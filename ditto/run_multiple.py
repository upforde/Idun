from subprocess import call
from random import random

times = 10

print("Running non-fine-tuned GPT-2 augmented")
for i in range(times):
    print("Times ran:", i+1)
    name = "Writer_output/non_ft_GPT-2_augmented_all/run_" +str(i+1) + ".txt"
    seed = str(round(random()*2147483647))
    call(["python", "train_ditto.py",  "--task=non_ft_GPT-2_all", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running baseline")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/Ditto_baseline/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     print(seed)
#     call(["python", "train_ditto.py",  "--task=Structured/Beer", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running Preliminary no matches")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/Prelim_augmented_no_matches/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=Preliminary_only_non_match", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running Preliminary with only matches")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/Prelim_augmented_with_matches/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=Preliminary_only_match", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running Preliminary with only generated")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/Prelim_synth_only/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=Preliminary_only_generated", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running Preliminary augmented")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/Prelim_augmented_all/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=Preliminary_all", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running GPT-2 no matches")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/GPT-2_augmented_no_matches/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=GPT-2_only_non_match", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running GPT-2 with only matches")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/GPT-2_augmented_with_matches_only/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=GPT-2_only_match", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running GPT-2 with only generated")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/GPT-2_synth_only/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=GPT-2_only_generated", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running GPT-2 augmented")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/GPT-2_augmented_all/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=GPT-2_all", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running non-fine-tuned GPT-2 no matches")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/non_ft_GPT-2_augmented_no_matches/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=non_ft_GPT-2_only_non_match", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running non-fine-tuned GPT-2 with only matches")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/non_ft_GPT-2_augmented_with_matches_only/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=non_ft_GPT-2_only_match", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])

# print("Running non-fine-tuned GPT-2 with only generated")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/non_ft_GPT-2_synth_only/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=non_ft_GPT-2_only_generated", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])


# print("Running GPT-2 hybrid")
# for i in range(times):
#     print("Times ran:", i+1)
#     name = "Writer_output/GPT-2_matches_ditto_prelim_non_matches/run_" +str(i+1) + ".txt"
#     seed = str(round(random()*2147483647))
#     call(["python", "train_ditto.py",  "--task=GPT-2_hybrid", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])