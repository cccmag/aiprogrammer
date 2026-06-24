use mini_ecs::*;

fn main() {
    println!("=== mini-ecs: Entity Component System Demo ===\n");

    let mut game = GameLoop::new();

    let player = game.world().spawn();
    game.world().add_component(player, Position { x: 0.0, y: 0.0 });
    game.world().add_component(player, Velocity { dx: 1.5, dy: 0.8 });
    game.world().add_component(player, Health(10));

    let enemy = game.world().spawn();
    game.world().add_component(enemy, Position { x: 50.0, y: 30.0 });
    game.world().add_component(enemy, Velocity { dx: -0.5, dy: -0.3 });
    game.world().add_component(enemy, Health(5));
    game.world().add_component(enemy, Enemy);

    let npc = game.world().spawn();
    game.world().add_component(npc, Position { x: 20.0, y: 15.0 });
    game.world().add_component(npc, Health(3));

    game.add_system(MovementSystem);
    game.add_system(HealthSystem);
    game.add_system(StatusSystem);

    game.run();

    println!("\n=== demo completed ===");
}
