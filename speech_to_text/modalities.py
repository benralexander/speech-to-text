import eel
import queue
import string

from .utils.shared_types import State, OutputSpec
from speech_to_text.websoket_server import WebSocketServer

from typing import NamedTuple
from faster_whisper import WhisperModel






class States() :
    def __init__(self):
        self.current_states = {State.NORMAL}
        self.error_msg = "All quiet on the western front..."


class Modalalities():
    def __init__(self):
        self.modes = States()

    def has(self,state:State)->bool:
        return state in self.modes.current_states

    def modify_by_state(self,in_str:str) -> str | None:
        ret_val = None
        if self.has(State.ERROR):
            print("We are in error state: {self.error_msg}")
            return ret_val
        if self.has(State.ASLEEP):
            return None
        ret_val = in_str
        if self.has(State.ALL_CAPS):
            ret_val = ret_val.upper()
        if self.has(State.NO_CAPS):
            ret_val = ret_val.lower()
        if not self.has(State.ALLOW_PUNCTUATION):
            pass
            #ret_val = str.maketrans('', '', string.punctuation)
        if  self.has(State.DEFINE_PYTHON_VAR):
            ret_val = "_".join(ret_val.lower().split(" "))
        return ret_val



    def generate_output(self, in_str: str, output:OutputSpec,webSocketServer: WebSocketServer) ->  None:
        if in_str is None or len(in_str)==0:
            return

        if output.include_debug:
            eel.display_transcription(in_str)

        if output.emulate_keyboard:
            output.keyboard.type(in_str)

        # if output.include_websocket is not None:
        #     await webSocketServer.send_message(in_str)


    def add_state(self,state:State)->None:
        if state in self.modes.current_states :
            eel.display_transcription("Note: tried to add {state}, but it was aleady set.")
        else:
            self.modes.current_states.add(state)

    def remove_state(self,state:State)->None:
        if state not in self.modes.current_states :
            return
        else:
            self.modes.current_states.remove(state)




    def look_for_state_change(self, in_str: str,output:OutputSpec ) -> bool:
        if self.modes.current_states is None or len(self.modes.current_states) == 0:
            raise Exception(f"Fatal error: current modality is {'empty' if len(self.modes.current_states) else 'None'}")
        elif in_str is None or len(in_str) == 0:
            return False
        else:
            if output.include_debug and self.has(State.ASLEEP):
                eel.display_transcription("sorry, but currently snoozing...")
            raw_text = in_str.translate(str.maketrans('', '', string.punctuation)).lower().strip()
            match raw_text:
                case "set all caps":
                    self.add_state(State.ALL_CAPS)
                    self.remove_state(State.CAP_FIRST_LETTER)
                    return False
                case "set no caps":
                    self.remove_state(State.ALL_CAPS)
                    self.remove_state(State.CAP_FIRST_LETTER)
                    return False
                case "cap first letter":
                    self.remove_state(State.ALL_CAPS)
                    self.add_state(State.CAP_FIRST_LETTER)
                    return len("cap first letter") <  raw_text
                case "cap first letter" | "define python variable":
                    self.remove_state(State.ALL_CAPS)
                    self.add_state(State.CAP_FIRST_LETTER)
                    return len("go to sleep") < raw_text
                case "allow punctuation":
                    self.remove_state(State.ALL_CAPS)
                    self.remove_state(State.CAP_FIRST_LETTER)
                case "go to sleep":
                    self.add_state(State.ASLEEP)
                    if output.include_debug:
                        eel.display_transcription("we just went to sleep")
                    return False
                case "wake up":
                    self.remove_state(State.ASLEEP)
                    if output.include_debug:
                        eel.display_transcription("we just woke up")

                    return False
                case _:
                    return True
            return True



    def process_speech(self, outputSpec: OutputSpec, webSocketServer: WebSocketServer, segments) -> str | None:
        ret_val = None
        for segment in segments:
            in_str = segment.text

            something_to_print = self.look_for_state_change(in_str,outputSpec)

            if something_to_print:
                self.generate_output(self.modify_by_state(in_str),outputSpec,webSocketServer)



