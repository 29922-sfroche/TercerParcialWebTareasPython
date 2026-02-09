-- =====================================================
-- MySQL - Productos_BD (con datos de ejemplo)
-- =====================================================

DROP DATABASE IF EXISTS Productos_BD;
CREATE DATABASE Productos_BD
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_spanish_ci;

USE Productos_BD;

-- =========================
-- 1) TABLAS
-- =========================

CREATE TABLE Clientes (
  ClienteID INT NOT NULL AUTO_INCREMENT,
  RazonSocial  VARCHAR(50)  NULL,
  Direccion    VARCHAR(100) NULL,
  Ciudad       VARCHAR(50)  NULL,
  Estado       VARCHAR(50)  NULL,
  CodigoPostal VARCHAR(10)  NULL,
  Rif          VARCHAR(15)  NULL,
  Pais         VARCHAR(50)  NULL,
  Telefonos    VARCHAR(50)  NULL,
  CONSTRAINT PK_Clientes PRIMARY KEY (ClienteID)
) ENGINE=InnoDB;

CREATE TABLE Productos (
  ProductoID  INT NOT NULL AUTO_INCREMENT,
  Descripcion VARCHAR(200) NOT NULL,
  Precio      DECIMAL(18,2) NOT NULL,
  Imagen      LONGTEXT NOT NULL,      -- nvarchar(max) -> LONGTEXT
  Detalles    VARCHAR(50) NOT NULL,
  CONSTRAINT PK_Productos PRIMARY KEY (ProductoID)
) ENGINE=InnoDB;

CREATE TABLE Pedidos (
  PedidoID INT NOT NULL AUTO_INCREMENT,
  ClienteID INT NULL,
  FechaPedido DATETIME NULL,
  CONSTRAINT PK_Pedidos PRIMARY KEY (PedidoID),
  CONSTRAINT FK_Pedidos_Clientes
    FOREIGN KEY (ClienteID)
    REFERENCES Clientes(ClienteID)
    ON UPDATE RESTRICT
    ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE PedidosItems (
  PedidoItemID INT NOT NULL AUTO_INCREMENT,
  PedidoID INT NOT NULL,
  ProductoID INT NOT NULL,
  Cantidad INT NOT NULL,
  CONSTRAINT PK_PedidosItems PRIMARY KEY (PedidoItemID),
  CONSTRAINT FK_PedidosItems_Pedidos
    FOREIGN KEY (PedidoID)
    REFERENCES Pedidos(PedidoID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT FK_PedidosItems_Productos
    FOREIGN KEY (ProductoID)
    REFERENCES Productos(ProductoID)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Índices (recomendado)
CREATE INDEX IX_Pedidos_ClienteID ON Pedidos(ClienteID);
CREATE INDEX IX_PedidosItems_PedidoID ON PedidosItems(PedidoID);
CREATE INDEX IX_PedidosItems_ProductoID ON PedidosItems(ProductoID);

-- =========================
-- 2) DATOS (orden: padre -> hija)
-- =========================

-- Clientes
INSERT INTO Clientes (ClienteID, RazonSocial, Direccion, Ciudad, Estado, CodigoPostal, Rif, Pais, Telefonos) VALUES
(1, 'Comercial Andina S.A.', 'Av. Siempre Viva 123', 'Quito', 'Pichincha', '170102', 'J-12345678-9', 'Ecuador', '0999999999'),
(2, 'Distribuidora Costa',   'Malecón 2000',        'Guayaquil', 'Guayas', '090101', 'J-98765432-1', 'Ecuador', '0988888888'),
(3, 'Tech Import',          'Calle 10 y Av. 6',    'Cuenca', 'Azuay', '010101', 'J-45678912-3', 'Ecuador', '0977777777');

-- Productos
INSERT INTO Productos (ProductoID, Descripcion, Precio, Imagen, Detalles) VALUES
(1, 'Mouse inalámbrico', 12.50, 'mouse.jpg', 'Periféricos'),
(2, 'Teclado mecánico',  45.99, 'teclado.jpg', 'Periféricos'),
(3, 'Monitor 24 pulgadas', 159.00, 'monitor.jpg', 'Pantallas'),
(4, 'Memoria USB 64GB',  9.75, 'usb64.jpg', 'Almacenamiento');

-- Pedidos
INSERT INTO Pedidos (PedidoID, ClienteID, FechaPedido) VALUES
(1, 1, '2026-01-10 10:30:00'),
(2, 2, '2026-01-11 15:05:00'),
(3, 1, '2026-01-12 09:20:00');

-- Items de pedidos
INSERT INTO PedidosItems (PedidoItemID, PedidoID, ProductoID, Cantidad) VALUES
(1, 1, 1, 2),  -- Pedido 1: 2 mouse
(2, 1, 4, 5),  -- Pedido 1: 5 usb
(3, 2, 3, 1),  -- Pedido 2: 1 monitor
(4, 2, 2, 1),  -- Pedido 2: 1 teclado
(5, 3, 2, 2);  -- Pedido 3: 2 teclados

-- (Opcional) Ajustar el siguiente AUTO_INCREMENT para evitar choques si insertaste IDs manualmente
ALTER TABLE Clientes AUTO_INCREMENT = 4;
ALTER TABLE Productos AUTO_INCREMENT = 5;
ALTER TABLE Pedidos AUTO_INCREMENT = 4;
ALTER TABLE PedidosItems AUTO_INCREMENT = 6;

-- =========================
-- 3) CONSULTA DE PRUEBA (opcional)
-- =========================
-- Ver pedidos con sus items
-- SELECT p.PedidoID, c.RazonSocial, p.FechaPedido, pr.Descripcion, pi.Cantidad, pr.Precio,
--        (pi.Cantidad * pr.Precio) AS Subtotal
-- FROM Pedidos p
-- JOIN Clientes c ON c.ClienteID = p.ClienteID
-- JOIN PedidosItems pi ON pi.PedidoID = p.PedidoID
-- JOIN Productos pr ON pr.ProductoID = pi.ProductoID
-- ORDER BY p.PedidoID, pi.PedidoItemID;
