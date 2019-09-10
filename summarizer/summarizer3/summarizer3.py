from summarizer import SingleModel

text_file = 'text.txt'
new_file = open(text_file, 'r')
body = new_file.read()
model = SingleModel()

#options
# model = SingleModel(
#     model(ratio: 1:1) #This gets used by the hugging face bert library to load the model, you can supply a custom trained model here
#     vector_size: int # This specifies the vector size of the output of the model. If you using a hugging face model, it will automatically be set
#     hidden: int # Needs to be negative, but allows you to pick which layer you want the embeddings to come from.
#     reduce_option: str # It can be 'mean', 'median', or 'max'. This reduces the embedding layer for pooling.
#     greedyness: float # number between 0 and 1. It is used for the coreference model. Anywhere from 0.35 to 0.45 seems to work well.
# )

# model(
#     body: str # The string body that you want to summarize
#     ratio: float # The ratio of sentences that you want for the final summary
#     min_length: int # Parameter to specify to remove sentences that are less than 40 characters
#     max_length: int # Parameter to specify to remove sentences greater than the max length
# )

result = model(body, ratio=(1/2), min_length=60)
full = ''.join(result)

print(full)

new_file.close()