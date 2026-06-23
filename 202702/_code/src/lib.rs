use std::any::{Any, TypeId};
use std::collections::HashMap;

// ---- Entity ----

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Entity(u64);

impl Entity {
    pub fn id(&self) -> u64 {
        self.0
    }
}

// ---- Component storage ----

trait ComponentVec: Any {
    fn as_any(&self) -> &dyn Any;
    fn as_any_mut(&mut self) -> &mut dyn Any;
    fn push_none(&mut self);
    fn len(&self) -> usize;
}

impl<T: 'static> ComponentVec for Vec<Option<T>> {
    fn as_any(&self) -> &dyn Any {
        self
    }
    fn as_any_mut(&mut self) -> &mut dyn Any {
        self
    }
    fn push_none(&mut self) {
        self.push(None);
    }
    fn len(&self) -> usize {
        self.len()
    }
}

// ---- World ----

pub struct World {
    next_id: u64,
    entities: Vec<Entity>,
    components: HashMap<TypeId, Box<dyn ComponentVec>>,
}

impl World {
    pub fn new() -> Self {
        World {
            next_id: 0,
            entities: Vec::new(),
            components: HashMap::new(),
        }
    }

    pub fn spawn(&mut self) -> Entity {
        let id = self.next_id;
        self.next_id += 1;
        let entity = Entity(id);
        self.entities.push(entity);
        for (_, storage) in self.components.iter_mut() {
            storage.push_none();
        }
        entity
    }

    pub fn add_component<T: 'static>(&mut self, entity: Entity, component: T) {
        let idx = self.entity_index(entity).expect("entity not found");
        let storage = self.components
            .entry(TypeId::of::<T>())
            .or_insert_with(|| {
                let mut v: Vec<Option<T>> = Vec::with_capacity(1024);
                v.resize_with(self.entities.len(), || None);
                Box::new(v)
            });
        let storage = storage.as_any_mut().downcast_mut::<Vec<Option<T>>>().unwrap();
        if idx >= storage.len() {
            storage.resize_with(idx + 1, || None);
        }
        storage[idx] = Some(component);
    }

    pub fn get_component<T: 'static>(&self, entity: Entity) -> Option<&T> {
        let idx = self.entity_index(entity)?;
        let storage = self.components.get(&TypeId::of::<T>())?;
        let storage = storage.as_any().downcast_ref::<Vec<Option<T>>>()?;
        storage.get(idx)?.as_ref()
    }

    pub fn get_component_mut<T: 'static>(&mut self, entity: Entity) -> Option<&mut T> {
        let idx = self.entity_index(entity)?;
        let storage = self.components.get_mut(&TypeId::of::<T>())?;
        let storage = storage.as_any_mut().downcast_mut::<Vec<Option<T>>>()?;
        storage.get_mut(idx)?.as_mut()
    }

    fn entity_index(&self, entity: Entity) -> Option<usize> {
        self.entities.iter().position(|e| *e == entity)
    }
}

// ---- Query ----

pub struct Query<'w, 's, T> {
    storage: &'s Vec<Option<T>>,
    entities: &'w [Entity],
}

impl<'w, 's, T: 'static> Query<'w, 's, T> {
    pub fn iter(&self) -> impl Iterator<Item = (Entity, &T)> {
        self.entities.iter().enumerate().filter_map(move |(idx, entity)| {
            self.storage.get(idx)?.as_ref().map(|c| (*entity, c))
        })
    }
}

pub struct QueryMut<'w, 's, T> {
    storage: &'s mut Vec<Option<T>>,
    entities: &'w [Entity],
}

impl<'w, 's, T: 'static> QueryMut<'w, 's, T> {
    pub fn iter_mut(&mut self) -> impl Iterator<Item = (Entity, &mut T)> {
        let ptr = self.storage.as_mut_ptr();
        let len = self.storage.len();
        let entities = self.entities;
        (0..len).filter_map(move |idx| {
            let cell = unsafe { &mut *ptr.add(idx) };
            cell.as_mut().map(|c| (entities[idx], c))
        })
    }
}

pub fn query<'w, 's, T: 'static>(world: &'w World, storage: &'s Vec<Option<T>>) -> Query<'w, 's, T> {
    Query { storage, entities: &world.entities }
}

pub fn query_mut<'w, 's, T: 'static>(
    world: &'w World, storage: &'s mut Vec<Option<T>>,
) -> QueryMut<'w, 's, T> {
    QueryMut { storage, entities: &world.entities }
}

// ---- System trait ----

pub trait System {
    fn run(&mut self, world: &mut World);
}

// ---- Game loop ----

pub struct GameLoop {
    world: World,
    systems: Vec<Box<dyn System>>,
    running: bool,
}

impl GameLoop {
    pub fn new() -> Self {
        GameLoop {
            world: World::new(),
            systems: Vec::new(),
            running: false,
        }
    }

    pub fn add_system(&mut self, system: impl System + 'static) {
        self.systems.push(Box::new(system));
    }

    pub fn world(&mut self) -> &mut World {
        &mut self.world
    }

    pub fn run(&mut self) {
        self.running = true;
        let mut frame = 0u64;
        while self.running && frame < 120 {
            println!("--- frame {} ---", frame);
            for system in &mut self.systems {
                system.run(&mut self.world);
            }
            frame += 1;
        }
    }

    pub fn stop(&mut self) {
        self.running = false;
    }
}

// ---- Demo components ----

pub struct Position {
    pub x: f32,
    pub y: f32,
}

pub struct Velocity {
    pub dx: f32,
    pub dy: f32,
}

pub struct Health(pub i32);

pub struct Enemy;

// ---- Demo systems ----

pub struct MovementSystem;

impl System for MovementSystem {
    fn run(&mut self, world: &mut World) {
        // Collect velocity snapshots to avoid borrow conflicts
        let snapshots: Vec<(Entity, f32, f32)> = {
            let vel_type = TypeId::of::<Velocity>();
            let vel_storage = world.components.get(&vel_type);
            let vel_storage = vel_storage.and_then(|s| {
                s.as_any().downcast_ref::<Vec<Option<Velocity>>>()
            });
            if vel_storage.is_none() { return; }
            let vel_storage = vel_storage.unwrap();
            world.entities.iter().enumerate().filter_map(|(idx, entity)| {
                vel_storage.get(idx)?.as_ref()
                    .map(|v| (*entity, v.dx, v.dy))
            }).collect::<Vec<_>>()
        };
        for (entity, dx, dy) in &snapshots {
            if let Some(pos) = world.get_component_mut::<Position>(*entity) {
                pos.x += dx;
                pos.y += dy;
            }
        }
    }
}

pub struct HealthSystem;

impl System for HealthSystem {
    fn run(&mut self, world: &mut World) {
        let hp_storage = world.components.get_mut(&TypeId::of::<Health>());
        let hp_storage = hp_storage.map(|s| {
            s.as_any_mut().downcast_mut::<Vec<Option<Health>>>().unwrap()
        });
        if let Some(hp_storage) = hp_storage {
            for hp in hp_storage.iter_mut().flatten() {
                if hp.0 > 0 {
                    hp.0 -= 1;
                }
            }
        }
    }
}

pub struct StatusSystem;

impl System for StatusSystem {
    fn run(&mut self, world: &mut World) {
        let (pos, hp) = {
            let pos_storage = world.components.get(&TypeId::of::<Position>());
            let hp_storage = world.components.get(&TypeId::of::<Health>());
            let pos = pos_storage.and_then(|s| s.as_any().downcast_ref::<Vec<Option<Position>>>());
            let hp = hp_storage.and_then(|s| s.as_any().downcast_ref::<Vec<Option<Health>>>());
            (pos, hp)
        };
        if let (Some(pos), Some(hp)) = (pos, hp) {
            for idx in 0..pos.len().min(hp.len()) {
                let p = pos[idx].as_ref();
                let h = hp[idx].as_ref();
                if let (Some(p), Some(h)) = (p, h) {
                    println!("  entity[{}] pos=({:.1},{:.1}) hp={}",
                        idx, p.x, p.y, h.0);
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_spawn_entity() {
        let mut world = World::new();
        let e = world.spawn();
        assert!(e.id() == 0);
    }

    #[test]
    fn test_add_component() {
        let mut world = World::new();
        let e = world.spawn();
        world.add_component(e, Position { x: 10.0, y: 20.0 });
        let pos = world.get_component::<Position>(e);
        assert!(pos.is_some());
        assert_eq!(pos.unwrap().x, 10.0);
    }

    #[test]
    fn test_mutate_component() {
        let mut world = World::new();
        let e = world.spawn();
        world.add_component(e, Health(100));
        {
            let hp = world.get_component_mut::<Health>(e).unwrap();
            hp.0 -= 10;
        }
        let hp = world.get_component::<Health>(e).unwrap();
        assert_eq!(hp.0, 90);
    }

    #[test]
    fn test_multiple_entities() {
        let mut world = World::new();
        let e1 = world.spawn();
        let e2 = world.spawn();
        world.add_component(e1, Position { x: 0.0, y: 0.0 });
        world.add_component(e2, Position { x: 5.0, y: 5.0 });
        world.add_component(e1, Velocity { dx: 1.0, dy: 0.0 });
        assert_eq!(world.entity_index(e1), Some(0));
        assert_eq!(world.entity_index(e2), Some(1));
    }

    #[test]
    fn test_query() {
        let mut world = World::new();
        let e = world.spawn();
        world.add_component(e, Position { x: 1.0, y: 2.0 });

        let storage = world.components.get(&TypeId::of::<Position>())
            .unwrap().as_any().downcast_ref::<Vec<Option<Position>>>().unwrap();
        let q = query(&world, storage);
        let results: Vec<_> = q.iter().collect();
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].1.x, 1.0);
    }

    #[test]
    fn test_movement_system() {
        let mut world = World::new();
        let e = world.spawn();
        world.add_component(e, Position { x: 0.0, y: 0.0 });
        world.add_component(e, Velocity { dx: 2.0, dy: 3.0 });

        let mut system = MovementSystem;
        system.run(&mut world);

        let pos = world.get_component::<Position>(e).unwrap();
        assert!((pos.x - 2.0).abs() < 1e-6);
        assert!((pos.y - 3.0).abs() < 1e-6);
    }

    #[test]
    fn test_health_system() {
        let mut world = World::new();
        let e = world.spawn();
        world.add_component(e, Health(5));
        world.add_component(e, Enemy);

        let mut system = HealthSystem;
        system.run(&mut world);
        system.run(&mut world);

        let hp = world.get_component::<Health>(e).unwrap();
        assert_eq!(hp.0, 3);
    }

    #[test]
    fn test_game_loop() {
        let mut game = GameLoop::new();
        let e = game.world().spawn();
        game.world().add_component(e, Position { x: 0.0, y: 0.0 });
        game.world().add_component(e, Velocity { dx: 1.0, dy: 0.5 });
        game.world().add_component(e, Health(3));
        game.add_system(MovementSystem);
        game.add_system(HealthSystem);
        game.run();
        let pos = game.world().get_component::<Position>(e).unwrap();
        assert!((pos.x - 120.0).abs() < 1e-6, "x={}", pos.x);
        assert!((pos.y - 60.0).abs() < 1e-6, "y={}", pos.y);
    }

    #[test]
    fn test_no_component_for_entity() {
        let mut world = World::new();
        let e = world.spawn();
        let comp = world.get_component::<Health>(e);
        assert!(comp.is_none());
    }

    #[test]
    fn test_entity_index_order() {
        let mut world = World::new();
        let e1 = world.spawn();
        let e2 = world.spawn();
        let e3 = world.spawn();
        assert_eq!(world.entity_index(e1), Some(0));
        assert_eq!(world.entity_index(e2), Some(1));
        assert_eq!(world.entity_index(e3), Some(2));
    }
}
