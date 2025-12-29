import os
from dotenv import load_dotenv
load_dotenv(override=True)
print("LIVEKIT_URL=", os.getenv("LIVEKIT_URL"))

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import google
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION
            )

room_input_Options = RoomInputOptions()

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            voice="charon"
        )
    )

   
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions,
        ),

    await ctx.connect()

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

