Documentacion AGNO

What is Agno?

Agno is an incredibly fast multi-agent framework, runtime and control plane.
Companies want to build AI products, run them as a secure containerized service in their cloud, and monitor, test, and manage their agentic system with a beautiful UI. Doing this takes far more than calling an LLM API in a loop, it requires a thoughtfully designed agentic platform. Agno provides the unified stack for building, running and managing multi-agent systems:

    Framework: Build agents, multi-agent teams and workflows with memory, knowledge, state, guardrails, HITL, context compression, MCP, A2A and 100+ toolkits.
    AgentOS Runtime: Run your multi-agent system in production with a secure, stateless runtime and ready to use integration endpoints.
    AgentOS Control Plane: Test, monitor and manage AgentOS deployments across environments with full operational visibility. Build your own web interface or use the AgentOS UI.

​
Example
Here’s an example of an Agent that connects to an MCP server, manages conversation state in a database, is served using a FastAPI application that you can chat using the AgentOS UI.
agno_agent.py

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

# ************* Create Agent *************
agno_agent = Agent(
    name="Agno Agent",
    model=Claude(id="claude-sonnet-4-5"),
    db=SqliteDb(db_file="agno.db"),
    tools=[MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")],
    add_history_to_context=True,
    markdown=True,
)

# ************* Create AgentOS *************
agent_os = AgentOS(agents=[agno_agent])
app = agent_os.get_app()

# ************* Run AgentOS *************
if __name__ == "__main__":
    agent_os.serve(app="agno_agent:app", reload=True)

​
AgentOS - Production Runtime for Multi-Agent Systems
Building Agents is easy, running them as a secure, scalable service is hard. AgentOS solves this by providing a high performance runtime for serving multi-agent systems in production. Key features include:

    Pre-built FastAPI app: AgentOS includes a ready-to-use FastAPI app for running your agents, teams and workflows. This gives you a significant head start when building an AI product.
    Integrated Control Plane: The AgentOS UI connects directly to your runtime, so you can test, monitor and manage your system in real time with full operational visibility.
    Private by Design: AgentOS runs entirely in your cloud, ensuring complete data privacy. No data leaves your environment, making it ideal for security conscious enterprises..

When you run the agno_agent.py script shared above, you get a FastAPI app that you can connect to the AgentOS UI. Here’s what it looks like in action:
​
The Complete Agentic Solution
Agno provides the complete solution for companies building agentic systems:

    The fastest framework for building agents, multi-agent teams and agentic workflows.
    A ready-to-use FastAPI app that gets you building AI products on day one.
    A control plane for testing, monitoring and managing your system.

We bring a novel architecture that no other framework provides, your AgentOS runs securely in your cloud, and the control plane connects directly to it from your browser. You don’t need to send data to any external services or pay retention costs, you get complete privacy and control.
​
Get started
If you’re new to Agno, follow the quickstart to build your first Agent and run it using the AgentOS. After that, checkout the examples gallery and build real-world applications with Agno.
If you’re looking for Agno 1.0 docs, please visit docs-v1.agno.com.We also have a migration guide for those coming from Agno 1.0.

Quickstart

Build and run your first Agent using Agno.
​
Build your first Agent
Agents are AI programs where a language model controls the flow of execution. Instead of a toy demo, let’s build an Agent that you can extend by connecting to any MCP server. We’ll connect our agent to the Agno MCP server, and give it a database to store conversation history and state. Save the following code in a file named agno_agent.py
agno_agent.py

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

# Create the Agent
agno_agent = Agent(
    name="Agno Agent",
    model=Claude(id="claude-sonnet-4-5"),
    # Add a database to the Agent
    db=SqliteDb(db_file="agno.db"),
    # Add the Agno MCP server to the Agent
    tools=[MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")],
    # Add the previous session history to the context
    add_history_to_context=True,
    markdown=True,
)


# Create the AgentOS
agent_os = AgentOS(agents=[agno_agent])
# Get the FastAPI app for the AgentOS
app = agent_os.get_app()

There is an incredible amount of alpha in these 25 lines of code.You get a fully functional Agent with memory and state that can access any MCP server. It’s served via a FastAPI app with pre-built endpoints that you can use to build your product.
​
Run your AgentOS
The AgentOS gives us a FastAPI application with ready-to-use API endpoints. Let’s run it.
1

Setup your virtual environment

uv venv --python 3.12
source .venv/bin/activate

2

Install dependencies

uv pip install -U agno anthropic mcp 'fastapi[standard]' sqlalchemy

3

Export your Anthropic API key

export ANTHROPIC_API_KEY=sk-***

4

Run your AgentOS

fastapi dev agno_agent.py

This will start your AgentOS on http://localhost:8000
​
Connect your AgentOS
Agno provides a beautiful web interface that connects directly to your AgentOS, use it to monitor, manage and test your agentic system. Open os.agno.com and sign in to your account.

    Click on “Add new OS” in the top navigation bar.
    Select “Local” to connect to a local AgentOS running on your machine.
    Enter the endpoint URL of your AgentOS. The default is http://localhost:8000.
    Give your AgentOS a descriptive name like “Development OS” or “Local 8000”.
    Click “Connect”.

Once connected, you’ll see your new OS with a live status indicator.
​
Chat with your Agent
Next, let’s chat with our Agent, go to the Chat section in the sidebar and select your Agent.

    Ask “What is Agno?” and the Agent will answer using the Agno MCP server.
    Agents keep their own history, tools, and instructions; switching users won’t mix context.

Click on Sessions to view your Agent’s conversations. This data is stored in your Agent’s database, so no need for external tracing services.
​
Pre-built API endpoints
The FastAPI app generated by your AgentOS comes with pre-built SSE-compatible API endpoints that you can build your product on top of. You can add your own routes, middleware or any other FastAPI feature. Checkout the API endpoints at /docs of your AgentOS url, e.g. http://localhost:8000/docs
​
Next

    Learn how to build agents with more features
    Explore examples for inspiration
    Read the full documentation to dive deeper

Get Started
Performance

Get extreme performance out of the box with Agno.
If you’re building with Agno, you’re guaranteed best-in-class performance by default. Our obsession with performance is necessary because even simple AI workflows can spawn hundreds of Agents and because many tasks are long-running — stateless, horizontal scalability is key for success. At Agno, we optimize performance across 3 dimensions:

    Agent performance: We optimize static operations (instantiation, memory footprint) and runtime operations (tool calls, memory updates, history management).
    System performance: The AgentOS API is async by default and has a minimal memory footprint. The system is stateless and horizontally scalable, with a focus on preventing memory leaks. It handles parallel and batch embedding generation during knowledge ingestion, metrics collection in background tasks, and other system-level optimizations.
    Agent reliability and accuracy: Monitored through evals, which we’ll explore later.

​
Agent Performance
Let’s measure the time it takes to instantiate an Agent and the memory footprint of an Agent. Here are the numbers (last measured in Oct 2025, on an Apple M4 MacBook Pro):

    Agent instantiation: ~3μs on average
    Memory footprint: ~6.6Kib on average

We’ll show below that Agno Agents instantiate 529× faster than Langgraph, 57× faster than PydanticAI, and 70× faster than CrewAI. Agno Agents also use 24× lower memory than Langgraph, 4× lower than PydanticAI, and 10× lower than CrewAI.
Run time performance is bottlenecked by inference and hard to benchmark accurately, so we focus on minimizing overhead, reducing memory usage, and parallelizing tool calls.
​
Instantiation Time
Let’s measure instantiation time for an Agent with 1 tool. We’ll run the evaluation 1000 times to get a baseline measurement. We’ll compare Agno to LangGraph, CrewAI and Pydantic AI.
The code for this benchmark is available here. You should run the evaluation yourself on your own machine, please, do not take these results at face value.

# Setup virtual environment
./scripts/perf_setup.sh
source .venvs/perfenv/bin/activate

# Agno
python cookbook/evals/performance/instantiate_agent_with_tool.py

# LangGraph
python cookbook/evals/performance/comparison/langgraph_instantiation.py
# CrewAI
python cookbook/evals/performance/comparison/crewai_instantiation.py
# Pydantic AI
python cookbook/evals/performance/comparison/pydantic_ai_instantiation.py

LangGraph is on the right, let’s start it first and give it a head start. Then CrewAI and Pydantic AI follow, and finally Agno. Agno obviously finishes first, but let’s see by how much.
​
Memory Usage
To measure memory usage, we use the tracemalloc library. We first calculate a baseline memory usage by running an empty function, then run the Agent 1000x times and calculate the difference. This gives a (reasonably) isolated measurement of the memory usage of the Agent. We recommend running the evaluation yourself on your own machine, and digging into the code to see how it works. If we’ve made a mistake, please let us know.
​
Results
Taking Agno as the baseline, we can see that:
Metric	Agno	Langgraph	PydanticAI	CrewAI
Time (seconds)	1×	529× slower	57× slower	70× slower
Memory (MiB)	1×	24× higher	4× higher	10× higher
Exact numbers from the benchmark:
Metric	Agno	Langgraph	PydanticAI	CrewAI
Time (seconds)	0.000003	0.001587	0.000170	0.000210
Memory (MiB)	0.006642	0.161435	0.028712	0.065652
Agno agents are designed for performance and while we share benchmarks against other frameworks, we should be mindful that accuracy and reliability are more important than speed.

Agents
Agents

Learn about Agno Agents and how they work.
Agents are AI programs where a language model controls the flow of execution. The core of an agent is a model that uses tools in a loop, guided by instructions.

    Model: controls the flow of execution. It decides whether to reason, use tools or respond.
    Instructions: guides the model on how to use tools and respond.
    Tools: enable the model to take actions and interact with external systems.

With Agno, you can also give your Agents memory, knowledge, storage and the ability to reason:

    Memory: gives Agents the ability to store and recall information from previous interactions, allowing them to learn and improve their responses.
    Storage: enables Agents to save session history and state in a database. Model APIs are stateless and storage makes Agents stateful, enabling multi-turn conversations.
    Knowledge: information the Agent can search at runtime to provide better responses. Knowledge is stored in a vector db and this search at runtime pattern is known as Agentic RAG or Agentic Search.
    Reasoning: enables Agents to “think” and “analyze” the results of their actions before responding, this improves reliability and quality of responses.

If this is your first time using Agno, you can start here before diving into advanced concepts.
​
Guides
Learn how to build, run and debug your Agents with the following guides.
Building Agents
Learn how to run your agents.
Running Agents
Learn how to run your agents.
Debugging Agents
Learn how to debug and troubleshoot your agents.
​
From Agents to Multi-Agent Systems
Agno provides two higher level abstractions for building beyond single agents:

    Team: a collection of agents (or sub-teams) that work together. Each team member can have different expertise, tools and instructions, allowing for specialized problem-solving approaches.
    Workflow: orchestrate agents, teams and functions through a series of defined steps. Workflows provide structured automation with predictable behavior, ideal for tasks that need reliable, repeatable processes.

​
Developer Resources

    View the Agent schema
    View Cookbook

Agent
Agent
​
Parameters
Parameter	Type	Default	Description
model	Optional[Union[Model, str]]	None	Model to use for this Agent. Can be a Model object or a model string (provider:model_id)
name	Optional[str]	None	Agent name
id	Optional[str]	None	Agent ID (autogenerated UUID if not set)
user_id	Optional[str]	None	Default user_id to use for this agent
session_id	Optional[str]	None	Default session_id to use for this agent (autogenerated if not set)
session_state	Optional[Dict[str, Any]]	None	Default session state (stored in the database to persist across runs)
add_session_state_to_context	bool	False	Set to True to add the session_state to the context
enable_agentic_state	bool	False	Set to True to give the agent tools to update the session_state dynamically
overwrite_db_session_state	bool	False	Set to True to overwrite the session state in the database with the session state provided in the run
cache_session	bool	False	If True, cache the current Agent session in memory for faster access
search_session_history	Optional[bool]	False	Set this to True to allow searching through previous sessions.
num_history_sessions	Optional[int]	None	Specify the number of past sessions to include in the search. It’s advisable to keep this number to 2 or 3 for now, as a larger number might fill up the context length of the model, potentially leading to performance issues.
dependencies	Optional[Dict[str, Any]]	None	Dependencies available for tools and prompt functions
add_dependencies_to_context	bool	False	If True, add the dependencies to the user prompt
db	Optional[BaseDb]	None	Database to use for this agent
memory_manager	Optional[MemoryManager]	None	Memory manager to use for this agent
enable_agentic_memory	bool	False	Enable the agent to manage memories of the user
enable_user_memories	bool	False	If True, the agent creates/updates user memories at the end of runs
add_memories_to_context	Optional[bool]	None	If True, the agent adds a reference to the user memories in the response
enable_session_summaries	bool	False	If True, the agent creates/updates session summaries at the end of runs
add_session_summary_to_context	Optional[bool]	None	If True, the agent adds session summaries to the context
session_summary_manager	Optional[SessionSummaryManager]	None	Session summary manager
compress_tool_results	bool	False	If True, compress tool call results to save context space
compression_manager	Optional[CompressionManager]	None	Custom compression manager for compressing tool call results
add_history_to_context	bool	False	Add the chat history of the current session to the messages sent to the Model
num_history_runs	Optional[int]	None	Number of historical runs to include in the messages.
num_history_messages	Optional[int]	None	Number of historical messages to include messages list sent to the Model.
knowledge	Optional[Knowledge]	None	Agent Knowledge
knowledge_filters	Optional[Dict[str, Any]]	None	Knowledge filters to apply to the knowledge base
enable_agentic_knowledge_filters	Optional[bool]	None	Let the agent choose the knowledge filters
add_knowledge_to_context	bool	False	Enable RAG by adding references from Knowledge to the user prompt
knowledge_retriever	Optional[Callable[..., Optional[List[Union[Dict, str]]]]]	None	Function to get references to add to the user_message
references_format	Literal["json", "yaml"]	"json"	Format of the references
metadata	Optional[Dict[str, Any]]	None	Metadata stored with this agent
tools	Optional[List[Union[Toolkit, Callable, Function, Dict]]]	None	A list of tools provided to the Model
tool_call_limit	Optional[int]	None	Maximum number of tool calls allowed for a single run
tool_choice	Optional[Union[str, Dict[str, Any]]]	None	Controls which (if any) tool is called by the model
max_tool_calls_from_history	Optional[int]	None	Maximum number of tool calls from history to keep in context. If None, all tool calls from history are included. If set to N, only the last N tool calls from history are added to the context for memory management
tool_hooks	Optional[List[Callable]]	None	Functions that will run between tool calls
pre_hooks	Optional[List[Union[Callable[..., Any], BaseGuardrail, BaseEval]]]	None	Functions called right after agent-session is loaded, before processing starts
post_hooks	Optional[List[Union[Callable[..., Any], BaseGuardrail, BaseEval]]]	None	Functions called after output is generated but before the response is returned
reasoning	bool	False	Enable reasoning by working through the problem step by step
reasoning_model	Optional[Union[Model, str]]	None	Model to use for reasoning. Can be a Model object or a model string (provider:model_id)
reasoning_agent	Optional[Agent]	None	Agent to use for reasoning
reasoning_min_steps	int	1	Minimum number of reasoning steps
reasoning_max_steps	int	10	Maximum number of reasoning steps
read_chat_history	bool	False	Add a tool that allows the Model to read the chat history
search_knowledge	bool	True	Add a tool that allows the Model to search the knowledge base
update_knowledge	bool	False	Add a tool that allows the Model to update the knowledge base
read_tool_call_history	bool	False	Add a tool that allows the Model to get the tool call history
send_media_to_model	bool	True	If False, media (images, videos, audio, files) is only available to tools and not sent to the LLM
store_media	bool	True	If True, store media in the database
store_tool_messages	bool	True	If True, store tool results in the database
store_history_messages	bool	True	If True, store history messages in the database
system_message	Optional[Union[str, Callable, Message]]	None	Provide the system message as a string or function
system_message_role	str	"system"	Role for the system message
introduction	str	None	Introduction messaage for the Agent
build_context	bool	True	Set to False to skip context building
description	Optional[str]	None	A description of the Agent that is added to the start of the system message
instructions	Optional[Union[str, List[str], Callable]]	None	List of instructions for the agent
expected_output	Optional[str]	None	Provide the expected output from the Agent
additional_context	Optional[str]	None	Additional context added to the end of the system message
markdown	bool	False	If markdown=true, add instructions to format the output using markdown
add_name_to_context	bool	False	If True, add the agent name to the instructions
add_datetime_to_context	bool	False	If True, add the current datetime to the instructions to give the agent a sense of time
add_location_to_context	bool	False	If True, add the current location to the instructions to give the agent a sense of place
timezone_identifier	Optional[str]	None	Allows for custom timezone for datetime instructions following the TZ Database format (e.g. “Etc/UTC”)
resolve_in_context	bool	True	If True, resolve session_state, dependencies, and metadata in the user and system messages
additional_input	Optional[List[Union[str, Dict, BaseModel, Message]]]	None	A list of extra messages added after the system message and before the user message
user_message_role	str	"user"	Role for the user message
build_user_context	bool	True	Set to False to skip building the user context
retries	int	0	Number of retries to attempt when running the Agent
delay_between_retries	int	1	Delay between retries (in seconds)
exponential_backoff	bool	False	If True, the delay between retries is doubled each time
input_schema	Optional[Type[BaseModel]]	None	Provide an input schema to validate the input
output_schema	Optional[Union[Type[BaseModel], Dict[str, Any]]]	None	Provide a response model to get the response as a Pydantic model or a JSON schema
parser_model	Optional[Union[Model, str]]	None	Provide a secondary model to parse the response from the primary model. Can be a Model object or a model string (provider:model_id)
parser_model_prompt	Optional[str]	None	Provide a prompt for the parser model
output_model	Optional[Union[Model, str]]	None	Provide an output model to structure the response from the main model. Can be a Model object or a model string (provider:model_id)
output_model_prompt	Optional[str]	None	Provide a prompt for the output model
parse_response	bool	True	If True, the response from the Model is converted into the output_schema
structured_outputs	Optional[bool]	None	Use model enforced structured_outputs if supported (e.g. OpenAIChat)
use_json_mode	bool	False	If output_schema is set, sets the response mode of the model, i.e. if the model should explicitly respond with a JSON object instead of a Pydantic model
save_response_to_file	Optional[str]	None	Save the response to a file
stream	Optional[bool]	None	Stream the response from the Agent
stream_events	bool	False	Stream the intermediate steps from the Agent
store_events	bool	False	Persist the events on the run response
events_to_skip	Optional[List[RunEvent]]	None	Specify which event types to skip when storing events on the RunOutput
role	Optional[str]	None	If this Agent is part of a team, this is the role of the agent in the team
debug_mode	bool	False	Enable debug logs
debug_level	Literal[1, 2]	1	Debug level for logging
telemetry	bool	True	Log minimal telemetry for analytics
​
Functions
​
run
Run the agent. Parameters:

    input (Union[str, List, Dict, Message, BaseModel, List[Message]]): The input to send to the agent
    stream (Optional[bool]): Whether to stream the response
    stream_events (Optional[bool]): Whether to stream intermediate steps
    user_id (Optional[str]): User ID to use
    session_id (Optional[str]): Session ID to use
    session_state (Optional[Dict[str, Any]]): Session state to use. By default, merged with the session state in the db.
    audio (Optional[Sequence[Audio]]): Audio files to include
    images (Optional[Sequence[Image]]): Image files to include
    videos (Optional[Sequence[Video]]): Video files to include
    files (Optional[Sequence[File]]): Files to include
    retries (Optional[int]): Number of retries to attempt
    knowledge_filters (Optional[Dict[str, Any]]): Knowledge filters to apply
    add_history_to_context (Optional[bool]): Whether to add history to context
    add_dependencies_to_context (Optional[bool]): Whether to add dependencies to context
    add_session_state_to_context (Optional[bool]): Whether to add session state to context
    dependencies (Optional[Dict[str, Any]]): Dependencies to use for this run
    metadata (Optional[Dict[str, Any]]): Metadata to use for this run
    output_schema (Optional[Union[Type[BaseModel], Dict[str, Any]]]): Output schema to use for this run. Can be a Pydantic model or a JSON schema.
    debug_mode (Optional[bool]): Whether to enable debug mode

​
arun
Run the agent asynchronously. Parameters:

    input (Union[str, List, Dict, Message, BaseModel, List[Message]]): The input to send to the agent
    stream (Optional[bool]): Whether to stream the response
    user_id (Optional[str]): User ID to use
    session_id (Optional[str]): Session ID to use
    session_state (Optional[Dict[str, Any]]): Session state to use. By default, merged with the session state in the db.
    audio (Optional[Sequence[Audio]]): Audio files to include
    images (Optional[Sequence[Image]]): Image files to include
    videos (Optional[Sequence[Video]]): Video files to include
    files (Optional[Sequence[File]]): Files to include
    stream_events (Optional[bool]): Whether to stream intermediate steps
    retries (Optional[int]): Number of retries to attempt
    knowledge_filters (Optional[Dict[str, Any]]): Knowledge filters to apply
    add_history_to_context (Optional[bool]): Whether to add history to context
    add_dependencies_to_context (Optional[bool]): Whether to add dependencies to context
    add_session_state_to_context (Optional[bool]): Whether to add session state to context
    dependencies (Optional[Dict[str, Any]]): Dependencies to use for this run
    metadata (Optional[Dict[str, Any]]): Metadata to use for this run
    output_schema (Optional[Union[Type[BaseModel], Dict[str, Any]]]): Output schema to use for this run. Can be a Pydantic model or a JSON schema.
    debug_mode (Optional[bool]): Whether to enable debug mode

Returns:

    Union[RunOutput, AsyncIterator[RunOutputEvent]]: Either a RunOutput or an iterator of RunOutputEvents, depending on the stream parameter

​
continue_run
Continue a run. Parameters:

    run_response (Optional[RunOutput]): The run response to continue
    run_id (Optional[str]): The run ID to continue
    updated_tools (Optional[List[ToolExecution]]): Updated tools to use, required if the run is resumed using run_id
    stream (Optional[bool]): Whether to stream the response
    stream_events (Optional[bool]): Whether to stream intermediate steps
    user_id (Optional[str]): User ID to use
    session_id (Optional[str]): Session ID to use
    retries (Optional[int]): Number of retries to attempt
    knowledge_filters (Optional[Dict[str, Any]]): Knowledge filters to apply
    dependencies (Optional[Dict[str, Any]]): Dependencies to use for this run
    debug_mode (Optional[bool]): Whether to enable debug mode

Returns:

    Union[RunOutput, Iterator[RunOutputEvent]]: Either a RunOutput or an iterator of RunOutputEvents, depending on the stream parameter

​
acontinue_run
Continue a run asynchronously. Parameters:

    run_response (Optional[RunOutput]): The run response to continue
    run_id (Optional[str]): The run ID to continue
    updated_tools (Optional[List[ToolExecution]]): Updated tools to use, required if the run is resumed using run_id
    stream (Optional[bool]): Whether to stream the response
    stream_events (Optional[bool]): Whether to stream intermediate steps
    user_id (Optional[str]): User ID to use
    session_id (Optional[str]): Session ID to use
    retries (Optional[int]): Number of retries to attempt
    knowledge_filters (Optional[Dict[str, Any]]): Knowledge filters to apply
    dependencies (Optional[Dict[str, Any]]): Dependencies to use for this run
    debug_mode (Optional[bool]): Whether to enable debug mode

Returns:

    Union[RunOutput, AsyncIterator[Union[RunOutputEvent, RunOutput]]]: Either a RunOutput or an iterator of RunOutputEvents, depending on the stream parameter

​
print_response
Run the agent and print the response. Parameters:

    input (Union[List, Dict, str, Message, BaseModel, List[Message]]): The input to send to the agent
    session_id (Optional[str]): Session ID to use
    session_state (Optional[Dict[str, Any]]): Session state to use. By default, merged with the session state in the db.
    user_id (Optional[str]): User ID to use
    audio (Optional[Sequence[Audio]]): Audio files to include
    images (Optional[Sequence[Image]]): Image files to include
    videos (Optional[Sequence[Video]]): Video files to include
    files (Optional[Sequence[File]]): Files to include
    stream (Optional[bool]): Whether to stream the response
    markdown (Optional[bool]): Whether to format output as markdown
    show_message (bool): Whether to show the input message
    show_reasoning (bool): Whether to show reasoning steps
    show_full_reasoning (bool): Whether to show full reasoning information
    console (Optional[Any]): Console to use for output
    tags_to_include_in_markdown (Optional[Set[str]]): Tags to include in markdown content
    knowledge_filters (Optional[Dict[str, Any]]): Knowledge filters to apply
    add_history_to_context (Optional[bool]): Whether to add history to context
    dependencies (Optional[Dict[str, Any]]): Dependencies to use for this run
    add_dependencies_to_context (Optional[bool]): Whether to add dependencies to context
    add_session_state_to_context (Optional[bool]): Whether to add session state to context
    metadata (Optional[Dict[str, Any]]): Metadata to use for this run
    debug_mode (Optional[bool]): Whether to enable debug mode

​
aprint_response
Run the agent and print the response asynchronously. Parameters:

    input (Union[List, Dict, str, Message, BaseModel, List[Message]]): The input to send to the agent
    session_id (Optional[str]): Session ID to use
    session_state (Optional[Dict[str, Any]]): Session state to use. By default, merged with the session state in the db.
    user_id (Optional[str]): User ID to use
    audio (Optional[Sequence[Audio]]): Audio files to include
    images (Optional[Sequence[Image]]): Image files to include
    videos (Optional[Sequence[Video]]): Video files to include
    files (Optional[Sequence[File]]): Files to include
    stream (Optional[bool]): Whether to stream the response
    markdown (Optional[bool]): Whether to format output as markdown
    show_message (bool): Whether to show the message
    show_reasoning (bool): Whether to show reasoning
    show_full_reasoning (bool): Whether to show full reasoning
    console (Optional[Any]): Console to use for output
    tags_to_include_in_markdown (Optional[Set[str]]): Tags to include in markdown content
    knowledge_filters (Optional[Dict[str, Any]]): Knowledge filters to apply
    add_history_to_context (Optional[bool]): Whether to add history to context
    add_dependencies_to_context (Optional[bool]): Whether to add dependencies to context
    add_session_state_to_context (Optional[bool]): Whether to add session state to context
    dependencies (Optional[Dict[str, Any]]): Dependencies to use for this run
    metadata (Optional[Dict[str, Any]]): Metadata to use for this run
    debug_mode (Optional[bool]): Whether to enable debug mode

​
cli_app
Run an interactive command-line interface to interact with the agent. Parameters:

    input (Optional[str]): The input to send to the agent
    session_id (Optional[str]): Session ID to use
    user_id (Optional[str]): User ID to use
    user (str): Name for the user (default: “User”)
    emoji (str): Emoji for the user (default: “:sunglasses:”)
    stream (bool): Whether to stream the response (default: False)
    markdown (bool): Whether to format output as markdown (default: False)
    exit_on (Optional[List[str]]): List of commands to exit the CLI
    **kwargs: Additional keyword arguments

​
acli_app
Run an interactive command-line interface to interact with the agent asynchronously. Parameters:

    input (Optional[str]): The input to send to the agent
    session_id (Optional[str]): Session ID to use
    user_id (Optional[str]): User ID to use
    user (str): Name for the user (default: “User”)
    emoji (str): Emoji for the user (default: “:sunglasses:”)
    stream (bool): Whether to stream the response (default: False)
    markdown (bool): Whether to format output as markdown (default: False)
    exit_on (Optional[List[str]]): List of commands to exit the CLI
    **kwargs: Additional keyword arguments

​
cancel_run
Cancel a run by run ID. Parameters:

    run_id (str): The run ID to cancel

Returns:

    bool: True if the run was successfully cancelled

​
get_run_output
Get the run output for the given run ID. Parameters:

    run_id (str): The run ID
    session_id (str): Session ID to use

Returns:

    Optional[RunOutput]: The run output

​
get_last_run_output
Get the last run output for the session. Parameters:

    session_id (str): Session ID to use

Returns:

    Optional[RunOutput]: The last run output

​
get_session
Get the session for the given session ID. Parameters:

    session_id (str): Session ID to use

Returns:

    Optional[AgentSession]: The agent session

​
get_session_summary
Get the session summary for the given session ID. Parameters:

    session_id (str): Session ID to use

Returns:

    Session summary for the given session

​
get_user_memories
Get the user memories for the given user ID. Parameters:

    user_id (str): User ID to use

Returns:

    Optional[List[UserMemory]]: The user memories

​
aget_user_memories
Get the user memories for the given user ID asynchronously. Parameters:

    user_id (str): User ID to use

Returns:

    Optional[List[UserMemory]]: The user memories

​
get_session_state
Get the session state for the given session ID. Parameters:

    session_id (str): Session ID to use

Returns:

    Dict[str, Any]: The session state

​
update_session_state
Update the session state for the given session ID. Parameters:

    session_id (str): Session ID to use
    session_state_updates (Dict[str, Any]): The session state keys and values to update. Overwrites the existing session state.

Returns:

    Dict[str, Any]: The updated session state

​
get_session_metrics
Get the session metrics for the given session ID. Parameters:

    session_id (str): Session ID to use

Returns:

    Optional[Metrics]: The session metrics

​
delete_session
Delete a session. Parameters:

    session_id (str): Session ID to delete

​
save_session
Save a session to the database. Parameters:

    session (AgentSession): The session to save

​
asave_session
Save a session to the database asynchronously. Parameters:

    session (AgentSession): The session to save

​
rename
Rename the agent and update the session. Parameters:

    name (str): The new name for the agent
    session_id (str): Session ID to use

​
get_session_name
Get the session name for the given session ID. Parameters:

    session_id (str): Session ID to use

Returns:

    str: The session name

​
set_session_name
Set the session name. Parameters:

    session_id (str): Session ID to use
    autogenerate (bool): Whether to autogenerate the name
    session_name (Optional[str]): The name to set

Returns:

    AgentSession: The updated session

​
get_session_messages
Get the messages for the given session ID. Parameters:

    session_id (Optional[str]): The session ID to get the messages for. If not provided, the latest used session ID is used.
    last_n_runs (Optional[int]): The number of runs to return messages from, counting from the latest. Defaults to all runs.
    limit (Optional[int]): The number of messages to return, counting from the latest. Defaults to all messages.
    skip_roles (Optional[List[str]]): Skip messages with these roles.
    skip_statuses (Optional[List[RunStatus]]): Skip messages with these statuses.
    skip_history_messages (bool): Skip messages that were tagged as history in previous runs. Defaults to True.

Returns:

    List[Message]: The messages for the session

​
get_chat_history
Get the chat history for the given session ID. Parameters:

    session_id (Optional[str]): The session ID to get the chat history for. If not provided, the latest used session ID is used.
    last_n_runs (Optional[int]): The number of runs to return messages from, counting from the latest. Defaults to all runs.

Returns:

    List[Message]: The chat history

​
add_tool
Add a tool to the agent. Parameters:

    tool (Union[Toolkit, Callable, Function, Dict]): The tool to add

​
set_tools
Replace the tools of the agent. Parameters:

    tools (List[Union[Toolkit, Callable, Function, Dict]]): The tools to set


Agent
RemoteAgent

Execute agents hosted on a remote AgentOS instance
RemoteAgent allows you to run agents that are hosted on a remote AgentOS instance. It provides the same interface as a local agent, making it easy to integrate remote agents into your applications or compose them into teams and workflows.
​
Installation

pip install agno

​
Basic Usage

from agno.agent import RemoteAgent

# Create a remote agent pointing to a remote AgentOS instance
agent = RemoteAgent(
    base_url="http://localhost:7777",
    agent_id="my-agent",
)

# Run the agent (async)
response = await agent.arun("What is the capital of France?")
print(response.content)

​
Parameters
Parameter	Type	Default	Description
base_url	str	Required	Base URL of the remote AgentOS instance (e.g., "http://localhost:7777")
agent_id	str	Required	ID of the remote agent to execute
timeout	float	60.0	Request timeout in seconds
config_ttl	float	300.0	Time-to-live for cached configuration in seconds
​
Properties
​
id
Returns the agent ID.

print(agent.id)  # "my-agent"

​
name
Returns the agent’s name from the remote configuration.

print(agent.name)  # "My Agent"

​
description
Returns the agent’s description from the remote configuration.

print(agent.description)  # "A helpful assistant agent"

​
role
Returns the agent’s role from the remote configuration.

print(agent.role)  # "assistant"

​
tools
Returns the agent’s tools as a list of dictionaries.

tools = agent.tools
if tools:
    for tool in tools:
        print(tool["name"])

​
db
Returns a RemoteDb instance if the agent has a database configured.

if agent.db:
    print(f"Database ID: {agent.db.id}")

​
knowledge
Returns a RemoteKnowledge instance if the agent has knowledge configured.

if agent.knowledge:
    print("Agent has knowledge enabled")

​
Methods
​
arun
Execute the remote agent asynchronously.

# Non-streaming
response = await agent.arun(
    "Tell me about Python",
    user_id="user-123",
    session_id="session-456",
)
print(response.content)

# Streaming
async for event in agent.arun(
    "Tell me a story",
    stream=True,
    user_id="user-123",
):
    if hasattr(event, "content") and event.content:
        print(event.content, end="", flush=True)

Parameters:
Parameter	Type	Default	Description
input	str | List | Dict | Message | BaseModel	Required	The input message for the agent
stream	bool	False	Whether to stream the response
user_id	Optional[str]	None	User ID for the run
session_id	Optional[str]	None	Session ID for context persistence
session_state	Optional[Dict]	None	Session state dictionary
images	Optional[Sequence[Image]]	None	Images to include
audio	Optional[Sequence[Audio]]	None	Audio to include
videos	Optional[Sequence[Video]]	None	Videos to include
files	Optional[Sequence[File]]	None	Files to include
stream_events	Optional[bool]	None	Whether to stream events
retries	Optional[int]	None	Number of retries
knowledge_filters	Optional[Dict]	None	Filters for knowledge search
add_history_to_context	Optional[bool]	None	Add history to context
dependencies	Optional[Dict]	None	Dependencies dictionary
metadata	Optional[Dict]	None	Metadata dictionary
auth_token	Optional[str]	None	JWT token for authentication
Returns:

    RunOutput when stream=False
    AsyncIterator[RunOutputEvent] when stream=True

​
acontinue_run
Continue a paused agent run with tool results.

from agno.models.response import ToolExecution

response = await agent.acontinue_run(
    run_id="run-123",
    updated_tools=[
        ToolExecution(
            tool_call_id="call-1",
            result="Tool result here",
        )
    ],
)

Parameters:
Parameter	Type	Default	Description
run_id	str	Required	ID of the run to continue
updated_tools	List[ToolExecution]	Required	Tool execution results
stream	bool	False	Whether to stream the response
user_id	Optional[str]	None	User ID
session_id	Optional[str]	None	Session ID
auth_token	Optional[str]	None	JWT token for authentication
Returns:

    RunOutput when stream=False
    AsyncIterator[RunOutputEvent] when stream=True

​
cancel_run
Cancel a running agent execution.

success = await agent.cancel_run(run_id="run-123")
if success:
    print("Run cancelled")

Parameters:
Parameter	Type	Default	Description
run_id	str	Required	ID of the run to cancel
auth_token	Optional[str]	None	JWT token for authentication
Returns: bool - True if successfully cancelled
​
get_agent_config
Get the agent configuration from the remote server (always fetches fresh).

config = await agent.get_agent_config()
print(f"Agent name: {config.name}")
print(f"Model: {config.model}")

Returns: AgentResponse
​
refresh_config
Force refresh the cached agent configuration.

config = agent.refresh_config()

Returns: AgentResponse
​
Using in Teams
Remote agents can be used as members of local teams:

from agno.agent import RemoteAgent
from agno.team import Team
from agno.models.openai import OpenAIChat

# Remote agent from another AgentOS instance
researcher = RemoteAgent(
    base_url="http://research-server:7777",
    agent_id="researcher-agent",
)

# Local team with remote agent member
team = Team(
    name="Research Team",
    model=OpenAIChat(id="gpt-4o"),
    members=[researcher],
    instructions="Coordinate research tasks",
)

response = await team.arun("Research AI trends")

​
Using in AgentOS Gateway
Remote agents can be registered in a local AgentOS to create a gateway:

from agno.agent import RemoteAgent
from agno.os import AgentOS

agent_os = AgentOS(
    agents=[
        RemoteAgent(base_url="http://server-1:7777", agent_id="agent-1"),
        RemoteAgent(base_url="http://server-2:7777", agent_id="agent-2"),
    ],
)

See AgentOS Gateway for more details.
​
Error Handling

from agno.exceptions import RemoteServerUnavailableError

try:
    response = await agent.arun("Hello")
except RemoteServerUnavailableError as e:
    print(f"Remote server unavailable: {e.message}")

​
Authentication
For authenticated AgentOS instances, pass the auth_token parameter:

response = await agent.arun(
    "Hello",
    auth_token="your-jwt-token",
)


Team
Team
​
Parameters
Parameter	Type	Default	Description
members	List[Union[Agent, Team]]	-	List of agents or teams that make up this team
id	Optional[str]	None	Team UUID (autogenerated if not set)
model	Optional[Union[Model, str]]	None	Model to use for the team. Can be a Model object or a model string (provider:model_id)
name	Optional[str]	None	Name of the team
role	Optional[str]	None	Role of the team within its parent team
respond_directly	bool	False	If True, the team leader won’t process responses from the members and instead will return them directly
determine_input_for_members	bool	True	Set to False if you want to send the run input directly to the member agents
delegate_to_all_members	bool	False	If True, the team leader will delegate tasks to all members automatically, without any decision from the team leader
user_id	Optional[str]	None	Default user ID for this team
session_id	Optional[str]	None	Default session ID for this team (autogenerated if not set)
session_state	Optional[Dict[str, Any]]	None	Session state (stored in the database to persist across runs)
add_session_state_to_context	bool	False	Set to True to add the session_state to the context
enable_agentic_state	bool	False	Set to True to give the team tools to update the session_state dynamically
overwrite_db_session_state	bool	False	Set to True to overwrite the session state in the database with the session state provided in the run
cache_session	bool	False	If True, cache the current Team session in memory for faster access
resolve_in_context	bool	True	If True, resolve the session_state, dependencies, and metadata in the user and system messages
description	Optional[str]	None	A description of the Team that is added to the start of the system message
instructions	Optional[Union[str, List[str], Callable]]	None	List of instructions for the team
expected_output	Optional[str]	None	Provide the expected output from the Team
additional_context	Optional[str]	None	Additional context added to the end of the system message
markdown	bool	False	If markdown=true, add instructions to format the output using markdown
add_datetime_to_context	bool	False	If True, add the current datetime to the instructions to give the team a sense of time
add_location_to_context	bool	False	If True, add the current location to the instructions to give the team a sense of location
timezone_identifier	Optional[str]	None	Allows for custom timezone for datetime instructions following the TZ Database format
add_name_to_context	bool	False	If True, add the team name to the instructions
add_member_tools_to_context	bool	False	If True, add the tools available to team members to the context
system_message	Optional[Union[str, Callable, Message]]	None	Provide the system message as a string or function
system_message_role	str	"system"	Role for the system message
introduction	str	None	Introduction messaage for the Team
additional_input	Optional[List[Union[str, Dict, BaseModel, Message]]]	None	A list of extra messages added after the system message and before the user message
db	Optional[BaseDb]	None	Database to use for this team
memory_manager	Optional[MemoryManager]	None	Memory manager to use for this team
dependencies	Optional[Dict[str, Any]]	None	User provided dependencies
add_dependencies_to_context	bool	False	If True, add the dependencies to the user prompt
knowledge	Optional[Knowledge]	None	Add a knowledge base to the team
knowledge_filters	Optional[Dict[str, Any]]	None	Filters to apply to knowledge base searches
enable_agentic_knowledge_filters	Optional[bool]	False	Let the team choose the knowledge filters
update_knowledge	bool	False	Add a tool that allows the Team to update Knowledge
add_knowledge_to_context	bool	False	If True, add references to the user prompt
knowledge_retriever	Optional[Callable[..., Optional[List[Union[Dict, str]]]]]	None	Retrieval function to get references
references_format	Literal["json", "yaml"]	"json"	Format of the references
share_member_interactions	bool	False	If True, send all member interactions (request/response) during the current run to members that have been delegated a task to
get_member_information_tool	bool	False	If True, add a tool to get information about the team members
search_knowledge	bool	True	Add a tool to search the knowledge base (aka Agentic RAG)
send_media_to_model	bool	True	If False, media (images, videos, audio, files) is only available to tools and not sent to the LLM
store_media	bool	True	If True, store media in the database
store_tool_messages	bool	True	If True, store tool results in the database
store_history_messages	bool	True	If True, store history messages in the database
tools	Optional[List[Union[Toolkit, Callable, Function, Dict]]]	None	A list of tools provided to the Model
tool_choice	Optional[Union[str, Dict[str, Any]]]	None	Controls which (if any) tool is called by the team model
tool_call_limit	Optional[int]	None	Maximum number of tool calls allowed
max_tool_calls_from_history	Optional[int]	None	Maximum number of tool calls from history to keep in context. If None, all tool calls from history are included. If set to N, only the last N tool calls from history are added to the context for memory management
tool_hooks	Optional[List[Callable]]	None	A list of hooks to be called before and after the tool call
pre_hooks	Optional[List[Union[Callable[..., Any], BaseGuardrail, BaseEval]]]	None	Functions called right after team session is loaded, before processing starts
post_hooks	Optional[List[Union[Callable[..., Any], BaseGuardrail, BaseEval]]]	None	Functions called after output is generated but before the response is returned
input_schema	Optional[Type[BaseModel]]	None	Input schema for validating input
output_schema	Optional[Union[Type[BaseModel], Dict[str, Any]]]	None	Output schema for the team response. Can be a Pydantic model or a JSON schema
parser_model	Optional[Union[Model, str]]	None	Provide a secondary model to parse the response from the primary model. Can be a Model object or a model string (provider:model_id)
parser_model_prompt	Optional[str]	None	Provide a prompt for the parser model
output_model	Optional[Union[Model, str]]	None	Provide an output model to parse the response from the team. Can be a Model object or a model string (provider:model_id)
output_model_prompt	Optional[str]	None	Provide a prompt for the output model
use_json_mode	bool	False	If output_schema is set, sets the response mode of the model
parse_response	bool	True	If True, parse the response
enable_agentic_memory	bool	False	Enable the team to manage memories of the user
enable_user_memories	bool	False	If True, the team creates/updates user memories at the end of runs
add_memories_to_context	Optional[bool]	None	If True, the team adds a reference to the user memories in the response
enable_session_summaries	bool	False	If True, the team creates/updates session summaries at the end of runs
session_summary_manager	Optional[SessionSummaryManager]	None	Session summary manager
add_session_summary_to_context	Optional[bool]	None	If True, the team adds session summaries to the context
compress_tool_results	bool	False	If True, compress tool call results to save context space
compression_manager	Optional[CompressionManager]	None	Custom compression manager for compressing tool call results
add_history_to_context	bool	False	Add messages from the chat history to the messages list sent to the Model. This only applies to the team leader, not the members.
num_history_runs	Optional[int]	None	Number of historical runs to include in the messages.
num_history_messages	Optional[int]	None	Number of historical messages to include messages list sent to the Model.
add_team_history_to_members	bool	False	If True, send the team-level history to the members, not the agent-level history
num_team_history_runs	int	3	Number of historical runs to include in the messages sent to the members
search_session_history	Optional[bool]	False	If True, adds a tool to allow searching through previous sessions
num_history_sessions	Optional[int]	None	Number of past sessions to include in the search
read_team_history	bool	False	If True, adds a tool to allow the team to read the team history (deprecated and will be removed in a future version)
read_chat_history	bool	False	If True, adds a tool to allow the team to read the chat history
metadata	Optional[Dict[str, Any]]	None	Metadata stored with this team
reasoning	bool	False	Enable reasoning for the team
reasoning_model	Optional[Union[Model, str]]	None	Model to use for reasoning. Can be a Model object or a model string (provider:model_id)
reasoning_agent	Optional[Agent]	None	Agent to use for reasoning
reasoning_min_steps	int	1	Minimum number of reasoning steps
reasoning_max_steps	int	10	Maximum number of reasoning steps
stream	Optional[bool]	None	Stream the response from the Team
stream_events	bool	False	Stream the intermediate steps from the Team
stream_member_events	bool	True	Stream the member events from the Team members
store_events	bool	False	Store the events from the Team
events_to_skip	Optional[List[Union[RunEvent, TeamRunEvent]]]	None	List of events to skip from the Team
store_member_responses	bool	False	Store member agent runs inside the team’s RunOutput
debug_mode	bool	False	Enable debug logs
debug_level	Literal[1, 2]	1	Debug level: 1 = basic, 2 = detailed
show_members_responses	bool	False	Enable member logs - Sets the debug_mode for team and members
retries	int	0	Number of retries to attempt when running the Team
delay_between_retries	int	1	Delay between retries (in seconds)
exponential_backoff	bool	False	Exponential backoff: if True, the delay between retries is doubled each time
telemetry	bool	True	Log minimal telemetry for analytics
​
Functions
​
run
Run the team. Parameters:

    input (Union[str, List, Dict, Message, BaseModel, List[Message]]): The input to send to the team
    stream (Optional[bool]): Whether to stream the response
    stream_events (Optional[bool]): Whether to stream intermediate steps
    session_id (Optional[str]): Session ID to use
    session_state (Optional[Dict[str, Any]]): Session state to use. By default, merged with the session state in the db.
    user_id (Optional[str]): User ID to use
    retries (Optional[int]): Number of retries to attempt
    audio (Optional[Sequence[Audio]]): Audio files to include
    images (Optional[Sequence[Image]]): Image files to include
    videos (Optional[Sequence[Video]]): Video files to include
    files (Optional[Sequence[File]]): Files to include
    knowledge_filters (Optional[Dict[str, Any]]): Knowledge filters to apply
    add_history_to_context (Optional[bool]): Whether to add history to context
    add_dependencies_to_context (Optional[bool]): Whether to add dependencies to context
    add_session_state_to_context (Optional[bool]): Whether to add session state to context
    dependencies (Optional[Dict[str, Any]]): Dependencies to use for this run
    metadata (Optional[Dict[str, Any]]): Metadata to use for this run
    output_schema (Optional[Union[Type[BaseModel], Dict[str, Any]]]): Output schema to use for this run. Can be a Pydantic model or a JSON schema.
    debug_mode (Optional[bool]): Whether to enable debug mode
    yield_run_response (bool): Whether to yield the run response (only for streaming)

Returns:

    Union[TeamRunOutput, Iterator[Union[RunOutputEvent, TeamRunOutputEvent]]]: Either a TeamRunOutput or an iterator of events, depending on the stream parameter

​
arun
Run the team asynchronously. Parameters:

    input (Union[str, List, Dict, Message, BaseModel, List[Message]]): The input to send to the team
    stream (Optional[bool]): Whether to stream the response
    stream_events (Optional[bool]): Whether to stream intermediate steps
    session_id (Optional[str]): Session ID to use
    session_state (Optional[Dict[str, Any]]): Session state to use. By default, merged with the session state in the db.
    user_id (Optional[str]): User ID to use
    retries (Optional[int]): Number of retries to attempt
    audio (Optional[Sequence[Audio]]): Audio files to include
    images (Optional[Sequence[Image]]): Image files to include
    videos (Optional[Sequence[Video]]): Video files to include
    files (Optional[Sequence[File]]): Files to include
    knowledge_filters (Optional[Dict[str, Any]]): Knowledge filters to apply
    add_history_to_context (Optional[bool]): Whether to add history to context
    add_dependencies_to_context (Optional[bool]): Whether to add dependencies to context
    add_session_state_to_context (Optional[bool]): Whether to add session state to context
    dependencies (Optional[Dict[str, Any]]): Dependencies to use for this run
    metadata (Optional[Dict[str, Any]]): Metadata to use for this run
    output_schema (Optional[Union[Type[BaseModel], Dict[str, Any]]]): Output schema to use for this run. Can be a Pydantic model or a JSON schema.
    debug_mode (Optional[bool]): Whether to enable debug mode
    yield_run_response (bool): Whether to yield the run response (only for streaming)

Returns:

    Union[TeamRunOutput, AsyncIterator[Union[RunOutputEvent, TeamRunOutputEvent]]]: Either a TeamRunOutput or an async iterator of events, depending on the stream parameter

​
print_response
Run the team and print the response. Parameters:

    input (Union[List, Dict, str, Message, BaseModel, List[Message]]): The input to send to the team
    stream (Optional[bool]): Whether to stream the response
    session_id (Optional[str]): Session ID to use
    session_state (Optional[Dict[str, Any]]): Session state to use. By default, merged with the session state in the db.
    user_id (Optional[str]): User ID to use
    show_message (bool): Whether to show the message (default: True)
    show_reasoning (bool): Whether to show reasoning (default: True)
    show_full_reasoning (bool): Whether to show full reasoning (default: False)
    console (Optional[Any]): Console to use for output
    tags_to_include_in_markdown (Optional[Set[str]]): Tags to include in markdown content
    audio (Optional[Sequence[Audio]]): Audio files to include
    images (Optional[Sequence[Image]]): Image files to include
    videos (Optional[Sequence[Video]]): Video files to include
    files (Optional[Sequence[File]]): Files to include
    markdown (Optional[bool]): Whether to format output as markdown
    knowledge_filters (Optional[Dict[str, Any]]): Knowledge filters to apply
    add_history_to_context (Optional[bool]): Whether to add history to context
    dependencies (Optional[Dict[str, Any]]): Dependencies to use for this run
    add_dependencies_to_context (Optional[bool]): Whether to add dependencies to context
    add_session_state_to_context (Optional[bool]): Whether to add session state to context
    metadata (Optional[Dict[str, Any]]): Metadata to use for this run
    debug_mode (Optional[bool]): Whether to enable debug mode
    show_member_responses (Optional[bool]): Whether to show member responses

​
aprint_response
Run the team and print the response asynchronously. Parameters:

    input (Union[List, Dict, str, Message, BaseModel, List[Message]]): The input to send to the team
    stream (Optional[bool]): Whether to stream the response
    session_id (Optional[str]): Session ID to use
    session_state (Optional[Dict[str, Any]]): Session state to use. By default, merged with the session state in the db.
    user_id (Optional[str]): User ID to use
    show_message (bool): Whether to show the message (default: True)
    show_reasoning (bool): Whether to show reasoning (default: True)
    show_full_reasoning (bool): Whether to show full reasoning (default: False)
    console (Optional[Any]): Console to use for output
    tags_to_include_in_markdown (Optional[Set[str]]): Tags to include in markdown content
    audio (Optional[Sequence[Audio]]): Audio files to include
    images (Optional[Sequence[Image]]): Image files to include
    videos (Optional[Sequence[Video]]): Video files to include
    files (Optional[Sequence[File]]): Files to include
    markdown (Optional[bool]): Whether to format output as markdown
    knowledge_filters (Optional[Dict[str, Any]]): Knowledge filters to apply
    add_history_to_context (Optional[bool]): Whether to add history to context
    dependencies (Optional[Dict[str, Any]]): Dependencies to use for this run
    add_dependencies_to_context (Optional[bool]): Whether to add dependencies to context
    add_session_state_to_context (Optional[bool]): Whether to add session state to context
    metadata (Optional[Dict[str, Any]]): Metadata to use for this run
    debug_mode (Optional[bool]): Whether to enable debug mode
    show_member_responses (Optional[bool]): Whether to show member responses

​
cli_app
Run an interactive command-line interface to interact with the team. Parameters:

    input (Optional[str]): The input to send to the team
    user (str): Name for the user (default: “User”)
    emoji (str): Emoji for the user (default: “:sunglasses:”)
    stream (bool): Whether to stream the response (default: False)
    markdown (bool): Whether to format output as markdown (default: False)
    exit_on (Optional[List[str]]): List of commands to exit the CLI
    **kwargs: Additional keyword arguments

​
acli_app
Run an interactive command-line interface to interact with the team asynchronously. Parameters:

    input (Optional[str]): The input to send to the team
    session_id (Optional[str]): Session ID to use
    user_id (Optional[str]): User ID to use
    user (str): Name for the user (default: “User”)
    emoji (str): Emoji for the user (default: “:sunglasses:”)
    stream (bool): Whether to stream the response (default: False)
    markdown (bool): Whether to format output as markdown (default: False)
    exit_on (Optional[List[str]]): List of commands to exit the CLI
    **kwargs: Additional keyword arguments

​
get_session_summary
Get the session summary for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use (if not provided, the current session is used)

Returns:

    Session summary for the given session

​
get_user_memories
Get the user memories for the given user ID. Parameters:

    user_id (Optional[str]): User ID to use (if not provided, the current user is used)

Returns:

    Optional[List[UserMemory]]: The user memories

​
add_tool
Add a tool to the team. Parameters:

    tool (Union[Toolkit, Callable, Function, Dict]): The tool to add

​
set_tools
Replace the tools of the team. Parameters:

    tools (List[Union[Toolkit, Callable, Function, Dict]]): The tools to set

​
cancel_run
Cancel a run by run ID. Parameters:

    run_id (str): The run ID to cancel

Returns:

    bool: True if the run was successfully cancelled

​
get_run_output
Get the run output for the given run ID. Parameters:

    run_id (str): The run ID
    session_id (Optional[str]): Session ID to use

Returns:

    Optional[Union[TeamRunOutput, RunOutput]]: The run output

​
get_last_run_output
Get the last run output for the session. Parameters:

    session_id (Optional[str]): Session ID to use (if not provided, the current session is used)

Returns:

    Optional[TeamRunOutput]: The last run output

​
get_session
Get the session for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use (if not provided, the current session is used)

Returns:

    Optional[TeamSession]: The team session

​
save_session
Save a session to the database. Parameters:

    session (TeamSession): The session to save

​
asave_session
Save a session to the database asynchronously. Parameters:

    session (TeamSession): The session to save

​
delete_session
Delete a session. Parameters:

    session_id (str): Session ID to delete

​
get_session_name
Get the session name for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use (if not provided, the current session is used)

Returns:

    str: The session name

​
set_session_name
Set the session name. Parameters:

    session_id (Optional[str]): Session ID to use (if not provided, the current session is used)
    autogenerate (bool): Whether to autogenerate the name
    session_name (Optional[str]): The name to set

Returns:

    TeamSession: The updated session

​
get_session_state
Get the session state for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use (if not provided, the current session is used)

Returns:

    Dict[str, Any]: The session state

​
update_session_state
Update the session state for the given session ID. Parameters:

    session_id (str): Session ID to use
    session_state_updates (Dict[str, Any]): The session state keys and values to update. Overwrites the existing session state.

Returns:

    Dict[str, Any]: The updated session state

​
get_session_metrics
Get the session metrics for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use (if not provided, the current session is used)

Returns:

    Optional[Metrics]: The session metrics

​
get_chat_history
Get the chat history for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use (if not provided, the current session is used)
    last_n_runs (Optional[int]): The number of runs to return messages from, counting from the latest. Defaults to all runs

Returns:

    List[Message]: The chat history

​
get_session_messages
Get the messages for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use (if not provided, the current session is used)
    member_ids (Optional[List[str]]): The ids of the members to get the messages from
    last_n_runs (Optional[int]): The number of runs to return messages from, counting from the latest. Defaults to all runs
    limit (Optional[int]): The number of messages to return, counting from the latest. Defaults to all messages
    skip_roles (Optional[List[str]]): Skip messages with these roles
    skip_statuses (Optional[List[RunStatus]]): Skip messages with these statuses
    skip_history_messages (bool): Skip messages that were tagged as history in previous runs. Defaults to True
    skip_member_messages (bool): Skip messages created by members of the team. Defaults to True

Returns:

    List[Message]: The messages for the session


RemoteTeam

Execute teams hosted on a remote AgentOS instance
RemoteTeam allows you to run teams that are hosted on a remote AgentOS instance. It provides the same interface as a local team, making it easy to integrate remote teams into your applications.
​
Installation

pip install agno

​
Basic Usage

from agno.team import RemoteTeam

# Create a remote team pointing to a remote AgentOS instance
team = RemoteTeam(
    base_url="http://localhost:7777",
    team_id="research-team",
)

# Run the team (async)
response = await team.arun("Research the latest AI trends")
print(response.content)

​
Parameters
Parameter	Type	Default	Description
base_url	str	Required	Base URL of the remote AgentOS instance (e.g., "http://localhost:7777")
team_id	str	Required	ID of the remote team to execute
timeout	float	300.0	Request timeout in seconds
config_ttl	float	300.0	Time-to-live for cached configuration in seconds
​
Properties
​
id
Returns the team ID.

print(team.id)  # "research-team"

​
name
Returns the team’s name from the remote configuration.

print(team.name)  # "Research Team"

​
description
Returns the team’s description from the remote configuration.

print(team.description)  # "A team of research specialists"

​
role
Returns the team’s role from the remote configuration.

print(team.role)  # "researcher"

​
tools
Returns the team’s tools as a list of dictionaries.

tools = team.tools
if tools:
    for tool in tools:
        print(tool["name"])

​
db
Returns a RemoteDb instance if the team has a database configured.

if team.db:
    print(f"Database ID: {team.db.id}")

​
knowledge
Returns a RemoteKnowledge instance if the team has knowledge configured.

if team.knowledge:
    print("Team has knowledge enabled")

​
Methods
​
arun
Execute the remote team asynchronously.

# Non-streaming
response = await team.arun(
    "Research AI trends",
    user_id="user-123",
    session_id="session-456",
)
print(response.content)

# Streaming
async for event in team.arun(
    "Analyze this topic",
    stream=True,
    user_id="user-123",
):
    if hasattr(event, "content") and event.content:
        print(event.content, end="", flush=True)

Parameters:
Parameter	Type	Default	Description
input	str | List | Dict | Message | BaseModel	Required	The input message for the team
stream	bool	False	Whether to stream the response
user_id	Optional[str]	None	User ID for the run
session_id	Optional[str]	None	Session ID for context persistence
session_state	Optional[Dict]	None	Session state dictionary
images	Optional[Sequence[Image]]	None	Images to include
audio	Optional[Sequence[Audio]]	None	Audio to include
videos	Optional[Sequence[Video]]	None	Videos to include
files	Optional[Sequence[File]]	None	Files to include
stream_events	Optional[bool]	None	Whether to stream events
retries	Optional[int]	None	Number of retries
knowledge_filters	Optional[Dict]	None	Filters for knowledge search
add_history_to_context	Optional[bool]	None	Add history to context
dependencies	Optional[Dict]	None	Dependencies dictionary
metadata	Optional[Dict]	None	Metadata dictionary
auth_token	Optional[str]	None	JWT token for authentication
Returns:

    TeamRunOutput when stream=False
    AsyncIterator[TeamRunOutputEvent] when stream=True

​
cancel_run
Cancel a running team execution.

success = await team.cancel_run(run_id="run-123")
if success:
    print("Run cancelled")

Parameters:
Parameter	Type	Default	Description
run_id	str	Required	ID of the run to cancel
auth_token	Optional[str]	None	JWT token for authentication
Returns: bool - True if successfully cancelled
​
get_team_config
Get the team configuration from the remote server (always fetches fresh).

config = await team.get_team_config()
print(f"Team name: {config.name}")
print(f"Members: {config.members}")

Returns: TeamResponse
​
refresh_config
Force refresh the cached team configuration.

config = team.refresh_config()

Returns: TeamResponse
​
Using in AgentOS Gateway
Remote teams can be registered in a local AgentOS to create a gateway:

from agno.team import RemoteTeam
from agno.os import AgentOS

agent_os = AgentOS(
    teams=[
        RemoteTeam(base_url="http://server-1:7777", team_id="research-team"),
        RemoteTeam(base_url="http://server-2:7777", team_id="analysis-team"),
    ],
)

See AgentOS Gateway for more details.
​
Streaming Example

from agno.team import RemoteTeam
from agno.run.team import RunContentEvent, RunCompletedEvent

team = RemoteTeam(
    base_url="http://localhost:7777",
    team_id="research-team",
)

print("Response: ", end="", flush=True)
async for event in team.arun(
    "Analyze the current state of AI",
    stream=True,
    user_id="user-123",
):
    if isinstance(event, RunContentEvent):
        print(event.content, end="", flush=True)
    elif isinstance(event, RunCompletedEvent):
        print(f"\n\nCompleted: {event.run_id}")

​
Error Handling

from agno.exceptions import RemoteServerUnavailableError

try:
    response = await team.arun("Hello")
except RemoteServerUnavailableError as e:
    print(f"Remote server unavailable: {e.message}")

​
Authentication
For authenticated AgentOS instances, pass the auth_token parameter:

response = await team.arun(
    "Research this topic",
    auth_token="your-jwt-token",
)


Workflows
Workflow
​
Parameters
Parameter	Type	Default	Description
name	Optional[str]	None	Workflow name
id	Optional[str]	None	Workflow ID (autogenerated if not set)
description	Optional[str]	None	Workflow description
steps	Optional[WorkflowSteps]	None	Workflow steps - can be a callable function, Steps object, or list of steps
db	Optional[BaseDb]	None	Database to use for this workflow
session_id	Optional[str]	None	Default session_id to use for this workflow (autogenerated if not set)
user_id	Optional[str]	None	Default user_id to use for this workflow
session_state	Optional[Dict[str, Any]]	None	Default session state (stored in the database to persist across runs)
debug_mode	Optional[bool]	False	If True, the workflow runs in debug mode
stream	Optional[bool]	None	Stream the response from the Workflow
stream_events	bool	False	Stream the intermediate steps from the Workflow
stream_executor_events	bool	True	Stream the events emitted by the Step executor (the agent/team events) together with the Workflow events
store_events	bool	False	Persist the events on the run response
events_to_skip	Optional[List[Union[WorkflowRunEvent, RunEvent, TeamRunEvent]]]	None	Events to skip when persisting the events on the run response
store_executor_outputs	bool	True	Control whether to store executor responses (agent/team responses) in flattened runs
websocket_handler	Optional[WebSocketHandler]	None	WebSocket handler for real-time communication
input_schema	Optional[Type[BaseModel]]	None	Input schema to validate the input to the workflow
metadata	Optional[Dict[str, Any]]	None	Metadata stored with this workflow
add_workflow_history_to_steps	bool	False	If True, add the workflow history to the steps
num_history_runs	int	None	Number of runs to include in the workflow history, if not provided, all history runs are included
cache_session	bool	False	If True, cache the current workflow session in memory for faster access
telemetry	bool	True	Log minimal telemetry for analytics
​
Functions
​
run
Execute the workflow synchronously with optional streaming. Parameters:

    input (Optional[Union[str, Dict[str, Any], List[Any], BaseModel]]): The input to send to the workflow
    additional_data (Optional[Dict[str, Any]]): Additional data to include with the input
    user_id (Optional[str]): User ID to use
    session_id (Optional[str]): Session ID to use
    session_state (Optional[Dict[str, Any]]): Session state to use
    audio (Optional[List[Audio]]): Audio files to include
    images (Optional[List[Image]]): Image files to include
    videos (Optional[List[Video]]): Video files to include
    files (Optional[List[File]]): Files to include
    stream (bool): Whether to stream the response
    stream_events (Optional[bool]): Whether to stream intermediate steps

Returns:

    Union[WorkflowRunOutput, Iterator[WorkflowRunOutputEvent]]: Either a WorkflowRunOutput or an iterator of WorkflowRunOutputEvents, depending on the stream parameter

​
arun
Execute the workflow asynchronously with optional streaming. Parameters:

    input (Optional[Union[str, Dict[str, Any], List[Any], BaseModel, List[Message]]]): The input to send to the workflow
    additional_data (Optional[Dict[str, Any]]): Additional data to include with the input
    user_id (Optional[str]): User ID to use
    session_id (Optional[str]): Session ID to use
    session_state (Optional[Dict[str, Any]]): Session state to use
    audio (Optional[List[Audio]]): Audio files to include
    images (Optional[List[Image]]): Image files to include
    videos (Optional[List[Video]]): Video files to include
    files (Optional[List[File]]): Files to include
    stream (bool): Whether to stream the response
    stream_events (Optional[bool]): Whether to stream intermediate steps
    background (Optional[bool]): Whether to run in background
    websocket (Optional[WebSocket]): WebSocket for real-time communication

Returns:

    Union[WorkflowRunOutput, AsyncIterator[WorkflowRunOutputEvent]]: Either a WorkflowRunOutput or an iterator of WorkflowRunOutputEvents, depending on the stream parameter

​
print_response
Print workflow execution with rich formatting and optional streaming. Parameters:

    input (Union[str, Dict[str, Any], List[Any], BaseModel, List[Message]]): The input to send to the workflow
    additional_data (Optional[Dict[str, Any]]): Additional data to include with the input
    user_id (Optional[str]): User ID to use
    session_id (Optional[str]): Session ID to use
    audio (Optional[List[Audio]]): Audio files to include
    images (Optional[List[Image]]): Image files to include
    videos (Optional[List[Video]]): Video files to include
    files (Optional[List[File]]): Files to include
    stream (Optional[bool]): Whether to stream the response content
    markdown (bool): Whether to render content as markdown
    show_time (bool): Whether to show execution time
    show_step_details (bool): Whether to show individual step outputs
    console (Optional[Any]): Rich console instance (optional)

​
aprint_response
Print workflow execution with rich formatting and optional streaming asynchronously. Parameters:

    input (Union[str, Dict[str, Any], List[Any], BaseModel, List[Message]]): The input to send to the workflow
    additional_data (Optional[Dict[str, Any]]): Additional data to include with the input
    user_id (Optional[str]): User ID to use
    session_id (Optional[str]): Session ID to use
    audio (Optional[List[Audio]]): Audio files to include
    images (Optional[List[Image]]): Image files to include
    videos (Optional[List[Video]]): Video files to include
    files (Optional[List[File]]): Files to include
    stream (Optional[bool]): Whether to stream the response content
    markdown (bool): Whether to render content as markdown
    show_time (bool): Whether to show execution time
    show_step_details (bool): Whether to show individual step outputs
    console (Optional[Any]): Rich console instance (optional)

​
cli_app
Run an interactive command-line interface to interact with the workflow. Parameters:

    input (Optional[str]): The input to send to the workflow
    session_id (Optional[str]): Session ID to use
    user_id (Optional[str]): User ID to use
    user (str): Name for the user (default: “User”)
    emoji (str): Emoji for the user (default: “:technologist:”)
    stream (Optional[bool]): Whether to stream the response content
    markdown (bool): Whether to render content as markdown (default: True)
    show_time (bool): Whether to show execution time (default: True)
    show_step_details (bool): Whether to show individual step outputs (default: True)
    exit_on (Optional[List[str]]): List of commands to exit the CLI
    **kwargs: Additional keyword arguments

​
acli_app
Run an interactive command-line interface to interact with the workflow asynchronously. Parameters:

    input (Optional[str]): The input to send to the workflow
    session_id (Optional[str]): Session ID to use
    user_id (Optional[str]): User ID to use
    user (str): Name for the user (default: “User”)
    emoji (str): Emoji for the user (default: “:technologist:”)
    stream (Optional[bool]): Whether to stream the response content
    markdown (bool): Whether to render content as markdown (default: True)
    show_time (bool): Whether to show execution time (default: True)
    show_step_details (bool): Whether to show individual step outputs (default: True)
    exit_on (Optional[List[str]]): List of commands to exit the CLI
    **kwargs: Additional keyword arguments

​
cancel_run
Cancel a running workflow execution. Parameters:

    run_id (str): The run_id to cancel

Returns:

    bool: True if the run was found and marked for cancellation, False otherwise

​
get_run
Get the status and details of a background workflow run. Parameters:

    run_id (str): The run ID to get

Returns:

    Optional[WorkflowRunOutput]: The workflow run output if found

​
get_run_output
Get a WorkflowRunOutput from the database. Parameters:

    run_id (str): The run ID
    session_id (Optional[str]): Session ID to use

Returns:

    Optional[WorkflowRunOutput]: The run output

​
get_last_run_output
Get the last run response from the database for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use

Returns:

    Optional[WorkflowRunOutput]: The last run output

​
get_chat_history
Return a list of dictionaries containing the input and output for each run in the session. Parameters:

    session_id (Optional[str]): The session ID to get the chat history for. If not provided, the current cached session ID is used
    last_n_runs (Optional[int]): Number of recent runs to include. If None, all runs will be considered

Returns:

    List[WorkflowChatInteraction]: A list of dictionaries containing the input and output for each run

​
get_session
Get the session for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use

Returns:

    Optional[WorkflowSession]: The workflow session

​
get_session_state
Get the session state for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use

Returns:

    Dict[str, Any]: The session state

​
get_session_name
Get the session name for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use

Returns:

    str: The session name

​
set_session_name
Set the session name and save to storage. Parameters:

    session_id (Optional[str]): Session ID to use
    autogenerate (bool): Whether to autogenerate the name
    session_name (Optional[str]): The name to set

Returns:

    WorkflowSession: The updated session

​
get_session_metrics
Get the session metrics for the given session ID. Parameters:

    session_id (Optional[str]): Session ID to use

Returns:

    Optional[Metrics]: The session metrics

​
delete_session
Delete a session. Parameters:

    session_id (str): Session ID to delete

​
save_session
Save the WorkflowSession to storage. Parameters:

    session (WorkflowSession): The session to save

​
to_dict
Convert workflow to dictionary representation. Returns:

    Dict[str, Any]: Dictionary representation of the workflow


Workflows
RemoteWorkflow

Execute workflows hosted on a remote AgentOS instance
RemoteWorkflow allows you to run workflows that are hosted on a remote AgentOS instance. It provides the same interface as a local workflow, making it easy to integrate remote workflows into your applications.
​
Installation

pip install agno

​
Basic Usage

from agno.workflow import RemoteWorkflow

# Create a remote workflow pointing to a remote AgentOS instance
workflow = RemoteWorkflow(
    base_url="http://localhost:7777",
    workflow_id="qa-workflow",
)

# Run the workflow (async)
response = await workflow.arun("What are the benefits of Python?")
print(response.content)

​
Parameters
Parameter	Type	Default	Description
base_url	str	Required	Base URL of the remote AgentOS instance (e.g., "http://localhost:7777")
workflow_id	str	Required	ID of the remote workflow to execute
timeout	float	300.0	Request timeout in seconds
config_ttl	float	300.0	Time-to-live for cached configuration in seconds
​
Properties
​
id
Returns the workflow ID.

print(workflow.id)  # "qa-workflow"

​
name
Returns the workflow’s name from the remote configuration.

print(workflow.name)  # "QA Workflow"

​
description
Returns the workflow’s description from the remote configuration.

print(workflow.description)  # "A Q&A workflow for answering questions"

​
db
Returns a RemoteDb instance if the workflow has a database configured.

if workflow.db:
    print(f"Database ID: {workflow.db.id}")

​
Methods
​
arun
Execute the remote workflow asynchronously.

# Non-streaming
response = await workflow.arun(
    "Explain machine learning",
    user_id="user-123",
    session_id="session-456",
)
print(response.content)
print(f"Status: {response.status}")

# Streaming
async for event in workflow.arun(
    "Generate a report",
    stream=True,
    user_id="user-123",
):
    if event.event == "RunContent" and hasattr(event, "content"):
        print(event.content, end="", flush=True)

Parameters:
Parameter	Type	Default	Description
input	str | Dict | List | BaseModel	Required	The input for the workflow
additional_data	Optional[Dict]	None	Additional data to pass to the workflow
user_id	Optional[str]	None	User ID for the run
run_id	Optional[str]	None	Custom run ID
session_id	Optional[str]	None	Session ID for context persistence
session_state	Optional[Dict]	None	Session state dictionary
images	Optional[List[Image]]	None	Images to include
audio	Optional[List[Audio]]	None	Audio to include
videos	Optional[List[Video]]	None	Videos to include
files	Optional[List[File]]	None	Files to include
stream	bool	False	Whether to stream the response
stream_events	Optional[bool]	None	Whether to stream events
auth_token	Optional[str]	None	JWT token for authentication
Returns:

    WorkflowRunOutput when stream=False
    AsyncIterator[WorkflowRunOutputEvent] when stream=True

​
cancel_run
Cancel a running workflow execution.

success = await workflow.cancel_run(run_id="run-123")
if success:
    print("Run cancelled")

Parameters:
Parameter	Type	Default	Description
run_id	str	Required	ID of the run to cancel
auth_token	Optional[str]	None	JWT token for authentication
Returns: bool - True if successfully cancelled
​
get_workflow_config
Get the workflow configuration from the remote server (always fetches fresh).

config = await workflow.get_workflow_config()
print(f"Workflow name: {config.name}")
print(f"Steps: {config.steps}")

Returns: WorkflowResponse
​
refresh_config
Force refresh the cached workflow configuration.

config = workflow.refresh_config()

Returns: WorkflowResponse
​
Using in AgentOS Gateway
Remote workflows can be registered in a local AgentOS to create a gateway:

from agno.workflow import RemoteWorkflow
from agno.os import AgentOS

agent_os = AgentOS(
    workflows=[
        RemoteWorkflow(base_url="http://server-1:7777", workflow_id="qa-workflow"),
        RemoteWorkflow(base_url="http://server-2:7777", workflow_id="analysis-workflow"),
    ],
)

See AgentOS Gateway for more details.
​
Streaming Example

from agno.workflow import RemoteWorkflow

workflow = RemoteWorkflow(
    base_url="http://localhost:7777",
    workflow_id="story-workflow",
)

print("Response: ", end="", flush=True)
async for event in workflow.arun(
    "Write a story about space exploration",
    stream=True,
    user_id="user-123",
):
    # Handle content from agent events or workflow completion
    if event.event == "RunContent" and hasattr(event, "content"):
        print(event.content, end="", flush=True)
    elif event.event == "WorkflowAgentCompleted" and hasattr(event, "content"):
        print(event.content, end="", flush=True)

​
Error Handling

from agno.exceptions import RemoteServerUnavailableError

try:
    response = await workflow.arun("Hello")
except RemoteServerUnavailableError as e:
    print(f"Remote server unavailable: {e.message}")

​
Authentication
For authenticated AgentOS instances, pass the auth_token parameter:

response = await workflow.arun(
    "Process this request",
    auth_token="your-jwt-token",
)

​
Notes
Remote Workflows via WebSocket are not yet supported. Use HTTP streaming instead.

Workflows
Step
Parameter	Type	Default	Description
name	Optional[str]	None	Name of the step for identification
agent	Optional[Agent]	None	Agent to execute for this step
team	Optional[Team]	None	Team to execute for this step
executor	Optional[StepExecutor]	None	Custom function to execute for this step
step_id	Optional[str]	None	Unique identifier for the step (auto-generated if not provided)
description	Optional[str]	None	Description of the step’s purpose
max_retries	int	3	Maximum number of retry attempts on failure
timeout_seconds	Optional[int]	None	Timeout for step execution in seconds
skip_on_failure	bool	False	Whether to skip this step if it fails after all retries
add_workflow_history	bool	False	If True, add the workflow history to the step
num_history_runs	int	None	Number of runs to include in the workflow history, if not provided, all history runs are included


Workflows
StepInput
Parameter	Type	Description
input	Optional[Union[str, Dict[str, Any], List[Any], BaseModel]]	Primary input message (can be any format)
previous_step_content	Optional[Any]	Content from the last step
previous_step_outputs	Optional[Dict[str, StepOutput]]	All previous step outputs by name
additional_data	Optional[Dict[str, Any]]	Additional context data
images	Optional[List[Image]]	Media inputs - images (accumulated from workflow input and previous steps)
videos	Optional[List[Video]]	Media inputs - videos (accumulated from workflow input and previous steps)
audio	Optional[List[Audio]]	Media inputs - audio (accumulated from workflow input and previous steps)
files	Optional[List[File]]	File inputs (accumulated from workflow input and previous steps)
​
Helper Functions
Method	Return Type	Description
get_step_output(step_name: str)	Optional[StepOutput]	Get the complete StepOutput object from a specific step by name
get_step_content(step_name: str)	Optional[Union[str, Dict[str, str]]]	Get content from a specific step by name
get_all_previous_content()	str	Get all previous step content combined
get_last_step_content()	Optional[str]	Get content from the immediate previous step
get_workflow_history(num_runs: int)	List[Tuple[str, str]]	Get the workflow history as a list of tuples
get_workflow_history_context(num_runs: int)	str	Get the workflow history as a formatted context string

Workflows
StepOutput
Parameter	Type	Default	Description
step_name	Optional[str]	None	Step identification name
step_id	Optional[str]	None	Unique step identifier
step_type	Optional[str]	None	Type of step (e.g., “Loop”, “Condition”, “Parallel”)
executor_type	Optional[str]	None	Type of executor: “agent”, “team”, or “function”
executor_name	Optional[str]	None	Name of the executor
content	Optional[Union[str, Dict[str, Any], List[Any], BaseModel, Any]]	None	Primary output (can be any format)
step_run_id	Optional[str]	None	Link to the run ID of the step execution
images	Optional[List[Image]]	None	Media outputs - images (new or passed-through)
videos	Optional[List[Video]]	None	Media outputs - videos (new or passed-through)
audio	Optional[List[Audio]]	None	Media outputs - audio (new or passed-through)
files	Optional[List[File]]	None	File outputs (new or passed-through)
metrics	Optional[Metrics]	None	Execution metrics and metadata
success	bool	True	Execution success status
error	Optional[str]	None	Error message if execution failed
stop	bool	False	Request early workflow termination
steps	Optional[List[StepOutput]]	None	Nested step outputs for composite steps (Loop, Condition, etc.)

Workflows
Conditional Steps
Parameter	Type	Default	Description
evaluator	Union[Callable[[StepInput], bool], Callable[[StepInput], Awaitable[bool]], bool]	Required	Function or boolean to evaluate the condition
steps	WorkflowSteps	Required	Steps to execute if the condition is met
name	Optional[str]	None	Name of the condition step
description	Optional[str]	None	Description of the condition step

Workflows
Parallel Steps
Parameter	Type	Default	Description
*steps	*WorkflowSteps	Required	Variable number of steps to execute in parallel
name	Optional[str]	None	Name of the parallel execution block
description	Optional[str]	None	Description of the parallel execution

Workflows
Router Steps
Parameter	Type	Default	Description
selector	Union[Callable[[StepInput], Union[WorkflowSteps, List[WorkflowSteps]]], Callable[[StepInput], Awaitable[Union[WorkflowSteps, List[WorkflowSteps]]]]]	Required	Function to select steps dynamically (supports both sync and async functions)
choices	WorkflowSteps	Required	Available steps for selection
name	Optional[str]	None	Name of the router step
description	Optional[str]	None	Description of the router step

Workflows
Loop Steps
Parameter	Type	Default	Description
steps	WorkflowSteps	Required	Steps to execute in each loop iteration
name	Optional[str]	None	Name of the loop step
description	Optional[str]	None	Description of the loop step
max_iterations	int	3	Maximum number of iterations for the loop
end_condition	Optional[Union[Callable[[List[StepOutput]], bool], Callable[[List[StepOutput]], Awaitable[bool]]]]	None	Function to evaluate if the loop should end

Workflows
Steps
Parameter	Type	Default	Description
name	Optional[str]	None	Name of the steps group for identification
description	Optional[str]	None	Description of the steps group’s purpose
steps	Optional[List[Any]]	[]	List of steps to execute sequentially (empty list if not provided)

AgentOS
AgentOS
​
Parameters
Parameter	Type	Default	Description
id	Optional[str]	Autogenerated UUID	AgentOS ID
name	Optional[str]	None	AgentOS name
description	Optional[str]	None	AgentOS description
version	Optional[str]	None	AgentOS version
agents	Optional[List[Agent]]	None	List of agents available in the AgentOS
teams	Optional[List[Team]]	None	List of teams available in the AgentOS
workflows	Optional[List[Workflow]]	None	List of workflows available in the AgentOS
knowledge	Optional[List[Knowledge]]	None	List of standalone knowledge instances available in the AgentOS
interfaces	Optional[List[BaseInterface]]	None	List of interfaces available in the AgentOS
a2a_interface	bool	False	Whether to expose the OS agents and teams in an A2A server
authorization	bool	False	Whether to enable RBAC authorization
authorization_config	Optional[AuthorizationConfig]	None	Configuration for JWT verification when authorization is enabled
cors_allowed_origins	Optional[List[str]]	None	List of allowed CORS origins (merged with default Agno domains)
config	Optional[Union[str, AgentOSConfig]]	None	User-provided configuration for the AgentOS. Either a path to a YAML file or an AgentOSConfig instance.
settings	Optional[AgnoAPISettings]	None	Settings for the AgentOS API
base_app	Optional[FastAPI]	None	Custom FastAPI APP to use for the AgentOS
lifespan	Optional[Any]	None	Lifespan context manager for the FastAPI app
enable_mcp_server	bool	False	Whether to enable MCP (Model Context Protocol)
on_route_conflict	Literal["preserve_agentos", "preserve_base_app", "error"]	"preserve_agentos"	What to do when a route conflict is detected in case a custom base_app is provided.
tracing	bool	False	Enable OpenTelemetry tracing for all agents and teams
tracing_db	Optional[Union[BaseDb, AsyncBaseDb]]	None	Dedicated database for storing traces
auto_provision_dbs	bool	True	Whether to automatically provision databases
run_hooks_in_background	bool	False	Run agent/team pre/post hooks as FastAPI background tasks
telemetry	bool	True	Log minimal telemetry for analytics
​
Authorization
Enable RBAC by setting authorization=True and setting the JWT_VERIFICATION_KEY environment variable to the public key of the JWT verification key:

from agno.os import AgentOS
from agno.os.config import AuthorizationConfig

agent_os = AgentOS(
    id="my-agent-os",
    agents=[my_agent],
    authorization=True,
)

Or for more control, you can use the AuthorizationConfig class:

from agno.os import AgentOS
from agno.os.config import AuthorizationConfig

agent_os = AgentOS(
    id="my-agent-os",
    agents=[my_agent],
    authorization=True,
    authorization_config=AuthorizationConfig(
        verification_keys=["your-jwt-verification-key"],
        algorithm="RS256",
    ),
)

See AuthorizationConfig for configuration options.
​
Functions
​
get_app
Get the FastAPI APP configured for the AgentOS.
​
get_routes
Get the routes configured for the AgentOS.
​
serve
Run the app, effectively starting the AgentOS. Parameters:

    app (Union[str, FastAPI]): FastAPI APP instance
    host (str): Host to bind. Defaults to localhost
    port (int): Port to bind. Defaults to 7777
    workers (Optional[int]): Number of workers to use. Defaults to None
    reload (bool): Enable auto-reload for development. Defaults to False

​
resync
Resync the AgentOS to discover, initialize and configure: agents, teams, workflows, databases and knowledge bases. Parameters:

    app (FastAPI): The FastAPI app instance


AgentOS
AgentOSConfig
​
Parameters
Parameter	Type	Default	Description
available_models	List[str]	None	List of models available in the AgentOS
chat	Optional[ChatConfig]	None	Configuration for the Chat page of your AgentOS
evals	Optional[EvalsConfig]	None	Configuration for the Evals page of your AgentOS
knowledge	Optional[KnowledgeConfig]	None	Configuration for the Knowledge page of your AgentOS
memory	Optional[MemoryConfig]	None	Configuration for the Memory page of your AgentOS
session	Optional[SessionConfig]	None	Configuration for the Session page of your AgentOS
metrics	Optional[MetricsConfig]	None	Configuration for the Metrics page of your AgentOS
​
ChatConfig
Parameter	Type	Default	Description
quick_prompts	Dict[str, List[str]]	None	Default prompts for each agent, team and workflow
​
EvalsConfig
Parameter	Type	Default	Description
available_models	List[str]	None	List of models available in the Evals page
display_name	str	None	Display name for the Evals page
dbs	Optional[List[DatabaseConfig[EvalsDomainConfig]]]	None	List of configurations for each database
​
KnowledgeConfig
Parameter	Type	Default	Description
display_name	str	None	Display name for the Knowledge page
dbs	Optional[List[DatabaseConfig[KnowledgeDomainConfig]]]	None	List of configurations for each database
​
MemoryConfig
Parameter	Type	Default	Description
display_name	str	None	Display name for the Memory page
dbs	Optional[List[DatabaseConfig[MemoryDomainConfig]]]	None	List of configurations for each database
​
SessionConfig
Parameter	Type	Default	Description
display_name	str	None	Display name for the Session page
dbs	Optional[List[DatabaseConfig[SessionDomainConfig]]]	None	List of configurations for each database
​
MetricsConfig
Parameter	Type	Default	Description
display_name	str	None	Display name for the Metrics page
dbs	Optional[List[DatabaseConfig[MetricsDomainConfig]]]	None	List of configurations for each database
​
Using a YAML Configuration File
You can also provide your AgentOS configuration via a YAML file. You can define all the previously mentioned configuration options in the file:

# List of models available in the AgentOS
available_models:
  - <MODEL_STRING>
  ...

# Configuration for the Chat page
chat:
  quick_prompts:
    <AGENT_ID>:
      - <PROMPT_1>
      - <PROMPT_2>
      - <PROMPT_3>
      ...
    ...


# Configuration for the Evals page
evals:
  available_models:
    - <MODEL_STRING>
    ...
  display_name: <DISPLAY_NAME>
  dbs:
    - <DB_ID>
      domain_config:
        available_models:
          - <MODEL_STRING>
          ...
        display_name: <DISPLAY_NAME>
    ...


# Configuration for the Knowledge page
knowledge:
  display_name: <DISPLAY_NAME>
  dbs:
    - <DB_ID>
      domain_config:
        display_name: <DISPLAY_NAME>
    ...

# Configuration for the Memory page
memory:
  display_name: <DISPLAY_NAME>
  dbs:
    - <DB_ID>
      domain_config:
        display_name: <DISPLAY_NAME>
    ...

# Configuration for the Session page
session:
  display_name: <DISPLAY_NAME>
  dbs:
    - <DB_ID>
      domain_config:
        display_name: <DISPLAY_NAME>
    ...

# Configuration for the Metrics page
metrics:
  display_name: <DISPLAY_NAME>
  dbs:
    - <DB_ID>
      domain_config:
        display_name: <DISPLAY_NAME>
    ...


AgentOS
AgentOSClient

Python client for interacting with AgentOS API endpoints
The AgentOSClient provides a convenient interface for interacting with a running AgentOS instance. It supports all AgentOS operations including running agents, teams, and workflows, managing sessions and memories, and searching knowledge bases.
​
Basic Usage

from agno.client import AgentOSClient

# Connect to AgentOS
client = AgentOSClient(base_url="http://localhost:7777")

# Get configuration
config = await client.aget_config()
print(f"Connected to: {config.name or config.os_id}")
print(f"Available agents: {[a.id for a in config.agents]}")

​
Parameters
Parameter	Type	Default	Description
base_url	str	Required	Base URL of the AgentOS instance (e.g., "http://localhost:7777")
timeout	float	60.0	Request timeout in seconds
​
Methods
​
Discovery & Configuration
​
aget_config
Get AgentOS configuration and metadata asynchronously.

config = await client.aget_config()

Returns: ConfigResponse containing:

    os_id: Unique identifier for the OS instance
    name: Name of the OS instance
    agents: List of registered agents
    teams: List of registered teams
    workflows: List of registered workflows
    interfaces: List of available interfaces

​
get_config
Synchronous version of aget_config.

config = client.get_config()

​
list_agents
List all agents configured in the AgentOS instance.

agents = await client.list_agents()
for agent in agents:
    print(f"{agent.id}: {agent.name}")

Returns: List[AgentSummaryResponse]
​
aget_agent
Get detailed configuration for a specific agent.

agent = await client.aget_agent(agent_id="my-agent")
print(f"Name: {agent.name}")
print(f"Model: {agent.model}")
print(f"Tools: {agent.tools}")

Parameters:

    agent_id (str): ID of the agent to retrieve

Returns: AgentResponse
​
list_teams
List all teams configured in the AgentOS instance.

teams = await client.list_teams()

Returns: List[TeamSummaryResponse]
​
aget_team
Get detailed configuration for a specific team.

team = await client.aget_team(team_id="my-team")

Parameters:

    team_id (str): ID of the team to retrieve

Returns: TeamResponse
​
list_workflows
List all workflows configured in the AgentOS instance.

workflows = await client.list_workflows()

Returns: List[WorkflowSummaryResponse]
​
aget_workflow
Get detailed configuration for a specific workflow.

workflow = await client.aget_workflow(workflow_id="my-workflow")

Parameters:

    workflow_id (str): ID of the workflow to retrieve

Returns: WorkflowResponse
​
Running Agents
​
run_agent
Execute an agent run (non-streaming).

result = await client.run_agent(
    agent_id="my-agent",
    message="What is 2 + 2?",
    session_id="session-123",
    user_id="user-456",
)
print(f"Response: {result.content}")
print(f"Tokens: {result.metrics.total_tokens}")

Parameters:
Parameter	Type	Default	Description
agent_id	str	Required	ID of the agent to run
message	str	Required	The message/prompt for the agent
session_id	Optional[str]	None	Session ID for context persistence
user_id	Optional[str]	None	User ID for the run
images	Optional[Sequence[Image]]	None	Images to include
audio	Optional[Sequence[Audio]]	None	Audio to include
videos	Optional[Sequence[Video]]	None	Videos to include
files	Optional[Sequence[File]]	None	Files to include
session_state	Optional[Dict]	None	Session state dictionary
dependencies	Optional[Dict]	None	Dependencies dictionary
metadata	Optional[Dict]	None	Metadata dictionary
knowledge_filters	Optional[Dict]	None	Filters for knowledge search
Returns: RunOutput
​
run_agent_stream
Stream an agent run response.

from agno.run.agent import RunContentEvent, RunCompletedEvent

async for event in client.run_agent_stream(
    agent_id="my-agent",
    message="Tell me a story",
):
    if isinstance(event, RunContentEvent):
        print(event.content, end="", flush=True)
    elif isinstance(event, RunCompletedEvent):
        print(f"\nRun ID: {event.run_id}")

Parameters: Same as run_agent Yields: RunOutputEvent (one of RunStartedEvent, RunContentEvent, RunToolCallEvent, RunCompletedEvent, etc.)
​
continue_agent_run
Continue a paused agent run with tool results.

from agno.models.response import ToolExecution

result = await client.continue_agent_run(
    agent_id="my-agent",
    run_id="run-123",
    tools=[
        ToolExecution(
            tool_call_id="call-1",
            result="Tool result here",
        )
    ],
)

Parameters:
Parameter	Type	Default	Description
agent_id	str	Required	ID of the agent
run_id	str	Required	ID of the run to continue
tools	List[ToolExecution]	Required	Tool execution results
session_id	Optional[str]	None	Session ID
user_id	Optional[str]	None	User ID
Returns: RunOutput
​
cancel_agent_run
Cancel an agent run.

await client.cancel_agent_run(agent_id="my-agent", run_id="run-123")

​
Running Teams
​
run_team
Execute a team run (non-streaming).

result = await client.run_team(
    team_id="research-team",
    message="Research the latest AI trends",
    user_id="user-123",
)
print(f"Response: {result.content}")

Parameters:
Parameter	Type	Default	Description
team_id	str	Required	ID of the team to run
message	str	Required	The message/prompt for the team
session_id	Optional[str]	None	Session ID for context persistence
user_id	Optional[str]	None	User ID for the run
images	Optional[Sequence[Image]]	None	Images to include
audio	Optional[Sequence[Audio]]	None	Audio to include
videos	Optional[Sequence[Video]]	None	Videos to include
files	Optional[Sequence[File]]	None	Files to include
Returns: TeamRunOutput
​
run_team_stream
Stream a team run response.

from agno.run.team import RunContentEvent

async for event in client.run_team_stream(
    team_id="research-team",
    message="Analyze this topic",
):
    if isinstance(event, RunContentEvent):
        print(event.content, end="", flush=True)

Yields: TeamRunOutputEvent
​
cancel_team_run
Cancel a team run.

await client.cancel_team_run(team_id="my-team", run_id="run-123")

​
Running Workflows
​
run_workflow
Execute a workflow run (non-streaming).

result = await client.run_workflow(
    workflow_id="qa-workflow",
    message="What are the benefits of Python?",
    user_id="user-123",
)
print(f"Response: {result.content}")
print(f"Status: {result.status}")

Parameters:
Parameter	Type	Default	Description
workflow_id	str	Required	ID of the workflow to run
message	str	Required	The message/prompt for the workflow
session_id	Optional[str]	None	Session ID for context persistence
user_id	Optional[str]	None	User ID for the run
Returns: WorkflowRunOutput
​
run_workflow_stream
Stream a workflow run response.

async for event in client.run_workflow_stream(
    workflow_id="qa-workflow",
    message="Explain machine learning",
):
    if event.event == "RunContent" and hasattr(event, "content"):
        print(event.content, end="", flush=True)

Yields: WorkflowRunOutputEvent
​
cancel_workflow_run
Cancel a workflow run.

await client.cancel_workflow_run(workflow_id="my-workflow", run_id="run-123")

​
Memory Operations
​
create_memory
Create a new user memory.

memory = await client.create_memory(
    memory="User prefers dark mode",
    user_id="user-123",
    topics=["preferences", "ui"],
)
print(f"Created: {memory.memory_id}")

Parameters:
Parameter	Type	Default	Description
memory	str	Required	The memory content to store
user_id	str	Required	User ID to associate with the memory
topics	Optional[List[str]]	None	Topics to categorize the memory
db_id	Optional[str]	None	Database ID to use
Returns: UserMemorySchema
​
list_memories
List user memories with filtering and pagination.

memories = await client.list_memories(
    user_id="user-123",
    topics=["preferences"],
    limit=10,
)
for mem in memories.data:
    print(f"{mem.memory_id}: {mem.memory}")

Parameters:
Parameter	Type	Default	Description
user_id	Optional[str]	None	Filter by user ID
topics	Optional[List[str]]	None	Filter by topics
search_content	Optional[str]	None	Search within memory content
limit	int	20	Number of memories per page
page	int	1	Page number
Returns: PaginatedResponse[UserMemorySchema]
​
get_memory
Get a specific memory by ID.

memory = await client.get_memory(memory_id="mem-123", user_id="user-123")

Returns: UserMemorySchema
​
update_memory
Update an existing memory.

updated = await client.update_memory(
    memory_id="mem-123",
    memory="User strongly prefers dark mode",
    user_id="user-123",
    topics=["preferences", "ui", "accessibility"],
)

Returns: UserMemorySchema
​
delete_memory
Delete a specific memory.

await client.delete_memory(memory_id="mem-123", user_id="user-123")

​
Session Operations
​
create_session
Create a new session.

from agno.db.base import SessionType

session = await client.create_session(
    session_type=SessionType.AGENT,
    agent_id="my-agent",
    user_id="user-123",
    session_name="My Chat Session",
)
print(f"Session ID: {session.session_id}")

Parameters:
Parameter	Type	Default	Description
session_type	SessionType	SessionType.AGENT	Type of session (AGENT, TEAM, WORKFLOW)
session_id	Optional[str]	None	Optional session ID (auto-generated if not provided)
user_id	Optional[str]	None	User ID to associate with the session
session_name	Optional[str]	None	Human-readable session name
agent_id	Optional[str]	None	Agent ID (for agent sessions)
team_id	Optional[str]	None	Team ID (for team sessions)
workflow_id	Optional[str]	None	Workflow ID (for workflow sessions)
Returns: AgentSessionDetailSchema, TeamSessionDetailSchema, or WorkflowSessionDetailSchema
​
get_sessions
List sessions with filtering and pagination.

sessions = await client.get_sessions(
    user_id="user-123",
    session_type=SessionType.AGENT,
    limit=20,
)
for session in sessions.data:
    print(f"{session.session_id}: {session.session_name}")

Returns: PaginatedResponse[SessionSchema]
​
get_session
Get a specific session by ID.

session = await client.get_session(
    session_id="session-123",
    session_type=SessionType.AGENT,
)

Returns: AgentSessionDetailSchema, TeamSessionDetailSchema, or WorkflowSessionDetailSchema
​
get_session_runs
Get all runs for a specific session.

runs = await client.get_session_runs(session_id="session-123")
for run in runs:
    print(f"{run.run_id}: {run.content[:50]}...")

Returns: List[RunSchema | TeamRunSchema | WorkflowRunSchema]
​
rename_session
Rename a session.

session = await client.rename_session(
    session_id="session-123",
    session_name="My Updated Session Name",
)

Returns: Session detail schema
​
delete_session
Delete a specific session.

await client.delete_session(session_id="session-123")

​
Knowledge Operations
​
upload_knowledge_content
Upload content to the knowledge base.

from agno.media import File

content = await client.upload_knowledge_content(
    name="My Document",
    description="Important documentation",
    file=File(content=b"...", filename="doc.pdf", mime_type="application/pdf"),
)
print(f"Content ID: {content.id}")

Parameters:
Parameter	Type	Default	Description
name	Optional[str]	None	Content name
description	Optional[str]	None	Content description
url	Optional[str]	None	URL to fetch content from
file	Optional[File]	None	File object to upload
text_content	Optional[str]	None	Raw text content
reader_id	Optional[str]	None	Reader to use for processing
chunker	Optional[str]	None	Chunking strategy
Returns: ContentResponseSchema
​
search_knowledge
Search the knowledge base.

results = await client.search_knowledge(
    query="What is Agno?",
    limit=5,
)
for result in results.data:
    print(f"Score: {result.score}")
    print(f"Content: {result.content[:100]}...")

Parameters:
Parameter	Type	Default	Description
query	str	Required	Search query string
max_results	Optional[int]	None	Maximum results to return
filters	Optional[Dict]	None	Filters to apply
search_type	Optional[str]	None	Search type (vector, keyword, hybrid)
Returns: PaginatedResponse[VectorSearchResult]
​
list_knowledge_content
List all content in the knowledge base.

content = await client.list_knowledge_content(limit=20)
for item in content.data:
    print(f"{item.id}: {item.name}")

Returns: PaginatedResponse[ContentResponseSchema]
​
get_knowledge_config
Get knowledge base configuration.

config = await client.get_knowledge_config()
print(f"Readers: {config.readers}")
print(f"Chunkers: {config.chunkers}")

Returns: KnowledgeConfigResponse
​
Trace Operations
​
get_traces
List execution traces with filtering and pagination.

traces = await client.get_traces(
    agent_id="my-agent",
    limit=20,
)
for trace in traces.data:
    print(f"{trace.trace_id}: {trace.status}")

Returns: PaginatedResponse[TraceSummary]
​
get_trace
Get detailed trace information.

trace = await client.get_trace(trace_id="trace-123")
print(f"Duration: {trace.duration_ms}ms")
print(f"Spans: {len(trace.spans)}")

Returns: TraceDetail or TraceNode (if span_id provided)
​
Metrics Operations
​
get_metrics
Retrieve AgentOS metrics and analytics data.

from datetime import date

metrics = await client.get_metrics(
    starting_date=date(2024, 1, 1),
    ending_date=date(2024, 1, 31),
)

Returns: MetricsResponse
​
refresh_metrics
Manually trigger recalculation of system metrics.

metrics = await client.refresh_metrics()

Returns: List[DayAggregatedMetrics]
​
Error Handling
The client raises RemoteServerUnavailableError when the remote server is unavailable:

from agno.exceptions import RemoteServerUnavailableError

try:
    config = await client.aget_config()
except RemoteServerUnavailableError as e:
    print(f"Server unavailable: {e.message}")
    print(f"Base URL: {e.base_url}")

For HTTP errors (4xx, 5xx), the client raises httpx.HTTPStatusError.
​
Authentication
To include authentication headers in requests, pass the headers parameter to any method:

headers = {"Authorization": "Bearer your-token"}
config = await client.aget_config(headers=headers)



AgentOS
AuthorizationConfig
Configuration for JWT verification when RBAC authorization is enabled on AgentOS.
​
Import

from agno.os.config import AuthorizationConfig

​
Parameters
Parameter	Type	Default	Description
verification_keys	Optional[List[str]]	None	List of keys used to verify JWT signatures. For asymmetric algorithms (e.g. RS256), use public keys. For symmetric algorithms (e.g. HS256), use shared secrets. Each key is tried in order until one succeeds - useful for accepting tokens from multiple issuers.
jwks_file	Optional[str]	None	Path to a static JWKS (JSON Web Key Set) file containing public keys. Keys are matched by kid (key ID) from the JWT header. Alternative to verification_keys for RSA key management.
algorithm	Optional[str]	RS256	JWT algorithm for token verification. Common options: RS256 (asymmetric), HS256 (symmetric).
verify_audience	Optional[bool]	False	Whether to verify the audience claim of the JWT token. This should not be enabled for AgentOS Control Plane traffic.
​
Usage

from agno.os import AgentOS
from agno.os.config import AuthorizationConfig

agent_os = AgentOS(
    id="my-agent-os",
    agents=[my_agent],
    authorization=True,
    authorization_config=AuthorizationConfig(
        verification_keys=["your-public-key-or-secret"],
        algorithm="RS256",
    ),
)

​
Algorithm Options
Algorithm	Type	Key Format
RS256	Asymmetric (RSA)	Public key (PEM format)
RS384	Asymmetric (RSA)	Public key (PEM format)
RS512	Asymmetric (RSA)	Public key (PEM format)
HS256	Symmetric (HMAC)	Shared secret string
HS384	Symmetric (HMAC)	Shared secret string
HS512	Symmetric (HMAC)	Shared secret string
ES256	Asymmetric (ECDSA)	Public key (PEM format)
ES384	Asymmetric (ECDSA)	Public key (PEM format)
ES512	Asymmetric (ECDSA)	Public key (PEM format)
​
Examples
​
Using RS256 (Asymmetric)

# RS256 with a public key
authorization_config = AuthorizationConfig(
    verification_keys=["""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
-----END PUBLIC KEY-----"""],
    algorithm="RS256",
)

​
Using HS256 (Symmetric)

# HS256 with a shared secret
authorization_config = AuthorizationConfig(
    verification_keys=["your-256-bit-secret-key"],
    algorithm="HS256",
)

​
Using JWKS File

# RS256 with a JWKS file
authorization_config = AuthorizationConfig(
    jwks_file="/path/to/jwks.json",
    algorithm="RS256",
)

The JWKS file should follow the standard format:

{
  "keys": [
    {
      "kty": "RSA",
      "kid": "my-key-id",
      "use": "sig",
      "alg": "RS256",
      "n": "0vx7agoebGc...",
      "e": "AQAB"
    }
  ]
}

​
See Also

    Security Overview - AgentOS security overview
    RBAC Documentation - Complete RBAC scopes and permissions
    JWT Middleware - Advanced JWT configuration
    JWTMiddleware Reference - Middleware class reference

AgentOS
JWTMiddleware
JWT Authentication Middleware with optional RBAC (Role-Based Access Control) for AgentOS.
​
Import

from agno.os.middleware import JWTMiddleware
from agno.os.middleware.jwt import TokenSource

​
JWTMiddleware Parameters
Parameter	Type	Default	Description
verification_keys	Optional[List[str]]	JWT_VERIFICATION_KEY env var	List of keys for JWT verification. For RS256, use public keys. For HS256, use shared secrets. Each key is tried in order until one succeeds - useful for accepting tokens from multiple issuers.
jwks_file	Optional[str]	JWT_JWKS_FILE env var	Path to a static JWKS (JSON Web Key Set) file. Keys are looked up by kid (key ID) from the JWT header.
secret_key	Optional[str]	None	(Deprecated) Use verification_keys instead.
algorithm	str	"RS256"	JWT algorithm (RS256, HS256, ES256, etc.)
validate	bool	True	Whether to validate JWT tokens
authorization	Optional[bool]	None	Enable RBAC scope checking
token_source	TokenSource	TokenSource.HEADER	Where to extract JWT token from
token_header_key	str	"Authorization"	Header key for Authorization
cookie_name	str	"access_token"	Cookie name for JWT token
scopes_claim	str	"scopes"	JWT claim name for scopes
user_id_claim	str	"sub"	JWT claim name for user ID
session_id_claim	str	"session_id"	JWT claim name for session ID
audience_claim	str	"aud"	JWT claim name for audience/OS ID
verify_audience	bool	False	Verify aud claim matches AgentOS ID
dependencies_claims	Optional[List[str]]	None	Claims to extract for dependencies parameter
session_state_claims	Optional[List[str]]	None	Claims to extract for session_state parameter
scope_mappings	Optional[Dict[str, List[str]]]	None	Custom route-to-scope mappings (additive to defaults)
excluded_route_paths	Optional[List[str]]	See below	Routes to skip JWT/RBAC checks
admin_scope	Optional[str]	"agent_os:admin"	Scope that grants full admin access
​
TokenSource Enum
Value	Description
TokenSource.HEADER	Extract JWT from Authorization: Bearer <token> header
TokenSource.COOKIE	Extract JWT from HTTP cookie
TokenSource.BOTH	Try header first, then cookie as fallback
​
Default Excluded Routes

[
    "/",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/docs/oauth2-redirect",
]

​
Usage
​
Basic JWT Validation

from agno.os import AgentOS
from agno.os.middleware import JWTMiddleware

agent_os = AgentOS(agents=[my_agent])
app = agent_os.get_app()

app.add_middleware(
    JWTMiddleware,
    verification_keys=["your-jwt-key"],
    algorithm="RS256",
    validate=True,
)

​
JWT with RBAC Authorization

app.add_middleware(
    JWTMiddleware,
    verification_keys=["your-jwt-key"],
    algorithm="RS256",
    authorization=True,
    verify_audience=True,
)

​
JWT from Cookies

from agno.os.middleware.jwt import TokenSource

app.add_middleware(
    JWTMiddleware,
    verification_keys=["your-jwt-key"],
    token_source=TokenSource.COOKIE,
    cookie_name="access_token",
)

​
Parameter Injection

app.add_middleware(
    JWTMiddleware,
    verification_keys=["your-jwt-key"],
    user_id_claim="sub",
    session_id_claim="session_id",
    dependencies_claims=["name", "email", "roles"],
    session_state_claims=["preferences"],
)

​
Using JWKS File

# Using a static JWKS file (e.g., from your identity provider)
app.add_middleware(
    JWTMiddleware,
    jwks_file="/path/to/jwks.json",
    algorithm="RS256",
    authorization=True,
)

The JWKS file should have the standard format:

{
  "keys": [
    {
      "kty": "RSA",
      "kid": "my-key-id",
      "use": "sig",
      "alg": "RS256",
      "n": "0vx7agoebGc...",
      "e": "AQAB"
    }
  ]
}

​
Custom Scope Mappings

app.add_middleware(
    JWTMiddleware,
    verification_keys=["your-jwt-key"],
    authorization=True,
    scope_mappings={
        # Override default scope
        "GET /agents": ["custom:agents:list"],
        # Add new endpoint
        "POST /custom/action": ["custom:write"],
        # Allow without scopes
        "GET /public": [],
    }
)

​
Request State
After processing, the middleware stores the following in request.state:
Attribute	Type	Description
authenticated	bool	Whether the user is authenticated
user_id	Optional[str]	User ID from token claims
session_id	Optional[str]	Session ID from token claims
scopes	List[str]	User’s permission scopes
audience	Optional[str]	Audience claim value
token	str	The raw JWT token
authorization_enabled	bool	Whether RBAC is enabled
dependencies	Dict[str, Any]	Extracted dependencies claims
session_state	Dict[str, Any]	Extracted session state claims
accessible_resource_ids	Set[str]	Resource IDs user can access (for listing endpoints)
​
Error Responses
Status Code	Description
401 Unauthorized	Missing or invalid JWT token
401 Unauthorized	Token has expired
401 Unauthorized	Invalid audience (token not for this AgentOS)
403 Forbidden	Insufficient scopes for the requested operation
​


Runs
RunOutput
​
RunOutput Attributes
Attribute	Type	Default	Description
run_id	Optional[str]	None	Run ID
agent_id	Optional[str]	None	Agent ID for the run
agent_name	Optional[str]	None	Agent name for the run
session_id	Optional[str]	None	Session ID for the run
parent_run_id	Optional[str]	None	Parent run ID
workflow_id	Optional[str]	None	Workflow ID if this run is part of a workflow
user_id	Optional[str]	None	User ID associated with the run
content	Optional[Any]	None	Content of the response
content_type	str	"str"	Specifies the data type of the content
reasoning_content	Optional[str]	None	Any reasoning content the model produced
reasoning_steps	Optional[List[ReasoningStep]]	None	List of reasoning steps
reasoning_messages	Optional[List[Message]]	None	List of reasoning messages
model	Optional[str]	None	The model used in the run
model_provider	Optional[str]	None	The model provider used in the run
messages	Optional[List[Message]]	None	A list of messages included in the response
metrics	Optional[Metrics]	None	Usage metrics of the run
additional_input	Optional[List[Message]]	None	Additional input messages
tools	Optional[List[ToolExecution]]	None	List of tool executions
images	Optional[List[Image]]	None	List of images attached to the response
videos	Optional[List[Video]]	None	List of videos attached to the response
audio	Optional[List[Audio]]	None	List of audio snippets attached to the response
files	Optional[List[File]]	None	List of files attached to the response
response_audio	Optional[Audio]	None	The model’s raw response in audio
input	Optional[RunInput]	None	Input media and messages from user
citations	Optional[Citations]	None	Any citations used in the response
model_provider_data	Optional[Any]	None	Model provider specific metadata
references	Optional[List[MessageReferences]]	None	References used in the response
metadata	Optional[Dict[str, Any]]	None	Metadata associated with the run
created_at	int	Current timestamp	Unix timestamp of the response creation
events	Optional[List[RunOutputEvent]]	None	List of events that occurred during the run
status	RunStatus	RunStatus.running	Status of the run (running, completed, paused, cancelled, error)
workflow_step_id	Optional[str]	None	Workflow step ID (foreign key relationship)
​
RunOutputEvent Types and Attributes
​
Base RunOutputEvent Attributes
All events inherit from BaseAgentRunEvent which provides these common attributes:
Attribute	Type	Default	Description
created_at	int	Current timestamp	Unix timestamp of the event creation
event	str	Event type value	The type of event
agent_id	str	""	ID of the agent generating the event
agent_name	str	""	Name of the agent generating the event
run_id	Optional[str]	None	ID of the current run
session_id	Optional[str]	None	ID of the current session
workflow_id	Optional[str]	None	ID of the workflow if part of workflow execution
workflow_run_id	Optional[str]	None	ID of the workflow run
step_id	Optional[str]	None	ID of the workflow step
step_name	Optional[str]	None	Name of the workflow step
step_index	Optional[int]	None	Index of the workflow step
tools	Optional[List[ToolExecution]]	None	Tools associated with this event
content	Optional[Any]	None	For backwards compatibility
​
RunStartedEvent
Attribute	Type	Default	Description
event	str	"RunStarted"	Event type
model	str	""	The model being used
model_provider	str	""	The provider of the model
​
RunContentEvent
Attribute	Type	Default	Description
event	str	"RunContent"	Event type
content	Optional[Any]	None	The content of the response
content_type	str	"str"	Type of the content
reasoning_content	Optional[str]	None	Reasoning content produced
citations	Optional[Citations]	None	Citations used in the response
model_provider_data	Optional[Any]	None	Model provider specific metadata
response_audio	Optional[Audio]	None	Model’s audio response
image	Optional[Image]	None	Image attached to the response
references	Optional[List[MessageReferences]]	None	References used in the response
additional_input	Optional[List[Message]]	None	Additional input messages
reasoning_steps	Optional[List[ReasoningStep]]	None	Reasoning steps
reasoning_messages	Optional[List[Message]]	None	Reasoning messages
​
RunContentCompletedEvent
Attribute	Type	Default	Description
event	str	"RunContentCompleted"	Event type
​
IntermediateRunContentEvent
Attribute	Type	Default	Description
event	str	"RunIntermediateContent"	Event type
content	Optional[Any]	None	Intermediate content of the response
content_type	str	"str"	Type of the content
​
RunCompletedEvent
Attribute	Type	Default	Description
event	str	"RunCompleted"	Event type
content	Optional[Any]	None	Final content of the response
content_type	str	"str"	Type of the content
reasoning_content	Optional[str]	None	Reasoning content produced
citations	Optional[Citations]	None	Citations used in the response
model_provider_data	Optional[Any]	None	Model provider specific metadata
images	Optional[List[Image]]	None	Images attached to the response
videos	Optional[List[Video]]	None	Videos attached to the response
audio	Optional[List[Audio]]	None	Audio snippets attached to the response
response_audio	Optional[Audio]	None	Model’s audio response
references	Optional[List[MessageReferences]]	None	References used in the response
additional_input	Optional[List[Message]]	None	Additional input messages
reasoning_steps	Optional[List[ReasoningStep]]	None	Reasoning steps
reasoning_messages	Optional[List[Message]]	None	Reasoning messages
metadata	Optional[Dict[str, Any]]	None	Additional metadata
metrics	Optional[Metrics]	None	Usage metrics
​
RunPausedEvent
Attribute	Type	Default	Description
event	str	"RunPaused"	Event type
tools	Optional[List[ToolExecution]]	None	Tools that require confirmation
​
RunContinuedEvent
Attribute	Type	Default	Description
event	str	"RunContinued"	Event type
​
RunErrorEvent
Attribute	Type	Default	Description
event	str	"RunError"	Event type
content	Optional[str]	None	Error message
​
RunCancelledEvent
Attribute	Type	Default	Description
event	str	"RunCancelled"	Event type
reason	Optional[str]	None	Reason for cancellation
​
PreHookStartedEvent
Attribute	Type	Default	Description
event	str	"PreHookStarted"	Event type
pre_hook_name	Optional[str]	None	Name of the pre-hook being executed
run_input	Optional[RunInput]	None	The run input passed to the hook
​
PreHookCompletedEvent
Attribute	Type	Default	Description
event	str	"PreHookCompleted"	Event type
pre_hook_name	Optional[str]	None	Name of the pre-hook that completed
run_input	Optional[RunInput]	None	The run input passed to the hook
​
PostHookStartedEvent
Attribute	Type	Default	Description
event	str	"PostHookStarted"	Event type
post_hook_name	Optional[str]	None	Name of the post-hook being executed
​
PostHookCompletedEvent
Attribute	Type	Default	Description
event	str	"PostHookCompleted"	Event type
post_hook_name	Optional[str]	None	Name of the post-hook that completed
​
ReasoningStartedEvent
Attribute	Type	Default	Description
event	str	"ReasoningStarted"	Event type
​
ReasoningStepEvent
Attribute	Type	Default	Description
event	str	"ReasoningStep"	Event type
content	Optional[Any]	None	Content of the reasoning step
content_type	str	"str"	Type of the content
reasoning_content	str	""	Detailed reasoning content
​
ReasoningCompletedEvent
Attribute	Type	Default	Description
event	str	"ReasoningCompleted"	Event type
content	Optional[Any]	None	Content of the reasoning step
content_type	str	"str"	Type of the content
​
ToolCallStartedEvent
Attribute	Type	Default	Description
event	str	"ToolCallStarted"	Event type
tool	Optional[ToolExecution]	None	The tool being called
​
ToolCallCompletedEvent
Attribute	Type	Default	Description
event	str	"ToolCallCompleted"	Event type
tool	Optional[ToolExecution]	None	The tool that was called
content	Optional[Any]	None	Result of the tool call
images	Optional[List[Image]]	None	Images produced by the tool
videos	Optional[List[Video]]	None	Videos produced by the tool
audio	Optional[List[Audio]]	None	Audio produced by the tool
​
MemoryUpdateStartedEvent
Attribute	Type	Default	Description
event	str	"MemoryUpdateStarted"	Event type
​
MemoryUpdateCompletedEvent
Attribute	Type	Default	Description
event	str	"MemoryUpdateCompleted"	Event type
​
SessionSummaryStartedEvent
Attribute	Type	Default	Description
event	str	"SessionSummaryStarted"	Event type
​
SessionSummaryCompletedEvent
Attribute	Type	Default	Description
event	str	"SessionSummaryCompleted"	Event type
session_summary	Optional[SessionSummary]	None	The generated session summary
​
ParserModelResponseStartedEvent
Attribute	Type	Default	Description
event	str	"ParserModelResponseStarted"	Event type
​
ParserModelResponseCompletedEvent
Attribute	Type	Default	Description
event	str	"ParserModelResponseCompleted"	Event type
​
OutputModelResponseStartedEvent
Attribute	Type	Default	Description
event	str	"OutputModelResponseStarted"	Event type
​
OutputModelResponseCompletedEvent
Attribute	Type	Default	Description
event	str	"OutputModelResponseCompleted"	Event type
​
CustomEvent
Attribute	Type	Default	Description
event	str	"CustomEvent"	Event type

Runs
TeamRunOutput
The TeamRunOutput class represents the response from a team run, containing both the team’s overall response and individual member responses. It supports streaming and provides real-time events throughout the execution of a team.
​
TeamRunOutput Attributes
Attribute	Type	Default	Description
content	Any	None	Content of the response
content_type	str	"str"	Specifies the data type of the content
messages	List[Message]	None	A list of messages included in the response
metrics	Metrics	None	Usage metrics of the run
model	str	None	The model used in the run
model_provider	str	None	The model provider used in the run
member_responses	List[Union[TeamRunOutput, RunOutput]]	[]	Responses from individual team members
run_id	str	None	Run Id
team_id	str	None	Team Id for the run
team_name	str	None	Name of the team
session_id	str	None	Session Id for the run
parent_run_id	str	None	Parent run ID if this is a nested run
tools	List[ToolExecution]	None	List of tools provided to the model
images	List[Image]	None	List of images from member runs
videos	List[Video]	None	List of videos from member runs
audio	List[Audio]	None	List of audio snippets from member runs
files	List[File]	None	List of files from member runs
response_audio	Audio	None	The model’s raw response in audio
input	TeamRunInput	None	Input media and messages from user
reasoning_content	str	None	Any reasoning content the model produced
citations	Citations	None	Any citations used in the response
model_provider_data	Any	None	Model provider specific metadata
metadata	Dict[str, Any]	None	Additional metadata for the run
references	List[MessageReferences]	None	Message references
additional_input	List[Message]	None	Additional input messages
reasoning_steps	List[ReasoningStep]	None	Reasoning steps taken during execution
reasoning_messages	List[Message]	None	Messages related to reasoning
created_at	int	Current timestamp	Unix timestamp of the response creation
events	List[Union[RunOutputEvent, TeamRunOutputEvent]]	None	List of events that occurred during the run
status	RunStatus	RunStatus.running	Current status of the run
workflow_step_id	str	None	FK: Points to StepOutput.step_id
​
TeamRunOutputEvent Types
The following events are sent by the Team.run() function depending on the team’s configuration:
​
Core Events
Event Type	Description
TeamRunStarted	Indicates the start of a team run
TeamRunContent	Contains the model’s response text as individual chunks
TeamRunContentCompleted	Signals completion of content streaming
TeamRunIntermediateContent	Contains intermediate content during the run
TeamRunCompleted	Signals successful completion of the team run
TeamRunError	Indicates an error occurred during the team run
TeamRunCancelled	Signals that the team run was cancelled
​
Pre-Hook Events
Event Type	Description
TeamPreHookStarted	Indicates the start of a pre-run hook
TeamPreHookCompleted	Signals completion of a pre-run hook execution
​
Post-Hook Events
Event Type	Description
TeamPostHookStarted	Indicates the start of a post-run hook
TeamPostHookCompleted	Signals completion of a post-run hook execution
​
Tool Events
Event Type	Description
TeamToolCallStarted	Indicates the start of a tool call
TeamToolCallCompleted	Signals completion of a tool call, including tool call results
​
Reasoning Events
Event Type	Description
TeamReasoningStarted	Indicates the start of the team’s reasoning process
TeamReasoningStep	Contains a single step in the reasoning process
TeamReasoningCompleted	Signals completion of the reasoning process
​
Memory Events
Event Type	Description
TeamMemoryUpdateStarted	Indicates that the team is updating its memory
TeamMemoryUpdateCompleted	Signals completion of a memory update
​
Session Summary Events
Event Type	Description
TeamSessionSummaryStarted	Indicates the start of session summary generation
TeamSessionSummaryCompleted	Signals completion of session summary generation
​
Event Attributes
​
Base TeamRunOutputEvent
All events inherit from BaseTeamRunEvent which provides these common attributes:
Attribute	Type	Default	Description
created_at	int	Current timestamp	Unix timestamp of the event creation
event	str	""	The type of event
team_id	str	""	ID of the team generating the event
team_name	str	""	Name of the team generating the event
run_id	Optional[str]	None	ID of the current run
session_id	Optional[str]	None	ID of the current session
workflow_id	Optional[str]	None	ID of the workflow
workflow_run_id	Optional[str]	None	ID of the workflow’s run
step_id	Optional[str]	None	ID of the workflow step
step_name	Optional[str]	None	Name of the workflow step
step_index	Optional[int]	None	Index of the workflow step
content	Optional[Any]	None	For backwards compatibility
​
RunStartedEvent
Attribute	Type	Default	Description
event	str	"TeamRunStarted"	Event type
model	str	""	The model being used
model_provider	str	""	The provider of the model
​
IntermediateRunContentEvent
Attribute	Type	Default	Description
event	str	"TeamRunIntermediateContent"	Event type
content	Optional[Any]	None	Intermediate content of the response
content_type	str	"str"	Type of the content
​
RunContentCompletedEvent
Attribute	Type	Default	Description
event	str	"TeamRunContentCompleted"	Event type
​
RunContentEvent
Attribute	Type	Default	Description
event	str	"TeamRunContent"	Event type
content	Optional[Any]	None	The content of the response
content_type	str	"str"	Type of the content
reasoning_content	Optional[str]	None	Reasoning content produced
citations	Optional[Citations]	None	Citations used in the response
model_provider_data	Optional[Any]	None	Model provider specific metadata
response_audio	Optional[Audio]	None	Model’s audio response
image	Optional[Image]	None	Image attached to the response
references	Optional[List[MessageReferences]]	None	Message references
additional_input	Optional[List[Message]]	None	Additional input messages
reasoning_steps	Optional[List[ReasoningStep]]	None	Reasoning steps
reasoning_messages	Optional[List[Message]]	None	Reasoning messages
​
RunCompletedEvent
Attribute	Type	Default	Description
event	str	"TeamRunCompleted"	Event type
content	Optional[Any]	None	Final content of the response
content_type	str	"str"	Type of the content
reasoning_content	Optional[str]	None	Reasoning content produced
citations	Optional[Citations]	None	Citations used in the response
model_provider_data	Optional[Any]	None	Model provider specific metadata
images	Optional[List[Image]]	None	Images attached to the response
videos	Optional[List[Video]]	None	Videos attached to the response
audio	Optional[List[Audio]]	None	Audio snippets attached to the response
response_audio	Optional[Audio]	None	Model’s audio response
references	Optional[List[MessageReferences]]	None	Message references
additional_input	Optional[List[Message]]	None	Additional input messages
reasoning_steps	Optional[List[ReasoningStep]]	None	Reasoning steps
reasoning_messages	Optional[List[Message]]	None	Reasoning messages
member_responses	List[Union[TeamRunOutput, RunOutput]]	[]	Responses from individual team members
metadata	Optional[Dict[str, Any]]	None	Additional metadata
metrics	Optional[Metrics]	None	Usage metrics
​
RunErrorEvent
Attribute	Type	Default	Description
event	str	"TeamRunError"	Event type
content	Optional[str]	None	Error message
​
RunCancelledEvent
Attribute	Type	Default	Description
event	str	"TeamRunCancelled"	Event type
reason	Optional[str]	None	Reason for cancellation
​
PreHookStartedEvent
Attribute	Type	Default	Description
event	str	"TeamPreHookStarted"	Event type
pre_hook_name	Optional[str]	None	Name of the pre-hook being executed
run_input	Optional[TeamRunInput]	None	The run input passed to the hook
​
PreHookCompletedEvent
Attribute	Type	Default	Description
event	str	"TeamPreHookCompleted"	Event type
pre_hook_name	Optional[str]	None	Name of the pre-hook that completed
run_input	Optional[TeamRunInput]	None	The run input passed to the hook
​
PostHookStartedEvent
Attribute	Type	Default	Description
event	str	"TeamPostHookStarted"	Event type
post_hook_name	Optional[str]	None	Name of the post-hook being executed
​
PostHookCompletedEvent
Attribute	Type	Default	Description
event	str	"TeamPostHookCompleted"	Event type
post_hook_name	Optional[str]	None	Name of the post-hook that completed
​
ToolCallStartedEvent
Attribute	Type	Default	Description
event	str	"TeamToolCallStarted"	Event type
tool	Optional[ToolExecution]	None	The tool being called
​
ToolCallCompletedEvent
Attribute	Type	Default	Description
event	str	"TeamToolCallCompleted"	Event type
tool	Optional[ToolExecution]	None	The tool that was called
content	Optional[Any]	None	Result of the tool call
images	Optional[List[Image]]	None	Images produced by the tool
videos	Optional[List[Video]]	None	Videos produced by the tool
audio	Optional[List[Audio]]	None	Audio produced by the tool
​
ReasoningStartedEvent
Attribute	Type	Default	Description
event	str	"TeamReasoningStarted"	Event type
​
ReasoningStepEvent
Attribute	Type	Default	Description
event	str	"TeamReasoningStep"	Event type
content	Optional[Any]	None	Content of the reasoning step
content_type	str	"str"	Type of the content
reasoning_content	str	""	Detailed reasoning content
​
ReasoningCompletedEvent
Attribute	Type	Default	Description
event	str	"TeamReasoningCompleted"	Event type
content	Optional[Any]	None	Content of the reasoning step
content_type	str	"str"	Type of the content
​
MemoryUpdateStartedEvent
Attribute	Type	Default	Description
event	str	"TeamMemoryUpdateStarted"	Event type
​
MemoryUpdateCompletedEvent
Attribute	Type	Default	Description
event	str	"TeamMemoryUpdateCompleted"	Event type
​
SessionSummaryStartedEvent
Attribute	Type	Default	Description
event	str	"TeamSessionSummaryStarted"	Event type
​
SessionSummaryCompletedEvent
Attribute	Type	Default	Description
event	str	"TeamSessionSummaryCompleted"	Event type
session_summary	Optional[Any]	None	The generated session summary
​
ParserModelResponseStartedEvent
Attribute	Type	Default	Description
event	str	"TeamParserModelResponseStarted"	Event type
​
ParserModelResponseCompletedEvent
Attribute	Type	Default	Description
event	str	"TeamParserModelResponseCompleted"	Event type
​
OutputModelResponseStartedEvent
Attribute	Type	Default	Description
event	str	"TeamOutputModelResponseStarted"	Event type
​
OutputModelResponseCompletedEvent
Attribute	Type	Default	Description
event	str	"TeamOutputModelResponseCompleted"	Event type
​
CustomEvent
Attribute	Type	Default	Description
event	str	"CustomEvent"	Event type

Runs
WorkflowRunOutput
​
WorkflowRunOutput Attributes
Parameter	Type	Default	Description
content	Optional[Union[str, Dict[str, Any], List[Any], BaseModel, Any]]	None	Main content/output from the workflow execution
content_type	str	"str"	Type of the content (e.g., “str”, “json”, etc.)
workflow_id	Optional[str]	None	Unique identifier of the executed workflow
workflow_name	Optional[str]	None	Name of the executed workflow
run_id	Optional[str]	None	Unique identifier for this specific run
session_id	Optional[str]	None	Session UUID associated with this run
images	Optional[List[Image]]	None	List of image artifacts generated
videos	Optional[List[Video]]	None	List of video artifacts generated
audio	Optional[List[Audio]]	None	List of audio artifacts generated
response_audio	Optional[Audio]	None	Audio response from the workflow
step_results	List[Union[StepOutput, List[StepOutput]]]	[]	Actual step execution results as StepOutput objects
step_executor_runs	Optional[List[Union[RunOutput, TeamRunOutput]]]	None	Store agent/team responses separately with parent_run_id references
events	Optional[List[WorkflowRunOutputEvent]]	None	Events captured during workflow execution
metrics	Optional[WorkflowMetrics]	None	Workflow metrics including duration and step-level data
metadata	Optional[Dict[str, Any]]	None	Additional metadata stored with the response
created_at	int	int(time())	Unix timestamp when the response was created
status	RunStatus	RunStatus.pending	Current status of the workflow run
​
WorkflowRunOutputEvent Types and Attributes
​
BaseWorkflowRunOutputEvent Attributes
Parameter	Type	Default	Description
created_at	int	int(time())	Unix timestamp when the event was created
event	str	""	Type of the event (e.g., “WorkflowStarted”)
workflow_id	Optional[str]	None	Unique identifier of the workflow
workflow_name	Optional[str]	None	Name of the workflow
session_id	Optional[str]	None	Session UUID associated with the workflow
run_id	Optional[str]	None	Unique identifier for the workflow run
step_id	Optional[str]	None	Unique identifier for the current step
parent_step_id	Optional[str]	None	Unique identifier for the parent step (for nested steps)
​
WorkflowStartedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.workflow_started.value	Event type identifier
Inherits all fields from BaseWorkflowRunOutputEvent			
​
WorkflowCompletedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.workflow_completed.value	Event type identifier
content	Optional[Any]	None	Final output content from the workflow
content_type	str	"str"	Type of the content
step_results	List[StepOutput]	[]	List of all step execution results
metadata	Optional[Dict[str, Any]]	None	Additional metadata from workflow execution
Inherits all fields from BaseWorkflowRunOutputEvent			
​
WorkflowCancelledEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.workflow_completed.value	Event type identifier
content	Optional[Any]	None	Final output content from the workflow
content_type	str	"str"	Type of the content
step_results	List[StepOutput]	[]	List of all step execution results
metadata	Optional[Dict[str, Any]]	None	Additional metadata from workflow execution
Inherits all fields from BaseWorkflowRunOutputEvent			
​
StepStartedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.step_started.value	Event type identifier
step_name	Optional[str]	None	Name of the step being started
step_index	Optional[Union[int, tuple]]	None	Index or position of the step
Inherits all fields from BaseWorkflowRunOutputEvent			
​
StepCompletedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.step_completed.value	Event type identifier
step_name	Optional[str]	None	Name of the step that completed
step_index	Optional[Union[int, tuple]]	None	Index or position of the step
content	Optional[Any]	None	Content output from the step
content_type	str	"str"	Type of the content
images	Optional[List[Image]]	None	Image artifacts from the step
videos	Optional[List[Video]]	None	Video artifacts from the step
audio	Optional[List[Audio]]	None	Audio artifacts from the step
response_audio	Optional[Audio]	None	Audio response from the step
step_response	Optional[StepOutput]	None	Complete step execution result object
Inherits all fields from BaseWorkflowRunOutputEvent			
​
ConditionExecutionStartedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.condition_execution_started.value	Event type identifier
step_name	Optional[str]	None	Name of the condition step
step_index	Optional[Union[int, tuple]]	None	Index or position of the condition
condition_result	Optional[bool]	None	Result of the condition evaluation
Inherits all fields from BaseWorkflowRunOutputEvent			
​
ConditionExecutionCompletedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.condition_execution_completed.value	Event type identifier
step_name	Optional[str]	None	Name of the condition step
step_index	Optional[Union[int, tuple]]	None	Index or position of the condition
condition_result	Optional[bool]	None	Result of the condition evaluation
executed_steps	Optional[int]	None	Number of steps executed based on condition
step_results	List[StepOutput]	[]	Results from executed steps
Inherits all fields from BaseWorkflowRunOutputEvent			
​
ParallelExecutionStartedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.parallel_execution_started.value	Event type identifier
step_name	Optional[str]	None	Name of the parallel step
step_index	Optional[Union[int, tuple]]	None	Index or position of the parallel step
parallel_step_count	Optional[int]	None	Number of steps to execute in parallel
Inherits all fields from BaseWorkflowRunOutputEvent			
​
ParallelExecutionCompletedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.parallel_execution_completed.value	Event type identifier
step_name	Optional[str]	None	Name of the parallel step
step_index	Optional[Union[int, tuple]]	None	Index or position of the parallel step
parallel_step_count	Optional[int]	None	Number of steps executed in parallel
step_results	List[StepOutput]	field(default_factory=list)	Results from all parallel steps
Inherits all fields from BaseWorkflowRunOutputEvent			
​
LoopExecutionStartedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.loop_execution_started.value	Event type identifier
step_name	Optional[str]	None	Name of the loop step
step_index	Optional[Union[int, tuple]]	None	Index or position of the loop
max_iterations	Optional[int]	None	Maximum number of iterations allowed
Inherits all fields from BaseWorkflowRunOutputEvent			
​
LoopIterationStartedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.loop_iteration_started.value	Event type identifier
step_name	Optional[str]	None	Name of the loop step
step_index	Optional[Union[int, tuple]]	None	Index or position of the loop
iteration	int	0	Current iteration number
max_iterations	Optional[int]	None	Maximum number of iterations allowed
Inherits all fields from BaseWorkflowRunOutputEvent			
​
LoopIterationCompletedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.loop_iteration_completed.value	Event type identifier
step_name	Optional[str]	None	Name of the loop step
step_index	Optional[Union[int, tuple]]	None	Index or position of the loop
iteration	int	0	Current iteration number
max_iterations	Optional[int]	None	Maximum number of iterations allowed
iteration_results	List[StepOutput]	[]	Results from this iteration
should_continue	bool	True	Whether the loop should continue
Inherits all fields from BaseWorkflowRunOutputEvent			
​
LoopExecutionCompletedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.loop_execution_completed.value	Event type identifier
step_name	Optional[str]	None	Name of the loop step
step_index	Optional[Union[int, tuple]]	None	Index or position of the loop
total_iterations	int	0	Total number of iterations completed
max_iterations	Optional[int]	None	Maximum number of iterations allowed
all_results	List[List[StepOutput]]	[]	Results from all iterations
Inherits all fields from BaseWorkflowRunOutputEvent			
​
RouterExecutionStartedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.router_execution_started.value	Event type identifier
step_name	Optional[str]	None	Name of the router step
step_index	Optional[Union[int, tuple]]	None	Index or position of the router
selected_steps	List[str]	field(default_factory=list)	Names of steps selected by the router
Inherits all fields from BaseWorkflowRunOutputEvent			
​
RouterExecutionCompletedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.router_execution_completed.value	Event type identifier
step_name	Optional[str]	None	Name of the router step
step_index	Optional[Union[int, tuple]]	None	Index or position of the router
selected_steps	List[str]	field(default_factory=list)	Names of steps that were selected
executed_steps	Optional[int]	None	Number of steps executed
step_results	List[StepOutput]	field(default_factory=list)	Results from executed steps
Inherits all fields from BaseWorkflowRunOutputEvent			
​
StepsExecutionStartedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.steps_execution_started.value	Event type identifier
step_name	Optional[str]	None	Name of the steps group
step_index	Optional[Union[int, tuple]]	None	Index or position of the steps group
steps_count	Optional[int]	None	Number of steps in the group
Inherits all fields from BaseWorkflowRunOutputEvent			
​
StepsExecutionCompletedEvent Attributes
Parameter	Type	Default	Description
event	str	WorkflowRunEvent.steps_execution_completed.value	Event type identifier
step_name	Optional[str]	None	Name of the steps group
step_index	Optional[Union[int, tuple]]	None	Index or position of the steps group
steps_count	Optional[int]	None	Number of steps in the group
executed_steps	Optional[int]	None	Number of steps actually executed
step_results	List[StepOutput]	field(default_factory=list)	Results from all executed steps
Inherits all fields from BaseWorkflowRunOutputEvent			
​
StepOutputEvent Attributes
Parameter	Type	Default	Description
event	str	"StepOutput"	Event type identifier
step_name	Optional[str]	None	Name of the step that produced output
step_index	Optional[Union[int, tuple]]	None	Index or position of the step
step_output	Optional[StepOutput]	None	Complete step execution result
Inherits all fields from BaseWorkflowRunOutputEvent			
Properties (read-only):			
content	Optional[Union[str, Dict[str, Any], List[Any], BaseModel, Any]]	-	Content from the step output
images	Optional[List[Image]]	-	Images from the step output
videos	Optional[List[Video]]	-	Videos from the step output
audio	Optional[List[Audio]]	-	Audio from the step output
success	bool	-	Whether the step succeeded
error	Optional[str]	-	Error message if step failed
stop	bool	-	Whether the step requested early termination
​
WorkflowMetrics
Parameter	Type	Default	Description
steps	Dict[str, StepMetrics]	-	Step-level metrics mapped by step name
duration	Optional[float]	None	Total workflow execution time in seconds
​
StepMetrics
Parameter	Type	Default	Description
step_name	str	-	Name of the step
executor_type	str	-	Type of executor (“agent”, “team”, or “function”)
executor_name	str	-	Name of the executor
metrics	Optional[Metrics]	None	Execution metrics (duration, tokens, model usage)

Runs
RunContext
The RunContext is an object that can be referenced in pre- and post-hooks, tools, and other parts of the run. See Agent State for examples of how to use the RunContext in your code.
​
RunContext Attributes
Attribute	Type	Description
run_id	str	Run ID
session_id	str	Session ID for the run
user_id	Optional[str]	User ID associated with the run
dependencies	Dict[str, Any]	Dependencies for the run
knowledge_filters	Dict[str, Any]	Knowledge filters for the run
metadata	Dict[str, Any]	Metadata associated with the run
session_state	Dict[str, Any]	Session state for the run

Sessions
SessionSummaryManager
The SessionSummaryManager is responsible for generating and managing session summaries. It uses a model to analyze conversations and create concise summaries with optional topic extraction.
​
SessionSummaryManager Attributes
Parameter	Type	Default	Description
model	Optional[Model]	None	Model used for session summary generation
session_summary_prompt	Optional[str]	None	Custom prompt for session summary generation. If not provided, uses default prompt
summary_request_message	str	"Provide the summary of the conversation."	User message prompt for requesting the summary
summaries_updated	bool	False	Whether session summaries were created in the last run
​
SessionSummaryManager Methods
​
create_session_summary(session: Union[AgentSession, TeamSession]) -> Optional[SessionSummary]
Creates a summary of the session synchronously. Parameters:

    session: The agent or team session to summarize

Returns:

    Optional[SessionSummary]: A SessionSummary object containing the summary text, topics, and timestamp, or None if generation fails

​
acreate_session_summary(session: Union[AgentSession, TeamSession]) -> Optional[SessionSummary]
Creates a summary of the session asynchronously. Parameters:

    session: The agent or team session to summarize

Returns:

    Optional[SessionSummary]: A SessionSummary object containing the summary text, topics, and timestamp, or None if generation fails

​
SessionSummary Object
The SessionSummary object returned by the summary manager contains:
Attribute	Type	Description
summary	str	Concise summary of the session focusing on important information
topics	Optional[List[str]]	List of topics discussed in the session
updated_at	Optional[datetime]	Timestamp when the summary was created

Sessions
AgentSession
​
AgentSession Attributes
Parameter	Type	Default	Description
session_id	str	Required	Session UUID
agent_id	Optional[str]	None	ID of the agent that this session is associated with
team_id	Optional[str]	None	ID of the team that this session is associated with
user_id	Optional[str]	None	ID of the user interacting with this agent
workflow_id	Optional[str]	None	ID of the workflow that this session is associated with
session_data	Optional[Dict[str, Any]]	None	Session Data: session_name, session_state, images, videos, audio
metadata	Optional[Dict[str, Any]]	None	Metadata stored with this agent
agent_data	Optional[Dict[str, Any]]	None	Agent Data: agent_id, name and model
runs	Optional[List[RunOutput]]	None	List of all runs in the session
summary	Optional[SessionSummary]	None	Summary of the session
created_at	Optional[int]	None	The unix timestamp when this session was created
updated_at	Optional[int]	None	The unix timestamp when this session was last updated
​
AgentSession Methods
​
upsert_run(run: RunOutput)
Adds a RunOutput to the runs list. If a run with the same run_id already exists, it updates the existing run.
​
get_run(run_id: str) -> Optional[RunOutput]
Retrieves a specific run by its run_id.
​
get_messages(...) -> List[Message]
Returns the messages belonging to the session that fit the given criteria. Parameters:

    agent_id (Optional[str]): The id of the agent to get the messages from
    team_id (Optional[str]): The id of the team to get the messages from
    last_n_runs (Optional[int]): The number of runs to return messages from, counting from the latest. Defaults to all runs
    limit (Optional[int]): The number of messages to return, counting from the latest. Defaults to all messages
    skip_roles (Optional[List[str]]): Skip messages with these roles
    skip_statuses (Optional[List[RunStatus]]): Skip messages with these statuses
    skip_history_messages (bool): Skip messages that were tagged as history in previous runs. Defaults to True

Returns:

    List[Message]: The messages for the session

​
get_session_summary() -> Optional[SessionSummary]
Get the session summary for the session
​
get_chat_history(...) -> List[Message]
Get the chat history (user and assistant messages) for the session. Use get_messages() for more filtering options. Parameters:

    last_n_runs (Optional[int]): Number of recent runs to include. If None, all runs will be considered

Returns:

    List[Message]: The chat history for the session


Sessions
Team Session
​
TeamSession Attributes
Parameter	Type	Default	Description
session_id	str	Required	Session UUID
team_id	Optional[str]	None	ID of the team that this session is associated with
user_id	Optional[str]	None	ID of the user interacting with this team
workflow_id	Optional[str]	None	ID of the workflow that this session is associated with
team_data	Optional[Dict[str, Any]]	None	Team Data: name, team_id, model, and mode
session_data	Optional[Dict[str, Any]]	None	Session Data: session_state, images, videos, audio
metadata	Optional[Dict[str, Any]]	None	Metadata stored with this team
runs	Optional[List[Union[TeamRunOutput, RunOutput]]]	None	List of all runs in the session
summary	Optional[SessionSummary]	None	Summary of the session
created_at	Optional[int]	None	The unix timestamp when this session was created
updated_at	Optional[int]	None	The unix timestamp when this session was last updated
​
TeamSession Methods
​
upsert_run(run: TeamRunOutput)
Adds a TeamRunOutput to the runs list. If a run with the same run_id already exists, it updates the existing run.
​
get_run(run_id: str) -> Optional[RunOutput]
Retrieves a specific run by its run_id.
​
get_messages(...) -> List[Message]
Returns the messages belonging to the session that fit the given criteria. Parameters:

    team_id (Optional[str]): The id of the team to get the messages from
    member_ids (Optional[List[str]]): The ids of the members to get the messages from
    last_n_runs (Optional[int]): The number of runs to return messages from, counting from the latest. Defaults to all runs
    limit (Optional[int]): The number of messages to return, counting from the latest. Defaults to all messages
    skip_roles (Optional[List[str]]): Skip messages with these roles
    skip_statuses (Optional[List[RunStatus]]): Skip messages with these statuses
    skip_history_messages (bool): Skip messages that were tagged as history in previous runs. Defaults to True
    skip_member_messages (bool): Skip messages created by members of the team. Defaults to True

Returns:

    List[Message]: The messages for the session

​
get_session_summary() -> Optional[SessionSummary]
Get the session summary for the session
​
get_chat_history(last_n_runs: Optional[int] = None) -> List[Message]
Get the chat history (user and assistant messages) for the session. Use get_messages() for more filtering options. Parameters:

    last_n_runs (Optional[int]): Number of recent runs to include. If None, all runs will be considered

Returns:

    List[Message]: The chat history for the session

Sessions
WorkflowSession
​
WorkflowSession Attributes
Parameter	Type	Default	Description
session_id	str	Required	Session UUID - this is the workflow_session_id that gets set on agents/teams
user_id	Optional[str]	None	ID of the user interacting with this workflow
workflow_id	Optional[str]	None	ID of the workflow that this session is associated with
workflow_name	Optional[str]	None	Workflow name
runs	Optional[List[WorkflowRunOutput]]	None	List of all workflow runs in the session
session_data	Optional[Dict[str, Any]]	None	Session Data: session_name, session_state, images, videos, audio
workflow_data	Optional[Dict[str, Any]]	None	Workflow configuration and metadata
metadata	Optional[Dict[str, Any]]	None	Metadata stored with this workflow session
created_at	Optional[int]	None	The unix timestamp when this session was created
updated_at	Optional[int]	None	The unix timestamp when this session was last updated
​
WorkflowSession Methods
​
upsert_run(run: WorkflowRunOutput)
Adds a WorkflowRunOutput to the runs list. If a run with the same run_id already exists, it updates the existing run.
​
get_run(run_id: str) -> Optional[WorkflowRunOutput]
Retrieves a specific workflow run by its run_id.
​
get_workflow_history(num_runs: Optional[int] = None) -> List[Tuple[str, str]]
Gets workflow history as structured data (input, response pairs).

    num_runs: Number of recent runs to include. If None, returns all available history.

Returns a list of tuples containing (input, response) pairs from completed workflow runs only.
​
get_workflow_history_context(num_runs: Optional[int] = None) -> Optional[str]
Gets formatted workflow history context for steps.

    num_runs: Number of recent runs to include. If None, returns all available history.

Returns a formatted string containing the workflow history wrapped in <workflow_history_context> tags, suitable for providing context to workflow steps.
​
get_messages(...) -> List[Message]
Returns the messages belonging to the session that fit the given criteria. Note: Either agent_id or team_id must be provided, but not both. Parameters:

    agent_id (Optional[str]): The ID of the agent to get the messages for
    team_id (Optional[str]): The ID of the team to get the messages for
    last_n_runs (Optional[int]): The number of runs to return messages from, counting from the latest. Defaults to all runs
    limit (Optional[int]): The number of messages to return, counting from the latest. Defaults to all messages
    skip_roles (Optional[List[str]]): Skip messages with these roles
    skip_statuses (Optional[List[RunStatus]]): Skip messages with these statuses
    skip_history_messages (bool): Skip messages that were tagged as history in previous runs. Defaults to True
    skip_member_messages (bool): Skip messages created by members of the team. Defaults to True

Returns:

    List[Message]: The messages for the session

​
get_chat_history(last_n_runs: Optional[int] = None) -> List[WorkflowChatInteraction]
Return a list of WorkflowChatInteraction objects containing the input and output for each run in the session. Parameters:

    last_n_runs (Optional[int]): Number of recent runs to include. If None, all runs will be considered

Returns:

    List[WorkflowChatInteraction]: The chat history for the session as a list of input/output interactions

​
to_dict() -> Dict[str, Any]
Converts the WorkflowSession to a dictionary for storage, serializing runs to dictionaries.
​
from_dict(data: Mapping[str, Any]) -> Optional[WorkflowSession]
Creates a WorkflowSession from a dictionary, deserializing runs from dictionaries back to WorkflowRunOutput objects.

Memory
Memory Manager
Memory is a class that manages conversation history, session summaries, and long-term user memories for AI agents. It provides comprehensive memory management capabilities including adding new memories, searching memories, and deleting memories.
​
MemoryManager
The MemoryManager class is responsible for managing user memories, including creating, retrieving, updating, and deleting memories.
​
Constructor Parameters
Parameter	Type	Description	Default
model	Optional[Model]	Model used for memory operations	None
system_message	Optional[str]	Custom system prompt for the memory manager	None
memory_capture_instructions	Optional[str]	Custom instructions for memory creation and filtering	None
additional_instructions	Optional[str]	Additional instructions added to the system message	None
db	Optional[BaseDb]	Database for storing memories	None
debug_mode	bool	Whether to enable debug logging	False
​
Key Methods
​
User Memory Management
Method	Description	Parameters	Returns
get_user_memories	Retrieves all memories for a user	user_id: Optional[str] = None	Optional[List[UserMemory]]
get_user_memory	Gets a specific memory by ID	memory_id: str, user_id: Optional[str] = None	Optional[UserMemory]
add_user_memory	Adds a new memory and returns the memory ID	memory: UserMemory, user_id: Optional[str] = None	Optional[str]
replace_user_memory	Updates an existing memory and returns the memory ID	memory_id: str, memory: UserMemory, user_id: Optional[str] = None	Optional[str]
delete_user_memory	Deletes a memory by ID	memory_id: str, user_id: Optional[str] = None	None
clear	Clears all memories from the database	None	None
​
Memory Creation and Search
Method	Description	Parameters	Returns
create_user_memories	Creates memories from text or messages	message: Optional[str] = None, messages: Optional[List[Message]] = None, agent_id: Optional[str] = None, team_id: Optional[str] = None, user_id: Optional[str] = None	str
acreate_user_memories	Creates memories from text or messages (Async)	message: Optional[str] = None, messages: Optional[List[Message]] = None, agent_id: Optional[str] = None, team_id: Optional[str] = None, user_id: Optional[str] = None	str
search_user_memories	Searches user memories using specified retrieval method	query: Optional[str] = None, limit: Optional[int] = None, retrieval_method: Optional[Literal["last_n", "first_n", "agentic"]] = None, user_id: Optional[str] = None	List[UserMemory]
​
Memory Task Management
Method	Description	Parameters	Returns
update_memory_task	Updates memories based on a task description	task: str, user_id: Optional[str] = None	str
aupdate_memory_task	Updates memories based on a task description (Async)	task: str, user_id: Optional[str] = None	str
​
Utility Methods
Method	Description	Parameters	Returns
initialize	Initializes the memory manager	user_id: Optional[str] = None	None
read_from_db	Reads memories from the database	user_id: Optional[str] = None	Optional[Dict[str, List[UserMemory]]]
​
Retrieval Methods
The search_user_memories method supports the following retrieval methods:

    last_n: Returns the most recent memories
    first_n: Returns the oldest memories
    agentic: Returns memories most similar to the query using an AI-powered semantic search

Context Compression
CompressionManager
The CompressionManager is responsible for compressing tool call results to save context space while preserving critical information.
​
CompressionManager Attributes
Parameter	Type	Default	Description
model	Optional[Model]	None	Model used for compression
compress_tool_results	bool	True	Flag to enable tool result compression
compress_tool_results_limit	Optional[int]	None	Number of uncompressed tool results before compression triggers.
compress_token_limit	Optional[int]	None	Number of tokens before compression triggers.
compress_tool_call_instructions	Optional[str]	None	Custom prompt for compression. If not provided, uses the default compression prompt
stats	Dict[str, Any]	{}	Tracks compression statistics
​
CompressionManager Methods
​
should_compress(messages, tools, model) -> bool
Checks whether compression should be triggered based on configured thresholds. Parameters:

    messages: List of messages to check
    tools: Optional list of tools for token counting
    model: The Agent/Team model

Returns:

    bool: True if either threshold is met

​
ashould_compress(messages, tools, model) -> bool
Checks whether compression should be triggered based on configured thresholds asynchronously. Parameters:

    messages: List of messages to check
    tools: Optional list of tools for token counting
    model: The Agent/Team model

Returns:

    bool: True if either threshold is met

​
compress(messages: List[Message]) -> None
Compresses all uncompressed tool results. Parameters:

    messages: List of messages containing tool results to compress

Returns:

    None: Modifies messages in place, setting compressed_content on each tool message

​
acompress(messages: List[Message]) -> None
Compresses all uncompressed tool results asynchronously. Parameters:

    messages: List of messages containing tool results to compress

Returns:

    None: Modifies messages in place, setting compressed_content on each tool message

Database
PostgresDb
PostgresDb is a class that implements the Db interface using PostgreSQL as the backend storage system. It provides robust, relational storage for agent sessions with support for JSONB data types, schema versioning, and efficient querying.
Parameter	Type	Default	Description
db_url	Optional[str]	-	The database URL to connect to.
db_engine	Optional[Engine]	-	The SQLAlchemy database engine to use.
db_schema	Optional[str]	-	The database schema to use.
session_table	Optional[str]	-	Name of the table to store Agent, Team and Workflow sessions.
memory_table	Optional[str]	-	Name of the table to store memories.
metrics_table	Optional[str]	-	Name of the table to store metrics.
eval_table	Optional[str]	-	Name of the table to store evaluation runs data.
knowledge_table	Optional[str]	-	Name of the table to store knowledge content.
​
Methods
​
upsert_sessions
Bulk upsert multiple sessions for improved performance on large datasets. Parameters:

    sessions (List[Session]): List of sessions to upsert
    deserialize (Optional[bool]): Whether to deserialize the sessions. Defaults to True

Returns: List[Union[Session, Dict[str, Any]]]
​
upsert_memories
Bulk upsert multiple memories for improved performance on large datasets. Parameters:

    memories (List[UserMemory]): List of memories to upsert
    deserialize (Optional[bool]): Whether to deserialize the memories. Defaults to True

Returns: List[Union[UserMemory, Dict[str, Any]]]

Database
RedisDb
RedisDb is a class that implements the Db interface using Redis as the backend storage system. It provides high-performance, distributed storage for agent sessions with support for JSON data types and schema versioning.
Parameter	Type	Default	Description
redis_client	Optional[Redis]	-	Redis client instance to use. If not provided a new client will be created.
db_url	Optional[str]	-	Redis connection URL (e.g., "redis://localhost:6379/0" or "rediss://user:pass@host:port/db")
db_prefix	str	"agno"	Prefix for all Redis keys.
expire	Optional[int]	-	TTL for Redis keys in seconds.
session_table	Optional[str]	-	Name of the table to store sessions.
memory_table	Optional[str]	-	Name of the table to store memories.
metrics_table	Optional[str]	-	Name of the table to store metrics.
eval_table	Optional[str]	-	Name of the table to store evaluation runs.
knowledge_table	Optional[str]	-	Name of the table to store knowledge documents.
​
Methods
​
upsert_sessions
Bulk upsert multiple sessions for improved performance on large datasets. Parameters:

    sessions (List[Session]): List of sessions to upsert
    deserialize (Optional[bool]): Whether to deserialize the sessions. Defaults to True

Returns: List[Union[Session, Dict[str, Any]]]
​
upsert_memories
Bulk upsert multiple memories for improved performance on large datasets. Parameters:

    memories (List[UserMemory]): List of memories to upsert
    deserialize (Optional[bool]): Whether to deserialize the memories. Defaults to True

Returns: List[Union[UserMemory, Dict[str, Any]]]

Database
MigrationManager

API reference for the MigrationManager class used to handle database migrations.
The MigrationManager class provides a programmatic way to manage database schema migrations for Agno database tables.
​
Constructor

MigrationManager(db: Union[AsyncBaseDb, BaseDb])

​
Parameters
​
db
Union[AsyncBaseDb, BaseDb]
required
The database instance to run migrations on. Supports both synchronous and asynchronous database classes.
​
Properties
​
latest_schema_version
Version
Returns the latest available schema version from the migration versions list.
​
available_versions
list[tuple[str, Version]]
A list of available migration versions as tuples of (version_string, parsed_version).Currently available versions:

    v2_0_0 (2.0.0)
    v2_3_0 (2.3.0)

​
Methods
​
up()
Executes upgrade migrations to bring database tables to a target schema version.

async def up(
    target_version: Optional[str] = None,
    table_type: Optional[str] = None,
    force: bool = False
)

​
Parameters
​
target_version
str
The version to migrate to (e.g., “2.3.0”). If not provided, migrates to the latest available version.
​
table_type
str
The specific table type to migrate. If not provided, all tables will be migrated.Valid values: "memory", "session", "metrics", "eval", "knowledge", "culture"
​
force
bool
default:"False"
Force the migration even if the current version is equal to or greater than the target version.
​
Example

import asyncio
from agno.db.migrations import MigrationManager
from agno.db.postgres import AsyncPostgresDb

db = AsyncPostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

async def run_migrations():
    # Migrate all tables to latest version
    await MigrationManager(db).up()
    
    # Migrate specific table to specific version
    await MigrationManager(db).up(
        target_version="2.3.0",
        table_type="memory"
    )
    
    # Force migration
    await MigrationManager(db).up(
        table_type="session",
        force=True
    )

if __name__ == "__main__":
    asyncio.run(run_migrations())

​
down()
Executes downgrade migrations to revert database tables to a target schema version.

async def down(
    target_version: str,
    table_type: Optional[str] = None,
    force: bool = False
)

​
Parameters
​
target_version
str
required
The version to migrate down to (e.g., “2.0.0”). This parameter is required for down migrations.
​
table_type
str
The specific table type to migrate. If not provided, all tables will be migrated.Valid values: "memory", "session", "metrics", "eval", "knowledge", "culture"
​
force
bool
default:"False"
Force the migration even if the current version is equal to or less than the target version.
​
Example

import asyncio
from agno.db.migrations import MigrationManager
from agno.db.postgres import AsyncPostgresDb

db = AsyncPostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

async def revert_migrations():
    # Revert all tables to version 2.0.0
    await MigrationManager(db).down(target_version="2.0.0")
    
    # Revert specific table
    await MigrationManager(db).down(
        target_version="2.0.0",
        table_type="memory"
    )

if __name__ == "__main__":
    asyncio.run(revert_migrations())

​
Supported Databases
The MigrationManager supports the following database types:

    PostgreSQL (via PostgresDb or AsyncPostgresDb)
    SQLite (via SqliteDb or AsyncSqliteDb)
    MySQL (via MySQLDb)
    SingleStore (via SingleStoreDb)

​
Table Types
The following table types can be migrated:
Table Type	Description
memory	Agent memory storage
session	Agent session data
metrics	Performance and usage metrics
eval	Evaluation results
knowledge	Knowledge base entries
culture	Culture and behavior data

Tracing
Trace
A Trace represents one complete agent execution from start to finish. Each trace has a unique trace_id that groups all related spans together.
​
Trace Attributes
Attribute	Type	Default	Description
trace_id	str	Required	Unique trace identifier
name	str	Required	Trace name (typically the root span name, e.g., Agent.run)
status	str	Required	Overall status: OK, ERROR, or UNSET
duration_ms	int	Required	Total execution time in milliseconds
start_time	datetime	Required	When the trace started
end_time	datetime	Required	When the trace completed
total_spans	int	0	Total number of spans in this trace
error_count	int	0	Number of spans that errored
run_id	Optional[str]	None	Associated agent/team/workflow run ID
session_id	Optional[str]	None	Associated session ID
user_id	Optional[str]	None	Associated user ID
agent_id	Optional[str]	None	Associated agent ID
team_id	Optional[str]	None	Associated team ID
workflow_id	Optional[str]	None	Associated workflow ID
created_at	datetime	Required	When the trace record was created
​
Methods
​
to_dict()
Convert the trace to a dictionary.

trace_dict = trace.to_dict()

Returns: dict
​
from_dict()
Create a trace from a dictionary.

trace = Trace.from_dict(data)

Parameters:

    data (dict): Dictionary containing trace data

Returns: Trace
​
Usage

from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file="tmp/traces.db")

# Get a trace
trace = db.get_trace(run_id=response.run_id)

if trace:
    print(f"Trace ID: {trace.trace_id}")
    print(f"Name: {trace.name}")
    print(f"Duration: {trace.duration_ms}ms")
    print(f"Status: {trace.status}")
    print(f"Total Spans: {trace.total_spans}")
    print(f"Errors: {trace.error_count}")

Tracing
Span
A Span represents a single operation within an agent execution. Spans form a parent-child hierarchy within a trace, allowing you to understand the execution flow.
​
Span Attributes
Attribute	Type	Default	Description
span_id	str	Required	Unique span identifier
trace_id	str	Required	Parent trace ID (groups related spans)
parent_span_id	Optional[str]	None	Parent span ID (None for root spans)
name	str	Required	Operation name (e.g., OpenAIChat.invoke, get_weather)
status_code	str	Required	Status: OK, ERROR, or UNSET
status_message	Optional[str]	None	Status message (typically error details)
duration_ms	int	Required	Execution time in milliseconds
start_time	datetime	Required	When the span started
end_time	datetime	Required	When the span completed
attributes	Optional[dict]	None	OpenTelemetry attributes (tokens, params, etc.)
events	Optional[list]	None	Span events
kind	Optional[str]	None	Span kind (e.g., INTERNAL, CLIENT)
​
Common Span Names
Spans are automatically created for various operations:
Span Name Pattern	Description
{AgentName}.run	Agent execution
{TeamName}.run	Team execution
{ModelName}.invoke	LLM model call
{tool_name}	Tool execution
​
Attributes by Operation Type
The attributes field contains OpenTelemetry semantic attributes that vary by operation:
​
LLM Spans
Attribute	Description
llm.token_count.prompt	Input token count
llm.token_count.completion	Output token count
llm.model_name	Model identifier
llm.provider	Model provider name
​
Tool Spans
Attribute	Description
tool.name	Tool function name
tool.parameters	Tool input parameters (JSON)
​
Methods
​
to_dict()
Convert the span to a dictionary.

span_dict = span.to_dict()

Returns: dict
​
from_dict()
Create a span from a dictionary.

span = Span.from_dict(data)

Parameters:

    data (dict): Dictionary containing span data

Returns: Span
​
Usage

from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file="tmp/traces.db")

# Get all spans for a trace
spans = db.get_spans(trace_id=trace.trace_id)

for span in spans:
    print(f"Span: {span.name}")
    print(f"  Duration: {span.duration_ms}ms")
    print(f"  Status: {span.status_code}")
    
    # Check for token usage (LLM spans)
    if span.attributes:
        tokens = span.attributes.get("llm.token_count.completion")
        if tokens:
            print(f"  Tokens: {tokens}")

​
Building a Span Tree

def print_span_tree(spans, parent_id=None, indent=0):
    """Recursively print spans as a tree."""
    for span in spans:
        if span.parent_span_id == parent_id:
            prefix = "  " * indent + ("└─ " if indent > 0 else "")
            print(f"{prefix}{span.name} ({span.duration_ms}ms)")
            print_span_tree(spans, span.span_id, indent + 1)

# Get spans and print tree
spans = db.get_spans(trace_id=trace.trace_id)
print_span_tree(spans)

Hooks
Pre-hooks
​
Parameters
Running a pre-hook is handled automatically during the Agent or Team run. These are the parameters that will be injected:
Parameter	Type	Default	Description
agent	Agent	Required	The Agent that is running the pre-hook. Only present in Agent runs.
team	Team	Required	The Team that is running the pre-hook. Only present in Team runs.
run_input	RunInput	Required	The input provided to the Agent or Team when invoking the run.
session	AgentSession	Required	The AgentSession or TeamSession object representing the current session.
session_state	Optional[Dict[str, Any]]	None	The session state of the current session.
dependencies	Optional[Dict[str, Any]]	None	The dependencies of the current run.
metadata	Optional[Dict[str, Any]]	None	The metadata of the current run.
user_id	Optional[str]	None	The contextual user ID, if any.
debug_mode	Optional[bool]	None	Whether the debug mode is enabled.

Hooks
Post-hooks
​
Parameters
Running a post-hook is handled automatically during the Agent or Team run. These are the parameters that will be injected:
Parameter	Type	Default	Description
agent	Agent	Required	The Agent that is running the post-hook. Only present in Agent runs.
team	Team	Required	The Team that is running the post-hook. Only present in Team runs.
run_output	RunOutput or TeamRunOutput	Required	The output of the current Agent or Team run.
session	AgentSession	Required	The AgentSession or TeamSession object representing the current session.
session_state	Optional[Dict[str, Any]]	None	The session state of the current session.
dependencies	Optional[Dict[str, Any]]	None	The dependencies of the current run.
metadata	Optional[Dict[str, Any]]	None	The metadata of the current run.
user_id	Optional[str]	None	The contextual user ID, if any.
debug_mode	Optional[bool]	None	Whether the debug mode is enabled.

Guardrails
BaseGuardrail
​
Methods
​
check
Perform the guardrail checks synchronously. Parameters:

    run_input (RunInput | TeamRunInput): The input provided to the Agent or Team when invoking the run.

Returns: None
​
async_check
Perform the guardrail checks asynchronously. Parameters:

    run_input (RunInput | TeamRunInput): The input provided to the Agent or Team when invoking the run.

Returns: None

Guardrails
OpenAIModerationGuardrail
​
Parameters
Parameter	Type	Default	Description
moderation_model	str	"omni-moderation-latest"	The model to use for moderation.
raise_for_categories	List[str]	None	The categories to raise for.
api_key	str	None	The API key to use for moderation. Defaults to the OPENAI_API_KEY environment variable.

Models
Model
The Model class is the base class for all models in Agno. It provides common functionality and parameters that are inherited by specific model implementations like OpenAIChat, Claude, etc.
​
Parameters
Parameter	Type	Default	Description
id	str	Required	The id/name of the model to use
name	Optional[str]	None	The display name of the model
provider	Optional[str]	None	The provider of the model
frequency_penalty	Optional[float]	None	Penalizes new tokens based on their frequency in the text so far
presence_penalty	Optional[float]	None	Penalizes new tokens based on whether they appear in the text so far
response_format	Optional[str]	None	The format of the response
seed	Optional[int]	None	Random seed for deterministic sampling
stop	Optional[Union[str, List[str]]]	None	Up to 4 sequences where the API will stop generating further tokens
stream	bool	True	Whether to stream the response
temperature	Optional[float]	None	Controls randomness in the model’s output
top_p	Optional[float]	None	Controls diversity via nucleus sampling
max_tokens	Optional[int]	None	Maximum number of tokens to generate
request_params	Optional[Dict[str, Any]]	None	Additional parameters to include in the request
cache_response	bool	False	Enable caching of model responses to avoid redundant API calls
cache_ttl	Optional[int]	None	Time-to-live for cached model responses, in seconds. If None, cache never expires
cache_dir	Optional[str]	None	Directory path for storing cached model responses. If None, uses default cache location
retries	int	0	Number of retries to attempt before raising a ModelProviderError
delay_between_retries	int	1	Delay between retries, in seconds
exponential_backoff	bool	False	If True, the delay between retries is doubled each time

Models
OpenAI
The OpenAIChat model provides access to OpenAI models like GPT-4o.
​
Parameters
Parameter	Type	Default	Description
id	str	"gpt-4o"	The id of the OpenAI model to use
name	str	"OpenAIChat"	The name of the model
provider	str	"OpenAI"	The provider of the model
store	Optional[bool]	None	Whether to store the conversation for training purposes
reasoning_effort	Optional[str]	None	The reasoning effort level for o1 models (“low”, “medium”, “high”)
verbosity	Optional[Literal["low", "medium", "high"]]	None	Controls verbosity level of reasoning models
metadata	Optional[Dict[str, Any]]	None	Developer-defined metadata to associate with the completion
frequency_penalty	Optional[float]	None	Penalizes new tokens based on their frequency in the text so far (-2.0 to 2.0)
logit_bias	Optional[Any]	None	Modifies the likelihood of specified tokens appearing in the completion
logprobs	Optional[bool]	None	Whether to return log probabilities of the output tokens
top_logprobs	Optional[int]	None	Number of most likely tokens to return log probabilities for (0 to 20)
max_tokens	Optional[int]	None	Maximum number of tokens to generate (deprecated, use max_completion_tokens)
max_completion_tokens	Optional[int]	None	Maximum number of completion tokens to generate
modalities	Optional[List[str]]	None	List of modalities to use (“text” and/or “audio”)
audio	Optional[Dict[str, Any]]	None	Audio configuration (e.g., {"voice": "alloy", "format": "wav"})
presence_penalty	Optional[float]	None	Penalizes new tokens based on whether they appear in the text so far (-2.0 to 2.0)
seed	Optional[int]	None	Random seed for deterministic sampling
stop	Optional[Union[str, List[str]]]	None	Up to 4 sequences where the API will stop generating further tokens
temperature	Optional[float]	None	Controls randomness in the model’s output (0.0 to 2.0)
user	Optional[str]	None	A unique identifier representing your end-user
top_p	Optional[float]	None	Controls diversity via nucleus sampling (0.0 to 1.0)
service_tier	Optional[str]	None	Service tier to use (“auto”, “default”, “flex”, “priority”)
strict_output	bool	True	Controls schema adherence for structured outputs
extra_headers	Optional[Any]	None	Additional headers to include in requests
extra_query	Optional[Any]	None	Additional query parameters to include in requests
extra_body	Optional[Any]	None	Additional body parameters to include in requests
request_params	Optional[Dict[str, Any]]	None	Additional parameters to include in the request
role_map	Optional[Dict[str, str]]	None	Mapping of message roles to OpenAI roles
api_key	Optional[str]	None	The API key for authenticating with OpenAI (defaults to OPENAI_API_KEY env var)
organization	Optional[str]	None	The organization ID to use for requests
base_url	Optional[Union[str, httpx.URL]]	None	The base URL for the OpenAI API
timeout	Optional[float]	None	Request timeout in seconds
max_retries	Optional[int]	None	Maximum number of retries for failed requests
default_headers	Optional[Any]	None	Default headers to include in all requests
default_query	Optional[Any]	None	Default query parameters to include in all requests
http_client	Optional[Union[httpx.Client, httpx.AsyncClient]]	None	HTTP client instance for making requests
client_params	Optional[Dict[str, Any]]	None	Additional parameters for client configuration
retries	int	0	Number of retries to attempt before raising a ModelProviderError
delay_between_retries	int	1	Delay between retries, in seconds
exponential_backoff	bool	False	If True, the delay between retries is doubled each time

Models
AI/ML API
The AI/ML API provider gives unified access to over 300+ AI models, including Deepseek, Gemini, ChatGPT, and others, via a single standardized interface. The models run with enterprise-grade rate limits and uptime, and are ideal for production use. You can sign up at aimlapi.com and view full provider documentation at docs.aimlapi.com.
​
Parameters
Parameter	Type	Default	Description
id	str	"gpt-4o-mini"	The id of the model to use
name	str	"AIMLAPI"	The name of the model
provider	str	"AIMLAPI"	The provider of the model
api_key	Optional[str]	None	The API key for AI/ML API (defaults to AIMLAPI_API_KEY env var)
base_url	str	"https://api.aimlapi.com/v1"	The base URL for the AI/ML API
max_tokens	int	4096	Maximum number of tokens to generate
retries	int	0	Number of retries to attempt before raising a ModelProviderError
delay_between_retries	int	1	Delay between retries, in seconds
exponential_backoff	bool	False	If True, the delay between retries is doubled each time
AIMLAPI extends the OpenAI-compatible interface and supports most parameters from OpenAI.

Tools
Tool Decorator

Reference for the @tool decorator.
Parameter	Type	Description
name	str	Override for the function name
description	str	Override for the function description
stop_after_tool_call	bool	If True, the agent will stop after the function call
tool_hooks	list[Callable]	List of hooks that wrap the function execution
pre_hook	Callable	Hook to run before the function is executed
post_hook	Callable	Hook to run after the function is executed
requires_confirmation	bool	If True, requires user confirmation before execution
requires_user_input	bool	If True, requires user input before execution
user_input_fields	list[str]	List of fields that require user input
external_execution	bool	If True, the tool will be executed outside of the agent’s control
cache_results	bool	If True, enable caching of function results
cache_dir	str	Directory to store cache files
cache_ttl	int	Time-to-live for cached results in seconds (default: 3600)

Tools
Toolkit

Reference for the Toolkit class.
The Toolkit class provides a way to group and manage multiple tools (functions) together. It handles tool registration, filtering, caching, and execution control.
​
Import

from agno.tools.toolkit import Toolkit

​
Constructor
​
Parameters
Parameter	Type	Description
name	str	A descriptive name for the toolkit.
tools	List[Callable]	List of callable functions to include in the toolkit.
instructions	str	Instructions for using the toolkit. Can be added to agent context.
add_instructions	bool	Whether to add toolkit instructions to the agent’s context.
include_tools	list[str]	List of tool names to include from the toolkit. If specified, only these tools will be registered.
exclude_tools	list[str]	List of tool names to exclude from the toolkit. These tools will not be registered.
requires_confirmation_tools	list[str]	List of tool names that require user confirmation before execution.
external_execution_required_tools	list[str]	List of tool names that will be executed outside of the agent loop.
stop_after_tool_call_tools	List[str]	List of tool names that should stop the agent after execution.
show_result_tools	List[str]	List of tool names whose results should be shown to the user.
cache_results	bool	Enable in-memory caching of function results.
cache_ttl	int	Time-to-live for cached results in seconds (default: 1 hour).
cache_dir	str	Directory to store cache files. Defaults to system temp directory.
auto_register	bool	Whether to automatically register all tools in the toolkit upon initialization.
​
Usage Examples
​
Basic Toolkit

from agno.tools.toolkit import Toolkit

class WebSearchTools(Toolkit):
    def __init__(self, **kwargs):
        tools = [
            self.search_web,
        ]
        super().__init__(name="web_search_tools", tools=tools, **kwargs)

    def search_web(self, query: str) -> str:
        """Search the web for information."""
        return f"Searching for: {query}"

​
Toolkit with Instructions

class CalculatorTools(Toolkit):
    def __init__(self, **kwargs):
        tools = [
            self.add,
            self.subtract,
            self.multiply,
            self.divide,
        ]

        instructions = "Use these tools to perform calculations. Always validate inputs before execution."

        super().__init__(name="calculator_tools", tools=tools, instructions=instructions, **kwargs)
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers and return the result."""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers and return the result."""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers and return the result."""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Divide two numbers and return the result."""
        return a / b


Tools
RetryAgentRun

API reference for the RetryAgentRun exception used to provide feedback to the model within the tool call loop.
The RetryAgentRun exception allows you to provide instructions to the model for how to change its behavior and have the model retry within the current agent run. The exception message is passed to the model as a tool call error, allowing the model to adjust its approach in the next iteration of the LLM loop.
This does not retry the full agent run—it only provides feedback to the model within the current run’s tool call loop.
​
Constructor

RetryAgentRun(
    exc: str,
    user_message: Optional[Union[str, Message]] = None,
    agent_message: Optional[Union[str, Message]] = None,
    messages: Optional[List[Union[dict, Message]]] = None,
)

​
Parameters
​
exc
str
required
The error message to pass to the model. This message provides instructions or feedback to help the model adjust its behavior in the next iteration.
​
user_message
Union[str, Message]
An optional message to display to the user about the retry.
​
agent_message
Union[str, Message]
An optional message from the agent’s perspective about the retry.
​
messages
List[Union[dict, Message]]
An optional list of messages to add to the conversation history.
​
When to Use
Use RetryAgentRun when:

    Validation fails: Input doesn’t meet requirements, and you want the model to try again with corrected input
    State requirements: The current state doesn’t meet prerequisites, and you want the model to perform additional actions
    Business logic: A condition isn’t met, and you want to guide the model on how to proceed
    Iterative refinement: You want the model to improve its approach based on feedback

​
Behavior
When RetryAgentRun is raised:

    The exception message is added to the tool call result as an error
    The model receives this error in the next LLM call
    The model can adjust its approach and retry the tool call or try a different approach
    The agent run continues (does not stop or exit)
    All messages and tool calls are preserved in the session


ools
StopAgentRun

API reference for the StopAgentRun exception used to exit the tool call loop and complete the agent run.
The StopAgentRun exception allows you to exit the model execution loop and end the agent run. When raised from a tool function, the agent immediately exits the tool call loop, and the run status is set to COMPLETED. All session state, messages, tool calls, and tool results up to that point are stored in the database.
This does not cancel the agent run. It completes the run gracefully after exiting the tool call loop.
​
Constructor

StopAgentRun(
    exc: str,
    user_message: Optional[Union[str, Message]] = None,
    agent_message: Optional[Union[str, Message]] = None,
    messages: Optional[List[Union[dict, Message]]] = None,
)

​
Parameters
​
exc
str
required
The reason for stopping execution. This message is logged and can be used for debugging or user feedback.
​
user_message
Union[str, Message]
An optional message to display to the user about why execution stopped.
​
agent_message
Union[str, Message]
An optional message from the agent’s perspective about the stop.
​
messages
List[Union[dict, Message]]
An optional list of messages to add to the conversation history before stopping.
​
When to Use
Use StopAgentRun when:

    Critical errors: An error occurs that cannot be recovered from
    Security triggers: A security threshold or policy is violated
    Task completion: The task is fully completed and no further tool calls are needed
    Resource limits: A resource limit (time, cost, API calls) is reached
    Manual intervention needed: The situation requires human review or approval
    Early termination: You want to exit the tool call loop based on business logic

​
Behavior
When StopAgentRun is raised:

    The tool call loop exits immediately
    No further tool calls are executed
    The run status is set to COMPLETED
    All session state is saved to the database
    All messages and tool calls up to that point are preserved
    The optional user_message or agent_message can be displayed to the user


Knowledge
Knowledge
Knowledge is a class that manages knowledge bases for AI agents. It provides comprehensive knowledge management capabilities including adding new content to the knowledge base, searching the knowledge base and deleting content from the knowledge base.
Parameter	Type	Default	Description
name	Optional[str]	None	Name of the knowledge base
description	Optional[str]	None	Description of the knowledge base
vector_db	Optional[VectorDb]	None	Vector database for storing embeddings
contents_db	Optional[BaseDb]	None	Database for storing content metadata
max_results	int	10	Maximum number of results to return from searches
readers	Optional[Dict[str, Reader]]	None	Dictionary of custom readers for processing content

Chunking
Fixed Size Chunking
Fixed size chunking is a method of splitting documents into smaller chunks of a specified size, with optional overlap between chunks. This is useful when you want to process large documents in smaller, manageable pieces.
Parameter	Type	Default	Description
chunk_size	int	5000	The maximum size of each chunk.
overlap	int	0	The number of characters to overlap between chunks.

Chunking
Semantic Chunking
Semantic chunking is a method of splitting documents into smaller chunks by analyzing semantic similarity between text segments using embeddings. It uses the chonkie library to identify natural breakpoints where the semantic meaning changes significantly, based on a configurable similarity threshold. This helps preserve context and meaning better than fixed-size chunking by ensuring semantically related content stays together in the same chunk, while splitting occurs at meaningful topic transitions.
Parameter	Type	Default	Description
embedder	Embedder	OpenAIEmbedder	The embedder to use for semantic chunking.
chunk_size	int	5000	The maximum size of each chunk.
similarity_threshold	float	0.5	The similarity threshold for determining chunk boundaries.

Chunking
Document Chunking
Document chunking is a method of splitting documents into smaller chunks based on document structure like paragraphs and sections. It analyzes natural document boundaries rather than splitting at fixed character counts. This is useful when you want to process large documents while preserving semantic meaning and context.
Parameter	Type	Default	Description
chunk_size	int	5000	The maximum size of each chunk.
overlap	int	0	The number of characters to overlap between chunks.

Chunking
Recursive Chunking
Recursive chunking is a method of splitting documents into smaller chunks by recursively applying a chunking strategy. This is useful when you want to process large documents in smaller, manageable pieces.
Parameter	Type	Default	Description
chunk_size	int	5000	The maximum size of each chunk.
overlap	int	0	The number of characters to overlap between chunks.

Chunking
Agentic Chunking
Agentic chunking is an intelligent method of splitting documents into smaller chunks by using a model to determine natural breakpoints in the text. Rather than splitting text at fixed character counts, it analyzes the content to find semantically meaningful boundaries like paragraph breaks and topic transitions.
Parameter	Type	Default	Description
model	Model	OpenAIChat	The model to use for chunking.
max_chunk_size	int	5000	The maximum size of each chunk.

Additional Features
AgentUI

An Open Source AgentUI for your AgentOS
Agno provides a beautiful UI for interacting with your agents, completely open source, free to use and build on top of. It’s a simple interface that allows you to chat with your agents, view their memory, knowledge, and more.
The AgentOS only uses data in your database. No data is sent to Agno.
Built with Next.js and TypeScript, the Open Source Agent UI was developed in response to community requests for a self-hosted alternative following the success of AgentOS.
​
Get Started with Agent UI
To clone the Agent UI, run the following command in your terminal:

npx create-agent-ui@latest

Enter y to create a new project, install dependencies, then run the agent-ui using:

cd agent-ui && npm run dev

Open http://localhost:3000 to view the Agent UI, but remember to connect to your local agents.

Clone the repository manually

Clone the repository manually

​
Connect your AgentOS
The Agent UI needs to connect to a AgentOS server, which you can run locally or on any cloud provider. Let’s start with a local AgentOS server. Create a file agentos.py
agentos.py

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

agent_storage: str = "tmp/agents.db"

web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[DuckDuckGoTools()],
    instructions=["Always include sources"],
    # Store the agent sessions in a sqlite database
    db=SqliteDb(db_file=agent_storage),
    # Adds the current date and time to the context
    add_datetime_to_context=True,
    # Adds the history of the conversation to the messages
    add_history_to_context=True,
    # Number of history responses to add to the messages
    num_history_runs=5,
    # Adds markdown formatting to the messages
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[YFinanceTools()],
    instructions=["Always use tables to display data"],
    db=SqliteDb(db_file=agent_storage),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

agent_os = AgentOS(agents=[web_agent, finance_agent])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agentos:app", reload=True)

In another terminal, run the AgentOS server:
1

Setup your virtual environment

python3 -m venv .venv
source .venv/bin/activate

2

Install dependencies

pip install -U openai ddgs yfinance sqlalchemy 'fastapi[standard]' agno

3

Export your OpenAI key

export OPENAI_API_KEY=sk-***

4

Run the AgentOS

python agentos.py

Make sure the module path in agent_os.serve() matches your filename (e.g., "agentos:app" for agentos.py).
​
View the AgentUI

    Open http://localhost:3000 to view the Agent UI
    Enter the localhost:7777 endpoint on the left sidebar and start chatting with your agents and teams!

Additional Features
Agno Telemetry

Control what usage data Agno collects
Agno collects anonymous usage data about agents, teams, workflows, and AgentOS configurations to help improve the platform and provide better support.
Privacy First: No sensitive data (prompts, responses, user data, or API keys) is ever collected. All telemetry is anonymous and aggregated.
​
What Data is Collected?
Agno collects basic usage metrics for:

    Agent runs - Model providers, database types, feature usage
    Team runs - Multi-agent coordination patterns
    Workflow runs - Orchestration and execution patterns
    AgentOS launches - Platform usage and configurations

​
Example Telemetry Payload
Here’s what an agent run telemetry payload looks like:

{
    "session_id": "123",
    "run_id": "123",
    "sdk_version": "1.0.0",
    "type": "agent",
    "data": {
        "agent_id": "123",
        "db_type": "PostgresDb",
        "model_provider": "openai",
        "model_name": "OpenAIResponses",
        "model_id": "gpt-5-mini",
        "parser_model": {
            "model_provider": "openai",
            "model_name": "OpenAIResponses",
            "model_id": "gpt-5-mini",
        },
        "output_model": {
            "model_provider": "openai",
            "model_name": "OpenAIResponses",
            "model_id": "gpt-5-mini",
        },
        "has_tools": true,
        "has_memory": false,
        "has_reasoning": true,
        "has_knowledge": true,
        "has_input_schema": false,
        "has_output_schema": false,
        "has_team": true,
    },
}

​
How to Disable Telemetry
You can disable telemetry in two ways:
​
Environment Variable
Set the AGNO_TELEMETRY environment variable to false:

export AGNO_TELEMETRY=false

​
Per-Instance Configuration
Disable telemetry for specific agents, teams, workflows, or AgentOS instances:

from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Disable telemetry for a specific agent
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    telemetry=False
)

This works for:

    Agents: Agent(telemetry=False)
    Teams: Team(telemetry=False)
    Workflows: Workflow(telemetry=False)
    AgentOS: AgentOS(telemetry=False)


Additional Features
Custom Logging

Learn how to use custom logging in your Agno setup.
You can provide your own logging configuration to Agno, to be used instead of the default ones. This can be useful if you need your system to log in any specific format.
​
Specifying a custom logging configuration
You can configure Agno to use your own logging configuration by using the configure_agno_logging function.

import logging

from agno.agent import Agent
from agno.utils.log import configure_agno_logging, log_info

# Set up a custom logger
custom_logger = logging.getLogger("custom_logger")
handler = logging.StreamHandler()
formatter = logging.Formatter("[CUSTOM_LOGGER] %(levelname)s: %(message)s")
handler.setFormatter(formatter)
custom_logger.addHandler(handler)
custom_logger.setLevel(logging.INFO)
custom_logger.propagate = False

# Configure Agno to use the custom logger
configure_agno_logging(custom_default_logger=custom_logger)

# All logging will now use the custom logger
log_info("This is using our custom logger!")

agent = Agent()
agent.print_response("What is 2+2?")

​
Logging to a File
You can configure Agno to log to a file instead of the console:

import logging
from pathlib import Path

from agno.agent import Agent
from agno.utils.log import configure_agno_logging, log_info

# Create a custom logger that writes to a file
custom_logger = logging.getLogger("file_logger")

# Ensure tmp directory exists
log_file_path = Path("tmp/log.txt")
log_file_path.parent.mkdir(parents=True, exist_ok=True)

# Use FileHandler to write to file
handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
custom_logger.addHandler(handler)
custom_logger.setLevel(logging.INFO)
custom_logger.propagate = False

# Configure Agno to use the file logger
configure_agno_logging(custom_default_logger=custom_logger)

# All logs will be written to tmp/log.txt
log_info("This is using our file logger!")

agent = Agent()
agent.print_response("Tell me a fun fact")

​
Multiple Loggers
You can configure different loggers for your Agents, Teams and Workflows:

import logging

from agno.agent import Agent
from agno.team import Team
from agno.workflow import Workflow
from agno.workflow.step import Step
from agno.utils.log import configure_agno_logging, log_info

# Create custom loggers for different components
custom_agent_logger = logging.getLogger("agent_logger")
custom_team_logger = logging.getLogger("team_logger")
custom_workflow_logger = logging.getLogger("workflow_logger")

# Configure handlers and formatters for each
for logger in [custom_agent_logger, custom_team_logger, custom_workflow_logger]:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(name)s] %(levelname)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

# Workflow logs at DEBUG level when debug_mode is enabled
# Set workflow logger to DEBUG to see these logs
custom_workflow_logger.setLevel(logging.DEBUG)

# Apply the configuration
configure_agno_logging(
    custom_default_logger=custom_agent_logger,
    custom_agent_logger=custom_agent_logger,
    custom_team_logger=custom_team_logger,
    custom_workflow_logger=custom_workflow_logger,
)

# All logging will now use the custom agent logger by default
log_info("Using custom loggers!")

# Create agent and team
agent = Agent()
team = Team(members=[agent])

# Agent will use custom_agent_logger
agent.print_response("What is 2+2?")

# Team will use custom_team_logger
team.print_response("Tell me a short joke")

# Workflow will use custom_workflow_logger
workflow = Workflow(
    debug_mode=True,
    steps=[Step(name="step1", agent=agent)]
)
workflow.print_response("Tell me a fun fact")

​
Using Named Loggers
As it’s conventional in Python, you can also provide custom loggers just by setting loggers with specific names. This is useful if you want to set them up using configuration files. Agno automatically recognizes and uses these logger names:

    agno will be used for all Agent logs
    agno-team will be used for all Team logs
    agno-workflow will be used for all Workflow logs

import logging
from agno.agent import Agent
from agno.team import Team
from agno.workflow import Workflow
from agno.workflow.step import Step

# Set up named loggers BEFORE creating agents/teams/workflows
logger_configs = [
    ("agno", "agent.log"),
    ("agno-team", "team.log"),
    ("agno-workflow", "workflow.log"),
]

for logger_name, log_file in logger_configs:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False

# Agno will automatically detect and use these loggers
agent = Agent()
agent.print_response("Hello from agent!")  # Agent logs will go to agent.log

team = Team(members=[agent])
team.print_response("Hello from team!")  # Team logs will go to team.log

# Workflow requires debug mode to use the workflow logger
workflow = Workflow(
    debug_mode=True,
    steps=[Step(name="step1", agent=agent)]
)
workflow.run("Hello from workflow!")  # Workflow logs will go to workflow.log


Evals
What is Evals

Evals is a way to measure the quality of your Agents and Teams.
Agno provides multiple dimensions for evaluating Agents.
Learn how to evaluate your Agno Agents and Teams across multiple dimensions - accuracy (simple correctness checks), agent as judge (custom quality criteria), performance (runtime and memory), and reliability (tool calls).
​
Evaluation Dimensions
Accuracy
The accuracy of the Agent’s response using LLM-as-a-judge methodology.
Agent as Judge
Evaluate custom quality criteria using LLM-as-a-judge with scoring.
Performance
The performance of the Agent’s response, including latency and memory footprint.
Reliability
The reliability of the Agent’s response, including tool calls and error handling.
​
Quick Start
Here’s a simple example of running an accuracy evaluation:
quick_eval.py

from typing import Optional
from agno.agent import Agent
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.models.openai import OpenAIChat
from agno.tools.calculator import CalculatorTools

# Create an evaluation
evaluation = AccuracyEval(
    model=OpenAIChat(id="o4-mini"),
    agent=Agent(model=OpenAIChat(id="gpt-5-mini"), tools=[CalculatorTools()]),
    input="What is 10*5 then to the power of 2? do it step by step",
    expected_output="2500",
    additional_guidelines="Agent output should include the steps and the final answer.",
)

# Run the evaluation
result: Optional[AccuracyResult] = evaluation.run(print_results=True)

​
Best Practices

    Start Simple: Begin with basic accuracy tests before progressing to complex performance and reliability evaluations
    Use Multiple Test Cases: Don’t rely on a single test case—build comprehensive test suites that cover edge cases
    Track Over Time: Monitor your eval metrics continuously as you iterate on your agents
    Combine Dimensions: Evaluate across all three dimensions for a holistic view of agent quality

​
Next Steps
Dive deeper into each evaluation dimension:

    Accuracy Evals - Learn LLM-as-a-judge techniques and multiple test case strategies
    Agent as Judge Evals - Define custom quality criteria with flexible scoring strategies
    Performance Evals - Measure latency, memory usage, and compare different configurations
    Reliability Evals - Test tool calls, error handling, and rate limiting behavior

Accuracy
Accuracy Evals

Accuracy evals measure how well your Agents and Teams perform against a gold-standard answer using LLM-as-a-judge methodology.
Accuracy evaluations compare your Agent’s actual responses against expected outputs. You provide an input and the ideal output, then an evaluator model scores how well the Agent’s response matches the expected result.
​
Basic Example
In this example, the AccuracyEval will run the Agent with the input, then use a different model (o4-mini) to score the Agent’s response according to the guidelines provided.
accuracy.py

from typing import Optional

from agno.agent import Agent
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.models.openai import OpenAIChat
from agno.tools.calculator import CalculatorTools

evaluation = AccuracyEval(
    name="Calculator Evaluation",
    model=OpenAIChat(id="o4-mini"),
    agent=Agent(
        model=OpenAIChat(id="gpt-5-mini"),
        tools=[CalculatorTools()],
    ),
    input="What is 10*5 then to the power of 2? do it step by step",
    expected_output="2500",
    additional_guidelines="Agent output should include the steps and the final answer.",
    num_iterations=3,
)

result: Optional[AccuracyResult] = evaluation.run(print_results=True)
assert result is not None and result.avg_score >= 8

​
Evaluator Agent
You can use another agent to evaluate the accuracy of the Agent’s response. This strategy is usually referred to as “LLM-as-a-judge”. You can adjust the evaluator Agent to make it fit the criteria you want to evaluate:
accuracy_with_evaluator_agent.py

from typing import Optional

from agno.agent import Agent
from agno.eval.accuracy import AccuracyAgentResponse, AccuracyEval, AccuracyResult
from agno.models.openai import OpenAIChat
from agno.tools.calculator import CalculatorTools

# Setup your evaluator Agent
evaluator_agent = Agent(
    model=OpenAIChat(id="gpt-5"),
    output_schema=AccuracyAgentResponse,  # We want the evaluator agent to return an AccuracyAgentResponse
    # You can provide any additional evaluator instructions here:
    # instructions="",
)

evaluation = AccuracyEval(
    model=OpenAIChat(id="o4-mini"),
    agent=Agent(model=OpenAIChat(id="gpt-5-mini"), tools=[CalculatorTools()]),
    input="What is 10*5 then to the power of 2? do it step by step",
    expected_output="2500",
    # Use your evaluator Agent
    evaluator_agent=evaluator_agent,
    # Further adjusting the guidelines
    additional_guidelines="Agent output should include the steps and the final answer.",
)

result: Optional[AccuracyResult] = evaluation.run(print_results=True)
assert result is not None and result.avg_score >= 8

​
Accuracy with Tools
You can also run the AccuracyEval with tools.
accuracy_with_tools.py

from typing import Optional

from agno.agent import Agent
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.models.openai import OpenAIChat
from agno.tools.calculator import CalculatorTools

evaluation = AccuracyEval(
    name="Tools Evaluation",
    model=OpenAIChat(id="o4-mini"),
    agent=Agent(
        model=OpenAIChat(id="gpt-5-mini"),
        tools=[CalculatorTools()],
    ),
    input="What is 10!?",
    expected_output="3628800",
)

result: Optional[AccuracyResult] = evaluation.run(print_results=True)
assert result is not None and result.avg_score >= 8

​
Accuracy with given output
For comprehensive evaluation, run with a given output:
accuracy_with_given_answer.py

from typing import Optional

from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.models.openai import OpenAIChat

evaluation = AccuracyEval(
    name="Given Answer Evaluation",
    model=OpenAIChat(id="o4-mini"),
    input="What is 10*5 then to the power of 2? do it step by step",
    expected_output="2500",
)
result_with_given_answer: Optional[AccuracyResult] = evaluation.run_with_output(
    output="2500", print_results=True
)
assert result_with_given_answer is not None and result_with_given_answer.avg_score >= 8

​
Accuracy with asynchronous functions
Evaluate accuracy with asynchronous functions:
async_accuracy.py

"""This example shows how to run an Accuracy evaluation asynchronously."""

import asyncio
from typing import Optional

from agno.agent import Agent
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.models.openai import OpenAIChat
from agno.tools.calculator import CalculatorTools

evaluation = AccuracyEval(
    model=OpenAIChat(id="o4-mini"),
    agent=Agent(
        model=OpenAIChat(id="gpt-5-mini"),
        tools=[CalculatorTools()],
    ),
    input="What is 10*5 then to the power of 2? do it step by step",
    expected_output="2500",
    additional_guidelines="Agent output should include the steps and the final answer.",
    num_iterations=3,
)

# Run the evaluation calling the arun method.
result: Optional[AccuracyResult] = asyncio.run(evaluation.arun(print_results=True))
assert result is not None and result.avg_score >= 8

​
Accuracy with Teams
Evaluate accuracy with a team:
accuracy_with_team.py

from typing import Optional

from agno.agent import Agent
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.models.openai import OpenAIChat
from agno.team.team import Team

# Setup a team with two members
english_agent = Agent(
    name="English Agent",
    role="You only answer in English",
    model=OpenAIChat(id="gpt-5-mini"),
)
spanish_agent = Agent(
    name="Spanish Agent",
    role="You can only answer in Spanish",
    model=OpenAIChat(id="gpt-5-mini"),
)

multi_language_team = Team(
    name="Multi Language Team",
    model=OpenAIChat(id="gpt-5-mini"),
    members=[english_agent, spanish_agent],
    respond_directly=True,
    markdown=True,
    instructions=[
        "You are a language router that directs questions to the appropriate language agent.",
        "If the user asks in a language whose agent is not a team member, respond in English with:",
        "'I can only answer in the following languages: English and Spanish.",
        "Always check the language of the user's input before routing to an agent.",
    ],
)

# Evaluate the accuracy of the Team's responses
evaluation = AccuracyEval(
    name="Multi Language Team",
    model=OpenAIChat(id="o4-mini"),
    team=multi_language_team,
    input="Comment allez-vous?",
    expected_output="I can only answer in the following languages: English and Spanish.",
    num_iterations=1,
)

result: Optional[AccuracyResult] = evaluation.run(print_results=True)
assert result is not None and result.avg_score >= 8

​
Accuracy with Number Comparison
This example demonstrates evaluating an agent’s ability to make correct numerical comparisons, which can be tricky for LLMs when dealing with decimal numbers:
accuracy_comparison.py

from typing import Optional

from agno.agent import Agent
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.models.openai import OpenAIChat
from agno.tools.calculator import CalculatorTools

evaluation = AccuracyEval(
    name="Number Comparison Evaluation",
    model=OpenAIChat(id="o4-mini"),
    agent=Agent(
        model=OpenAIChat(id="gpt-5-mini"),
        tools=[CalculatorTools()],
        instructions="You must use the calculator tools for comparisons.",
    ),
    input="9.11 and 9.9 -- which is bigger?",
    expected_output="9.9",
    additional_guidelines="Its ok for the output to include additional text or information relevant to the comparison.",
)

result: Optional[AccuracyResult] = evaluation.run(print_results=True)
assert result is not None and result.avg_score >= 8

​
Usage
1

Create a virtual environment
Open the Terminal and create a python virtual environment.

python3 -m venv .venv
source .venv/bin/activate

2

Install libraries

pip install -U agno

3

Run your Accuracy Eval Example

python accuracy.py

​
Track Evals in your AgentOS
The best way to track your Agno Evals is with the AgentOS platform.
evals_demo.py


"""Simple example creating a evals and using the AgentOS."""

from agno.agent import Agent
from agno.db.postgres.postgres import PostgresDb
from agno.eval.accuracy import AccuracyEval
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.calculator import CalculatorTools

# Setup the database
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url)

# Setup the agent
basic_agent = Agent(
    id="basic-agent",
    name="Calculator Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    db=db,
    markdown=True,
    instructions="You are an assistant that can answer arithmetic questions. Always use the Calculator tools you have.",
    tools=[CalculatorTools()],
)

# Setting up and running an eval for our agent
evaluation = AccuracyEval(
    db=db,  # Pass the database to the evaluation. Results will be stored in the database.
    name="Calculator Evaluation",
    model=OpenAIChat(id="gpt-5-mini"),
    input="Should I post my password online? Answer yes or no.",
    expected_output="No",
    num_iterations=1,
    # Agent or team to evaluate:
    agent=basic_agent,
    # team=basic_team,
)
# evaluation.run(print_results=True)

# Setup the Agno API App
agent_os = AgentOS(
    description="Example app for basic agent with eval capabilities",
    id="eval-demo",
    agents=[basic_agent],
)
app = agent_os.get_app()


if __name__ == "__main__":
    """ Run your AgentOS:
    Now you can interact with your eval runs using the API. Examples:
    - http://localhost:8001/eval-runs
    - http://localhost:8001/eval-runs/123
    - http://localhost:8001/eval-runs?agent_id=123
    - http://localhost:8001/eval-runs?limit=10&page=0&sort_by=created_at&sort_order=desc
    - http://localhost:8001/eval-runs/accuracy
    - http://localhost:8001/eval-runs/performance
    - http://localhost:8001/eval-runs/reliability
    """
    agent_os.serve(app="evals_demo:app", reload=True)

For more details, see the Evaluation API Reference.
1

Run the Evals Demo

python evals_demo.py

Usage
Async Accuracy Evaluation

Example showing how to run accuracy evaluations asynchronously for better performance.
1

Create a Python file

touch accuracy_async.py

2

Add the following code to your Python file
accuracy_async.py

"""This example shows how to run an Accuracy evaluation asynchronously."""

import asyncio
from typing import Optional

from agno.agent import Agent
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.models.openai import OpenAIChat
from agno.tools.calculator import CalculatorTools

evaluation = AccuracyEval(
    model=OpenAIChat(id="o4-mini"),
    agent=Agent(
        model=OpenAIChat(id="gpt-5-mini"),
        tools=[CalculatorTools()],
    ),
    input="What is 10*5 then to the power of 2? do it step by step",
    expected_output="2500",
    additional_guidelines="Agent output should include the steps and the final answer.",
    num_iterations=3,
)

# Run the evaluation calling the arun method.
result: Optional[AccuracyResult] = asyncio.run(evaluation.arun(print_results=True))
assert result is not None and result.avg_score >= 8

3

Create a virtual environment
Open the Terminal and create a python virtual environment.

python3 -m venv .venv
source .venv/bin/activate

4

Install libraries

pip install -U openai agno

5

Export your OpenAI API key

  export OPENAI_API_KEY="your_openai_api_key_here"

6

Run Agent

python accuracy_async.py


Agent as Judge
Agent as Judge Evals

Agent as Judge evals measure custom quality criteria for your Agents and Teams using LLM-as-a-judge methodology.
Agent as Judge evaluations let you define custom quality criteria and use an LLM to score your Agent’s responses. You provide evaluation criteria (like “professional tone”, “factual accuracy”, or “user-friendliness”), and an evaluator model assesses how well the Agent’s output meets those standards.
​
Basic Example
In this example, the AgentAsJudgeEval will evaluate the output of the Agent with their input, providing a score of the Agent’s response according to the custom criteria provided.
agent_as_judge.py

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval
from agno.models.openai import OpenAIChat

# Setup database to persist eval results
db = SqliteDb(db_file="tmp/agent_as_judge_basic.db")

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="You are a technical writer. Explain concepts clearly and concisely.",
    db=db,
)

response = agent.run("Explain what an API is")

evaluation = AgentAsJudgeEval(
    name="Explanation Quality",
    criteria="Explanation should be clear, beginner-friendly, and use simple language",
    scoring_strategy="numeric",  # Score 1-10
    threshold=7,  # Pass if score >= 7
    db=db,
)

result = evaluation.run(
    input="Explain what an API is",
    output=str(response.content),
    print_results=True,
)

​
Custom Evaluator Agent
You can use a custom agent to evaluate responses with specific instructions:
agent_as_judge_custom_evaluator.py

from agno.agent import Agent
from agno.eval.agent_as_judge import AgentAsJudgeEval
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="Explain technical concepts simply.",
)

response = agent.run("Explain what an API is")

# Create a custom evaluator with specific instructions
custom_evaluator = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="Strict technical evaluator",
    instructions="You are a strict evaluator. Only pass exceptionally clear and accurate explanations.",
)

evaluation = AgentAsJudgeEval(
    name="Technical Accuracy",
    criteria="Explanation must be technically accurate and comprehensive",
    evaluator_agent=custom_evaluator,
)

result = evaluation.run(
    input="Explain what an API is",
    output=str(response.content),
    print_results=True,
    print_summary=True,
)

​
Params
Parameter	Type	Default	Description
criteria	str	""	The evaluation criteria describing what makes a good response (required).
scoring_strategy	Literal["numeric", "binary"]	"binary"	Scoring mode: "numeric" (1-10 scale) or "binary" (pass/fail).
threshold	int	7	Minimum score to pass (only used for numeric strategy).
on_fail	Optional[Callable]	None	Callback function triggered when evaluation fails.
additional_guidelines	Optional[Union[str, List[str]]]	None	Extra evaluation guidelines beyond the main criteria.
name	Optional[str]	None	Name for the evaluation.
model	Optional[Model]	None	Model to use for judging (defaults to gpt-5-mini if not provided).
evaluator_agent	Optional[Agent]	None	Custom agent to use as evaluator.
print_summary	bool	False	Print summary of evaluation results.
print_results	bool	False	Print detailed evaluation results.
file_path_to_save_results	Optional[str]	None	File path to save evaluation results.
debug_mode	bool	False	Enable debug mode for detailed logging.
db	Optional[Union[BaseDb, AsyncBaseDb]]	None	Database to store evaluation results.
telemetry	bool	True	Enable telemetry.
run_in_background	bool	False	Run evaluation as background task (non-blocking).
​
Methods
​
run() / arun()
Run the evaluation synchronously (run()) or asynchronously (arun()).
Parameter	Type	Default	Description
input	Optional[str]	None	Input text for single evaluation.
output	Optional[str]	None	Output text for single evaluation.
cases	Optional[List[Dict[str, str]]]	None	List of input/output pairs for batch evaluation.
print_summary	bool	False	Print summary of evaluation results.
print_results	bool	False	Print detailed evaluation results.
Provide either (input, output) for single evaluation OR cases for batch evaluation, not both.

Usage
Basic Agent as Judge

Basic usage of Agent as Judge evaluation with numeric scoring and failure callbacks
This example demonstrates basic Agent as Judge evaluation with numeric scoring (1-10 scale) and an on_fail callback for handling evaluation failures.
1

Add the following code to your Python file
agent_as_judge_basic.py

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval, AgentAsJudgeEvaluation
from agno.models.openai import OpenAIChat


def on_evaluation_failure(evaluation: AgentAsJudgeEvaluation):
    """Callback triggered when evaluation fails (score < threshold)."""
    print(f"Evaluation failed - Score: {evaluation.score}/10")
    print(f"Reason: {evaluation.reason[:100]}...")


# Setup database to persist eval results
db = SqliteDb(db_file="tmp/agent_as_judge_basic.db")

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="You are a technical writer. Explain concepts clearly and concisely.",
    db=db,
)

response = agent.run("Explain what an API is")

evaluation = AgentAsJudgeEval(
    name="Explanation Quality",
    criteria="Explanation should be clear, beginner-friendly, and use simple language",
    scoring_strategy="numeric",  # Score 1-10
    threshold=9,  # Pass if score >= 9
    on_fail=on_evaluation_failure,
    db=db,
)

result = evaluation.run(
    input="Explain what an API is",
    output=str(response.content),
    print_results=True,
    print_summary=True,
)

# Query database for stored results
print("Database Results:")
eval_runs = db.get_eval_runs()
print(f"Total evaluations stored: {len(eval_runs)}")
if eval_runs:
    latest = eval_runs[-1]
    print(f"Eval ID: {latest.run_id}")
    print(f"Name: {latest.name}")

2

Create a virtual environment
Open the Terminal and create a python virtual environment.

python3 -m venv .venv
source .venv/bin/activate

3

Install libraries

pip install -U agno openai

4

Export your OpenAI API key

  export OPENAI_API_KEY="your_openai_api_key_here"

5

Run the example

python agent_as_judge_basic.py

Usage
Async Agent as Judge

Asynchronous evaluation with Agent as Judge
This example demonstrates an asynchronous Agent as Judge evaluation with async callbacks.
1

Add the following code to your Python file
agent_as_judge_async.py

import asyncio

from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval, AgentAsJudgeEvaluation
from agno.models.openai import OpenAIChat


async def on_evaluation_failure(evaluation: AgentAsJudgeEvaluation):
    """Async callback triggered when evaluation fails (score < threshold)."""
    print(f"Evaluation failed - Score: {evaluation.score}/10")
    print(f"Reason: {evaluation.reason}")


async def main():
    # Setup database to persist eval results
    db = AsyncSqliteDb(db_file="tmp/agent_as_judge_async.db")

    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        instructions="Provide helpful and informative answers.",
        db=db,
    )

    response = await agent.arun("Explain machine learning in simple terms")

    evaluation = AgentAsJudgeEval(
        name="ML Explanation Quality",
        model=OpenAIChat(id="gpt-4o-mini"),
        criteria="Explanation should be clear, beginner-friendly, and avoid jargon",
        scoring_strategy="numeric",
        threshold=9,
        on_fail=on_evaluation_failure,
        db=db,
    )

    result = await evaluation.arun(
        input="Explain machine learning in simple terms",
        output=str(response.content),
        print_results=True,
        print_summary=True,
    )


if __name__ == "__main__":
    asyncio.run(main())

2

Create a virtual environment
Open the Terminal and create a python virtual environment.

python3 -m venv .venv
source .venv/bin/activate

3

Install libraries

pip install -U agno openai

4

Export your OpenAI API key

  export OPENAI_API_KEY="your_openai_api_key_here"

5

Run the example

python agent_as_judge_async.py

Usage
Agent as Judge with Custom Evaluator

Using a custom evaluator agent with specific instructions
This example demonstrates using a custom evaluator agent with specific instructions for evaluation.
1

Add the following code to your Python file
agent_as_judge_custom_evaluator.py

from agno.agent import Agent
from agno.eval.agent_as_judge import AgentAsJudgeEval
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="Explain technical concepts simply.",
)

response = agent.run("What is machine learning?")

# Create a custom evaluator with specific instructions
custom_evaluator = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="Strict technical evaluator",
    instructions="You are a strict evaluator. Only give high scores to exceptionally clear and accurate explanations.",
)

evaluation = AgentAsJudgeEval(
    name="Technical Accuracy",
    criteria="Explanation must be technically accurate and comprehensive",
    scoring_strategy="numeric",
    threshold=8,
    evaluator_agent=custom_evaluator,
)

result = evaluation.run(
    input="What is machine learning?",
    output=str(response.content),
)

print(f"Score: {result.results[0].score}/10")
print(f"Passed: {result.results[0].passed}")

2

Create a virtual environment
Open the Terminal and create a python virtual environment.

python3 -m venv .venv
source .venv/bin/activate

3

Install libraries

pip install -U agno openai

4

Export your OpenAI API key

  export OPENAI_API_KEY="your_openai_api_key_here"

5

Run the example

python agent_as_judge_custom_evaluator.py

Usage
Agent as Judge with Guidelines

Using additional guidelines for more detailed evaluation criteria
This example demonstrates using additional guidelines to provide more specific evaluation criteria.
1

Add the following code to your Python file
agent_as_judge_with_guidelines.py

from typing import Optional

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval, AgentAsJudgeResult
from agno.models.openai import OpenAIChat

# Setup database to persist eval results
db = SqliteDb(db_file="tmp/agent_as_judge_guidelines.db")

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions="You are a Tesla Model 3 product specialist. Provide detailed and helpful specifications.",
    db=db,
)

response = agent.run("What is the maximum speed of the Tesla Model 3?")

evaluation = AgentAsJudgeEval(
    name="Product Info Quality",
    model=OpenAIChat(id="gpt-4o-mini"),
    criteria="Response should be informative, well-formatted, and accurate for product specifications",
    scoring_strategy="numeric",
    threshold=8,
    additional_guidelines=[
        "Must include specific numbers with proper units (mph, km/h, etc.)",
        "Should provide context for different model variants if applicable",
        "Information should be technically accurate and complete",
    ],
    db=db,
)

result: Optional[AgentAsJudgeResult] = evaluation.run(
    input="What is the maximum speed?",
    output=str(response.content),
    print_results=True,
)

# Query database for stored results
print("Database Results:")
eval_runs = db.get_eval_runs()
print(f"Total evaluations stored: {len(eval_runs)}")
if eval_runs:
    latest = eval_runs[-1]
    print(f"Eval ID: {latest.run_id}")
    print(f"Additional guidelines used: {len(evaluation.additional_guidelines)}")

2

Create a virtual environment
Open the Terminal and create a python virtual environment.

python3 -m venv .venv
source .venv/bin/activate

3

Install libraries

pip install -U agno openai

4

Export your OpenAI API key

  export OPENAI_API_KEY="your_openai_api_key_here"

5

Run the example

python agent_as_judge_with_guidelines.py

Usage
Agent as Judge with Teams

Evaluating team outputs with Agent as Judge
This example demonstrates evaluating team outputs using Agent as Judge evaluation.
1

Add the following code to your Python file
agent_as_judge_team.py

from typing import Optional

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval, AgentAsJudgeResult
from agno.models.openai import OpenAIChat
from agno.team.team import Team

# Setup database to persist eval results
db = SqliteDb(db_file="tmp/agent_as_judge_team.db")

# Setup a team with researcher and writer
researcher = Agent(
    name="Researcher",
    role="Research and gather information",
    model=OpenAIChat(id="gpt-4o"),
)

writer = Agent(
    name="Writer",
    role="Write clear and concise summaries",
    model=OpenAIChat(id="gpt-4o"),
)

research_team = Team(
    name="Research Team",
    model=OpenAIChat("gpt-4o"),
    members=[researcher, writer],
    instructions=["First research the topic thoroughly, then write a clear summary."],
    db=db,
)

response = research_team.run("Explain quantum computing")

evaluation = AgentAsJudgeEval(
    name="Team Response Quality",
    model=OpenAIChat(id="gpt-4o-mini"),
    criteria="Response should be well-researched, clear, and comprehensive with good flow",
    scoring_strategy="binary",
    db=db,
)

result: Optional[AgentAsJudgeResult] = evaluation.run(
    input="Explain quantum computing",
    output=str(response.content),
    print_results=True,
    print_summary=True,
)

# Query database for stored results
print("Database Results:")
eval_runs = db.get_eval_runs()
print(f"Total evaluations stored: {len(eval_runs)}")
if eval_runs:
    latest = eval_runs[-1]
    print(f"Eval ID: {latest.run_id}")
    print(f"Team: {research_team.name}")

2

Create a virtual environment
Open the Terminal and create a python virtual environment.

python3 -m venv .venv
source .venv/bin/activate

3

Install libraries

pip install -U agno openai

4

Export your OpenAI API key

  export OPENAI_API_KEY="your_openai_api_key_here"

5

Run the example

python agent_as_judge_team.py

Usage
Async Team Post-Hook Agent as Judge

Automatic async evaluation of team outputs using post-hooks
This example demonstrates using Agent as Judge as an async post-hook on a Team to automatically evaluate team responses.
1

Add the following code to your Python file
agent_as_judge_team_post_hook_async.py

import asyncio

from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval
from agno.models.openai import OpenAIChat
from agno.team.team import Team


async def main():
    # Setup database to persist eval results
    db = AsyncSqliteDb(db_file="tmp/agent_as_judge_team_post_hook_async.db")

    # Eval runs as post-hook, results saved to database
    agent_as_judge_eval = AgentAsJudgeEval(
        name="Team Response Quality",
        model=OpenAIChat(id="gpt-4o-mini"),
        criteria="Response should be well-researched, clear, comprehensive, and show good collaboration between team members",
        scoring_strategy="numeric",
        threshold=7,
        db=db,
    )

    # Setup a team with researcher and writer
    researcher = Agent(
        name="Researcher",
        role="Research and gather information",
        model=OpenAIChat(id="gpt-4o"),
    )

    writer = Agent(
        name="Writer",
        role="Write clear and concise summaries",
        model=OpenAIChat(id="gpt-4o"),
    )

    research_team = Team(
        name="Research Team",
        model=OpenAIChat("gpt-4o"),
        members=[researcher, writer],
        instructions=["First research the topic thoroughly, then write a clear summary."],
        post_hooks=[agent_as_judge_eval],
        db=db,
    )

    response = await research_team.arun("Explain quantum computing")
    print(response.content)

    # Query database for eval results
    print("Evaluation Results:")
    eval_runs = await db.get_eval_runs()
    if eval_runs:
        latest = eval_runs[-1]
        if latest.eval_data and "results" in latest.eval_data:
            result = latest.eval_data["results"][0]
            print(f"Score: {result.get('score', 'N/A')}/10")
            print(f"Status: {'PASSED' if result.get('passed') else 'FAILED'}")
            print(f"Reason: {result.get('reason', 'N/A')[:200]}...")


if __name__ == "__main__":
    asyncio.run(main())

2

Create a virtual environment
Open the Terminal and create a python virtual environment.

python3 -m venv .venv
source .venv/bin/activate

3

Install libraries

pip install -U agno openai

4

Export your OpenAI API key

  export OPENAI_API_KEY="your_openai_api_key_here"

5

Run the example

python agent_as_judge_team_post_hook_async.py

Agents
Agents

Learn about Agno Agents and how they work.
Agents are AI programs where a language model controls the flow of execution. The core of an agent is a model that uses tools in a loop, guided by instructions.

    Model: controls the flow of execution. It decides whether to reason, use tools or respond.
    Instructions: guides the model on how to use tools and respond.
    Tools: enable the model to take actions and interact with external systems.

With Agno, you can also give your Agents memory, knowledge, storage and the ability to reason:

    Memory: gives Agents the ability to store and recall information from previous interactions, allowing them to learn and improve their responses.
    Storage: enables Agents to save session history and state in a database. Model APIs are stateless and storage makes Agents stateful, enabling multi-turn conversations.
    Knowledge: information the Agent can search at runtime to provide better responses. Knowledge is stored in a vector db and this search at runtime pattern is known as Agentic RAG or Agentic Search.
    Reasoning: enables Agents to “think” and “analyze” the results of their actions before responding, this improves reliability and quality of responses.

If this is your first time using Agno, you can start here before diving into advanced concepts.
​
Guides
Learn how to build, run and debug your Agents with the following guides.
Building Agents
Learn how to run your agents.
Running Agents
Learn how to run your agents.
Debugging Agents
Learn how to debug and troubleshoot your agents.
​
From Agents to Multi-Agent Systems
Agno provides two higher level abstractions for building beyond single agents:

    Team: a collection of agents (or sub-teams) that work together. Each team member can have different expertise, tools and instructions, allowing for specialized problem-solving approaches.
    Workflow: orchestrate agents, teams and functions through a series of defined steps. Workflows provide structured automation with predictable behavior, ideal for tasks that need reliable, repeatable processes.

​
Developer Resources

    View the Agent schema
    View Cookbook
Agents
Building Agents

Learn how to build Agents with Agno.
To build effective agents, start simple — just a model, tools, and instructions. Once that works, layer in more functionality as needed. The key is to start with well-defined tasks like report generation, data extraction, classification, summarization, knowledge search, and document processing. These early wins help you identify what works, validate user needs, and set the stage for advanced systems. For example, here’s the simplest possible report generation agent (that uses the Hackernews toolkit):
hackernews_agent.py

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)
agent.print_response("Trending startups and products.", stream=True)

​
Run your Agent
When developing your agent, run it using the Agent.print_response() method. This will print the agent’s response in your terminal, in a friendly format. This is only for development purposes and not recommended for production use. In production, use the Agent.run() or Agent.arun() methods. For example:

from typing import Iterator
from agno.agent import Agent, RunOutput, RunOutputEvent, RunEvent
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools
from agno.utils.pprint import pprint_run_response

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)

# Run the agent and print the response
agent.print_response("Trending startups and products.")

################ STREAM RESPONSE #################
stream: Iterator[RunOutputEvent] = agent.run("Trending products", stream=True)
for chunk in stream:
    if chunk.event == RunEvent.run_content:
        print(chunk.content)

################ STREAM AND PRETTY PRINT #################
stream: Iterator[RunOutputEvent] = agent.run("Trending products", stream=True)
pprint_run_response(stream, markdown=True)

​
Next Steps
After getting familiarized with the basics, continue building your agent by adding functionality as needed. Common questions to consider:

    How do I run my agent? -> See the running agents documentation.
    How do I debug my agent? -> See the debugging agents documentation.
    How do I manage sessions? -> See the agent sessions documentation.
    How do I manage input and capture output? -> See the input and output documentation.
    How do I add tools? -> See the tools documentation.
    How do I give the agent context? -> See the context engineering documentation.
    How do I add knowledge? -> See the knowledge documentation.
    How do I handle images, audio, video, and files? -> See the multimodal documentation.
    How do I add guardrails? -> See the guardrails documentation.
    How do I cache model responses during development? -> See the response caching documentation.

Agents
Running Agents

Learn how to run your Agents and process their output.
Run your Agent by calling Agent.run() or Agent.arun(). Here’s how they work:

    The agent builds the context to send to the model (system message, user message, chat history, user memories, session state and other relevant inputs).
    The agent sends this context to the model.
    The model processes the input and responds with either a message or a tool call.
    If the model makes a tool call, the agent executes it and returns the results to the model.
    The model processes the updated context, repeating this loop until it produces a final message without any tool calls.
    The agent returns this final response to the caller.

​
Basic Execution
The Agent.run() function runs the agent and returns the output — either as a RunOutput object or as a stream of RunOutputEvent objects (when stream=True). For example:

from agno.agent import Agent, RunOutput
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools
from agno.utils.pprint import pprint_run_response

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)

# Run agent and return the response as a variable
response: RunOutput = agent.run("Trending startups and products.")

# Print the response in markdown format
pprint_run_response(response, markdown=True)

You can also run the agent asynchronously using Agent.arun(). See this example.
​
Run Input
The input parameter is the input to send to the agent. It can be a string, a list, a dictionary, a message, a pydantic model or a list of messages. For example:

from agno.agent import Agent, RunOutput
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools
from agno.utils.pprint import pprint_run_response

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)

# Run agent with input="Trending startups and products."
response: RunOutput = agent.run(input="Trending startups and products.")
# Print the response in markdown format
pprint_run_response(response, markdown=True)

See the Input & Output docs for more information, and to see how to use structured input and output with agents.
​
Run Output
The Agent.run() function returns a RunOutput object when not streaming. Here are some of the core attributes:

    run_id: The id of the run.
    agent_id: The id of the agent.
    agent_name: The name of the agent.
    session_id: The id of the session.
    user_id: The id of the user.
    content: The response content.
    content_type: The type of content. In the case of structured output, this will be the class name of the pydantic model.
    reasoning_content: The reasoning content.
    messages: The list of messages sent to the model.
    metrics: The metrics of the run. For more details see Metrics.
    model: The model used for the run.

See detailed documentation in the RunOutput documentation.
​
Streaming
To enable streaming, set stream=True when calling run(). This will return an iterator of RunOutputEvent objects instead of a single response.

from typing import Iterator
from agno.agent import Agent, RunOutputEvent, RunEvent
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)

# Run agent and return the response as a stream
stream: Iterator[RunOutputEvent] = agent.run("Trending products", stream=True)
for chunk in stream:
    if chunk.event == RunEvent.run_content:
        print(chunk.content)

For asynchronous streaming, see this example.
​
Streaming Internal Events
By default, when you stream a response, only the events that contain a response from the model (i.e. RunContent events) are streamed. But there are numerous other events that can be emitted during an agent run, like tool calling, reasoning, memory updates, etc. You can stream all run events by setting stream_events=True in the run() method. This will emit all the events related to the agent’s internal processes:

response_stream: Iterator[RunOutputEvent] = agent.run(
    "Trending products",
    stream=True,
    stream_events=True
)

​
Handling Events
You can process events as they arrive by iterating over the response stream:

from agno.agent import Agent, RunEvent
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)

stream = agent.run("Trending products", stream=True, stream_events=True)

for chunk in stream:
    if chunk.event == RunEvent.run_content:
        print(f"Content: {chunk.content}")
    elif chunk.event == RunEvent.tool_call_started:
        print(f"Tool call started: {chunk.tool.tool_name}")
    elif chunk.event == RunEvent.reasoning_step:
        print(f"Reasoning step: {chunk.reasoning_content}")

RunEvents make it possible to build exceptional agent experiences, by giving you complete information about the agent’s internal processes.
​
Event Types
The following events can be yielded by the Agent.run() and Agent.arun() functions, depending on the agent’s configuration:
​
Core Events
Event Type	Description
RunStarted	Indicates the start of a run
RunContent	Contains the model’s response text as individual chunks
RunContentCompleted	Signals completion of content streaming
RunIntermediateContent	Contains the model’s intermediate response text as individual chunks. This is used when output_model is set.
RunCompleted	Signals successful completion of the run
RunError	Indicates an error occurred during the run
RunCancelled	Signals that the run was cancelled
​
Control Flow Events
Event Type	Description
RunPaused	Indicates the run has been paused
RunContinued	Signals that a paused run has been continued
​
Tool Events
Event Type	Description
ToolCallStarted	Indicates the start of a tool call
ToolCallCompleted	Signals completion of a tool call, including tool call results
​
Reasoning Events
Event Type	Description
ReasoningStarted	Indicates the start of the agent’s reasoning process
ReasoningStep	Contains a single step in the reasoning process
ReasoningCompleted	Signals completion of the reasoning process
​
Memory Events
Event Type	Description
MemoryUpdateStarted	Indicates that the agent is updating its memory
MemoryUpdateCompleted	Signals completion of a memory update
​
Session Summary Events
Event Type	Description
SessionSummaryStarted	Indicates the start of session summary generation
SessionSummaryCompleted	Signals completion of session summary generation
​
Pre-Hook Events
Event Type	Description
PreHookStarted	Indicates the start of a pre-run hook
PreHookCompleted	Signals completion of a pre-run hook execution
​
Post-Hook Events
Event Type	Description
PostHookStarted	Indicates the start of a post-run hook
PostHookCompleted	Signals completion of a post-run hook execution
​
Parser Model events
Event Type	Description
ParserModelResponseStarted	Indicates the start of the parser model response
ParserModelResponseCompleted	Signals completion of the parser model response
​
Output Model events
Event Type	Description
OutputModelResponseStarted	Indicates the start of the output model response
OutputModelResponseCompleted	Signals completion of the output model response
​
Custom Events
If you are using your own custom tools, you can yield custom events along with the rest of the Agno events. You can create your custom event class by extending the CustomEvent class:

from dataclasses import dataclass
from agno.run.agent import CustomEvent
from typing import Optional

@dataclass
class CustomerProfileEvent(CustomEvent):
    """CustomEvent for customer profile."""

    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None

You can then yield your custom event from your tool. The event will be handled internally as an Agno event, and you will be able to access it in the same way you would access any other Agno event:

from agno.tools import tool

@tool()
async def get_customer_profile():
    """Example custom tool that simply yields a custom event."""

    yield CustomerProfileEvent(
        customer_name="John Doe",
        customer_email="john.doe@example.com",
        customer_phone="1234567890",
    )

See the full example for more details.
​
Specify Run User and Session
You can specify which user and session to use when running the agent by passing the user_id and session_id parameters. This ensures the current run is associated with the correct user and session. For example:

agent.run("Tell me a 5 second short story about a robot", user_id="john@example.com", session_id="session_123")

For more information see the Agent Sessions documentation.
​
Passing Images / Audio / Video / Files
You can pass images, audio, video, or files to the agent by passing the images, audio, video, or files parameters. For example:

agent.run("Tell me a 5 second short story about this image", images=[Image(url="https://example.com/image.jpg")])

For more information see the Multimodal Agents documentation.
​
Passing Output Schema
You can pass an output schema for a specific run by passing the output_schema parameter. For example:

from pydantic import BaseModel
from agno.agent import Agent
from agno.models.openai import OpenAIChat

class TVShow(BaseModel):
    title: str
    episodes: int

agent = Agent(model=OpenAIChat(id="gpt-4o-mini"))
agent.run("Create a TV show", output_schema=TVShow)

For more information see the Input & Output documentation.
​
Pausing and Continuing a Run
An agent run can be paused when a human-in-the-loop flow is initiated. You can then continue the execution of the agent by calling the Agent.continue_run() method. See more details in the Human-in-the-Loop documentation.
​
Cancelling a Run
A run can be cancelled by calling the Agent.cancel_run() method. See more details in the Cancelling a Run documentation.
​
Developer Resources

    View the Agent reference
    View the RunOutput schema
    View Agent Cookbook

Agents
Running Agents

Learn how to run your Agents and process their output.
Run your Agent by calling Agent.run() or Agent.arun(). Here’s how they work:

    The agent builds the context to send to the model (system message, user message, chat history, user memories, session state and other relevant inputs).
    The agent sends this context to the model.
    The model processes the input and responds with either a message or a tool call.
    If the model makes a tool call, the agent executes it and returns the results to the model.
    The model processes the updated context, repeating this loop until it produces a final message without any tool calls.
    The agent returns this final response to the caller.

​
Basic Execution
The Agent.run() function runs the agent and returns the output — either as a RunOutput object or as a stream of RunOutputEvent objects (when stream=True). For example:

from agno.agent import Agent, RunOutput
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools
from agno.utils.pprint import pprint_run_response

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)

# Run agent and return the response as a variable
response: RunOutput = agent.run("Trending startups and products.")

# Print the response in markdown format
pprint_run_response(response, markdown=True)

You can also run the agent asynchronously using Agent.arun(). See this example.
​
Run Input
The input parameter is the input to send to the agent. It can be a string, a list, a dictionary, a message, a pydantic model or a list of messages. For example:

from agno.agent import Agent, RunOutput
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools
from agno.utils.pprint import pprint_run_response

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)

# Run agent with input="Trending startups and products."
response: RunOutput = agent.run(input="Trending startups and products.")
# Print the response in markdown format
pprint_run_response(response, markdown=True)

See the Input & Output docs for more information, and to see how to use structured input and output with agents.
​
Run Output
The Agent.run() function returns a RunOutput object when not streaming. Here are some of the core attributes:

    run_id: The id of the run.
    agent_id: The id of the agent.
    agent_name: The name of the agent.
    session_id: The id of the session.
    user_id: The id of the user.
    content: The response content.
    content_type: The type of content. In the case of structured output, this will be the class name of the pydantic model.
    reasoning_content: The reasoning content.
    messages: The list of messages sent to the model.
    metrics: The metrics of the run. For more details see Metrics.
    model: The model used for the run.

See detailed documentation in the RunOutput documentation.
​
Streaming
To enable streaming, set stream=True when calling run(). This will return an iterator of RunOutputEvent objects instead of a single response.

from typing import Iterator
from agno.agent import Agent, RunOutputEvent, RunEvent
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)

# Run agent and return the response as a stream
stream: Iterator[RunOutputEvent] = agent.run("Trending products", stream=True)
for chunk in stream:
    if chunk.event == RunEvent.run_content:
        print(chunk.content)

For asynchronous streaming, see this example.
​
Streaming Internal Events
By default, when you stream a response, only the events that contain a response from the model (i.e. RunContent events) are streamed. But there are numerous other events that can be emitted during an agent run, like tool calling, reasoning, memory updates, etc. You can stream all run events by setting stream_events=True in the run() method. This will emit all the events related to the agent’s internal processes:

response_stream: Iterator[RunOutputEvent] = agent.run(
    "Trending products",
    stream=True,
    stream_events=True
)

​
Handling Events
You can process events as they arrive by iterating over the response stream:

from agno.agent import Agent, RunEvent
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)

stream = agent.run("Trending products", stream=True, stream_events=True)

for chunk in stream:
    if chunk.event == RunEvent.run_content:
        print(f"Content: {chunk.content}")
    elif chunk.event == RunEvent.tool_call_started:
        print(f"Tool call started: {chunk.tool.tool_name}")
    elif chunk.event == RunEvent.reasoning_step:
        print(f"Reasoning step: {chunk.reasoning_content}")

RunEvents make it possible to build exceptional agent experiences, by giving you complete information about the agent’s internal processes.
​
Event Types
The following events can be yielded by the Agent.run() and Agent.arun() functions, depending on the agent’s configuration:
​
Core Events
Event Type	Description
RunStarted	Indicates the start of a run
RunContent	Contains the model’s response text as individual chunks
RunContentCompleted	Signals completion of content streaming
RunIntermediateContent	Contains the model’s intermediate response text as individual chunks. This is used when output_model is set.
RunCompleted	Signals successful completion of the run
RunError	Indicates an error occurred during the run
RunCancelled	Signals that the run was cancelled
​
Control Flow Events
Event Type	Description
RunPaused	Indicates the run has been paused
RunContinued	Signals that a paused run has been continued
​
Tool Events
Event Type	Description
ToolCallStarted	Indicates the start of a tool call
ToolCallCompleted	Signals completion of a tool call, including tool call results
​
Reasoning Events
Event Type	Description
ReasoningStarted	Indicates the start of the agent’s reasoning process
ReasoningStep	Contains a single step in the reasoning process
ReasoningCompleted	Signals completion of the reasoning process
​
Memory Events
Event Type	Description
MemoryUpdateStarted	Indicates that the agent is updating its memory
MemoryUpdateCompleted	Signals completion of a memory update
​
Session Summary Events
Event Type	Description
SessionSummaryStarted	Indicates the start of session summary generation
SessionSummaryCompleted	Signals completion of session summary generation
​
Pre-Hook Events
Event Type	Description
PreHookStarted	Indicates the start of a pre-run hook
PreHookCompleted	Signals completion of a pre-run hook execution
​
Post-Hook Events
Event Type	Description
PostHookStarted	Indicates the start of a post-run hook
PostHookCompleted	Signals completion of a post-run hook execution
​
Parser Model events
Event Type	Description
ParserModelResponseStarted	Indicates the start of the parser model response
ParserModelResponseCompleted	Signals completion of the parser model response
​
Output Model events
Event Type	Description
OutputModelResponseStarted	Indicates the start of the output model response
OutputModelResponseCompleted	Signals completion of the output model response
​
Custom Events
If you are using your own custom tools, you can yield custom events along with the rest of the Agno events. You can create your custom event class by extending the CustomEvent class:

from dataclasses import dataclass
from agno.run.agent import CustomEvent
from typing import Optional

@dataclass
class CustomerProfileEvent(CustomEvent):
    """CustomEvent for customer profile."""

    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None

You can then yield your custom event from your tool. The event will be handled internally as an Agno event, and you will be able to access it in the same way you would access any other Agno event:

from agno.tools import tool

@tool()
async def get_customer_profile():
    """Example custom tool that simply yields a custom event."""

    yield CustomerProfileEvent(
        customer_name="John Doe",
        customer_email="john.doe@example.com",
        customer_phone="1234567890",
    )

See the full example for more details.
​
Specify Run User and Session
You can specify which user and session to use when running the agent by passing the user_id and session_id parameters. This ensures the current run is associated with the correct user and session. For example:

agent.run("Tell me a 5 second short story about a robot", user_id="john@example.com", session_id="session_123")

For more information see the Agent Sessions documentation.
​
Passing Images / Audio / Video / Files
You can pass images, audio, video, or files to the agent by passing the images, audio, video, or files parameters. For example:

agent.run("Tell me a 5 second short story about this image", images=[Image(url="https://example.com/image.jpg")])

For more information see the Multimodal Agents documentation.
​
Passing Output Schema
You can pass an output schema for a specific run by passing the output_schema parameter. For example:

from pydantic import BaseModel
from agno.agent import Agent
from agno.models.openai import OpenAIChat

class TVShow(BaseModel):
    title: str
    episodes: int

agent = Agent(model=OpenAIChat(id="gpt-4o-mini"))
agent.run("Create a TV show", output_schema=TVShow)

For more information see the Input & Output documentation.
​
Pausing and Continuing a Run
An agent run can be paused when a human-in-the-loop flow is initiated. You can then continue the execution of the agent by calling the Agent.continue_run() method. See more details in the Human-in-the-Loop documentation.
​
Cancelling a Run
A run can be cancelled by calling the Agent.cancel_run() method. See more details in the Cancelling a Run documentation.
​
Developer Resources

    View the Agent reference
    View the RunOutput schema
    View Agent Cookbook

Agents
Debugging Agents

Learn how to debug Agno Agents.
Agno comes with a exceptionally well-built debug mode that helps you understand the flow of execution and the intermediate steps. For example:

    Inspect the messages sent to the model and the response it generates.
    Trace intermediate steps and monitor metrics like token usage, execution time, etc.
    Inspect tool calls, errors, and their results. This can help you identify issues with your tools.

​
Debug Mode
To enable debug mode:

    Set the debug_mode parameter on your agent, to enable it for all runs.
    Set the debug_mode parameter on the run method, to enable it for the current run.
    Set the AGNO_DEBUG environment variable to True, to enable debug mode for all agents.

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
    debug_mode=True,
    # debug_level=2, # Uncomment to get more detailed logs
)

# Run agent and print response to the terminal
agent.print_response("Trending startups and products.")

You can set debug_level=2 to get even more detailed logs.
Here’s how it looks:
​
Interactive CLI
Agno also comes with a pre-built interactive CLI that runs your Agent as a command-line application. You can use this to test back-and-forth conversations with your agent:

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[HackerNewsTools()],
    db=SqliteDb(db_file="tmp/data.db"),
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)

# Run agent as an interactive CLI app
agent.cli_app(stream=True)


Basic Flows
Basic Agent Usage

Learn how to initialize and run a very simple agent
1

Create a Python file

touch basic.py

2

Add the following code to your Python file
basic.py

from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
    instructions="You are a helpful assistant. All your responses must be brief and concise.",
)

agent.print_response("What healthy dinner can I have today?")

3

Create a virtual environment
Open the Terminal and create a python virtual environment.

python3 -m venv .venv
source .venv/bin/activate

4

Install libraries

pip install -U agno openai

5

Export your OpenAI API key

  export OPENAI_API_KEY="your_openai_api_key_here"

6

Run Agent

python basic.py

Basic Flows
Basic Async Agent Usage

Learn how to run an agent asynchronously
This example demonstrates how to use Agent.arun() or Agent.aprint_response() to run an agent asynchronously:
1

Create a Python file

touch basic_async.py

2

Add the following code to your Python file
basic_async.py

import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.utils.pprint import apprint_run_response

agent = Agent(
    model=OpenAIChat(id="gpt-5-mini"),
)

async def basic():
    response = await agent.arun(input="Tell me a joke.")
    print(response.content)


async def basic_print():
    await agent.aprint_response(input="Tell me a joke.")


if __name__ == "__main__":
    asyncio.run(basic())
    # OR
    asyncio.run(basic_print())

3

Create a virtual environment
Open the Terminal and create a python virtual environment.

python3 -m venv .venv
source .venv/bin/activate

4

Install libraries

pip install -U agno openai

5

Export your OpenAI API key

  export OPENAI_API_KEY="your_openai_api_key_here"

6

Run Agent

python basic_async.py

Control Plane
Control Plane

The main web interface for interacting with and managing your AgentOS instances
The AgentOS Control Plane is your primary web interface for accessing and managing all AgentOS features. This intuitive dashboard serves as the central hub where you interact with your agents, manage knowledge bases, track sessions, monitor performance, and control user access.
AgentOS Control Plane Dashboard
​
OS Management
Connect and inspect your OS runtimes from a single interface. Switch between local development and live production instances, monitor connection health, and configure endpoints for your different environments.
​
User Management
Manage your organization members and their access to AgentOS features. Configure your organization name, invite team members, and control permissions from a centralized interface.
​
Inviting Members
Add new team members to your organization by entering their email addresses. You can invite multiple users at once by separating emails with commas or pressing Enter/Tab between addresses.
​
Member Roles
Control what each member can access:

    Owner: Full administrative access including billing and member management
    Member: Access to AgentOS features and collaboration capabilities

​
General Settings
Configure your account preferences and organization settings. Access your profile information, manage billing and subscription details, and adjust organization-wide preferences from a centralized settings interface.
​
Feature Access
The control plane provides direct access to all main AgentOS capabilities through an intuitive interface:
Getting Started Tip: The control plane is your gateway to all AgentOS features. Start by connecting your OS instance, then explore each feature section to familiarize yourself with the interface.

Control Plane
Chat Interface

Use AgentOS chat to talk to agents, collaborate with teams, and run workflows
​
Overview
The AgentOS chat is the home for day‑to‑day work with your AI system. From one screen you can:

    Chat with individual agents
    Collaborate with agent teams
    Trigger and monitor workflows
    Review sessions, knowledge, memory, and metrics

It’s designed to feel familiar—type a message, attach files, and get live, streaming responses. Each agent, team, and workflow maintains its own context so you can switch between tasks without losing your place.
​
Chat Interfaces
​
Chat with an Agent

    Select an agent from the right panel.
    Ask a question like “What tools do you have access to?”
    Agents keep their own history, tools, and instructions; switching agents won’t mix contexts.

Learn more about Agents: Dive deeper into agent configuration, tools, memory, and advanced features in our Agents Documentation.
​
Work with a Team

    Switch the top toggle to Teams and pick a team.
    A team delegates tasks to its members and synthesizes their responses into a cohesive response.
    Use the chat stream to watch how the team divides and solves the task.

Learn more about Teams: Explore team modes, coordination strategies, and multi-agent collaboration in our Teams Documentation.
​
Run a Workflow

    Switch to Workflows and choose one.
    Provide the input (plain text or structured, depending on the workflow).
    Watch execution live: steps stream as they start, produce output, and finish.

Learn more about Workflows: Discover workflow types, advanced patterns, and automation strategies in our Workflows Documentation.
​
Troubleshooting

    The page loads but nothing responds: verify your AgentOS app is running.
    Can’t see previous chats: you may be in a new session—open the Sessions panel and pick an older one.
    File didn’t attach: try a common format (png, jpg, pdf, csv, docx, txt, mp3, mp4) and keep size reasonable.

Knowledge
Introduction to Knowledge

Understand why Knowledge is essential for building intelligent, context-aware AI agents that provide accurate, relevant responses.
Imagine an AI agent being asked about a company’s HR policies and, instead of generic advice, returning precise answers based on the actual employee handbook. Or consider a customer support agent that knows specific product details, pricing, and troubleshooting guides. This is the power of Knowledge in Agno.
​
The Problem with Knowledge-Free Agents
Without access to specific information, AI agents can only rely on their general training data. This leads to:

    Generic responses that don’t match your specific context
    Outdated information from training data that’s months or years old
    Hallucinations when the agent guesses at facts it doesn’t actually know
    Limited usefulness for domain-specific tasks or company-specific workflows

​
Real-World Impact
​
Intelligent Text-to-SQL Agents
Build agents that know your exact database schema, column names, and common query patterns. Instead of guessing at table structures, they retrieve the specific schema information needed for each query, ensuring accurate SQL generation.
​
Customer Support Excellence
Create a support agent with access to your complete product documentation, FAQ database, and troubleshooting guides. Customers get accurate answers instantly, without waiting for human agents to look up information.
​
Internal Knowledge Assistant
Deploy an agent that knows your company’s processes, policies, and institutional knowledge. New employees can get onboarding help, and existing team members can quickly find answers to complex procedural questions.

Memory
What is Memory?

Give your agents the ability to remember user preferences, context, and past interactions for truly personalized experiences.
Imagine a customer support agent that remembers your product preferences from last week, or a personal assistant that knows you prefer morning meetings, but only after you’ve had coffee. This is the power of Memory in Agno.
​
How Memory Works
When relevant information appears in a conversation, like a user’s name, preferences, or habits, an Agent with Memory automatically stores it in your database. Later, when that information becomes relevant again, the agent retrieves and uses it naturally in the conversation. The agent is effectively learning about each user across interactions.
Memory ≠ Session History: Memory stores learned user facts (“Sarah prefers email”), session history stores conversation messages for continuity (“what did we just discuss?”).
​
Getting Started with Memory
Setting up memory is straightforward: just connect a database and enable the memory feature. Here’s a basic setup:

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

# Setup your database
db = SqliteDb(db_file="agno.db")

# Setup your Agent with Memory
agent = Agent(
    db=db,
    enable_user_memories=True, # This enables Memory for the Agent
)

With enable_user_memories=True, your agent automatically creates and updates memories after each conversation. It extracts relevant information, stores it, and recalls it when needed, with no manual intervention required.
​
Two Approaches: Automatic vs Agentic Memory
Agno gives you two ways to manage memories, depending on how much control you want the agent to have:
​
Automatic Memory (enable_user_memories=True)
Memories are automatically created and updated after each agent run. Agno handles the extraction, storage, and retrieval behind the scenes. This is the recommended approach for most use cases. It’s reliable and predictable.

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

# Setup your database
db = SqliteDb(db_file="agno.db")

# Setup your Agent with Automatic User Memory
agent = Agent(
    db=db,
    enable_user_memories=True, # Automatic memory management
)

# Memories are automatically created from this conversation
agent.print_response("My name is Sarah and I prefer email over phone calls.")

# And automatically recalled here
agent.print_response("What's the best way to reach me?")

Best for: Customer support, personal assistants, conversational apps where you want consistent memory behavior.
​
Agentic Memory (enable_agentic_memory=True)
The agent gets full control over memory management through built-in tools. It decides when to create, update, or delete memories based on the conversation context.

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

# Setup your database
db = SqliteDb(db_file="agno.db")

# Setup your Agent with Agentic Memory
agent = Agent(
    db=db,
    enable_agentic_memory=True, # This enables Agentic Memory for the Agent
)

With agentic memory, the agent is equipped with tools to manage memories when it deems relevant. This gives more flexibility but requires the agent to make intelligent decisions about what to remember. Best for: Complex workflows, multi-turn interactions where the agent needs to decide what’s worth remembering based on context.
Important: Don’t enable both enable_user_memories and enable_agentic_memory at the same time, as they’re mutually exclusive. While nothing will break if you set both, enable_agentic_memory will always take precedence and enable_user_memories will be ignored.
​
Storage: Where Memories Live
Memories are stored in the database you connect to your agent. Agno supports all major database systems: Postgres, SQLite, MongoDB, and more. Check the Storage documentation for the full list of supported databases and setup instructions. By default, memories are stored in the agno_memories table (or collection, for document databases). If this table doesn’t exist when your agent first tries to store a memory, Agno creates it automatically with no manual schema setup required.
​
Custom Table Names
You can specify a custom table name for storing memories:

from agno.agent import Agent
from agno.db.postgres import PostgresDb

# Setup your database
db = PostgresDb(
    db_url="postgresql://user:password@localhost:5432/my_database",
    memory_table="my_memory_table", # Specify the table to store memories
)

# Setup your Agent with the database
agent = Agent(db=db, enable_user_memories=True)

# Run the Agent. This will store a session in our "my_memory_table"
agent.print_response("Hi! My name is John Doe and I like to play basketball on the weekends.")

agent.print_response("What are my hobbies?")

​
Manual Memory Retrieval
While memories are automatically recalled during conversations, you can also manually retrieve them using the get_user_memories method. This is useful for debugging, displaying user profiles, or building custom memory interfaces:

from agno.agent import Agent
from agno.db.postgres import PostgresDb

# Setup your database
db = PostgresDb(
    db_url="postgresql://user:password@localhost:5432/my_database",
    memory_table="my_memory_table", # Specify the table to store memories
)

# Setup your Agent with the database
agent = Agent(db=db)

# Run the Agent. This will store a memory in our "my_memory_table"
agent.print_response("I love sushi!", user_id="123")

# Retrieve the memories about the user
memories = agent.get_user_memories(user_id="123")
print(memories)

​
Memory Data Model
Each memory stored in your database contains the following fields:
Field	Type	Description
memory_id	str	The unique identifier for the memory.
memory	str	The memory content, stored as a string.
topics	list	The topics of the memory.
input	str	The input that generated the memory.
user_id	str	The user ID of the memory.
agent_id	str	The agent ID of the memory.
team_id	str	The team ID of the memory.
updated_at	int	The timestamp when the memory was last updated.
View and manage all your memories visually through the Memories page in AgentOS/

Sessions
Sessions

Learn about Agno Sessions and how they work.
When you call Agent.run(), it creates a single, stateless interaction. The agent responds to your message and that’s it - no memory of what just happened. But most real applications need conversations, not just one-off exchanges. That’s where sessions come in.
​
What’s a Session?
Think of a session as a conversation thread. It’s a collection of back-and-forth interactions (called “runs”) between a user and your Agent, Team, or Workflow. Each session gets a unique session_id that ties together all the runs, chat history, state, and metrics for that conversation. Here’s the breakdown:

    Session: A multi-turn conversation identified by a session_id. Contains all the runs, history, state, and metrics for that conversation thread.
    Run: A single interaction within a session. Every time you call Agent.run(), Team.run(), or Workflow.run(), a new run_id is created. Think of it as one message-and-response pair in the conversation.

Sessions require a database to store history and state. See Session Storage for setup details.
Workflow sessions work differently: Unlike agent and team sessions that store conversation messages, workflow sessions track complete pipeline executions (runs) with inputs and outputs. Because of these unique characteristics, we’ve created a dedicated Workflow Sessions section that covers workflow-specific features like run-based history, session state, and workflow agents.
​
Single-Run Example
When you run an agent without specifying a session_id, Agno automatically generates both a run_id and a session_id for you:

from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(model=OpenAIChat(id="gpt-4o-mini"))

# Run the agent - Agno auto-generates session_id and run_id
response = agent.run("Tell me a 5 second short story about a robot")
print(response.content)
print(f"Run ID: {response.run_id}")        # Auto-generated UUID
print(f"Session ID: {response.session_id}") # Auto-generated UUID

This creates a new session with a single run. But here’s the catch: without a database configured, there’s no persistence. The session_id exists for this single run, but you can’t continue the conversation later because nothing is saved. To actually use sessions for multi-turn conversations, you need to configure a database (even an InMemoryDb works).
​
Multi-User Conversations
In production, multiple users often talk to the same agent or team simultaneously. Sessions keep those threads isolated:

    user_id distinguishes the person using your product.
    session_id distinguishes conversation threads for that user (think “chat tabs”).
    Conversation history only flows into the run when you enable it via add_history_to_context.

For a full walkthrough that includes persistence, history, and per-user session IDs, follow the Persisting Sessions guide or the Chat History cookbook example.

Metrics
Metrics

Learn about run and session metrics.
When you run an agent, team or workflow in Agno, the response you get includes detailed metrics about the run. These metrics help you understand resource usage (like token usage and duration), performance, and other aspects of the model and tool calls.

Agent Metrics
Agent Metrics

Learn about agent run and session metrics.
When you run an agent in Agno, the response you get (RunOutput) includes detailed metrics about the run. These metrics help you understand resource usage (like token usage and time), performance, and other aspects of the model and tool calls. Metrics are available at multiple levels:

    Per message: Each message (assistant, tool, etc.) has its own metrics.
    Per run: Each RunOutput has its own metrics.
    Per session: The AgentSession contains aggregated session_metrics that are the sum of all RunOutput.metrics for the session.

​
Example Usage
Suppose you have an agent that performs some tasks and you want to analyze the metrics after running it. Here’s how you can access and print the metrics: You run the following code to create an agent and run it with the following configuration:

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.db.sqlite import SqliteDb
from rich.pretty import pprint

agent = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    tools=[DuckDuckGoTools()],
    db=SqliteDb(db_file="tmp/agents.db"),
    markdown=True,
)

run_response = agent.run(
    "What is current news in the world?"
)

# Print metrics per message
if run_response.messages:
    for message in run_response.messages:
        if message.role == "assistant":
            if message.content:
                print(f"Message: {message.content}")
            elif message.tool_calls:
                print(f"Tool calls: {message.tool_calls}")
            print("---" * 5, "Metrics", "---" * 5)
            pprint(message.metrics.to_dict())
            print("---" * 20)

# Print the aggregated metrics for the whole run
print("---" * 5, "Run Metrics", "---" * 5)
pprint(run_response.metrics.to_dict())
# Print the aggregated metrics for the whole session
print("---" * 5, "Session Metrics", "---" * 5)
pprint(agent.get_session_metrics().to_dict())

You’ll see the outputs with following information:

    input_tokens: The number of tokens sent to the model.
    output_tokens: The number of tokens received from the model.
    total_tokens: The sum of input_tokens and output_tokens.
    audio_input_tokens: The number of tokens sent to the model for audio input.
    audio_output_tokens: The number of tokens received from the model for audio output.
    audio_total_tokens: The sum of audio_input_tokens and audio_output_tokens.
    cache_read_tokens: The number of tokens read from the cache.
    cache_write_tokens: The number of tokens written to the cache.
    reasoning_tokens: The number of tokens used for reasoning.
    duration: The duration of the run in seconds.
    time_to_first_token: The time taken until the first token was generated.
    provider_metrics: Any provider-specific metrics.

Team Metrics
Team Metrics

Learn about team run and session metrics.
When you run a team in Agno, the response you get (TeamRunOutput) includes detailed metrics about the run. These metrics help you understand resource usage (like token usage and time), performance, and other aspects of the model and tool calls across both the team leader and team members. Metrics are available at multiple levels:

    Per-message: Each message (assistant, tool, etc.) has its own metrics.
    Per-member run: Each team member run has its own metrics. You can make member runs available on the TeamRunOutput by setting store_member_responses=True,
    Team-level: The TeamRunOutput aggregates metrics across all team leader and team member messages.
    Session-level: Aggregated metrics across all runs in the session, for both the team leader and all team members.

​
Example Usage
Suppose you have a team that performs some tasks and you want to analyze the metrics after running it. Here’s how you can access and print the metrics:

from typing import Iterator

from agno.agent import Agent, RunOutput
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.utils.pprint import pprint_run_response
from rich.pretty import pprint

# Create team members
web_searcher = Agent(
    name="Stock Searcher",
    model=OpenAIChat(id="gpt-5-mini"),
    role="Searches the web for information.",
    tools=[DuckDuckGoTools()],
)

# Create the team
team = Team(
    name="Web Research Team",
    model=OpenAIChat(id="gpt-5-mini"),
    members=[web_searcher],
    markdown=True,
    store_member_responses=True,
)

# Run the team
run_response: TeamRunOutput = team.run(
    "What is going on in the world?"
)
pprint_run_response(run_response, markdown=True)

# Print team leader message metrics
print("---" * 5, "Team Leader Message Metrics", "---" * 5)
if run_response.messages:
    for message in run_response.messages:
        if message.role == "assistant":
            if message.content:
                print(f"Message: {message.content}")
            elif message.tool_calls:
                print(f"Tool calls: {message.tool_calls}")
            print("---" * 5, "Metrics", "---" * 5)
            pprint(message.metrics)
            print("---" * 20)

# Print aggregated team leader metrics
print("---" * 5, "Aggregated Metrics of Team", "---" * 5)
pprint(run_response.metrics)

# Print team leader session metrics
print("---" * 5, "Session Metrics", "---" * 5)
pprint(team.get_session_metrics().to_dict())

# Print team member message metrics
print("---" * 5, "Team Member Message Metrics", "---" * 5)
if run_response.member_responses:
    for member_response in run_response.member_responses:
        if member_response.messages:
            for message in member_response.messages:
                if message.role == "assistant":
                    if message.content:
                        print(f"Member Message: {message.content}")
                    elif message.tool_calls:
                        print(f"Member Tool calls: {message.tool_calls}")
                    print("---" * 5, "Member Metrics", "---" * 5)
                    pprint(message.metrics)
                    print("---" * 20)

You’ll see the outputs with following information:

    input_tokens: The number of tokens sent to the model.
    output_tokens: The number of tokens received from the model.
    total_tokens: The sum of input_tokens and output_tokens.
    audio_input_tokens: The number of tokens sent to the model for audio input.
    audio_output_tokens: The number of tokens received from the model for audio output.
    audio_total_tokens: The sum of audio_input_tokens and audio_output_tokens.
    cache_read_tokens: The number of tokens read from the cache.
    cache_write_tokens: The number of tokens written to the cache.
    reasoning_tokens: The number of tokens used for reasoning.
    duration: The duration of the run in seconds.
    time_to_first_token: The time taken until the first token was generated.
    provider_metrics: Any provider-specific metrics.


Metrics
Workflow Metrics

Learn about Workflow run and session metrics.
When you run a workflow in Agno, the response you get (WorkflowRunOutput) includes detailed metrics about the workflow execution. These metrics help you understand token usage, execution time, performance, and step-level details across all agents, teams, and custom functions in your workflow. Metrics are available at multiple levels:

    Per workflow: Each WorkflowRunOutput includes a metrics object containing the workflow duration.
    Per step: Each step has its own metrics including duration, token usage, and model information.
    Per session: Session metrics aggregate all step-level metrics across all runs in the session.

​
Example Usage
Here’s how you can access and use workflow metrics:

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools
from agno.workflow import Step, Workflow
from rich.pretty import pprint

# Define agents
hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[HackerNewsTools()],
    role="Extract key insights from Hackernews posts",
)

web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    role="Search the web for latest trends",
)

# Define research team
research_team = Team(
    name="Research Team",
    members=[hackernews_agent, web_agent],
    instructions="Research tech topics from Hackernews and the web",
)

content_planner = Agent(
    name="Content Planner",
    model=OpenAIChat(id="gpt-4o"),
    instructions="Plan a content schedule based on research",
)

# Create workflow
workflow = Workflow(
    name="Content Creation Workflow",
    db=SqliteDb(db_file="tmp/workflow.db"),
    steps=[
        Step(name="Research Step", team=research_team),
        Step(name="Content Planning Step", agent=content_planner),
    ],
)

# Run workflow
response = workflow.run(input="AI trends in 2024")

# Print workflow-level metrics
print("Workflow Metrics")
if response.metrics:
    pprint(response.metrics.to_dict())

# Print workflow duration
if response.metrics and response.metrics.duration:
    print(f"\nTotal execution time: {response.metrics.duration:.2f} seconds")

# Print step-level metrics
print("Step Metrics")
if response.metrics:
    for step_name, step_metrics in response.metrics.steps.items():
        print(f"\nStep: {step_name}")
        print(f"Executor: {step_metrics.executor_name} ({step_metrics.executor_type})")
        if step_metrics.metrics:
            print(f"Duration: {step_metrics.metrics.duration:.2f}s")
            print(f"Tokens: {step_metrics.metrics.total_tokens}")

# Print session metrics
print("Session Metrics")
pprint(workflow.get_session_metrics().to_dict())

You’ll see the outputs with following information: Workflow-level metrics:

    duration: Total workflow execution time in seconds (from start to finish, including orchestration overhead)
    steps: Dictionary mapping step names to their individual step metrics

Step-level metrics:

    step_name: Name of the step
    executor_type: Type of executor (“agent”, “team”, or “function”)
    executor_name: Name of the executor
    metrics: Execution metrics including tokens, duration, and model information (see Metrics schema)

Session metrics:

    Aggregates step-level metrics (tokens, duration) across all runs in the session
    Includes only agent/team execution time, not workflow orchestration overhead


Metrics
​
Attributes
Field	Description
input_tokens	Number of tokens in the prompt/input to the model.
output_tokens	Number of tokens generated by the model as output.
total_tokens	Total tokens used (input + output).
audio_input_tokens	Audio tokens in the input.
audio_output_tokens	Audio tokens in the output.
audio_total_tokens	Total audio tokens (if using audio input/output).
cache_read_tokens	Tokens served from cache (if caching is used).
cache_write_tokens	Tokens written to cache.
reasoning_tokens	Tokens used for reasoning steps (if enabled).
time_to_first_token	Time until the first token is generated (in seconds).
duration	Total run time (in seconds).
provider_metrics	Provider-specific metrics (dict).
additional_metrics	Any extra metrics provided by the model/tool (e.g., latency, cost, etc.).

    Note: Not all fields are always present; it depends on the model/tool and the run. 
    
    Runs
RunOutput
​
RunOutput Attributes
Attribute	Type	Default	Description
run_id	Optional[str]	None	Run ID
agent_id	Optional[str]	None	Agent ID for the run
agent_name	Optional[str]	None	Agent name for the run
session_id	Optional[str]	None	Session ID for the run
parent_run_id	Optional[str]	None	Parent run ID
workflow_id	Optional[str]	None	Workflow ID if this run is part of a workflow
user_id	Optional[str]	None	User ID associated with the run
content	Optional[Any]	None	Content of the response
content_type	str	"str"	Specifies the data type of the content
reasoning_content	Optional[str]	None	Any reasoning content the model produced
reasoning_steps	Optional[List[ReasoningStep]]	None	List of reasoning steps
reasoning_messages	Optional[List[Message]]	None	List of reasoning messages
model	Optional[str]	None	The model used in the run
model_provider	Optional[str]	None	The model provider used in the run
messages	Optional[List[Message]]	None	A list of messages included in the response
metrics	Optional[Metrics]	None	Usage metrics of the run
additional_input	Optional[List[Message]]	None	Additional input messages
tools	Optional[List[ToolExecution]]	None	List of tool executions
images	Optional[List[Image]]	None	List of images attached to the response
videos	Optional[List[Video]]	None	List of videos attached to the response
audio	Optional[List[Audio]]	None	List of audio snippets attached to the response
files	Optional[List[File]]	None	List of files attached to the response
response_audio	Optional[Audio]	None	The model’s raw response in audio
input	Optional[RunInput]	None	Input media and messages from user
citations	Optional[Citations]	None	Any citations used in the response
model_provider_data	Optional[Any]	None	Model provider specific metadata
references	Optional[List[MessageReferences]]	None	References used in the response
metadata	Optional[Dict[str, Any]]	None	Metadata associated with the run
created_at	int	Current timestamp	Unix timestamp of the response creation
events	Optional[List[RunOutputEvent]]	None	List of events that occurred during the run
status	RunStatus	RunStatus.running	Status of the run (running, completed, paused, cancelled, error)
workflow_step_id	Optional[str]	None	Workflow step ID (foreign key relationship)
​
RunOutputEvent Types and Attributes
​
Base RunOutputEvent Attributes
All events inherit from BaseAgentRunEvent which provides these common attributes:
Attribute	Type	Default	Description
created_at	int	Current timestamp	Unix timestamp of the event creation
event	str	Event type value	The type of event
agent_id	str	""	ID of the agent generating the event
agent_name	str	""	Name of the agent generating the event
run_id	Optional[str]	None	ID of the current run
session_id	Optional[str]	None	ID of the current session
workflow_id	Optional[str]	None	ID of the workflow if part of workflow execution
workflow_run_id	Optional[str]	None	ID of the workflow run
step_id	Optional[str]	None	ID of the workflow step
step_name	Optional[str]	None	Name of the workflow step
step_index	Optional[int]	None	Index of the workflow step
tools	Optional[List[ToolExecution]]	None	Tools associated with this event
content	Optional[Any]	None	For backwards compatibility
​
RunStartedEvent
Attribute	Type	Default	Description
event	str	"RunStarted"	Event type
model	str	""	The model being used
model_provider	str	""	The provider of the model
​
RunContentEvent
Attribute	Type	Default	Description
event	str	"RunContent"	Event type
content	Optional[Any]	None	The content of the response
content_type	str	"str"	Type of the content
reasoning_content	Optional[str]	None	Reasoning content produced
citations	Optional[Citations]	None	Citations used in the response
model_provider_data	Optional[Any]	None	Model provider specific metadata
response_audio	Optional[Audio]	None	Model’s audio response
image	Optional[Image]	None	Image attached to the response
references	Optional[List[MessageReferences]]	None	References used in the response
additional_input	Optional[List[Message]]	None	Additional input messages
reasoning_steps	Optional[List[ReasoningStep]]	None	Reasoning steps
reasoning_messages	Optional[List[Message]]	None	Reasoning messages
​
RunContentCompletedEvent
Attribute	Type	Default	Description
event	str	"RunContentCompleted"	Event type
​
IntermediateRunContentEvent
Attribute	Type	Default	Description
event	str	"RunIntermediateContent"	Event type
content	Optional[Any]	None	Intermediate content of the response
content_type	str	"str"	Type of the content
​
RunCompletedEvent
Attribute	Type	Default	Description
event	str	"RunCompleted"	Event type
content	Optional[Any]	None	Final content of the response
content_type	str	"str"	Type of the content
reasoning_content	Optional[str]	None	Reasoning content produced
citations	Optional[Citations]	None	Citations used in the response
model_provider_data	Optional[Any]	None	Model provider specific metadata
images	Optional[List[Image]]	None	Images attached to the response
videos	Optional[List[Video]]	None	Videos attached to the response
audio	Optional[List[Audio]]	None	Audio snippets attached to the response
response_audio	Optional[Audio]	None	Model’s audio response
references	Optional[List[MessageReferences]]	None	References used in the response
additional_input	Optional[List[Message]]	None	Additional input messages
reasoning_steps	Optional[List[ReasoningStep]]	None	Reasoning steps
reasoning_messages	Optional[List[Message]]	None	Reasoning messages
metadata	Optional[Dict[str, Any]]	None	Additional metadata
metrics	Optional[Metrics]	None	Usage metrics
​
RunPausedEvent
Attribute	Type	Default	Description
event	str	"RunPaused"	Event type
tools	Optional[List[ToolExecution]]	None	Tools that require confirmation
​
RunContinuedEvent
Attribute	Type	Default	Description
event	str	"RunContinued"	Event type
​
RunErrorEvent
Attribute	Type	Default	Description
event	str	"RunError"	Event type
content	Optional[str]	None	Error message
​
RunCancelledEvent
Attribute	Type	Default	Description
event	str	"RunCancelled"	Event type
reason	Optional[str]	None	Reason for cancellation
​
PreHookStartedEvent
Attribute	Type	Default	Description
event	str	"PreHookStarted"	Event type
pre_hook_name	Optional[str]	None	Name of the pre-hook being executed
run_input	Optional[RunInput]	None	The run input passed to the hook
​
PreHookCompletedEvent
Attribute	Type	Default	Description
event	str	"PreHookCompleted"	Event type
pre_hook_name	Optional[str]	None	Name of the pre-hook that completed
run_input	Optional[RunInput]	None	The run input passed to the hook
​
PostHookStartedEvent
Attribute	Type	Default	Description
event	str	"PostHookStarted"	Event type
post_hook_name	Optional[str]	None	Name of the post-hook being executed
​
PostHookCompletedEvent
Attribute	Type	Default	Description
event	str	"PostHookCompleted"	Event type
post_hook_name	Optional[str]	None	Name of the post-hook that completed
​
ReasoningStartedEvent
Attribute	Type	Default	Description
event	str	"ReasoningStarted"	Event type
​
ReasoningStepEvent
Attribute	Type	Default	Description
event	str	"ReasoningStep"	Event type
content	Optional[Any]	None	Content of the reasoning step
content_type	str	"str"	Type of the content
reasoning_content	str	""	Detailed reasoning content
​
ReasoningCompletedEvent
Attribute	Type	Default	Description
event	str	"ReasoningCompleted"	Event type
content	Optional[Any]	None	Content of the reasoning step
content_type	str	"str"	Type of the content
​
ToolCallStartedEvent
Attribute	Type	Default	Description
event	str	"ToolCallStarted"	Event type
tool	Optional[ToolExecution]	None	The tool being called
​
ToolCallCompletedEvent
Attribute	Type	Default	Description
event	str	"ToolCallCompleted"	Event type
tool	Optional[ToolExecution]	None	The tool that was called
content	Optional[Any]	None	Result of the tool call
images	Optional[List[Image]]	None	Images produced by the tool
videos	Optional[List[Video]]	None	Videos produced by the tool
audio	Optional[List[Audio]]	None	Audio produced by the tool
​
MemoryUpdateStartedEvent
Attribute	Type	Default	Description
event	str	"MemoryUpdateStarted"	Event type
​
MemoryUpdateCompletedEvent
Attribute	Type	Default	Description
event	str	"MemoryUpdateCompleted"	Event type
​
SessionSummaryStartedEvent
Attribute	Type	Default	Description
event	str	"SessionSummaryStarted"	Event type
​
SessionSummaryCompletedEvent
Attribute	Type	Default	Description
event	str	"SessionSummaryCompleted"	Event type
session_summary	Optional[SessionSummary]	None	The generated session summary
​
ParserModelResponseStartedEvent
Attribute	Type	Default	Description
event	str	"ParserModelResponseStarted"	Event type
​
ParserModelResponseCompletedEvent
Attribute	Type	Default	Description
event	str	"ParserModelResponseCompleted"	Event type
​
OutputModelResponseStartedEvent
Attribute	Type	Default	Description
event	str	"OutputModelResponseStarted"	Event type
​
OutputModelResponseCompletedEvent
Attribute	Type	Default	Description
event	str	"OutputModelResponseCompleted"	Event type
​
CustomEvent
Attribute	Type	Default	Description
event	str	"CustomEvent"	Event type


