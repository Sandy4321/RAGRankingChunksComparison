import random
import pandas as pd
N = 7 # < 26
# Set seed for reproducibility
random.seed(42)

# Step 1: Simulate a question
question = "What is climate change and what are its main causes?"

# Step 2: Generate 2 good answers
good_answers = [
        "Climate change refers to long-term shifts in temperatures and weather patterns. These changes may be natural, but since the 1800s, human activities is the main cause.",
        "Climate change involves significant changes in global temperature, precipitation, and wind patterns over decades or longer. The primary driver today is human activity."
    ]



# Step 3: Generate 4 medium answers
medium_answers = [
        "Climate change is when the Earth is weather changes a lot over time. Some people say humans are causing it by polluting the air.",
        "It has something to do with rising temperatures and ice melting. I think cars and factories might be part of the problem.",
        "Scientists believe that the planet is getting warmer due to things like pollution and cutting down trees.",
        "Climate change is about changes in the environment caused by both natural events and some human actions."
    ]



# Step 4: Generate 20 bad answers
bad_answers = [
    "I do not know much about that.",
    "Something about the weather changing?",
    "Maybe it is when the seasons get mixed up.",
    "That is probably because of the sun getting hotter.",
    "I think animals have something to do with it.",
    "Probably aliens are causing it.",
    "It is just a theory invented by scientists.",
    "Governments use it to control us.",
    "It is the same thing as the ozone hole.",
    "I heard it is not real and will go away soon.",
    "The Earth always goes through hot and cold phases.",
    "It is mostly about recycling more.",
    "People should stop driving so many cars.",
    "Trees help with everything, right?",
    "I think it is just a hoax.",
    "Global warming and climate change are different things.",
    "It is mostly a problem in big cities.",
    "There is no proof it is actually happening.",
    "I saw a video saying it is fake news.",
    "Some people just want more taxes.",
    "It is caused by too many airplanes flying around.",
    "Maybe it is because of all the plastic in the ocean.",
    "I think it is about the moon’s orbit changing.",
    "It is just nature doing its thing.",
    "People are overreacting to normal weather patterns.",
    "It is probably because of too many factories.",
    "I heard it is caused by volcanic eruptions.",
    "It is just a way to sell more electric cars.",
    "The Earth is flat, so it cannot be climate change.",
    "It is because people use too much air conditioning.",
    "I think it is related to Wi-Fi signals.",
    "It is just a cycle that happens every few years.",
    "Maybe it is because of too many cows farting.",
    "It is caused by people not recycling enough.",
    "I heard it is because of solar flares.",
    "It is just a way to scare people.",
    "Maybe it is because of too many skyscrapers.",
    "I think it is caused by bad farming practices.",
    "It is probably just a conspiracy theory.",
    "The weather has always been like this.",
    "It is because of too many people on Earth.",
    "I think it is related to the internet.",
    "It is caused by too much pollution in space.",
    "Maybe it is because of underground volcanoes.",
    "It is just something made up by the media.",
    "I heard it is because of magnetic pole shifts.",
    "It is probably caused by too many wind turbines.",
    "I think it is about the Earth spinning faster.",
    "It is just a way to make money off green energy.",
    "Maybe it is caused by cosmic rays."
]



# Step 5: Combine all answers
all_answers = good_answers +  medium_answers +  bad_answers
#all_answers =  all_answers[0:N]

# Shuffle answers
random.shuffle(all_answers)



# Step 6: Save files

# File 1: Just the question
with open("question.txt", "w") as f:
    f.write(question)

# File 2: Only the answers (for input to a model or evaluator)
z = pd.DataFrame(all_answers)[0]

z.to_csv("answers54.csv", index=False, header=False)

# File 3: Answers + True Labels (for evaluation later)
#pd.DataFrame({"answer": texts, "label": labels}).to_csv("answers_with_labels.csv", index=False)

print("✅ Files saved:")
print("- question.txt")
print("- answers54.csv")
#print("- answers_with_labels.csv")