// Queries for PC part recommendation system

// Query to add components to the database

CREATE
  (cpu1:CPU {id: 'cpu1', brand: 'Intel', model: 'i7-10700K', cores: 8, threads: 16, base_clock: 3.8, boost_clock: 5.1, tdp: 125}),
  (cpu2:CPU {id: 'cpu2', brand: 'AMD', model: 'Ryzen 7 5800X', cores: 8, threads: 16, base_clock: 3.8, boost_clock: 4.7, tdp: 105}),
  (gpu1:GPU {id: 'gpu1', brand: 'NVIDIA', model: 'RTX 3080', vram: 10, base_clock: 1440, boost_clock: 1710, tdp: 320}),
  (gpu2:GPU {id: 'gpu2', brand: 'AMD', model: 'Radeon RX 6800 XT', vram: 16, base_clock: 1825, boost_clock: 2250, tdp: 300}),
  (ram1:RAM {id: 'ram1', brand: 'Corsair', model: 'Vengeance LPX', capacity_gb: 16, speed_mhz: 3200, type: 'DDR4'}),
  (ram2:RAM {id: 'ram2', brand: 'G.Skill', model: 'Trident Z RGB', capacity_gb: 32, speed_mhz: 3600, type: 'DDR4'}),
  (mb1:MOTHERBOARD {id: 'mb1', brand: 'ASUS', model: 'ROG Strix Z490-E', socket: 'LGA1200', form_factor: 'ATX'}),
  (mb2:MOTHERBOARD {id: 'mb2', brand: 'MSI', model: 'MAG B550 TOMAHAWK', socket: 'AM4', form_factor: 'ATX'});

// Query to add an order

CREATE
  (order1:Order {id: 'order1', customer_name: 'John Doe', order_date: date('2024-06-15'), status: 'Processing'}),
  (order2:Order {id: 'order2', customer_name: 'Jane Smith', order_date: date('2024-06-16'), status: 'Shipped'});

// Query to add component to a build

MATCH (o:Order {id: 'order1'}), (c:CPU {id: 'cpu1'})
CREATE (o)-[:INCLUDES]->(c);

MATCH (p:{part_type} {part_id: $part_id}), (n) WHERE NOT (n:Build) AND NOT (n:{part_type}) RETURN FALSE