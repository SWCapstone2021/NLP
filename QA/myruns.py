import torch

cached_features_file = 'data/cached_dev_models_512_ORI'

features_and_dataset = torch.load(cached_features_file)
features, dataset, examples = (
    features_and_dataset["features"],
    features_and_dataset["dataset"],
    features_and_dataset["examples"],
)
# print(len(features))
# print(features[0])
#
# print(len(dataset))
# print(dataset[0])

print(len(examples))
print(examples[0].qas_id)
print(examples[0].question_text)
print(examples[0].context_text)
print(examples[0].title)
print(examples[0].answers)
