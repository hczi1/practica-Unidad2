# 📖 Guía de Usuario - Sistema de Gestión para Cafetería La Chida

Bienvenido al sistema de pedidos para la **Cafetería La Chida**. Esta guía detalla el uso completo de la aplicación desarrollada en Python con interfaz gráfica Tkinter.

---

## 🧾 Descripción General

Esta aplicación permite a **clientes** y **empleados** gestionar pedidos, visualizar productos, personalizarlos, y administrar inventario de forma sencilla.

---

## 👤 Ingreso al Sistema

Al iniciar el programa (`cafeteria.py`), se abre una ventana emergente solicitando:

- **Nombre**
- **Correo electrónico**
- Rol: `usuario` o `empleado`

El flujo del sistema se adapta según tu rol.

---

## ☕ Interfaz de Usuario

La aplicación está dividida en pestañas mediante `ttk.Notebook`, con 3 secciones:

### 1. Menú de Productos
- Visualiza bebidas y postres cargados desde `productos.json`.
- Haz clic en un botón para agregar un producto al carrito.
- Si es una bebida, se abrirá una ventana para seleccionar ingredientes (cargados dinámicamente desde `inventario.json`).
- La personalización se guarda junto al producto seleccionado.

### 2. Carrito de Compras
- Muestra en tiempo real todos los productos seleccionados.
- Opciones disponibles:
  - `Eliminar Seleccionado`: elimina el producto activo.
  - `Finalizar Compra`: guarda el pedido en `pedidos.json` y limpia el carrito.

### 3. Panel de Administración (solo empleados)
- Permite:
  - Agregar nuevos productos al menú.
  - Modificar cantidades de ingredientes existentes en el inventario.
- Cambios actualizan automáticamente los archivos JSON correspondientes.

---

## 🛠️ Gestión de Inventario

- Si un ingrediente se queda sin stock, el sistema **bloquea su selección** en bebidas.
- Esta verificación se hace dinámicamente en tiempo real durante la personalización del producto.

---

## 🔁 Navegación General

- `⏪ Retroceder`: vuelve a la pestaña anterior.
- `❌ Salir`: cierra el programa con seguridad.

---

## 💾 Archivos Relevantes

- `cafeteria.py`: archivo principal de la aplicación.
- `productos.json`: lista de productos disponibles.
- `inventario.json`: inventario de ingredientes.
- `pedidos.json`: historial de pedidos realizados.

---

## 📝 Notas Importantes

- Todos los cambios se guardan automáticamente en archivos `.json`.
- El sistema está preparado para evitar errores por falta de stock.
- Los datos del cliente se usan para registrar el pedido correctamente.

---

## 📸 Recomendaciones para Documentación Visual

Agregar capturas en un documento adicional para ilustrar:

1. Menú con productos personalizables.
2. Vista del carrito y opciones.
3. Panel de administración.

---

**Autor:** [Irvin Hernandez Carmona]  
**Fecha:** 02/05/2025

