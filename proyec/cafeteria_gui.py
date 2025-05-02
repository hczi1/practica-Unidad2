import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

PRODUCTOS_FILE = 'productos.json'
INVENTARIO_FILE = 'inventario.json'
PEDIDOS_FILE = 'pedidos.json'

def cargar_datos(archivo, por_defecto):
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return por_defecto

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

productos = cargar_datos(PRODUCTOS_FILE, {"bebidas": [], "postres": []})
inventario = cargar_datos(INVENTARIO_FILE, {})
carrito = []

class CafeteriaApp:
    def __init__(self, master):
        self.master = master
        master.title("Cafetería La Chida")
        master.geometry("800x800")
        master.configure(bg="#fefbf6")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#fefbf6")
        style.configure("TNotebook.Tab", background="#e8d9c4", foreground="#4b2e2e", font=("Segoe UI", 12, "bold"), padding=[12, 8])
        style.map("TNotebook.Tab", background=[("selected", "#c9b29b")])
        style.configure("TLabel", background="#fefbf6", font=("Segoe UI", 11), foreground="#3d3d3d")
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), background="#fefbf6", foreground="#6a4e42")
        style.configure("TButton", font=("Segoe UI", 11), background="#d9cfc1", foreground="#3d3d3d", padding=6)
        style.map("TButton", background=[('active', '#c1b6a5')], relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        self.usuario = self.solicitar_datos_usuario()
        self.tipo_usuario = self.usuario['tipo']

        header = ttk.Label(master, text=f"Bienvenido {self.usuario['nombre']} ☕", style="Header.TLabel")
        header.pack(pady=10)

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.frames = {}
        for nombre in ['Menú', 'Carrito', 'Inventario']:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=nombre)
            self.frames[nombre] = frame

        if self.tipo_usuario == 'empleado':
            admin_frame = ttk.Frame(self.notebook)
            self.notebook.add(admin_frame, text='Administración')
            self.frames['Administración'] = admin_frame

        self.inicializar_menu()
        self.inicializar_carrito()
        self.inicializar_inventario()
        if self.tipo_usuario == 'empleado':
            self.inicializar_administracion()

    def solicitar_datos_usuario(self):
        while True:
            nombre = simpledialog.askstring("Nombre", "Ingresa tu nombre")
            if nombre:
                break
        while True:
            correo = simpledialog.askstring("Correo", "Ingresa tu correo")
            if correo:
                break
        while True:
            tipo = simpledialog.askstring("Tipo", "¿Eres usuario o empleado?").lower()
            if tipo in ['usuario', 'empleado']:
                break
        return {"nombre": nombre, "correo": correo, "tipo": tipo}

    def inicializar_menu(self):
        frame = self.frames['Menú']
        ttk.Label(frame, text="☕ Bebidas", style="Header.TLabel").pack(pady=5)
        for bebida in productos['bebidas']:
            ttk.Button(frame, text=f"{bebida['nombre']} - ${bebida['precio']:.2f}",
                       command=lambda b=bebida: self.seleccionar_personalizacion(b)).pack(pady=2, fill='x', padx=20)

        ttk.Label(frame, text="🧁 Postres", style="Header.TLabel").pack(pady=10)
        for postre in productos['postres']:
            ttk.Button(frame, text=f"{postre['nombre']} - ${postre['precio']:.2f}",
                       command=lambda p=postre: self.agregar_postre(p)).pack(pady=2, fill='x', padx=20)

    def inicializar_carrito(self):
        self.frame_carrito = self.frames['Carrito']
        self.lista_carrito = tk.Listbox(self.frame_carrito, width=70, font=("Courier", 11))
        self.lista_carrito.pack(pady=10, padx=10)
        ttk.Button(self.frame_carrito, text="Eliminar Seleccionado", command=self.eliminar_seleccionado).pack(pady=2)
        ttk.Button(self.frame_carrito, text="Finalizar Compra", command=self.finalizar_compra).pack(pady=5)

    def inicializar_inventario(self):
        frame = self.frames['Inventario']
        self.labels_inventario = {}
        ttk.Label(frame, text="Ingredientes Disponibles", style="Header.TLabel").pack(pady=10)
        for ing, cant in inventario.items():
            lbl = ttk.Label(frame, text=f"{ing}: {cant}")
            lbl.pack()
            self.labels_inventario[ing] = lbl

    def inicializar_administracion(self):
        frame = self.frames['Administración']
        ttk.Label(frame, text="Agregar nuevo producto", style="Header.TLabel").pack(pady=10)
        self.entry_nombre = ttk.Entry(frame)
        self.entry_precio = ttk.Entry(frame)
        self.entry_tipo = ttk.Combobox(frame, values=["bebida", "postre"])
        self.entry_nombre.pack(pady=2)
        self.entry_precio.pack(pady=2)
        self.entry_tipo.pack(pady=2)
        ttk.Button(frame, text="Agregar", command=self.agregar_producto).pack(pady=5)

        ttk.Label(frame, text="Actualizar inventario", style="Header.TLabel").pack(pady=10)
        self.entry_ing = ttk.Entry(frame)
        self.entry_cant = ttk.Entry(frame)
        self.entry_ing.pack(pady=2)
        self.entry_cant.pack(pady=2)
        ttk.Button(frame, text="Actualizar", command=self.actualizar_inventario).pack(pady=5)

    def agregar_producto(self):
        nombre = self.entry_nombre.get()
        precio = float(self.entry_precio.get())
        tipo = self.entry_tipo.get()
        personalizable = []
        if tipo == 'bebida':
            opciones = ['extra leche', 'sin azúcar', 'tamaño grande']
            personalizable = simpledialog.askstring("Personalización", f"Opciones separadas por coma ({', '.join(opciones)}):")
            if personalizable:
                personalizable = [p.strip() for p in personalizable.split(',')]
        nuevo = {"nombre": nombre, "precio": precio, "personalizable": personalizable} if tipo == 'bebida' else {"nombre": nombre, "precio": precio}
        productos[tipo + 's'].append(nuevo)
        guardar_datos(PRODUCTOS_FILE, productos)
        messagebox.showinfo("Éxito", "Producto agregado. Reinicia para verlo en el menú.")

    def actualizar_inventario(self):
        ing = self.entry_ing.get()
        cant = int(self.entry_cant.get())
        inventario[ing] = inventario.get(ing, 0) + cant
        guardar_datos(INVENTARIO_FILE, inventario)
        if ing not in self.labels_inventario:
            self.labels_inventario[ing] = ttk.Label(self.frames['Inventario'], text="")
            self.labels_inventario[ing].pack()
        self.labels_inventario[ing].config(text=f"{ing}: {inventario[ing]}")
        messagebox.showinfo("Inventario", "Inventario actualizado.")

    def seleccionar_personalizacion(self, bebida):
        win = tk.Toplevel(self.master)
        win.title(f"Personalizar {bebida['nombre']}")
        win.geometry("300x400")
        win.configure(bg="#fefbf6")

        selecciones = {}
        for ing in bebida.get("personalizable", []):
            if inventario.get(ing, 0) > 0:
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(win, text=f"{ing} ({inventario[ing]})", variable=var)
                cb.pack(anchor='w', padx=10, pady=2)
                selecciones[ing] = var
            else:
                ttk.Label(win, text=f"{ing} (Agotado)", style="TLabel").pack(anchor='w', padx=10, pady=2)

        def agregar():
            seleccionados = [k for k, v in selecciones.items() if v.get()]
            for s in seleccionados:
                inventario[s] -= 1
            carrito.append({"tipo": "bebida", "nombre": bebida['nombre'], "precio": bebida['precio'], "personalizaciones": seleccionados})
            guardar_datos(INVENTARIO_FILE, inventario)
            self.actualizar_carrito()
            win.destroy()

        ttk.Button(win, text="Agregar al carrito", command=agregar).pack(pady=10)

    def agregar_postre(self, postre):
        carrito.append({"tipo": "postre", "nombre": postre['nombre'], "precio": postre['precio']})
        self.actualizar_carrito()

    def actualizar_carrito(self):
        self.lista_carrito.delete(0, tk.END)
        for i, item in enumerate(carrito):
            extra = f" con {', '.join(item['personalizaciones'])}" if item.get('personalizaciones') else ""
            self.lista_carrito.insert(tk.END, f"{i+1}. {item['nombre']} - ${item['precio']:.2f}{extra}")

    def eliminar_seleccionado(self):
        sel = self.lista_carrito.curselection()
        if sel:
            carrito.pop(sel[0])
            self.actualizar_carrito()

    def finalizar_compra(self):
        if not carrito:
            messagebox.showwarning("Vacío", "No hay productos en el carrito.")
            return
        total = sum(item['precio'] for item in carrito)
        recibo = f"Cliente: {self.usuario['nombre']}\nCorreo: {self.usuario['correo']}\nTotal: ${total:.2f}"
        if messagebox.askyesno("Confirmar", recibo + "\n\n¿Confirmar compra?"):
            pedidos = cargar_datos(PEDIDOS_FILE, [])
            pedidos.append({"usuario": self.usuario['nombre'], "correo": self.usuario['correo'], "items": carrito.copy(), "total": total})
            guardar_datos(PEDIDOS_FILE, pedidos)
            carrito.clear()
            self.actualizar_carrito()
            messagebox.showinfo("Gracias", "Compra realizada correctamente.")

    def agregar_botones_generales(self):
        frame_botones = ttk.Frame(self.master)
        frame_botones.pack(pady=10)

        boton_retroceder = ttk.Button(frame_botones, text="⏪ Retroceder", command=self.retroceder_pestana)
        boton_retroceder.pack(side="left", padx=10)

        boton_salir = ttk.Button(frame_botones, text="❌ Salir", command=self.master.quit)
        boton_salir.pack(side="left", padx=10)

    def retroceder_pestana(self):
        index = self.notebook.index(self.notebook.select())
        if index > 0:
            self.notebook.select(index - 1)

if __name__ == '__main__':
    root = tk.Tk()
    app = CafeteriaApp(root)
    app.agregar_botones_generales()
    root.mainloop()
