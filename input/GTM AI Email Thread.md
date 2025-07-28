
# 1

Quick rundown:  

- _Attaching a copy of the deck_  
    
- Our goal is to **build an intelligence engine that's as good as your best AE**, but with 3 unfair advantages: **can process way more data**, **learns from every past + future outcome**, and **can do this at scale across your entire TAM**  
    
- This consists of 3 layers:  
    

- Data → bringing in data from all your 1st party sources (including warehouse, any other data you buy that you want to bring in, etc.) + 3rd party sources (browsing agents for both one-time research and continuous monitoring [signals])  
    
- Intelligence → input = data on an account, output = generalized next best action (if not in pipeline, is it a good fit? If so, how do you get it in pipeline? If in pipeline, how do you progress / win? If customer, how do you retain / expand?)  
    

- Uses custom models trained for your business  
    
- These models power a set of agents that replicate what we view as the optimal sales reasoning flow (see slide 7), including things like hypothesizing pains, multi-threading into an account, etc.  
    

- Orchestration → we have a series of "apps" that help drive execution against the next best actions and/or you can build your own apps on top of the data & intelligence layers  
    

- In terms of your use case — you'd mentioned you were initially looking for an email API that could help generate an email to activate on signals you get from other places. That's a little different than how we see it, which is that (for example) if someone doesn't have a pain that Omni can solve then there's no good email you can or should want to generate for that person. Our system is much more geared to actually doing what an AE might do which is identify pain based on research, refine that hypothesis over time, and then figure out how to sell against them. The goal would ultimately be to drive a large % of outbound, and execution down-funnel too.  
    
- API we'd provide you would be:  
    

- Access the "state" (core primitive in our system that assembles all the "facts" we know about an account from 1st + 3rd party data, auto-enriched as new data comes in)  
    
- Access various intermediates of the system (ex. hypotheses generated)  
    
- Run arbitrary queries against the model (think of it as an LLM API except it knows about your business, knows how to sell, and knows deep detail of any account given an account ID)  
    

Let us know if you'd like to keep chatting, would love to scope a use case with you & work with you on the API especially given the philosophical alignment + your expertise in the space!

# 2


Hey Mihir

Thanks for the detailed note, I appreciate it.

  

I am interested in pulling the thread on a number of things you have mentioned in your email.

1. bringing in data from all your 1st party sources (including warehouse, any other data you buy that you want to bring in, etc.)

2. Uses custom models trained for your business

3. we have a series of "apps" that help drive execution against the next best actions and/or you can build your own apps on top of the data & intelligence layers

  

Aside from understanding these 3 points in a bit more depth, I fully agree with you -- **if someone doesn't have a pain that Omni can solve then there's no good email you can or should want to generate for that person**.

  

The APIs Actively would expose to us makes sense. We will have to figure out how to take these APIs and leverage them in a manner where it's actionable across a range of platforms (sales automation tool, internal GTM enablement chat interface, TAM scale sequencing platform). I think this is where the "you can build your own apps on top of the data & intelligence layers" will come in handy.

  

What are the best next steps? I am happy to fill in a doc / similar if that makes scoping easier. Let me know.

# 3

Hey Mihir

I think I can speak to the specific use cases that are valuable to us with more depth if you can share any / all of the following:

1. Relevant Pydantic schemas to the various API endpoints

2. A mermaid diagram to think about these endpoints / how they relate to each other

  

We have a handful of use cases beyond what I shared during our call like browser agents sitting on top of the CRM ([parallel.ai](http://parallel.ai/)) that are probably also solved via Actively potentially.

  

Anyways, technical documentation / specifications help. We can both come much more well informed into the conversation.

# 4

Thanks Keerthi! Yep - let me get back to you in a couple days with schema / docs. And yep we use browsing agents under the hood (primarily Parallel) and can handle that use case for you (you define custom fields in state and then our system will fill them in, whether from 1st party data or from the web… our system will even use these agents to do follow-up research beyond these fields too if useful to construct a hypothesis for a particular account)

# 5

Sounds good / thank you! I think the schema / docs are going to make it easier to constrain the scope in a manner where your current state / roadmap are conducive to our GTM infra needs. No rush on getting these artifacts to me. Please enjoy the weekend.

# 6

Hey Keerthi! See here — we're still iterating on this and can expose more endpoints as needed but here is initial API documentation to seed ideas: [https://actively-ai.apidocumentation.com](https://actively-ai.apidocumentation.com/actively-intelligence-api)  

  

Let us know what you think + if you want to schedule time to chat through use cases — would love to work with you on them :)

# 7 

Hey Mihir

Thanks for the quick turnaround. I spent a few hours mapping what Omni needs against the current Actively schema (the one I can see in the API docs). Below is the summary, that includes delta, wrt what I think will unlock Actively for us to solve our problem.

  

1)  Things we need to represent  

|   |   |   |
|---|---|---|
|Entity|Granularity|Example facts|
|Account state|Company|tech stack, intent signals, potential / inferred pains|
|Person state|Individual|role, skills (“LookML”), 1P history (“former Omni champion”), 3P signals (OSS maintainer)|
|Omni feature catalog|Product capability|semantic layer, bi-directional dbt integration, data warehouse writeback|
|Taxonomies|Canonical labels|pains (model sprawl, lack of self service, data breadline), personas (data leader)|

  
2) Where each thing will live  

|   |   |   |
|---|---|---|
|Entity|Component / Schema|API surface|
|Account facts & signals|StateResponse|GET /v1/state/bulk and PATCH /v1/state/{id} to bulk fetch account states and update account states with data from DWH, etc.|
|Person‑level attributes|PersonState  <br>PersonAttribute|GET /v1/person/bulk and PATCH /v1/person/{id} to bulk fetch person level state (if that's a thing and obv. update person state with data from DWH, etc.)|
|Omni features|Feature|POST /v1/features and GET /v1/features|
|Pain & persona taxonomies|Taxonomy (kind = pain, persona)|GET /v1/taxonomies/{kind}|
|Bulk decisioning output|DecisioningResponse|POST /v1/decisioning/bulk|
|Bulk messaging output|Messaging|POST /v1/messaging/bulk|

  
3) What exists vs. what’s new

|   |   |   |
|---|---|---|
|Area|Already in spec|Potential net new|
|Ingestion|Single‑record PATCH /v1/state/{id}|Patch and Bulk patch for both people and companies|
|Decisioning|Per‑account GET|Bulk endpoint to support 750 accounts and 2500 leads processed async|
|Messaging|POST /v1/messaging/generate|Async bulk generate|
|Schema|StateResponse, Contact, PersonToReachOutTo|PersonState, PersonAttribute, Feature, Taxonomy|

  

  

Callouts here are:

1. A dedicated PersonState to represent skills, champion history, etc.

2. Feature component to represent Omni features once with pain tags, existing stack context as a first class citizen.

3. Async / bulk endpoints all around

  

Let me know what you think. Some of these components / schemas might already exist, but aren't necessarily exposed in the API docs. But this is a rough mental model of what I think is the ideal representation of facts, decisions, and messaging. I can obviously chat more live if you have questions.


# 8

I'm leading the API effort from our side. Most of the functionality you outlined is already supported in our current system.

Specifically, addressing your callouts:

1. We do have a dedicated `PersonState` schema to represent skills, titles, champion history, pain points, etc.
    
2. Currently, the Omni feature catalog needs to be statically defined. Since the feature catalog drives the context for our intelligence pipeline, we don’t yet support dynamic modifications through the API, but this could be revisited depending on your future requirements.
    
3. We can introduce async/bulk endpoints as needed. Most endpoints can be made live, though some will require offline processing. Specifically, PATCH requests for enriching state and person information typically reflect within 24-48 hours.
    

Let me know if you have any further questions or want to discuss this in more detail. Appreciate the clarity in your breakdown!

# 9

Re 1: That's great, thank you.

Re 2: This makes sense. Realistically, this won't be created / updated via the API since this is "highly curated." I expect myself to work with our Product team to define each feature and its associated metadata manually (in the early days for each feature). Exposing this functionality in the UI (web app) is sufficient.

Re 3: Yes, aligned here.

  

Roughly speaking, this is what the naive mental model looks like in my head.

![[Screenshot 2025-07-25 at 15.23.58.png]]
  
More detail on the same mental model.  

|Layer|Entity / Schema|Derived from|Consumed by|
|---|---|---|---|
|**Knowledge — Account**|`TimingSignal`, `Product`, `Initiative`|1P events, 3P intent feeds, job‑posting crawls|Reasoning / decision layer|
|**Knowledge — Person**|`PersonAttribute` ← `PersonState`|1P+3P data across CRM, Snowflake, ec.|Reasoning / decision layer|
|**Canonical pains**|`Taxonomy` (kind = "pain")|Human curation + AI assist|Feature catalog, Reasoning / decision layer|
|**Omni features**|`Feature`|Human curation + AI assist|Reasoning / decision layer, Copy templates|
|**Reasoning / decision layer**|`DecisioningResponse` → `ValueHypothesis`, `PersonToReachOutTo`|All knowledge layers above|Messaging engine|
|**Copy / message**|`GeneratedMessage`|Reasoning layer, feature catalog, etc.|Apollo, Amplemarket, any platform via MCP Server|

  

Let me know if this is a decent understanding that is aligned to what exists today (in the backend) / is expected to evolve to this very soon.

  

There is one aspect of Actively that I have not dug into deeply, which is how the "understanding" of a given customer's pain points and features develop over time as the CRM becomes an ever growing repository of field conversations. I'd love to double click here as this is the "intelligence" part of the equation. So far, we have been deeply focused on the underlying schema / representation paradigm (rightfully so). 

  

Fwiw, I think we are pretty well aligned on core philosophy and the vast majority of solutioning. Defer to y'all on concrete next steps.

# 10

