from models import Pipe, PipeGap

class CreatePipeResult:
    top_pipe: None
    bottom_pipe: None
    pipe_gap: None

    def __init__(self, top_pipe: Pipe, bottom_pipe: Pipe, pipe_gap: PipeGap):
        self.top_pipe = top_pipe
        self.bottom_pipe = bottom_pipe
        self.pipe_gap = pipe_gap