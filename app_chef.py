import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sqlite3

class AppChef:
    def __init__(self, root):
        self.root = root
        self.root.title("Chef-Costos - Panel de Control")
        self.root.geometry("450x600")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)
        
        # LOGO O TEXTO DE RESPALDO
        try:
            ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
            img = Image.open(ruta_logo).convert("RGB").resize((100, 100), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.logo_img, bg="#2c3e50").pack(pady=10)
        except Exception:
            tk.Label(self.root, text="👨‍🍳 CHEF-COSTOS", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack(pady=10)
        
        # BOTONES CRUD
        frame_crud = tk.Frame(self.root, bg="#2c3e50")
        frame_crud.pack(pady=10)
        
        tk.Button(frame_crud, text="➕ Ingresar Nuevo Costo", bg="#27ae60", fg="white", width=25, font=("Arial", 11, "bold"), command=self.crear).pack(pady=5)
        tk.Button(frame_crud, text="📖 Auditar Historial", bg="#f39c12", fg="white", width=25, font=("Arial", 11, "bold"), command=self.leer).pack(pady=5)
        tk.Button(frame_crud, text="✏️ Actualizar Mercado", bg="#d35400", fg="white", width=25, font=("Arial", 11, "bold"), command=self.actualizar).pack(pady=5)
        tk.Button(frame_crud, text="🗑️ Eliminar Registro", bg="#c0392b", fg="white", width=25, font=("Arial", 11, "bold"), command=self.eliminar).pack(pady=5)
        
        # BOTÓN A POWER BI
        tk.Label(self.root, text="Inteligencia de Negocios", font=("Arial", 10, "italic"), bg="#2c3e50", fg="#bdc3c7").pack(pady=15)
        tk.Button(self.root, text="📊 ABRIR POWER BI", bg="#2980b9", fg="white", font=("Arial", 12, "bold"), width=25, command=self.abrir_pbi).pack(pady=5)

    def obtener_ruta_db(self):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Backend", "chef_costos.db")

    def crear(self):
        ventana = tk.Toplevel(self.root)
        ventana.geometry("300x350")
        ventana.title("Nuevo Costo")
        ventana.configure(bg="#ecf0f1")
        ventana.grab_set()
        
        tk.Label(ventana, text="ID Proveedor (1-5):", bg="#ecf0f1").pack(pady=2)
        e_prov = tk.Entry(ventana, justify="center")
        e_prov.pack(pady=2)
        
        tk.Label(ventana, text="ID Ingrediente (101-105):", bg="#ecf0f1").pack(pady=2)
        e_ing = tk.Entry(ventana, justify="center")
        e_ing.pack(pady=2)
        
        tk.Label(ventana, text="Precio Histórico ($):", bg="#ecf0f1").pack(pady=2)
        e_hist = tk.Entry(ventana, justify="center")
        e_hist.pack(pady=2)
        
        tk.Label(ventana, text="Precio Mercado Nuevo ($):", bg="#ecf0f1").pack(pady=2)
        e_mer = tk.Entry(ventana, justify="center")
        e_mer.pack(pady=2)
        
        tk.Label(ventana, text="Fecha (YYYY-MM-DD):", bg="#ecf0f1").pack(pady=2)
        e_fec = tk.Entry(ventana, justify="center")
        e_fec.pack(pady=2)
        
        def guardar():
            try:
                with sqlite3.connect(self.obtener_ruta_db()) as conn:
                    conn.cursor().execute("INSERT INTO fact_costos (id_proveedor, id_ingrediente, precio_historico, precio_mercado, fecha) VALUES (?, ?, ?, ?, ?)",
                                          (int(e_prov.get()), int(e_ing.get()), float(e_hist.get()), float(e_mer.get()), e_fec.get()))
                    conn.commit()
                messagebox.showinfo("Éxito", "Costo registrado en la base de datos.", parent=ventana)
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error de Formato", str(e), parent=ventana)
                
        tk.Button(ventana, text="💾 Guardar", command=guardar, bg="#27ae60", fg="white", font=("Arial", 10, "bold")).pack(pady=15)

    def leer(self):
        ventana = tk.Toplevel(self.root)
        ventana.geometry("600x300")
        ventana.title("Auditoría de Costos")
        ventana.grab_set()
        
        tabla = ttk.Treeview(ventana, columns=("ID Registro", "Proveedor", "Ingrediente", "Mercado ($)", "Fecha"), show="headings")
        tabla.heading("ID Registro", text="ID")
        tabla.heading("Proveedor", text="Proveedor")
        tabla.heading("Ingrediente", text="Ingrediente")
        tabla.heading("Mercado ($)", text="Mercado ($)")
        tabla.heading("Fecha", text="Fecha")
        
        tabla.column("ID Registro", width=50, anchor="center")
        tabla.column("Mercado ($)", width=100, anchor="center")
        tabla.column("Fecha", width=100, anchor="center")
        
        tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        try:
            with sqlite3.connect(self.obtener_ruta_db()) as conn:
                registros = conn.cursor().execute('''SELECT f.id_registro, p.nombre, i.articulo, f.precio_mercado, f.fecha 
                                                     FROM fact_costos f JOIN dim_proveedores p ON f.id_proveedor = p.id_proveedor 
                                                     JOIN dim_ingredientes i ON f.id_ingrediente = i.id_ingrediente''').fetchall()
                for r in registros: tabla.insert("", tk.END, values=r)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        ventana_act = tk.Toplevel(self.root)
        ventana_act.title("Actualizar Mercado")
        ventana_act.geometry("300x250")
        ventana_act.configure(bg="#ecf0f1")
        ventana_act.grab_set()

        tk.Label(ventana_act, text="ID del Registro a Modificar:", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(pady=10)
        entry_id = tk.Entry(ventana_act, justify="center")
        entry_id.pack(pady=5)

        tk.Label(ventana_act, text="Nuevo Precio de Mercado ($):", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(pady=10)
        entry_precio = tk.Entry(ventana_act, justify="center")
        entry_precio.pack(pady=5)

        def ejecutar_actualizacion():
            try:
                id_reg = int(entry_id.get())
                nuevo_precio = float(entry_precio.get())
                
                with sqlite3.connect(self.obtener_ruta_db()) as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE fact_costos SET precio_mercado = ? WHERE id_registro = ?", (nuevo_precio, id_reg))
                    
                    if cursor.rowcount == 0:
                        raise ValueError("No se encontró ningún registro con ese ID en el historial.")
                    conn.commit()

                messagebox.showinfo("Éxito", f"El registro #{id_reg} ha sido actualizado con el nuevo precio de mercado.", parent=ventana_act)
                ventana_act.destroy()

            except ValueError as ve:
                messagebox.showwarning("Dato Inválido", str(ve), parent=ventana_act)
            except Exception as e:
                messagebox.showerror("Error Crítico", str(e), parent=ventana_act)

        tk.Button(ventana_act, text="✏️ Guardar Cambios", bg="#d35400", fg="white", font=("Arial", 10, "bold"), command=ejecutar_actualizacion).pack(pady=15)

    def eliminar(self):
        ventana_elim = tk.Toplevel(self.root)
        ventana_elim.title("Eliminar Registro")
        ventana_elim.geometry("300x200")
        ventana_elim.configure(bg="#ecf0f1")
        ventana_elim.grab_set()

        tk.Label(ventana_elim, text="ID del Registro a Eliminar:", bg="#ecf0f1", fg="#c0392b", font=("Arial", 10, "bold")).pack(pady=15)
        entry_id = tk.Entry(ventana_elim, justify="center")
        entry_id.pack(pady=5)

        def ejecutar_eliminacion():
            try:
                id_reg = int(entry_id.get())
                
                # Confirmación de seguridad
                respuesta = messagebox.askyesno("Confirmación Crítica", f"¿Está seguro de que desea eliminar definitivamente el registro #{id_reg}?\n\nEsta acción alterará el reporte financiero en Power BI.", parent=ventana_elim)
                
                if respuesta:
                    with sqlite3.connect(self.obtener_ruta_db()) as conn:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM fact_costos WHERE id_registro = ?", (id_reg,))
                        
                        if cursor.rowcount == 0:
                            raise ValueError("No existe un registro de costos con ese ID para borrar.")
                        conn.commit()
                        
                    messagebox.showinfo("Borrado", f"El registro #{id_reg} ha sido eliminado permanentemente.", parent=ventana_elim)
                    ventana_elim.destroy()

            except ValueError as ve:
                messagebox.showwarning("Error de Captura", str(ve), parent=ventana_elim)
            except Exception as e:
                messagebox.showerror("Error en Base de Datos", str(e), parent=ventana_elim)

        tk.Button(ventana_elim, text="🗑️ Eliminar Definitivamente", bg="#c0392b", fg="white", font=("Arial", 10, "bold"), command=ejecutar_eliminacion).pack(pady=15)

    def abrir_pbi(self):
        try:
            ruta_pbix = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Chef_Dashboard.pbix")
            os.startfile(ruta_pbix)
        except Exception as e:
            messagebox.showerror("Archivo no encontrado", "Asegúrese de guardar el Dashboard de Power BI con el nombre exacto 'Chef_Dashboard.pbix' en la carpeta raíz del proyecto.")