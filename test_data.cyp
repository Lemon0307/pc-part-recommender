// Create CPU nodes
CREATE (cpu1:CPU {id: 'cpu_1', name: 'Intel Core i9-13900K', manufacturer: 'Intel', price: 589.99, quantity: 15, cores: 24, threads: 32, baseClock: 3.0, boostClock: 5.8, l2Cache: 32, l3Cache: 36, tdp: 253, socket: 'LGA1700'})
CREATE (cpu2:CPU {id: 'cpu_2', name: 'Intel Core i7-13700K', manufacturer: 'Intel', price: 419.99, quantity: 22, cores: 16, threads: 24, baseClock: 3.4, boostClock: 5.4, l2Cache: 24, l3Cache: 30, tdp: 253, socket: 'LGA1700'})
CREATE (cpu3:CPU {id: 'cpu_3', name: 'AMD Ryzen 9 7950X', manufacturer: 'AMD', price: 549.99, quantity: 18, cores: 16, threads: 32, baseClock: 4.5, boostClock: 5.7, l2Cache: 16, l3Cache: 64, tdp: 170, socket: 'AM5'})
CREATE (cpu4:CPU {id: 'cpu_4', name: 'AMD Ryzen 7 7700X', manufacturer: 'AMD', price: 299.99, quantity: 25, cores: 8, threads: 16, baseClock: 4.5, boostClock: 5.4, l2Cache: 8, l3Cache: 32, tdp: 105, socket: 'AM5'})

// Create GPU nodes
CREATE (gpu1:GPU {id: 'gpu_1', name: 'NVIDIA RTX 4090', manufacturer: 'NVIDIA', price: 1699.99, quantity: 8, chipset: 'AD102', vram: 24, memoryType: 'GDDR6X', coreClock: 2.23, baseClock: 2.23, gpuInterface: 'PCIe 4.0', length: 336, tdp: 450, hdmi: 2, displayPort: 3, fans: 3})
CREATE (gpu2:GPU {id: 'gpu_2', name: 'NVIDIA RTX 4080', manufacturer: 'NVIDIA', price: 1199.99, quantity: 12, chipset: 'AD104', vram: 16, memoryType: 'GDDR6X', coreClock: 2.51, baseClock: 2.51, gpuInterface: 'PCIe 4.0', length: 320, tdp: 320, hdmi: 2, displayPort: 3, fans: 3})
CREATE (gpu3:GPU {id: 'gpu_3', name: 'AMD Radeon RX 7900 XT', manufacturer: 'AMD', price: 799.99, quantity: 14, chipset: 'RDNA 3', vram: 20, memoryType: 'GDDR6', coreClock: 2.5, baseClock: 2.5, gpuInterface: 'PCIe 4.0', length: 280, tdp: 420, hdmi: 1, displayPort: 3, fans: 3})
CREATE (gpu4:GPU {id: 'gpu_4', name: 'NVIDIA RTX 4070', manufacturer: 'NVIDIA', price: 599.99, quantity: 20, chipset: 'AD104', vram: 12, memoryType: 'GDDR6', coreClock: 2.61, baseClock: 2.61, gpuInterface: 'PCIe 4.0', length: 243, tdp: 200, hdmi: 2, displayPort: 3, fans: 2})

// Create Motherboard nodes
CREATE (mobo1:Motherboard {id: 'mobo_1', name: 'ASUS ROG MAXIMUS Z790-E', manufacturer: 'ASUS', price: 349.99, quantity: 16, socket: 'LGA1700', chipset: 'Z790', formFactor: 'ATX', maxMemory: 192, memorySlots: 4, memoryType: 'DDR5', pciSlots: 5, sataPort: 6, m2Slots: 5, wifi: true})
CREATE (mobo2:Motherboard {id: 'mobo_2', name: 'MSI MPG B850E-E64 EDGE', manufacturer: 'MSI', price: 299.99, quantity: 19, socket: 'AM5', chipset: 'B850E', formFactor: 'ATX', maxMemory: 192, memorySlots: 4, memoryType: 'DDR5', pciSlots: 5, sataPort: 4, m2Slots: 4, wifi: true})
CREATE (mobo3:Motherboard {id: 'mobo_3', name: 'GIGABYTE B860M-K', manufacturer: 'GIGABYTE', price: 129.99, quantity: 24, socket: 'LGA1700', chipset: 'B860', formFactor: 'MicroATX', maxMemory: 192, memorySlots: 2, memoryType: 'DDR5', pciSlots: 3, sataPort: 4, m2Slots: 2, wifi: false})
CREATE (mobo4:Motherboard {id: 'mobo_4', name: 'ASRock B850M-HDV', manufacturer: 'ASRock', price: 99.99, quantity: 28, socket: 'AM5', chipset: 'B850', formFactor: 'MicroATX', maxMemory: 192, memorySlots: 2, memoryType: 'DDR5', pciSlots: 2, sataPort: 4, m2Slots: 2, wifi: false})

// Create RAM nodes
CREATE (ram1:RAM {id: 'ram_1', name: 'Corsair Vengeance DDR5 64GB', manufacturer: 'Corsair', price: 249.99, quantity: 20, type: 'DDR5', speed: 6000, modules: 2, cas: 30})
CREATE (ram2:RAM {id: 'ram_2', name: 'G.Skill Trident Z5 32GB', manufacturer: 'G.Skill', price: 129.99, quantity: 26, type: 'DDR5', speed: 6000, modules: 2, cas: 28})
CREATE (ram3:RAM {id: 'ram_3', name: 'Kingston Fury Beast 16GB', manufacturer: 'Kingston', price: 64.99, quantity: 32, type: 'DDR5', speed: 5600, modules: 1, cas: 28})
CREATE (ram4:RAM {id: 'ram_4', name: 'ADATA XPG Lancer 32GB', manufacturer: 'ADATA', price: 119.99, quantity: 25, type: 'DDR5', speed: 5600, modules: 2, cas: 28})

// Create Storage nodes
CREATE (storage1:Storage {id: 'storage_1', name: 'Samsung 990 Pro 2TB', manufacturer: 'Samsung', price: 179.99, quantity: 18, capacity: 2000, type: 'NVMe SSD', cache: 256})
CREATE (storage2:Storage {id: 'storage_2', name: 'WD Black SN850X 1TB', manufacturer: 'Western Digital', price: 99.99, quantity: 22, capacity: 1000, type: 'NVMe SSD', cache: 96})
CREATE (storage3:Storage {id: 'storage_3', name: 'Seagate Barracuda 4TB', manufacturer: 'Seagate', price: 89.99, quantity: 28, capacity: 4000, type: 'HDD', cache: 256})
CREATE (storage4:Storage {id: 'storage_4', name: 'Crucial MX500 500GB', manufacturer: 'Crucial', price: 54.99, quantity: 30, capacity: 500, type: 'SATA SSD', cache: 64})

// Create Power Supply nodes
CREATE (psu1:PowerSupply {id: 'psu_1', name: 'Corsair RM1000e 1000W', manufacturer: 'Corsair', price: 179.99, quantity: 14, formFactor: 'ATX', efficiency: '80+ Gold', modular: true, wattage: 1000})
CREATE (psu2:PowerSupply {id: 'psu_2', name: 'EVGA SuperNOVA 850 G6', manufacturer: 'EVGA', price: 134.99, quantity: 19, formFactor: 'ATX', efficiency: '80+ Gold', modular: true, wattage: 850})
CREATE (psu3:PowerSupply {id: 'psu_3', name: 'Seasonic Focus 750W', manufacturer: 'Seasonic', price: 119.99, quantity: 21, formFactor: 'ATX', efficiency: '80+ Gold', modular: true, wattage: 750})
CREATE (psu4:PowerSupply {id: 'psu_4', name: 'MSI MAG A550GL 550W', manufacturer: 'MSI', price: 64.99, quantity: 26, formFactor: 'ATX', efficiency: '80+ Bronze', modular: false, wattage: 550})

// Create CPU Cooler nodes
CREATE (cooler1:CPUCooler {id: 'cooler_1', name: 'Noctua NH-D15', manufacturer: 'Noctua', price: 99.99, quantity: 17, waterCooled: false, tdp: 250, cpuBrand: 'Both'})
CREATE (cooler2:CPUCooler {id: 'cooler_2', name: 'Corsair iCUE H150i Elite', manufacturer: 'Corsair', price: 189.99, quantity: 12, waterCooled: true, tdp: 380, cpuBrand: 'Intel'})
CREATE (cooler3:CPUCooler {id: 'cooler_3', name: 'BeQuiet Dark Rock Pro 4', manufacturer: 'BeQuiet', price: 89.99, quantity: 19, waterCooled: false, tdp: 250, cpuBrand: 'Both'})
CREATE (cooler4:CPUCooler {id: 'cooler_4', name: 'ARCTIC Liquid Freezer II 360', manufacturer: 'ARCTIC', price: 109.99, quantity: 15, waterCooled: true, tdp: 420, cpuBrand: 'Both'})

// Create Chassis nodes
CREATE (chassis1:Chassis {id: 'chassis_1', name: 'Lian Li Lancool 3', manufacturer: 'Lian Li', price: 99.99, quantity: 16, formFactor: 'ATX', sidePanelMaterial: 'Tempered Glass', psuShroud: true, maxRadiatorSize: 360, maxGpuLength: 390})
CREATE (chassis2:Chassis {id: 'chassis_2', name: 'Fractal Design Core 1000', manufacturer: 'Fractal Design', price: 49.99, quantity: 24, formFactor: 'ATX', sidePanelMaterial: 'Steel', psuShroud: false, maxRadiatorSize: 280, maxGpuLength: 330})
CREATE (chassis3:Chassis {id: 'chassis_3', name: 'NZXT H510 Flow', manufacturer: 'NZXT', price: 99.99, quantity: 18, formFactor: 'ATX', sidePanelMaterial: 'Tempered Glass', psuShroud: true, maxRadiatorSize: 280, maxGpuLength: 370})
CREATE (chassis4:Chassis {id: 'chassis_4', name: 'Thermaltake Core V21', manufacturer: 'Thermaltake', price: 69.99, quantity: 22, formFactor: 'MicroATX', sidePanelMaterial: 'Tempered Glass', psuShroud: false, maxRadiatorSize: 240, maxGpuLength: 290})

// Create compatibility relationships
CREATE (cpu1)-[:COMPATIBLE_WITH]->(mobo1)
CREATE (cpu2)-[:COMPATIBLE_WITH]->(mobo1)
CREATE (cpu2)-[:COMPATIBLE_WITH]->(mobo3)
CREATE (cpu3)-[:COMPATIBLE_WITH]->(mobo2)
CREATE (cpu4)-[:COMPATIBLE_WITH]->(mobo2)
CREATE (cpu4)-[:COMPATIBLE_WITH]->(mobo4)
CREATE (ram1)-[:COMPATIBLE_WITH]->(mobo1)
CREATE (ram2)-[:COMPATIBLE_WITH]->(mobo1)
CREATE (ram2)-[:COMPATIBLE_WITH]->(mobo2)
CREATE (ram3)-[:COMPATIBLE_WITH]->(mobo3)
CREATE (ram4)-[:COMPATIBLE_WITH]->(mobo2)
CREATE (gpu1)-[:FITS_IN]->(chassis1)
CREATE (gpu2)-[:FITS_IN]->(chassis1)
CREATE (gpu2)-[:FITS_IN]->(chassis3)
CREATE (gpu3)-[:FITS_IN]->(chassis1)
CREATE (gpu4)-[:FITS_IN]->(chassis2)
CREATE (mobo1)-[:FITS_IN]->(chassis1)
CREATE (mobo1)-[:FITS_IN]->(chassis3)
CREATE (mobo2)-[:FITS_IN]->(chassis1)
CREATE (cooler1)-[:COOLS]->(cpu1)
CREATE (cooler2)-[:COOLS]->(cpu2)
CREATE (cooler4)-[:COOLS]->(cpu3)