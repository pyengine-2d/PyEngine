from pyengine import Window, const, Controls, ControlType, WindowCallbacks
from pyengine.Entities import Entity
from pyengine.Components import PositionComponent, SpriteComponent, PhysicsComponent, MoveComponent, ControlComponent
from pyengine.Systems import EntitySystem
from pyengine.Utils import Colors, Vec2
from random import randint


class Jeu:
    def __init__(self):
        self.window = Window(800, 400, Colors.WHITE.value)
        self.window.title = "Pong"

        self.window.set_callback(WindowCallbacks.OUTOFWINDOW, self.outofwindow)

        self.j1 = Entity()
        self.j1.add_component(PositionComponent(Vec2(10, 175)))
        spritej1 = self.j1.add_component(SpriteComponent("images/sprite0.png"))
        spritej1.size = Vec2(20, 50)
        controlj1 = self.j1.add_component(ControlComponent(ControlType.UPDOWN, 3))
        controlj1.set_control(Controls.UPJUMP, const.K_w)
        controlj1.set_control(Controls.DOWN, const.K_s)
        self.j1.add_component(PhysicsComponent(False))

        self.j2 = Entity()
        self.j2.add_component(PositionComponent(Vec2(770, 175)))
        spritej2 = self.j2.add_component(SpriteComponent("images/sprite0.png"))
        spritej2.size = Vec2(20, 50)
        controlj2 = self.j2.add_component(ControlComponent(ControlType.UPDOWN, 3))
        controlj2.set_control(Controls.UPJUMP, const.K_UP)
        controlj2.set_control(Controls.DOWN, const.K_DOWN)
        self.j2.add_component(PhysicsComponent(False))

        self.ball = Entity()
        self.ball.add_component(PositionComponent(Vec2(390, 190)))
        spriteballe = self.ball.add_component(SpriteComponent("images/sprite0.png"))
        spriteballe.size = Vec2(20, 20)
        physball = self.ball.add_component(PhysicsComponent(False))
        physball.callback = self.collision
        self.ball.add_component(MoveComponent(Vec2(randint(50, 100), randint(50, 100))))

        entitysystem = self.window.world.get_system(EntitySystem)
        entitysystem.add_entity(self.j1)
        entitysystem.add_entity(self.j2)
        entitysystem.add_entity(self.ball)

        self.window.run()

    def collision(self, entity, others, space, data):
        move = entity.get_component(MoveComponent)
        move.direction = Vec2(-move.direction.x, move.direction.y)

    def outofwindow(self, obj, pos):
        if obj == self.j1:
            position = self.j1.get_component(PositionComponent)
            if pos.y <= obj.rect.height / 2:
                position.position = Vec2(10, obj.rect.height / 2)
            else:
                position.position = Vec2(10, 400 - obj.rect.height / 2)

        elif obj == self.j2:
            position = self.j2.get_component(PositionComponent)
            if pos.y <= obj.rect.height / 2:
                position.position = Vec2(770, obj.rect.height / 2)
            else:
                position.position = Vec2(770, 400 - obj.rect.height / 2)

        else:
            if pos.x < 10 or pos.x > 790:
                position = self.ball.get_component(PositionComponent)
                position.position = Vec2(390, 190)
                self.ball.get_component(MoveComponent).direction = Vec2(randint(50, 100), randint(50, 100))
            else:
                move = self.ball.get_component(MoveComponent)
                move.direction = Vec2(move.direction.x, -move.direction.y)


Jeu()
