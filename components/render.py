from render_order import RenderOrder
class RenderData:
    def __init__(self, char, color, render_order: RenderOrder):
        self.char = char
        self.color = color
        self.render_order = render_order