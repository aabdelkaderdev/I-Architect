<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop -->

Modulev1.2.13 (latest)●Since v0.3

# human\_in\_the\_loop

Human in the loop middleware.

## Attributes

[attribute

ResponseT](/python/langchain/agents/middleware/human_in_the_loop/ResponseT)[attribute

StateT](/python/langchain/agents/middleware/human_in_the_loop/StateT)[attribute

DecisionType: Literal['approve', 'edit', 'reject']](/python/langchain/agents/middleware/human_in_the_loop/DecisionType)

## Classes

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/human_in_the_loop/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/human_in_the_loop/AgentState)[class

Action

Represents an action with a name and args.](/python/langchain/agents/middleware/human_in_the_loop/Action)[class

ActionRequest

Represents an action request with a name, args, and description.](/python/langchain/agents/middleware/human_in_the_loop/ActionRequest)[class

ReviewConfig

Policy for reviewing a HITL request.](/python/langchain/agents/middleware/human_in_the_loop/ReviewConfig)[class

HITLRequest

Request for human feedback on a sequence of actions requested by a model.](/python/langchain/agents/middleware/human_in_the_loop/HITLRequest)[class

ApproveDecision

Response when a human approves the action.](/python/langchain/agents/middleware/human_in_the_loop/ApproveDecision)[class

EditDecision

Response when a human edits the action.](/python/langchain/agents/middleware/human_in_the_loop/EditDecision)[class

RejectDecision

Response when a human rejects the action.](/python/langchain/agents/middleware/human_in_the_loop/RejectDecision)[class

HITLResponse

Response payload for a HITLRequest.](/python/langchain/agents/middleware/human_in_the_loop/HITLResponse)[class

InterruptOnConfig

Configuration for an action requiring human in the loop.

This is the configuration format used in the `HumanInTheLoopMiddleware.__init__`
method.](/python/langchain/agents/middleware/human_in_the_loop/InterruptOnConfig)[class

HumanInTheLoopMiddleware

Human in the loop middleware.](/python/langchain/agents/middleware/human_in_the_loop/HumanInTheLoopMiddleware)

## Type Aliases

[typeAlias

Decision](/python/langchain/agents/middleware/human_in_the_loop/Decision)


