from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory
from core.cli_chat import CliChat
import json
from pyboxen import boxen


class CliApp:
    def __init__(self, agent: CliChat):
        self.agent = agent
        self.history = InMemoryHistory()
        self.session = PromptSession(
            history=self.history,
            style=Style.from_dict(
                {
                    "prompt": "#aaaaaa",
                    "completion-menu.completion": "bg:#222222 #ffffff",
                    "completion-menu.completion.current": "bg:#444444 #ffffff",
                }
            ),
            complete_while_typing=True,
            complete_in_thread=True,
        )

    async def initialize(self):
        pass

    async def run(self):
        while True:
            try:
                user_input = await self.session.prompt_async("> ")
                if not user_input.strip():
                    continue

                print()

                tool_calls = {}
                response_text = ""

                async def handle_event(event):
                    nonlocal response_text
                    if hasattr(event, "type"):
                        if event.type == "content_block_delta":
                            if hasattr(event, "delta") and hasattr(
                                event.delta, "type"
                            ):
                                if event.delta.type == "text_delta":
                                    response_text += event.delta.text
                                    print(event.delta.text, end="", flush=True)
                                elif event.delta.type == "input_json_delta":
                                    # Track tool call arguments as they stream
                                    index = event.index
                                    if index not in tool_calls:
                                        tool_calls[index] = {
                                            "name": "",
                                            "args": "",
                                        }
                                    tool_calls[index]["args"] += (
                                        event.delta.partial_json
                                    )
                        elif event.type == "content_block_start":
                            if hasattr(event, "content_block") and hasattr(
                                event.content_block, "type"
                            ):
                                if event.content_block.type == "tool_use":
                                    print()  # New line before tool call
                                    # Store tool name but don't print yet
                                    index = getattr(event, "index", 0)
                                    if index not in tool_calls:
                                        tool_calls[index] = {
                                            "name": "",
                                            "args": "",
                                        }
                                    tool_calls[index]["name"] = (
                                        event.content_block.name
                                    )
                        elif event.type == "content_block_stop":
                            if event.index in tool_calls:
                                tool_name = tool_calls[event.index]["name"]
                                args_json = tool_calls[event.index]["args"]

                                try:
                                    parsed_args = json.loads(args_json)
                                    formatted_args = json.dumps(
                                        parsed_args, indent=2
                                    )
                                    tool_content = f"🔧 {tool_name}\n\nArguments:\n{formatted_args}"
                                except (
                                    json.JSONDecodeError,
                                    TypeError,
                                    ValueError,
                                ):
                                    tool_content = f"🔧 {tool_name}\n\nArguments: {args_json}"

                                tool_box = boxen(
                                    tool_content,
                                    title="Tool Call",
                                    style="rounded",
                                    color="blue",
                                    padding=0,
                                )
                                print(tool_box)
                                del tool_calls[event.index]

                await self.agent.run(
                    user_input, stream=True, on_event=handle_event
                )

                print()  # Add newline after everything

            except KeyboardInterrupt:
                break
