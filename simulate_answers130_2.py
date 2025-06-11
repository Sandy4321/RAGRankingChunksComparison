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
    "I don’t know much about climate change, to be honest. It might be something about the weather getting strange. I think it’s just a natural thing. Maybe it’ll sort itself out soon.",
    "Climate change could be when the seasons get all jumbled up. I’m not sure what causes it, but it might be the sun acting weird. It’s probably not a big deal. The weather always changes, right? I don’t think we need to worry too much.",
    "I heard climate change is when the weather doesn’t act normal. Maybe it’s because the sun is hotter these days. It’s probably just a phase. Nothing to panic about, I bet.",
    "Climate change is probably caused by the sun getting more intense. I think it heats up the Earth more than usual. That’s why we get weird storms and stuff. It’s not like humans are doing it.",
    "I think animals might be involved in climate change somehow. Maybe their behavior is messing with the environment. I don’t know the details. It’s probably not the main issue, though.",
    "Climate change could be aliens messing with our planet. I saw something online about extraterrestrials causing weather changes. It sounds wild, but who knows? Maybe they’re experimenting on us. It’s not like we can prove it’s not true.",
    "Climate change is just a scientist’s theory to get more funding. They need something to research, so they made this up. I haven’t seen any real proof it’s happening. It’s probably exaggerated.",
    "I think climate change is a government scheme to control people. They use it to push new rules and taxes. The weather doesn’t seem that different to me. It’s probably just a scare tactic.",
    "Climate change is probably the same as the ozone hole issue. It’s all about the atmosphere getting messed up. I don’t know why they call it different names. It’s confusing for no reason.",
    "I read that climate change isn’t real and will disappear soon. Some say it’s just a temporary thing. The Earth has always had weird weather. I don’t think it’s a big problem. People are overreacting.",
    "The Earth goes through hot and cold cycles naturally. Climate change is just one of those phases. It’s not caused by humans or anything. It’ll probably fix itself over time.",
    "Climate change is all about recycling more, I think. If people just sorted their trash better, it wouldn’t be an issue. That’s probably the main fix we need. It’s not that complicated.",
    "I heard climate change is because people drive too many cars. The exhaust fumes must be messing with the air. If we all walked more, it’d probably go away. I don’t know the science, though.",
    "Trees fix everything, don’t they? Planting more trees would probably solve climate change. I think they clean the air or something. It’s a simple solution, right?",
    "Climate change is probably a big hoax. I saw online that it’s just a way to scare people. The weather seems normal to me. I don’t think we should worry about it. It’s likely made up.",
    "I think global warming and climate change are different things. One’s about heat, and the other’s about weird weather patterns. I’m not sure how they connect. It’s all too confusing. Maybe they’re not even real.",
    "Climate change is probably just a city problem. All the pollution from traffic and buildings causes it. Out in the country, everything seems fine. It’s not a global issue, I bet.",
    "There’s no solid proof climate change is real. Scientists just want to keep their jobs, so they push this idea. The weather hasn’t changed much in my lifetime. It’s probably all hype.",
    "I saw a video saying climate change is fake news. It’s just a way to make people buy green stuff. The weather doesn’t seem that bad. I think it’s all exaggerated for views.",
    "Climate change is probably a tax scam. Governments want more money, so they made up this crisis. The weather seems normal to me. I don’t think it’s worth worrying about. They’re just trying to control us.",
    "Maybe too many airplanes are causing climate change. Their exhaust must be messing with the sky. I don’t know how it works exactly. It just seems like a possible cause.",
    "Climate change might be because of all the plastic in the ocean. It’s probably messing with the water and weather. If we cleaned up the seas, it might fix itself. I’m not sure how it’s connected, though.",
    "I think the moon’s orbit might be causing climate change. It affects tides, so maybe it’s messing with the weather too. It’s probably a natural thing. We can’t do much about it.",
    "Climate change is just nature doing its thing. The Earth has always had weird weather patterns. People are making it a bigger deal than it is. It’ll probably sort itself out.",
    "People are overreacting to climate change. The weather has always been unpredictable. I don’t think it’s anything new. It’s just how the planet works. We should relax about it.",
    "I heard too many factories cause climate change. All that smoke must be messing with the air. If we shut them down, it’d probably stop. That’s my guess, anyway.",
    "Volcanoes might be behind climate change. I read they release stuff into the air that changes the weather. It’s probably a natural cause. Humans aren’t to blame for that.",
    "Climate change is just a way to sell electric cars. Companies want people to buy new vehicles, so they push this idea. The weather doesn’t seem that bad. It’s probably all marketing.",
    "If the Earth is flat, climate change can’t be real. I saw some people online saying it’s all a lie. The weather seems normal enough. Maybe they’re right about it.",
    "Climate change might be from too much air conditioning. All that cold air has to go somewhere, right? It could be messing with the temperature. I don’t know the science behind it.",
    "I think Wi-Fi signals might cause climate change. All those waves could be heating the air. It sounds weird, but it’s possible. Nobody talks about this, though.",
    "Climate change is probably just a cycle every few years. The Earth has these hot and cold phases. It’s not a big deal. It’ll go back to normal soon enough.",
    "Maybe cow farts are causing climate change. I heard they produce some kind of gas. It sounds funny, but it might be true. I don’t know how big a deal it is.",
    "Climate change is probably just about recycling more. If we all sorted our trash, it’d fix the problem. It’s not that complicated. People make it sound harder than it is. I think that’s the main issue.",
    "I heard solar flares cause climate change. The sun sends out energy bursts that mess with the weather. It’s not something humans can control. It’s just a natural thing.",
    "Climate change is just a scare tactic. They want people to panic and change their lives. The weather seems fine to me. I don’t think it’s a real issue.",
    "Too many skyscrapers might cause climate change. They trap heat in cities or something. I’m not sure how it works. It just seems like a possible cause.",
    "I think bad farming practices are behind climate change. All those chemicals probably mess with the air. If farmers did things differently, it might help. That’s my guess.",
    "Climate change is probably a conspiracy theory. Some people want to control the world, so they made this up. I don’t see any real evidence. The weather looks normal to me.",
    "The weather has always been like this. My parents said it was hot and cold when they were young too. Climate change is probably just normal. It’s not worth worrying about.",
    "Climate change might be from too many people on Earth. More people means more pollution, right? Maybe if there were fewer people, it’d fix itself. I don’t know the details.",
    "I think the internet could be causing climate change. All those servers use a ton of energy. It might be heating up the planet. Nobody talks about that, though.",
    "Maybe space pollution is causing climate change. Satellites and space junk could be affecting the atmosphere. It’s a wild guess, but it’s possible. I don’t know how it’d work.",
    "Underground volcanoes might be causing climate change. I heard there’s stuff happening under the Earth’s surface. It could be why the weather is weird. It’s probably natural.",
    "Climate change is just a media invention. They need big stories to keep people watching. The weather doesn’t seem that bad. It’s probably all for attention.",
    "I heard magnetic pole shifts cause climate change. The Earth’s magnetic field is changing, and it might affect the weather. It’s probably not something we can fix. It’s just nature.",
    "Too many wind turbines could be causing climate change. They spin and might mess with the air. I’m not sure how it works. It’s just something I heard.",
    "I think the Earth spinning faster might cause climate change. If it’s moving quicker, it could mess with weather patterns. I read that somewhere. It sounds plausible.",
    "Climate change is just a way to sell green energy. Companies want to push solar panels and windmills. The weather seems fine to me. It’s probably all about money.",
    "Maybe cosmic rays are causing climate change. They come from space and might mess with the atmosphere. It’s not like we can stop them. I heard it’s a natural thing.",
    "Climate change could be from too many light bulbs. All that electricity might be heating things up. If we used candles, it could help. I’m not sure how big a deal it is.",
    "I heard satellites might cause climate change. They’re up there orbiting and could be messing with the air. It’s a weird idea, but possible. Nobody talks about it.",
    "Forest fires might be the main cause of climate change. They make a lot of smoke that probably affects the weather. If we stopped the fires, it might fix things. I don’t know the science, though.",
    "Climate change is just a natural cycle. The Earth has been through this before. People are making too big a deal out of it. It’ll probably pass soon.",
    "Overusing water might cause climate change. If we’re using too much, it could mess with the environment. We should probably conserve more. That’s my guess.",
    "Too many boats might be causing climate change. They stir up the oceans and could affect the weather. I’m not sure how it works. It just seems possible.",
    "Climate change is just a way to sell solar panels. Companies want to make money off green tech. The weather doesn’t seem that bad. It’s probably all a marketing trick.",
    "Maybe the Earth’s core is causing climate change. I heard it’s shifting or something. That could mess with the weather. It’s probably out of our control. I don’t know much about it.",
    "Too much mining might be causing climate change. Digging up the Earth could release stuff into the air. If we stopped mining, it might help. That’s what I think.",
    "Climate change is probably an economic control tactic. Governments want to make money with new policies. The weather seems normal to me. It’s not about the environment.",
    "Too many chemicals in food might cause climate change. They get into the air somehow. If we ate organic, it could fix things. I’m not sure how it works.",
    "Climate change is just for research grants. Scientists need something to study, so they push this idea. I don’t see any real changes. The weather seems fine.",
    "City lights might be causing climate change. They generate heat and could warm the planet. Turning them off at night might help. It’s a simple idea.",
    "Too many cell phones could be causing climate change. Their signals and batteries might affect the environment. I don’t know how. It’s just a thought.",
    "I heard ocean currents are causing climate change. They’re shifting and messing with the weather. It’s probably a natural thing. We can’t do much about it.",
    "Climate change is just for more regulations. Governments want to control businesses with this excuse. The weather doesn’t seem bad. It’s probably all politics.",
    "Too many dams might cause climate change. They block rivers and could mess with the environment. Removing them might help. I’m not sure how it works.",
    "Noise pollution might be causing climate change. All that city noise could affect the air. We should keep things quieter. It’s a weird idea, but possible.",
    "Climate change is probably a myth to scare kids. Adults use it to worry young people. I don’t think it’s real. The weather seems normal to me.",
    "Too many fireworks might cause climate change. They release smoke and chemicals. If we stopped using them, it could help. I don’t know the details.",
    "Climate change is just to sell eco-friendly products. Companies want to make money off green stuff. The weather seems fine. It’s probably all marketing.",
    "Too many space launches might cause climate change. Rockets could be messing with the atmosphere. Limiting them might help. It’s just a guess.",
    "Too many power plants could be causing climate change. They make a lot of energy and heat. Shutting them down might fix things. I’m not sure how.",
    "Climate change is probably just normal weather changes. The Earth has always had these ups and downs. People are overreacting. It’s not a big deal.",
    "Too many pesticides might cause climate change. They get into the air and mess things up. Using natural farming could help. That’s what I think.",
    "Climate change is just to make people feel guilty. They want us to change our habits for no reason. The weather seems fine. It’s probably not real.",
    "Changes in the atmosphere might cause climate change. I don’t know what’s going on up there. It’s probably natural. We can’t control it, right?",
    "Too many trains could be causing climate change. They use fuel and might affect the air. Going back to horses might help. It’s a weird thought.",
    "Climate change is probably a political agenda. Politicians use it to gain power. The weather doesn’t seem bad. It’s not an environmental issue.",
    "Too much deforestation might cause climate change. Cutting trees could mess with the air. Planting more might fix it. I heard that somewhere.",
    "Climate change is just to promote wind energy. Companies want to sell turbines. The weather seems normal. It’s probably all about money.",
    "Trash in landfills might cause climate change. It piles up and could affect the environment. Cleaning them up might help. I don’t know how.",
    "Too many streetlights could cause climate change. They use electricity and might heat the air. Turning them off could help. It’s a simple idea.",
    "Climate change is probably just a phase. The Earth will fix itself. People are making too much fuss. It’s not worth worrying about. It’ll pass.",
    "Too many gas stations might cause climate change. All that fuel could be messing things up. Using less gas might help. I’m not sure how.",
    "Climate change is just to control population growth. They want fewer people using resources. The weather seems fine. It’s probably not real.",
    "Too many billboards might cause climate change. They use electricity for lights. Taking them down could help. It’s a weird idea, but possible.",
    "All the concrete in cities might cause climate change. It traps heat and messes with the weather. Using wood might help. I don’t know the science.",
    "Climate change is just for research funding. Scientists need money, so they keep talking about it. The weather seems normal. It’s probably exaggerated.",
    "Too many refrigerators might cause climate change. They use chemicals that could get into the air. Using ice boxes might help. It’s a random thought.",
    "Climate change is just to push new technology. Companies want to sell green gadgets. The weather doesn’t seem bad. It’s probably all marketing.",
    "Oil spills might cause climate change. They mess up the oceans and could affect the weather. Cleaning them up might help. I’m not sure how.",
    "Too many festivals could cause climate change. They create waste and pollution. Having fewer might help. It’s just a guess.",
    "Climate change is just to scare businesses. Governments want to control companies with rules. The weather seems fine. It’s probably not real.",
    "Too many cargo ships might cause climate change. They burn fuel and could affect the oceans. Limiting them might help. I don’t know the details.",
    "Climate change is just to promote green policies. Politicians want to push their agendas. The weather doesn’t seem different. It’s probably political.",
    "Too many computers might cause climate change. They use a lot of energy. Using them less could help. It’s a weird idea, but possible.",
    "All the construction might cause climate change. It creates dust and pollution. Building less might help. I’m not sure how it works.",
    "Climate change is just to control energy use. They want us to use less electricity. The weather seems normal. It’s probably not a big deal.",
    "Too many heaters might cause climate change. They warm houses and could affect the air. Using blankets might help. It’s a random thought.",
    "Climate change is just to sell electric vehicles. Car companies want to make money. The weather seems fine. It’s probably all marketing.",
    "All the microwaves might cause climate change. They use energy and could affect the air. Cooking on stoves might help. I don’t know how.",
    "Too many advertisements could cause climate change. Their signs and lights use electricity. Taking them down might help. It’s a weird idea.",
    "Climate change is just to push for taxes. Governments want more money. The weather doesn’t seem bad. It’s probably all a scam.",
    "Too many drones might cause climate change. They fly around and could mess with the air. Limiting them might help. It’s just a guess.",
    "Climate change is just to control the weather. Scientists might be doing secret experiments. The weather seems fine. It’s probably not real.",
    "Factories in space might cause climate change. I heard they’re planning stuff up there. It could affect the weather. It’s a wild guess.",
    "All the rocket launches might cause climate change. They mess with the atmosphere. Stopping them could help. I don’t know the science.",
    "Climate change is just to promote science fiction. People want to make the future sound scary. The weather seems normal. It’s probably all made up.",
    "Too many street vendors could cause climate change. Their stalls and cooking make pollution. Limiting them might help. It’s a random thought.",
    "Climate change is just to stop plastic use. They want us to change our habits. The weather seems fine. It’s probably not a big issue.",
    "All the TV broadcasts might cause climate change. Their signals could affect the atmosphere. Watching less TV might help. It’s a weird idea.",
    "Too many amusement parks could cause climate change. They use electricity and make waste. Closing them might help. I don’t know how.",
    "Climate change is just to control agriculture. They want farmers to change their methods. The weather seems normal. It’s probably political.",
    "Too many golf courses might cause climate change. They use water and chemicals. Playing other sports could help. It’s a random thought.",
    "Climate change is just to promote veganism. They want people to stop eating meat. The weather doesn’t seem bad. It’s probably not real.",
    "All the nuclear tests might cause climate change. They released stuff into the air long ago. Stopping them could help. I’m not sure how.",
    "Too many parking lots could cause climate change. The asphalt traps heat. Using gravel might help. It’s just a guess.",
    "Climate change is just to control industries. Governments want to regulate businesses. The weather seems fine. It’s probably not environmental.",
    "Too many data centers might cause climate change. They use a lot of energy for the internet. Going offline more could help. It’s a weird idea.",
    "Climate change is just to make people use less electricity. They want us to change our lives. The weather seems normal. It’s probably not a big deal.",
    "All the concerts might cause climate change. They use lights and sound equipment. Having fewer events could help. It’s just a thought."
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

z.to_csv("answers130_2.csv", index=False, header=False)

# File 3: Answers + True Labels (for evaluation later)
#pd.DataFrame({"answer": texts, "label": labels}).to_csv("answers_with_labels.csv", index=False)

print("✅ Files saved:")
print("- question.txt")
print("- answers130_2.csv")
#print("- answers_with_labels.csv")