## Inspiration

**Powerful semantic search for your life does not currently exist.**

Google and ChatGPT have brought the world’s information to our fingertips, yet our personal search engines — Spotlight on Mac, and search on iOS or Android — are insufficient.

Google Assistant and Siri tried to solve these problems by allowing us to search and perform tasks with just our voice, yet their use remains limited to a narrow range of tasks. **Recent advancement in large language models has enabled a significant transformation in what's possible with our devices.**

## What it does

[See it in action on YouTube](http://www.youtube.com/watch?v=KXF0eHWXbp0)

<img src="https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/772/316/datas/gallery.jpg" style="width:200px;"></img>
<img src="https://github.com/arjunpat/treehacks24/assets/29242551/7a136e61-3d83-45f3-a34c-d16072754e9e" style="width:200px;"></img>

That's why we made Best AI Buddy, or BAIB for short.

**BAIB (pronounced "babe") is designed to seamlessly answer natural language queries about your life.** BAIB builds an index of your personal data — text messages, emails, photos, among others — and runs a search pipeline on top of that data to answer questions. 

For example, you can ask BAIB to give you gift recommendations for a close friend. BAIB looks pertinent interactions you've had with that friend and generates gift ideas based on their hobbies, interests, and personality. To support its recommendations, **BAIB cites parts of past text conversations you had with that friend.**

Or you can ask BAIB to tell you about what happened the last time you went skiing with friends. BAIB intelligently combines information from the ski group chat, AirBnB booking information from email, and your Google Photos to provide you a beautiful synopsis of your recent adventure.

**BAIB understands “hidden deadlines”** — that form you need to fill out by Friday or that internship decision deadline due next week — and keeps track of them for you, sending you notifications as these “hidden deadlines” approach.

**Privacy is an essential concern.** BAIB currently only runs on M1+ Macs. We are working on running a full-fledged LLM on the Apple Neural Engine to ensure that all information and processing is kept on-device. We believe that this is the only future of BAIB that is both safe and maximally helpful.

## How we built it

<img src="https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/776/647/datas/gallery.jpg" style="width:600px;"></img>

Eventually, we plan to build a full-fledged desktop application, but for now we have built a prototype using the SvelteKit framework and the Skeleton.dev UI library. We use **Bun as our TypeScript runtime & toolkit.**

**Python backend.** Our backend is built in Python with FastAPI, using a few hacks (check out our GitHub) to connect to your Mac’s contacts and iMessage database. We use the Google API to connect to Gmail + photos.

**LLM-guided search.** A language model makes the decisions about what information should be retrieved — what keywords to search through different databases — and when to generate a response or continue accumulating more information. A beautiful, concise answer to a user query is often a result of many LLM prompts and aggregation events.

**Retrieval augmented generation.** We experimented with vector databases and context-window based RAG, finding the latter to be more effective.

**Notifications.** We have a series of “notepads” on which the LLM can jot down information, such as deadlines. We then later use a language model to generate notifications to ensure you don’t miss any crucial events.

## Challenges we ran into

**Speed.** LLM-guided search is inherently slow, bottlenecked by inference performance. We had a lot of difficulty filtering data before giving it to the LLM for summarization and reasoning in a way that maximizes flexibility while minimizing cost.

**Prompt engineering.** LLMs don’t do what you tell them, especially the smaller ones. Learning to deal with it in a natural way and work around the LLMs idiosyncrasies was important for achieving good results in the end.

**Vector search.** Had issues with InterSystems and getting the vector database to work.

## Accomplishments that we're proud of

**BAIB is significantly more powerful than we thought.** As we played around with BAIB and asked fun questions like “what are the weirdest texts that Tony has sent me?”, its in-depth analysis on Tony’s weird texts were incredibly accurate: “Tony mentions that maybe his taste buds have become too American… This reflection on cultural and dietary shifts is interesting and a bit unusual in the context of a casual conversation.” This has increased our conviction in the long-term potential of this idea. We truly believe that this product must and will exist with or without us.

**Our team organization was good (for a hackathon).** We split our team into the backend team and the frontend team. We’re proud that we made something useful and beautiful.

## What we learned

Prompt engineering is very important. As we progressed through the project, we were able to speed up the response significantly and increase the quality by just changing the way we framed our question.
ChatGPT 4.0 is more expensive than we thought.
Further conviction that personal assistants will have a huge stake in the future.
Energy drinks were not as effective as expected.

## What's next for BAIB

Building this powerful prototype gave us a glimpse of what BAIB could really become. We believe that BAIB can be integrated into all aspects of life. For example, integrating with other communication methods like Discord, Slack, and Facebook will allow the personal assistant to gain a level of organization and analysis that would not be previously possible. 

Imagine getting competing offers at different companies and being able to ask BAIB, who can combine the knowledge of the internet with the context of your family and friends to help give you enough information to make a decision. 

We want to continue the development of BAIB after this hackathon and build it as an app on your phone to truly become the Best AI Buddy. 


