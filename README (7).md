# 👨‍🍳 Chef-Costos: Ecosistema Tecnológico B2B (Reto 2)

Solución integral desarrollada para el sector gastronómico, diseñada para auditar la inflación de ingredientes frente a precios históricos y garantizar el margen de rentabilidad. Este repositorio consolida los requerimientos técnicos y analíticos del **Taller 12 (Dashboard BI)** y el **Taller Final Corte 3 (Ecosistema E2E)**.

## 👥 Equipo de Ingeniería y Desarrollo
* **Samuel David Simancas Contreras** (Arquitectura de Base de Datos y Lógica Backend)
* **Alejandra León Vargas** (Diseño de Interfaces UI/UX e Integración Frontend)
* **Daniel Camacho** (Ingeniería de Datos DAX e Inteligencia de Negocios)

## 🏗️ Arquitectura Técnica (Taller Final Corte 3)
* **Backend y Base de Datos:** Motor relacional en SQLite (`Backend/database.py`). Cuenta con Modelo Estrella (Hechos y Dimensiones) y *Data Seeding* de 5 registros insertados de manera autónoma.
* **Frontend Transaccional:** Interfaz gráfica desarrollada en `Tkinter` (`Frontend/app_chef.py`). Incluye módulos CRUD operacionales conectados a SQLite y puente de ejecución a Power BI. El sistema implementa validaciones robustas mediante `try-except` y alertas `messagebox`.
* **Orquestador:** Archivo principal `main.py` para la ejecución global de la aplicación de escritorio.

## 📊 Inteligencia de Negocios y Analítica (Taller 12)
* **Archivo Analítico:** `Chef_Dashboard.pbix`.
* **Integración Irrompible:** Conectado mediante un script puente nativo de Python (`pandas` y `sqlite3`) para evitar errores de ruta en el despliegue del evaluador.
* **Modelado y DAX:** Incluye Tabla Calendario para inteligencia de tiempo. Implementa Columnas Calculadas y Medidas DAX avanzadas (`CALCULATE`, `DIVIDE`, `SUM`) para el monitoreo de la inflación.
* **Visualización Dinámica:** Paleta corporativa orientada a la gastronomía. Presenta 6 visualizaciones clave, incluyendo mapa de calor de proveedores (Matriz) y tendencias de tiempo (Líneas).
* **Auditoría Financiera:** Pestaña resolutiva **Q&A - Respuestas de Negocio** que responde 4 preguntas gerenciales críticas para la viabilidad del restaurante.

## 🚀 Instrucciones de Despliegue Local
1. Clonar el repositorio en su máquina local.
2. Ejecutar `python main.py` para levantar la base de datos operativa y abrir la interfaz de usuario.
3. Utilizar los controles de Tkinter para ingresar nuevas variaciones de mercado.
4. Abrir Power BI. En *Transformar Datos*, modificar el origen del Script de Python asignando la ruta de su máquina local a la variable `ruta_db`. Al presionar **Actualizar** en el menú de inicio, el Dashboard leerá los registros nuevos en tiempo real.
