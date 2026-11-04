# 📦 NexStock ERP — Full Stack Inventory & Asset Management (`Django + Vue.js 3 + REST API + SQL`)

Plataforma web **Full Stack** de gestión de inventarios, control de SKUs, alertas de stock crítico en tiempo real y análisis financiero de activos. Diseñada bajo arquitectura desacoplada cliente-servidor mediante **API REST (JSON)**.

Desarrollado por **Bryan Francisco López León** ([github.com/BRyanLopez23](https://github.com/BRyanLopez23)) — Software Engineering Student.

---

## 🚀 Stack Tecnológico & Arquitectura

| Capa | Tecnologías y Conceptos |
| :--- | :--- |
| **Backend & API REST** | **Python 3**, **Django**, Arquitectura de Servicios basada en **POO**, serialización **JSON**, autenticación y sesiones |
| **Frontend Reactivo** | **JavaScript (ES6+)**, **Vue.js 3**, **HTML5**, **CSS3** con **Diseño Responsivo** (Mobile & Desktop) |
| **Base de Datos (SQL)** | **MySQL** / **SQLite**, modelado relacional normalizado, consultas optimizadas (`JOIN`, `GROUP BY`, índices) |
| **Algoritmos & Estructuras** | Búsqueda binaria `O(log n)`, colas `FIFO` con `deque`, agregaciones `O(n)` con tablas hash (`inventario/estructuras_algoritmos.py`) |
| **Seguridad & Calidad** | Validación de payload en servidor, protección de endpoints, autenticación de usuario y *debugging* estructurado |

---

## 📂 Estructura del Proyecto

```text
nexstock-erp-api/
├── config/                         # Configuración principal de Django (MySQL / SQLite)
├── inventario/
│   ├── models.py                   # Modelos POO (CategoriaProducto, LoteInventario)
│   ├── services.py                 # Lógica de negocio, validaciones y cálculo de KPIs
│   ├── views.py                    # Controladores y Endpoints API REST / JSON
│   ├── estructuras_algoritmos.py   # Algoritmos O(log n), Colas FIFO y Tablas Hash
│   ├── urls.py                     # Enrutamiento Web y API REST
│   └── templates/
│       └── index.html              # SPA Reactiva con Vue.js 3 y Diseño Responsivo
├── sql/
│   └── schema_mysql.sql            # DDL MySQL + Consultas SQL avanzadas de reporte
├── manage.py
└── requirements.txt
```

---

## 🔌 Endpoints de la API REST (`/api/`)

* `GET /api/lotes/?q=&categoria_id=&estado=` — Lista productos/SKUs con filtrado dinámico y retorna indicadores **KPI** en formato **JSON**.
* `POST /api/lotes/` — Registra un nuevo SKU/Lote validando reglas de negocio.
* `GET /api/lotes/<id>/` — Obtiene el detalle de un registro específico.
* `PUT /api/lotes/<id>/` — Actualiza stock, costos, estado o ubicación.
* `DELETE /api/lotes/<id>/` — Elimina un registro del inventario.
* `GET /api/categorias/` — Lista las categorías activas.
* `POST /api/auth/login/` — Autenticación de usuarios y apertura de sesión segura.

---

## ⚙️ Instalación y Ejecución Local

1. **Clonar el repositorio e instalar dependencias:**
   ```bash
   git clone https://github.com/BRyanLopez23/nexstock-erp-api.git
   cd nexstock-erp-api
   pip install -r requirements.txt
   ```

2. **Ejecutar migraciones de base de datos:**
   ```bash
   python manage.py makemigrations inventario
   python manage.py migrate
   ```

3. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
   Abre `http://127.0.0.1:8000/` en tu navegador. Los datos de demostración se cargan automáticamente en el primer inicio.
