import mysql.connector
from tkinter import ttk
from tkinter import *
import tkinter as tk
import sys
from tkinter import messagebox

class Productos:
    def __init__(self, root):
        self.wind = root
        self.wind.title("Sistema de Inventarios y Ventas")
        self.wind.geometry("850x600")

        self.notebook = ttk.Notebook(self.wind)
        self.notebook.pack(fill="both", expand="yes", padx=10, pady=10)

        self.frame_inventario = ttk.Frame(self.notebook)
        self.frame_clientes = ttk.Frame(self.notebook)
        self.frame_ventas = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_inventario, text="Inventario")
        self.notebook.add(self.frame_clientes, text="Clientes")
        self.notebook.add(self.frame_ventas, text="Ventas")

        self.inventario_frame()
        self.clientes_frame()
        self.ventas_frame()

    def run_query(self, query, parameters=()):
        host = "localhost"
        user = "root"
        password = "123456789"
        database = "base_de_datos"

        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute(query, parameters)

        if query.upper().startswith("SELECT"):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = None

        conn.close()
        return result

    # Funciones para el inventario
    def inventario_frame(self):
        frame = Frame(self.frame_inventario)
        frame.pack(fill="both", expand="yes", padx=20, pady=10)

        # Área para productos
        self.trv_productos = ttk.Treeview(frame, columns=("Código", "Nombre", "Existencia", "Proveedor", "Precio"), show="headings", height=10)
        self.trv_productos.grid(row=0, column=0, columnspan=2)

        self.trv_productos.heading("Código", text="Código")
        self.trv_productos.heading("Nombre", text="Nombre")
        self.trv_productos.heading("Existencia", text="Existencia")
        self.trv_productos.heading("Proveedor", text="Proveedor")
        self.trv_productos.heading("Precio", text="Precio")
        self.consulta_productos()

        btn_agregar_producto = Button(frame, text="Agregar Producto", command=self.agregar_producto, width=15)
        btn_agregar_producto.grid(row=1, column=0, padx=10)

        btn_actualizar_producto = Button(frame, text="Actualizar Producto", command=self.actualizar_producto, width=15)
        btn_actualizar_producto.grid(row=1, column=1, padx=10)

        btn_eliminar_producto = Button(frame, text="Eliminar Producto", command=self.eliminar_producto, width=15)
        btn_eliminar_producto.grid(row=1, column=2, padx=10)

        # Campos para agregar productos
        al1 = Label(frame, text="Código", width=15)
        al1.grid(row=2, column=0, padx=5, pady=3)
        self.ent1 = Entry(frame)
        self.ent1.grid(row=2, column=1, padx=5, pady=3)

        al2 = Label(frame, text="Nombre", width=15)
        al2.grid(row=3, column=0, padx=5, pady=3)
        self.ent2 = Entry(frame)
        self.ent2.grid(row=3, column=1, padx=5, pady=3)

        al3 = Label(frame, text="Existencia", width=15)
        al3.grid(row=4, column=0, padx=5, pady=3)
        self.ent3 = Entry(frame)
        self.ent3.grid(row=4, column=1, padx=5, pady=3)

        al4 = Label(frame, text="Proveedor", width=15)
        al4.grid(row=5, column=0, padx=5, pady=3)
        self.ent4 = Entry(frame)
        self.ent4.grid(row=5, column=1, padx=5, pady=3)

        al5 = Label(frame, text="Precio", width=15)
        al5.grid(row=6, column=0, padx=5, pady=3)
        self.ent5 = Entry(frame)
        self.ent5.grid(row=6, column=1, padx=5, pady=3)

    def consulta_productos(self):
        for row in self.trv_productos.get_children():
            self.trv_productos.delete(row)
        query = 'SELECT codigo, nombre, existencia, proveedor, precio FROM articulos'
        rows = self.run_query(query)
        for row in rows:
            self.trv_productos.insert("", "end", values=row)

    def agregar_producto(self):
        if self.validation_producto():
            codigo = self.ent1.get()
            nombre = self.ent2.get()
            existencia = int(self.ent3.get())
            proveedor = self.ent4.get()
            precio = float(self.ent5.get())

            if existencia < 0:
                messagebox.showerror("Error", "La existencia no puede ser negativa.")
                return

            query = 'INSERT INTO articulos (codigo, nombre, existencia, proveedor, precio) VALUES (%s, %s, %s, %s, %s)'
            parameters = (codigo, nombre, existencia, proveedor, precio)
            self.run_query(query, parameters)
            self.ent1.delete(0, END)
            self.ent2.delete(0, END)
            self.ent3.delete(0, END)
            self.ent4.delete(0, END)
            self.ent5.delete(0, END)
            self.consulta_productos()

    def actualizar_producto(self):
        try:
            seleccion = self.trv_productos.selection()[0]
            codigo = self.trv_productos.item(seleccion, "values")[0]
        except IndexError:
            messagebox.showerror("Error", "Por favor, seleccione un producto para actualizar.")
            return

        self.edit_wind = Toplevel()
        self.edit_wind.title("Actualizar Producto")

        frame = Frame(self.edit_wind)
        frame.pack(padx=20, pady=10)

        Label(frame, text="Nuevo Precio:", width=15).grid(row=0, column=0, padx=5, pady=3)
        nuevo_precio = Entry(frame)
        nuevo_precio.grid(row=0, column=1, padx=5, pady=3)

        Label(frame, text="Nueva Existencia:", width=15).grid(row=1, column=0, padx=5, pady=3)
        nueva_existencia = Entry(frame)
        nueva_existencia.grid(row=1, column=1, padx=5, pady=3)

        Button(frame, text="Actualizar", command=lambda: self.edit_record(codigo, nuevo_precio.get(), nueva_existencia.get()), width=15).grid(row=2, column=1, padx=10)

    def eliminar_producto(self):
        try:
            seleccion = self.trv_productos.selection()[0]
            codigo = self.trv_productos.item(seleccion, "values")[0]
        except IndexError:
            messagebox.showerror("Error", "Por favor, seleccione un producto para eliminar.")
            return

        respuesta = messagebox.askyesno("Eliminar Producto", "¿Está seguro que desea eliminar este producto?")
        if respuesta:
            query = 'DELETE FROM articulos WHERE codigo = %s'
            self.run_query(query, (codigo,))
            self.consulta_productos()

    def validation_producto(self):
        return all([self.ent1.get(), self.ent2.get(), self.ent3.get(), self.ent4.get(), self.ent5.get()])

    def edit_record(self, codigo, nuevo_precio, nueva_existencia):
        if not nuevo_precio and not nueva_existencia:
            messagebox.showerror("Error", "Por favor, ingrese al menos un valor para actualizar.")
            return

        if nuevo_precio:
            query = 'UPDATE articulos SET precio = %s WHERE codigo = %s'
            self.run_query(query, (float(nuevo_precio), codigo))

        if nueva_existencia:
            if int(nueva_existencia) < 0:
                messagebox.showerror("Error", "La existencia no puede ser negativa.")
                return
            query = 'UPDATE articulos SET existencia = %s WHERE codigo = %s'
            self.run_query(query, (int(nueva_existencia), codigo))

        self.edit_wind.destroy()
        self.consulta_productos()

    # Funciones para clientes
    def clientes_frame(self):
        frame = Frame(self.frame_clientes)
        frame.pack(fill="both", expand="yes", padx=20, pady=10)

        # Área para clientes
        self.trv_clientes = ttk.Treeview(frame, columns=("Código", "Nombre", "Dirección"), show="headings", height=10)
        self.trv_clientes.grid(row=0, column=0, columnspan=2)

        self.trv_clientes.heading("Código", text="Código")
        self.trv_clientes.heading("Nombre", text="Nombre")
        self.trv_clientes.heading("Dirección", text="Dirección")
        self.consulta_clientes()

        btn_agregar_cliente = Button(frame, text="Agregar Cliente", command=self.agregar_cliente, width=15)
        btn_agregar_cliente.grid(row=1, column=0, padx=10)

        btn_actualizar_cliente = Button(frame, text="Actualizar Cliente", command=self.actualizar_cliente, width=15)
        btn_actualizar_cliente.grid(row=1, column=1, padx=10)

        btn_eliminar_cliente = Button(frame, text="Eliminar Cliente", command=self.eliminar_cliente, width=15)
        btn_eliminar_cliente.grid(row=1, column=2, padx=10)

        # Campos para agregar clientes
        al6 = Label(frame, text="Código Cliente", width=15)
        al6.grid(row=2, column=0, padx=5, pady=3)
        self.ent6 = Entry(frame)
        self.ent6.grid(row=2, column=1, padx=5, pady=3)

        al7 = Label(frame, text="Nombre Cliente", width=15)
        al7.grid(row=3, column=0, padx=5, pady=3)
        self.ent7 = Entry(frame)
        self.ent7.grid(row=3, column=1, padx=5, pady=3)

        al8 = Label(frame, text="Dirección Cliente", width=15)
        al8.grid(row=4, column=0, padx=5, pady=3)
        self.ent8 = Entry(frame)
        self.ent8.grid(row=4, column=1, padx=5, pady=3)

    def consulta_clientes(self):
        for row in self.trv_clientes.get_children():
            self.trv_clientes.delete(row)
        query = 'SELECT codigo_cliente, nombre_cliente, direccion_cliente FROM clientes'
        rows = self.run_query(query)
        for row in rows:
            self.trv_clientes.insert("", "end", values=row)

    def agregar_cliente(self):
        if self.validation_cliente():
            codigo_cliente = self.ent6.get()
            nombre_cliente = self.ent7.get()
            direccion_cliente = self.ent8.get()

            query = 'INSERT INTO clientes (codigo_cliente, nombre_cliente, direccion_cliente) VALUES (%s, %s, %s)'
            parameters = (codigo_cliente, nombre_cliente, direccion_cliente)
            self.run_query(query, parameters)
            self.ent6.delete(0, END)
            self.ent7.delete(0, END)
            self.ent8.delete(0, END)
            self.consulta_clientes()

    def actualizar_cliente(self):
        try:
            seleccion = self.trv_clientes.selection()[0]
            codigo_cliente = self.trv_clientes.item(seleccion, "values")[0]
        except IndexError:
            messagebox.showerror("Error", "Por favor, seleccione un cliente para actualizar.")
            return

        self.edit_cliente_wind = Toplevel()
        self.edit_cliente_wind.title("Editar Cliente")

        frame = Frame(self.edit_cliente_wind)
        frame.pack(padx=20, pady=10)

        Label(frame, text="Nombre Cliente:", width=15).grid(row=0, column=0, padx=5, pady=3)
        nuevo_nombre_cliente = Entry(frame)
        nuevo_nombre_cliente.grid(row=0, column=1, padx=5, pady=3)

        Label(frame, text="Dirección Cliente:", width=15).grid(row=1, column=0, padx=5, pady=3)
        nueva_direccion_cliente = Entry(frame)
        nueva_direccion_cliente.grid(row=1, column=1, padx=5, pady=3)

        Button(frame, text="Actualizar", command=lambda: self.edit_cliente(codigo_cliente, nuevo_nombre_cliente.get(), nueva_direccion_cliente.get()), width=15).grid(row=2, column=1, padx=10)

    def eliminar_cliente(self):
        try:
            seleccion = self.trv_clientes.selection()[0]
            codigo_cliente = self.trv_clientes.item(seleccion, "values")[0]
        except IndexError:
            messagebox.showerror("Error", "Por favor, seleccione un cliente para eliminar.")
            return

        respuesta = messagebox.askyesno("Eliminar Cliente", "¿Está seguro que desea eliminar este cliente?")
        if respuesta:
            query = 'DELETE FROM clientes WHERE codigo_cliente = %s'
            self.run_query(query, (codigo_cliente,))
            self.consulta_clientes()

    def validation_cliente(self):
        return all([self.ent6.get(), self.ent7.get(), self.ent8.get()])

    def edit_cliente(self, codigo_cliente, nuevo_nombre_cliente, nueva_direccion_cliente):
        query = 'UPDATE clientes SET nombre_cliente = %s, direccion_cliente = %s WHERE codigo_cliente = %s'
        parameters = (nuevo_nombre_cliente, nueva_direccion_cliente, codigo_cliente)
        self.run_query(query, parameters)
        self.edit_cliente_wind.destroy()
        self.consulta_clientes()

    # Funciones para ventas
    def ventas_frame(self):
        frame = Frame(self.frame_ventas)
        frame.pack(fill="both", expand="yes", padx=20, pady=10)

        # Área para ventas
        self.trv_ventas = ttk.Treeview(frame, columns=("Código Venta", "Código Producto", "Código Cliente", "Cantidad", "Total"), show="headings", height=10)
        self.trv_ventas.grid(row=0, column=0, columnspan=2)

        self.trv_ventas.heading("Código Venta", text="Código Venta")
        self.trv_ventas.heading("Código Producto", text="Código Producto")
        self.trv_ventas.heading("Código Cliente", text="Código Cliente")
        self.trv_ventas.heading("Cantidad", text="Cantidad")
        self.trv_ventas.heading("Total", text="Total")
        self.consulta_ventas()

        btn_crear_venta = Button(frame, text="Crear Venta", command=self.crear_venta, width=15)
        btn_crear_venta.grid(row=1, column=0, padx=10)

        btn_anular_venta = Button(frame, text="Anular Venta", command=self.anular_venta, width=15)
        btn_anular_venta.grid(row=1, column=1, padx=10)

        # Campos para agregar ventas
        al9 = Label(frame, text="Código Venta", width=15)
        al9.grid(row=2, column=0, padx=5, pady=3)
        self.ent9 = Entry(frame)
        self.ent9.grid(row=2, column=1, padx=5, pady=3)

        al10 = Label(frame, text="Código Producto", width=15)
        al10.grid(row=3, column=0, padx=5, pady=3)
        self.ent10 = Entry(frame)
        self.ent10.grid(row=3, column=1, padx=5, pady=3)

        al11 = Label(frame, text="Código Cliente", width=15)
        al11.grid(row=4, column=0, padx=5, pady=3)
        self.ent11 = Entry(frame)
        self.ent11.grid(row=4, column=1, padx=5, pady=3)

        al12 = Label(frame, text="Cantidad", width=15)
        al12.grid(row=5, column=0, padx=5, pady=3)
        self.ent12 = Entry(frame)
        self.ent12.grid(row=5, column=1, padx=5, pady=3)

    def consulta_ventas(self):
        for row in self.trv_ventas.get_children():
            self.trv_ventas.delete(row)
        query = 'SELECT codigo_venta, codigo_producto, codigo_cliente, cantidad, total FROM ventas'
        rows = self.run_query(query)
        for row in rows:
            self.trv_ventas.insert("", "end", values=row)

    def crear_venta(self):
        if self.validation_venta():
            codigo_venta = self.ent9.get()
            codigo_producto = self.ent10.get()
            codigo_cliente = self.ent11.get()
            cantidad = int(self.ent12.get())
            total = self.calcular_total(codigo_producto, cantidad)

            query = 'INSERT INTO ventas (codigo_venta, codigo_producto, codigo_cliente, cantidad, total) VALUES (%s, %s, %s, %s, %s)'
            parameters = (codigo_venta, codigo_producto, codigo_cliente, cantidad, total)
            self.run_query(query, parameters)
            self.ent9.delete(0, END)
            self.ent10.delete(0, END)
            self.ent11.delete(0, END)
            self.ent12.delete(0, END)
            self.consulta_ventas()

    def anular_venta(self):
        try:
            seleccion = self.trv_ventas.selection()[0]
            codigo_venta = self.trv_ventas.item(seleccion, "values")[0]
        except IndexError:
            messagebox.showerror("Error", "Por favor, seleccione una venta para anular.")
            return

        respuesta = messagebox.askyesno("Anular Venta", "¿Está seguro que desea anular esta venta?")
        if respuesta:
            query = 'DELETE FROM ventas WHERE codigo_venta = %s'
            self.run_query(query, (codigo_venta,))
            self.consulta_ventas()

    def validation_venta(self):
        return all([self.ent9.get(), self.ent10.get(), self.ent11.get(), self.ent12.get()])

    def calcular_total(self, codigo_producto, cantidad):
        query = 'SELECT precio FROM articulos WHERE codigo = %s'
        result = self.run_query(query, (codigo_producto,))
        if result:
            precio = result[0][0]
            total = precio * cantidad
            return total
        return 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        comando = sys.argv[1]

        if comando == "--ayuda":
            print("Uso:")
            print("python mi-proyecto.py --ayuda")
            print("python mi-proyecto.py --inventario listar")
            print("python mi-proyecto.py --inventario crear P001 Leche 100 'Proveedor S.A' 9.50")
            print("python mi-proyecto.py --inventario actualizar P001 Leche 100 'Proveedor S.A' 9.90")
            print("python mi-proyecto.py --inventario existencia P001 89")
            print("python mi-proyecto.py --inventario eliminar P001")
        else:
            root = Tk()
            product = Productos(root)
            root.mainloop()
    else:
        root = Tk()
        product = Productos(root)
        root.mainloop()