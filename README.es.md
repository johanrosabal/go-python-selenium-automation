# 🐍 Python Selenium Automation Framework

Este es un framework de automatización de nivel profesional y alta performance, diseñado para ofrecer escalabilidad, robustez y una experiencia de desarrollo excepcional. Basado en el patrón **Page Object Model (POM)** con **Singletons**, implementa una **Interfaz Fluida (Fluent API)**, ejecución en **Paralelo** y una arquitectura de **Pruebas Basadas en Datos (Data-Driven)**.

---

## 🏆 Calificación del Proyecto

| Categoría | Calificación | Nivel |
| :--- | :---: | :--- |
| **Arquitectura (POM + Fluent)** | ⭐⭐⭐⭐⭐ | **Enterprise** |
| **Performance (Parallel/Skip)** | ⭐⭐⭐⭐⭐ | **High Speed** |
| **Escalabilidad (Orchestrator)** | ⭐⭐⭐⭐⭐ | **Unbeatable** |
| **Mantenibilidad (JSON Data)** | ⭐⭐⭐⭐⭐ | **Simplified** |
| **Infraestructura (Grid/Video/DB)**| ⭐⭐⭐⭐⭐ | **Full Stack** |

**Estatus General: `PROFESSIONAL GRADE / PRODUCTION READY`**

---

## 🛠️ Guía de Instalación

Sigue estos pasos para configurar tu entorno de desarrollo en minutos:

### 1. Requisitos Previos
- **Python**: Versión 3.10 o superior. [Descargar](https://www.python.org/downloads/).
- **Git**: Para gestión de versiones.
- **Chrome/Edge/Firefox**: Navegador instalado.

### 2. Clonar y Configurar
```bash
git clone https://github.com/tu-usuario/python-selenium-automation.git
cd python-selenium-automation
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### 🏢 Entornos Corporativos (Certificados SSL)
Si te encuentras detrás de un proxy corporativo que requiere certificados de seguridad:

*   **Uso de certificado específico:**
    ```bash
    pip install --cert path/to/certificate.pem -r requirements.txt
    ```
*   **Configuración de Host Confiable (Opcional):**
    ```bash
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
    ```

### 4. Verificar Instalación
Ejecuta el comando para verificar que los drivers y dependencias carguen correctamente:
```bash
$env:PYTHONPATH = "."; pytest --version
```

---

## 🔌 Extensiones Recomendadas (VS Code)
Para una mejor experiencia de desarrollo, instala estas extensiones:
- **Python (Microsoft)**: Soporte completo de lenguaje e IntelliSense.
- **Pylance**: Análisis de código estático rápido.
- **vscode-icons**: Para identificar carpetas de forma visual.
- **Allure Support**: Para visualización de resultados dentro del IDE.

---

## 📁 Arquitectura del Proyecto

El sistema separa estrictamente la infraestructura (`core`) de los proyectos individuales (`applications`):

```text
├── .github/workflows/      # 🔄 CI/CD (GitHub Actions Pipeline)
├── applications/web/       # 📂 Capa de Aplicaciones (Proyectos reales)
│   └── demo/               # 🍏 SauceDemo Project
│       ├── app/            # 📦 Orquestador de Aplicación (Entry Point)
│       ├── config/         # ⚙️ Configuración YAML por Ambiente
│       ├── data/json/      # 📊 Datos por ID (CT-XXX.json)
│       ├── pages/          # 🏗️ Page Objects (POM)
│       └── tests/          # 🧪 Casos de Prueba (Scripts)
├── core/                   # 🧠 Núcleo del Framework (Inmutable)
│   ├── ui/actions/         # 🕹️ Componentes de Acción UI (Stateful Pattern)
│   ├── ui/common/          # 🧱 Singleton, BasePage, BaseTest UI
│   ├── api/actions/        # 🌐 Componentes de Acción API (GET, POST, etc.)
│   ├── api/common/         # 🏛️ BaseEndpoint, BaseAPITest, APIResponse
│   └── utils/              # 🧰 Logger, Config, Loader, Decorators
├── logs/                   # 🔎 Trazabilidad (automation.log)
├── reports/                # 📊 Resultados de Allure
└── pytest.ini              # ⚙️ Orquestador de Ejecución
```

---

## 📏 Convenciones y Estándares de Código

### 1. Nomenclatura (Naming)
| Elemento | Formato | Ejemplo |
| :--- | :--- | :--- |
| **Clases de Página** | `PascalCase` | `LoginPage`, `InventoryPage` |
| **Métodos de Acción**| `snake_case` (Verbo) | `login_as()`, `add_product()` |
| **Locators** | `CAPS_SNAKE` (Prefijo) | `INP_USERNAME`, `BTN_LOGIN` |

### 2. Estándar de Locadores (Prefixes)
| Prefijo | Elemento | Ejemplo |
| :--- | :--- | :--- |
| `btn` | Botones | `btn_login`, `btn_submit` |
| `inp` | Inputs / Campos | `inp_username`, `inp_search` |
| `txt` | Etiquetas / Textos| `txt_error_msg`, `txt_title` |
| `sel` | Dropdowns / Select | `sel_country`, `sel_size` |
| `chk` | Checkboxes | `chk_terms`, `chk_remember` |

---

## ⚙️ Sistema de Configuración (YAML)

El framework utiliza archivos YAML para gestionar parámetros específicos de cada ambiente (QA, DEV, PROD). Esto permite desacoplar los datos sensibles y las URLs del código fuente.

### 1. Ubicación de Archivos
Los archivos se encuentran en:
`applications/web/demo/config/environments/{env}.yaml`

### 2. Estructura Típica (`qa.yaml`)

El archivo de configuración permite centralizar todo lo que puede cambiar entre un ambiente y otro. A continuación se detallan las secciones principales:

#### 📝 Metadatos y Gestión
*   **`name`**: Nombre descriptivo del proyecto (ej: "SauceDemo - Swag Labs").
*   **`tms`**: URL base de tu herramienta de gestión de casos de prueba (Test Management System).

#### 🌐 Web y Navegación
*   **`web.base_url`**: La URL principal donde inician las pruebas. Usada por el método `.open()` sin argumentos.

#### 🖥️ Browser (Overrides Locales)
*   **`browser.edge_path`**: (Opcional) Ruta absoluta al ejecutable del driver si necesitas usar una versión específica cargada localmente.
*   **`default.browser`**: Define qué navegador usar si no se especifica uno por linea de comandos.

#### 📹 Grabación de Video (OpenCV)
*   **`video.enable_local`**: Activa/Desactiva la captura de pantalla (`true`/`false`).
*   **`video.fps`**: Velocidad de captura. Un valor de `10` es ideal para automatización.
*   **`video.monitor_index`**: Define qué monitor grabar (`0` para todos los monitores combinados, `1` para el monitor principal).

#### 👥 Datos de Usuario y Validación
Puedes definir múltiples perfiles de usuario para pruebas negativas y positivas:
*   **`user`**: Credenciales para el "Happy Path".
*   **`locked_user`**: Usuario bloqueado para probar mensajes de error.
*   **`messages`**: Textos esperados para aserciones (ej: `error_locked`, `error_invalid`).

#### 🛠️ Ejemplo de Uso de Mensajes
```python
def test_user_locked(self):
    mensaje_esperado = ConfigManager.get("messages.error_locked")
    self.app.login_page.login("locked_out_user", "secret_sauce")
    assert self.app.login_page.get_error_message() == mensaje_esperado
```

### 3. Cómo usar el `ConfigManager`
Para acceder a estos valores desde tus Page Objects o Tests, usa la notación de punto (`.`):

```python
from core.utils.config_manager import ConfigManager

# Obtener URL base
url = ConfigManager.get("web.base_url")

# Obtener credenciales
user = ConfigManager.get("user.username")

# Con valor por defecto si no existe
timeout = ConfigManager.get("web.timeout", 30)
```

> [!NOTE]
> El ambiente activo se define mediante la variable de entorno `$env:ENV`. Si no se define, el framework carga `qa.yaml` por defecto.

---

## 🚀 Guía del Desarrollador (Productividad)

Sigue este flujo para añadir nuevas pruebas al framework de forma estandarizada. Tienes dos opciones: usar las herramientas automatizadas o el proceso manual.

### ⚡ Opción A: Creación Automatizada (Recomendado)

El framework incluye un sistema de **Scaffolding** integrado con VS Code para acelerar el desarrollo.

#### 1. Uso desde VS Code (Interfaz Visual)
1. Presiona `Ctrl + Shift + P` y busca **`Tasks: Run Task`**.
2. Selecciona una de las tareas inteligentes:
   - **`🚀 Scaffold: New Page Object`**: Crea la página y la registra en el Orquestador automáticamente.
   - **`🧪 Scaffold: New Test Case`**: Genera un archivo de prueba con decoradores listos.
   - **`🖥️ Runner: Launch UI`**: Levanta la interfaz gráfica del Test Runner (Flask).
   - **`📊 Allure: Open Report Server`**: Genera y abre el servidor de reportes Allure.
3. Sigue los cuadros de diálogo para ingresar el nombre de la app, clase e ID.

#### 2. Uso desde Terminal (CLI)
Si prefieres la terminal, usa el script `tools/scaffold.py`:

```powershell
# Crear y registrar una Page
python tools/scaffold.py page --name PerfilPage --app go_hotel

# Crear un Test Case
python tools/scaffold.py test --name Perfil --app go_hotel --id HOTEL-001 --feature Perfil
```

---

### 🛠️ Opción B: Creación Manual (Paso a Paso)
Crea un archivo en `applications/web/demo/pages/nombre_page.py`. Hereda de `BasePage` y usa la **API Fluida**.

```python
from core.ui.common.base_page import BasePage
from selenium.webdriver.common.by import By

class DashboardPage(BasePage):
    # 1. Definir Locadores (CAPS_SNAKE)
    BTN_PERFIL = (By.ID, "user-profile")
    
    # 2. Métodos de Acción (Fluent)
    def ir_a_perfil(self):
        self.element(self.BTN_PERFIL).click()
        return self # Permite encadenar: page.ir_a_perfil().validar...
```

### 2. Registrar en el Orquestador (DemoApp)

El **Orquestador (App Orchestrator)** es el corazón de la interactuación en tus tests. Su función es centralizar todas las "Páginas" del proyecto en un solo lugar, permitiendo que tus tests sean mucho más limpios y fáciles de escribir.

#### 💡 ¿Por qué usar un Orquestador?
1.  **Punto de Entrada Único**: En tus tests solo usas `self.app`, no necesitas instanciar clases manualmente.
2.  **Lazy Loading (Carga Perezosa)**: Las páginas solo se crean en memoria si el test realmente las necesita. Si un test solo usa el Login, el sistema no gastará recursos creando el resto de las páginas.
3.  **IntelliSense Total**: Al usar tipado de Python (`-> LoginPage`), el editor te sugerirá todos los métodos disponibles automáticamente mientras escribes.

#### 🛠️ Cómo registrar una nueva Página
Sigue este patrón en `applications/web/demo/app/demo_app.py`:

1.  **Importar la Clase**:
    ```python
    from applications.web.demo.pages.perfil_page import PerfilPage
    ```

2.  **Crear la Propiedad con Lazy Loading**:
    ```python
    @property
    def perfil_page(self) -> PerfilPage:
        """Instancia de PerfilPage con carga perezosa."""
        # Verifica si ya existe la instancia, si no, la crea una sola vez
        if not hasattr(self, "_perfil_page") or self._perfil_page is None:
            self._perfil_page = PerfilPage()
        return self._perfil_page
    ```

#### 🚀 Uso en los Tests
Gracias al registro, ahora puedes acceder a cualquier página de forma fluida:

```python
def test_ejemplo(self):
    # Sin orquestador: login = LoginPage(); login.open()...
    # CON orquestador:
    self.app.login_page.open().login()
    self.app.perfil_page.editar_nombre("Antigravity")
```

### 3. Preparar Datos de Prueba (JSON)

El framework utiliza archivos JSON para inyectar datos dinámicos en los tests. Esto permite ejecutar la misma lógica con diferentes juegos de datos sin tocar el código del test.

#### 📁 Ubicación y Naming
Los archivos deben guardarse en:
`applications/web/{app_name}/data/environments/{env_name}/{test_id}.json`

> [!IMPORTANT]
> **Convención de Naming**: El nombre del archivo debe coincidir con el `id` que uses en el decorador `@test_case(id="...")`. Por ejemplo, si el ID es `CT-LOGIN-001`, el archivo debe llamarse `CT-LOGIN-001.json`.

#### 🏗️ Estructura del JSON
El framework espera una raíz `tests` que contenga un objeto `data`. Dentro de `data` puedes estructurar la información como prefieras:

```json
{
  "tests": {
    "id": "CT-LOGIN-001",
    "title": "Login con credenciales válidas",
    "description": "Login con credenciales válidas",
    "feature": "Authentication",
    "story": "Login",
    "severity": "CRITICAL",
    "tag": ["smoke", "p1"],
    "data": {
      "user": "standard_user",
      "pass": "secret_sauce",
      "expected_url": "/dashboard"
    }
  }
}
```

#### 🛠️ Cómo recuperar los datos en el Test
Dentro de tu clase de test (que hereda de `BaseTest`), usa el método `self.get_data_for_test()`:

```python
@test_case(id="CT-LOGIN-001")
def test_valid_login(self):
    # Carga automáticamente CT-LOGIN-001.json
    test_data = self.get_data_for_test()
    
    # Extraer valores específicos
    user = test_data.get("user")
    password = test_data.get("pass")
    
    self.app.login_page.open().login(user, password)
```

#### 💡 Ventajas de este enfoque
1.  **Mantenibilidad**: Si cambian las credenciales o los valores esperados, solo editas el JSON.
2.  **Reportes Enriquecidos**: El ID se vincula automáticamente en los reportes de Allure.
3.  **Trazabilidad**: Permite mapear fácilmente cada script de automatización con su caso de prueba en herramientas de gestión (TMS).

### 4. Crear el Test Case
Crea un archivo en `applications/web/demo/tests/test_feature.py`. Hereda de `BaseTest` y usa `self.app`.

```python
from core.ui.common.base_test import BaseTest
from core.utils.decorators import test_case

class TestDashboard(BaseTest):
    @test_case(id="CT-DASH-001")
    def test_acceso_perfil(self):
        data = self.get_data_for_test()
        # El orquestador ya tiene el driver configurado
        self.app.login_page.open().login()
        self.app.dashboard_page.ir_a_perfil()
        
        assert "profile" in self.get_url()
```

### 5. Ejecutar Pruebas
```powershell
# Ejecutar todos los tests del proyecto
$env:PYTHONPATH = "."; pytest applications/web/demo/tests

# Ejecutar un test específico con reporte Allure
pytest applications/web/demo/tests/test_feature.py --alluredir=reports
```

### 6. Manejo de Precondiciones (Fixtures)
Para acciones repetitivas antes de un test (ej. Login), usa Pytest Fixtures en `fixtures/preconditions.py`.

```python
# 1. Definir en fixtures/preconditions.py
@pytest.fixture
def logged_in(app):
    app.login_page.open().login("user", "pass")
    return app

# 2. Usar en el test
def test_mi_flujo(self, logged_in):
    # El test inicia ya logueado
    self.app.inventory_page.hacer_algo()
```

### 7. Compartir Datos entre Tests (SessionContext)
Si necesitas pasar un ID o valor generado en un Test A a un Test B.

```python
from core.utils.session_context import SessionContext

def test_a_crear_orden(self):
    orden_id = self.app.orden_page.crear()
    SessionContext.set("last_order", orden_id)

def test_b_validar_orden(self):
    orden_id = SessionContext.get("last_order")
    self.app.orden_page.buscar(orden_id)
```

---

## 🚀 Arquitectura de Tests y Patrones Avanzados

El framework implementa patrones avanzados para maximizar la velocidad de ejecución y la facilidad de desarrollo.

### 1. Sesiones Persistentes (`persistent_session = True`)
Por defecto, el framework abre y cierra el navegador para cada método de test (aislamiento total). Sin embargo, en flujos largos o suites de regresión, puedes habilitar la persistencia a nivel de clase:

```python
class TestReserved(BaseTest):
    # Mantiene el mismo navegador para todos los métodos de esta clase
    persistent_session = True 
```
*   **Ventaja**: Reduce el tiempo total de ejecución hasta en un 40% al evitar el "cold start" del navegador.
*   **Limpieza**: El framework se encarga de cerrar el navegador automáticamente al finalizar el último test de la clase.

### 2. Tipado y Autocompletado (`app: GoHotelApp`)
Para aprovechar al máximo el poder de VS Code (IntelliSense), es fundamental definir el tipo del orquestador en tu clase de test:

```python
class TestReserved(BaseTest):
    # Indica al editor que 'self.app' es un GoHotelApp
    app: GoHotelApp 
```
*   **Resultado**: Al escribir `self.app.`, el editor te sugerirá automáticamente todas las páginas disponibles (`login_page`, `reserved_page`, etc.) y sus métodos internos. No necesitas adivinar los nombres.

### 3. Decorador de Aplicación (`@go_hotel`)
Este decorador de clase configura instantáneamente el contexto de ejecución para un proyecto específico:

```python
@go_hotel
class TestLogin(BaseTest):
    ...
```
*   **¿Qué hace?**: Establece los valores por defecto de `app_name`, `profile` (dev/qa), y `browser`. Esto permite ejecutar el test directamente desde el botón "Run" del IDE sin configurar variables de entorno manualmente.

### 4. Decorador de Caso de Prueba (`@test_case`)
Es el componente más potente para la trazabilidad y la inyección de datos. **Solo necesitas pasar el `id`** — el resto de los metadatos se leen automáticamente del JSON:

```python
@test_case(id="HOTEL-001")
def test_login_exitoso(self):
    ...
```

*   **Inyección de Metadatos Automática**: El framework carga `HOTEL-001.json` durante el `setup` y extrae el `title`, `description`, `severity`, `feature`, `story` y `tag` directamente del bloque `tests`. No necesitas repetirlos en el decorador.
*   **Prioridad de Resolución**: `JSON → Argumento del decorador → Nombre de la función`. Si defines `title=` en el decorador, sobrescribe el JSON. Si no defines nada, usa el nombre de la función.
*   **Reportes Allure**: Sincroniza automáticamente todos los metadatos del JSON con el reporte (título, severidad, tags, TMS link).
*   **Integración TMS**: Si tienes una herramienta de gestión de tests (Jira/TestRail), el `id` crea un enlace directo en el reporte Allure.

> [!TIP]
> **Regla de oro**: el decorador solo necesita el `id`. Todo lo demás vive en el JSON, que es la única fuente de verdad.

---

## 🕹️ Catálogo Detallado de Métodos

### 1. Navegación y Contexto (BasePage)
| Método | Retorna | Descripción |
| :--- | :--- | :--- |
| `.open(url)` | `this` | Navega a la URL especificada (o `base_url`). |
| `.open_relative(path)` | `this` | Navega a una ruta relativa (ej: `/inventory`). |
| `.get_url()` | `string` | Retorna la URL actual del navegador. |
| `.wait_for_url(url)` | `this` | Espera hasta que la URL contenga el texto. |
| `.navigation.back()` | `this` | Vuelve a la página anterior. |
| `.navigation.forward()` | `this` | Va a la página siguiente en el historial. |
| `.navigation.refresh()` | `this` | Recarga la página actual. |
| `.navigation.get_current_url()` | `string` | Retorna la URL actual (vía componente). |

### 2. Ventanas y Frames (BasePage)
| Método | Retorna | Descripción |
| :--- | :--- | :--- |
| `.window.open_new()` | `this` | Abre una nueva pestaña/ventana en blanco. |
| `.window.switch_to_new()` | `this` | Cambia el foco a la última pestaña abierta. |
| `.window.switch_to_main()` | `this` | Vuelve a la pestaña inicial (índice 0). |
| `.window.to_tab(index)` | `this` | Cambia a una pestaña por su índice numérico. |
| `.window.close_current()` | `this` | Cierra la pestaña actual y vuelve a la anterior. |
| `.window.get_handles()` | `list` | Retorna todos los IDs de ventana del driver. |
| `.frame.switch_to(loc)` | `this` | Cambia el foco a un iframe específico. |
| `.frame.switch_to_parent()` | `this` | Sube un nivel al frame padre. |
| `.frame.switch_to_default()`| `this` | Vuelve al documento principal del navegador. |
| `.alert.wait_presence()`   | `this` | Espera que aparezca una alerta/confirm/prompt. |
| `.alert.accept()`          | `this` | Acepta la alerta (OK). |
| `.alert.dismiss()`         | `this` | Cancela la alerta (Cancel). |
| `.alert.type(text)`        | `this` | Escribe en un prompt de JavaScript. |
| `.alert.get_text()`        | `string` | Retorna el texto del diálogo. |

### 3. Interacciones de Mouse (UIElement)
| Método | Retorna | Descripción |
| :--- | :--- | :--- |
| `.click()` | `this` | Clic izquierdo con espera de clickabilidad. |
| `.js_click()` | `this` | Clic forzado mediante JavaScript. |
| `.double_click()` | `this` | Doble clic (ActionChains). |
| `.right_click()` | `this` | Clic derecho (Context Click). |
| `.hover()` | `this` | Mover el mouse sobre el elemento. |
| `.drag_and_drop(loc)` | `this` | Arrastra el elemento hasta otro destino. |
| `.click_and_hold()` | `this` | Mantiene el clic presionado. |
| `.release_mouse()` | `this` | Releases mouse button. |
| `.release()` | `this` | Alias for `.release_mouse()`. |

### 4. Teclado y Datos (UIElement)
| Método | Retorna | Descripción |
| :--- | :--- | :--- |
| `.type(text)` | `this` | Escribe texto (limpia el campo por defecto). |
| `.type_encrypted(key)` | `this` | Escribe texto ocultándolo en los logs. |
| `.type_by_character(v)` | `this` | Simula escritura humana (carácter a carácter). |
| `.press(key)` | `this` | Envía una tecla especial (ej: `Keys.ENTER`). |
| `.press_enter()` | `this` | Acceso rápido para la tecla ENTER. |
| `.press_tab()` | `this` | Acceso rápido para la tecla TAB. |
| `.press_return()` | `this` | Acceso rápido para la tecla RETURN. |
| `.press_escape()` | `this` | Acceso rápido para la tecla ESCAPE. |
| `.clear()` | `this` | Vacía el contenido de un input. |

### 5. Scroll y Visibilidad (UIElement)
| Método | Retorna | Descripción |
| :--- | :--- | :--- |
| `.scroll_to(offset)` | `this` | Scrolls viewport to element with an optional offset. |
| `.scroll_to_center()` | `this` | Centra el elemento exactamente en pantalla. |
| `.scroll_to_top()` | `this` | Sube al inicio de la página. |
| `.scroll_to_bottom()` | `this` | Baja al final de la página. |

### 6. Dropdowns y Listas (UIElement)
| Método | Retorna | Descripción |
| :--- | :--- | :--- |
| `.select_by_text(val)` | `this` | Selecciona por texto visible exacto. |
| `.select_by_value(val)` | `this` | Selecciona por el atributo 'value'. |
| `.select_by_index(i)` | `this` | Selecciona por índice (0-based). |
| `.select_by_partial_text`| `this` | Selecciona si contiene el texto indicado. |
| `.deselect_all()` | `this` | Quita todas las selecciones (multi-select). |
| `.get_dropdown_options()`| `list` | Retorna todos los textos de las opciones. |

### 7. Estados y Esperas (UIElement)
| Método | Retorna | Descripción |
| :--- | :--- | :--- |
| `.wait_visible()` | `bool` | Espera hasta que el elemento sea visible. |
| `.wait_present()` | `bool` | Espera hasta que esté en el DOM. |
| `.wait_clickable()` | `this` | Espera hasta que se pueda interactuar. |
| `.wait_disappear()` | `this` | Espera hasta que el elemento se oculte/borre. |
| `.wait_text_contains(v)`| `this` | Espera hasta que el texto contenga un valor. |
| `.is_visible()` | `bool` | Retorna si es visible actualmente. |
| `.is_present()` | `bool` | Retorna si está presente en el DOM. |
| `.is_enabled()` | `bool` | Retorna si el elemento está habilitado. |
| `.is_enabled_js()` | `bool` | Verifica estado habilitado vía JS. |
| `.is_clickable()` | `bool` | Verifica si es visible y habilitado. |
| `.get_css_value(p)` | `string` | Retorna el valor de una propiedad CSS. |
| `.set_css_value(p, v)` | `this` | Ajusta una propiedad CSS vía JS. |

### 8. Tablas y Grillas (UIElement)
| Método | Retorna | Descripción |
| :--- | :--- | :--- |
| `.get_cell_text(r, c)` | `string` | Retorna el texto de una celda (Fila, Col). |
| `.get_row_count()` | `int` | Retorna el número total de filas. |
| `.get_table_headers()` | `list` | Retorna todos los nombres de columnas. |
| `.get_table_data()` | `list[dict]`| Extrae toda la tabla como lista de dicts. |
| `.click_table_header(t)` | `this` | Clic en cabecera por texto o índice. |
| `.table_check_row(r)` | `this` | Marca el checkbox de una fila específica. |
| `.table_click_button(r, c, t)` | `this` | Clic en botón dentro de celda. |
| `.table_click_link(r, c, t)` | `this` | Clic en link dentro de celda. |
| `.table_wait_for_rows(n)`| `this` | Espera a que la tabla tenga N filas. |
| `.table_wait_not_empty()`| `this` | Espera a que la tabla tenga datos. |

### 9. Capturas y Sincronización Global (BasePage)
| Método | Retorna | Descripción |
| :--- | :--- | :--- |
| `.scroll_to_top()` | `this` | Sube al inicio de la página (Global). |
| `.scroll_to_bottom()` | `this` | Baja al final de la página (Global). |
| `.screenshot.capture(n)` | `this` | Captura viewport actual. |
| `.screenshot.full_page` | `this` | Captura página completa (scroll). |
| `.wait_for_page_load()` | `this` | Espera a que el DOM esté 'complete'. |
| `.wait_for_js_completion`| `this` | Espera a que termine actividad JS/jQuery. |

### 10. Extracción de Datos y Atributos (UIElement)
| Método | Retorna | Descripción |
| :--- | :--- | :--- |
| `.get_text()` | `string` | Retorna el texto visible del elemento. |
| `.get_trimmed_text()`| `string` | Retorna el texto sin espacios al inicio/final. |
| `.get_value()` | `string` | Retorna el valor del atributo 'value'. |
| `.get_int()` | `int` | Extrae el primer número entero del texto. |
| `.get_float()` | `float` | Extrae el primer número decimal del texto. |
| `.all_texts()` | `list[str]`| Retorna los textos de todos los elementos hijos. |
| `.get_inner_html()` | `string` | Captura el código HTML interno. |
| `.get_outer_html()` | `string` | Captura el HTML completo del tag. |
| `.get_text_content()`| `string` | Captura texto incluso si está oculto. |
| `.get_attribute(n)` | `string` | Retorna el valor de un atributo específico. |
| `.contains_text(t)` | `bool` | Verifica si contiene el texto indicado. |
| `.matches_regex(p)` | `bool` | Valida el texto contra un Regex. |
| `.is_empty()` | `bool` | Verifica si no tiene contenido de texto. |
| `.wait_until_text_is(t)`| `this` | Espera hasta que el texto sea idéntico. |
| `.at(seconds)` | `this` | Ajusta el timeout para la siguiente acción. |
| `.upload_file(path)` | `this` | Sube un archivo. |

---

## 💡 Ejemplos Prácticos de Uso (Catálogo Completo)

### 1. Navegación y Gestión de Ventanas
```python
def login_y_nueva_pestana(self):
    self.open_relative("/dashboard")
    
    # Abre ventana, espera carga y valida URL
    self.window.open_new()
    self.window.switch_to_new()
    self.wait_for_page_load()
    self.navigation.wait_url_contains("google.com", timeout=5)
    
    # Cierra y vuelve al contexto original
    self.window.close_current() 
    self.window.switch_to_main()
```

### 2. Formularios y Teclado Avanzado
```python
def completar_perfil(self):
    # Escritura humana (carácter a carácter)
    self.element(BIO).type_by_character("Amo la automatización...")
    
    # Teclas rápidas encadenadas
    self.element(SEARCH).type("Playwright").press_enter().press_escape()
    
    # Datos sensibles (no aparecerán en logs)
    self.element(PWD).type_encrypted("SuperSecret123")
```

### 3. Dropdowns y Selección (Selects)
```python
def configurar_preferencias(self):
    # Selección por múltiples criterios
    self.element(PAIS).select_by_text("España")
    self.element(MONEDA).select_by_value("EUR")
    self.element(IDIOMA).select_by_index(0)
    
    # Multi-select: deseleccionar todo
    self.element(INTERESES).deselect_all()
    
    # Validar opciones disponibles
    opciones = self.element(MODULO).get_dropdown_options()
    if "Admin" in opciones:
        self.element(MODULO).select_by_partial_text("Admin")
```

### 4. Tablas y Grillas Dinámicas
```python
def gestionar_usuarios(self):
    # Esperas inteligentes para tablas
    self.element(USERS_TABLE).table_wait_not_empty()
    self.element(USERS_TABLE).table_wait_for_rows(5)
    
    # Extracción masiva
    data = self.element(USERS_TABLE).get_table_data()
    headers = self.element(USERS_TABLE).get_table_headers()
    
    # (row=1-based, col=nombre o índice)
    self.element(USERS_TABLE).table_click_button(row=2, col="Acciones", text="Eliminar")
    self.element(USERS_TABLE).table_check_row(row=4, column=1) # Marca checkbox
```

### 5. IFrames y Contextos
```python
def interactuar_con_frame(self):
    # Entra al iframe
    self.frame.switch_to(self.PAYMENT_IFRAME_LOCATOR)
    
    # Acciones dentro del frame
    self.element(CARD_NUMBER).type("4242...")
    
    # Vuelve al documento principal
    self.frame.switch_to_default()
    
    # O sube solo un nivel si hay anidamiento
    self.frame.switch_to_parent()
```

### 6. Desplazamiento (Scroll) y Visibilidad
```python
def validar_footer_pixel_perfect(self):
    # Scroll global (BasePage)
    self.scroll_to_bottom()
    
    # Scroll local al elemento con offset
    self.element(FOOTER).scroll_to(offset=100)
    
    # Centrar exactamente para capturas
    self.element(LOGO).scroll_to_center().screenshot("logo_centrado")
```

### 7. Verificaciones y Extracción de Datos
```python
def validar_totales(self):
    # Parseo automático de números
    monto_total = self.element(TOTAL_LBL).get_float() # Retorna float real
    conteo = self.element(BADGE).get_int() # Retorna int real
    
    # Regex y patrones
    if self.element(FECHA).matches_regex(r"\d{2}/\d{2}/\d{4}"):
         print("Formato de fecha correcto")
         
    # Atributos técnicos
    clase_css = self.element(BTN).get_attribute("class")
    html_crudo = self.element(BODY).get_outer_html()
```

### 8. Gestión de Tiempos Críticos (`at()`)
```python
def flujo_pesado(self):
    # Forza un timeout largo solo para ESTA acción específica
    self.element(EXPORT_BTN).at(60).click()
    
    # Espera que un texto específico aparezca después de un proceso
    self.element(STATUS).at(120).wait_until_text_is("Completado")
```

### 9. Manejo de Alertas y Prompts
```python
def manejo_de_alertas(self):
    # Escribir en un prompt y aceptar
    self.alert.wait_presence().type("Antigravity").accept()
    
    # Validar texto y cancelar
    if "Seguro?" in self.alert.get_text():
        self.alert.dismiss()
```

### 10. Carga de Archivos (Smart Discovery)
```python
    # Soporta rutas absolutas
    self.element(UPLOAD_INP).upload_file("C:/temp/manual.pdf")
```

---

> [!TIP]
> **✨ El Poder de la Interfaz Fluida (Method Chaining)**
>
> Puedes encadenar múltiples acciones quirúrgicas sobre un solo elemento en una sola línea. El framework gestiona las esperas y el contexto de forma transparente:
>
> ```python
> # 1. Selecciona el elemento
> # 2. Aplica un timeout de 30s solo para esta cadena
> # 3. Se desplaza hasta centrarlo en pantalla
> # 4. Pone el mouse encima (hover) para activar efectos CSS
> # 5. Captura una evidencia visual del hover
> # 6. Espera a que sea cliqueable (por si tiene animaciones)
> # 7. Realiza el click final
> self.app.dashboard_page.element(BTN_ADAVANCED_CONFIG) \
>     .at(30) \
>     .scroll_to_center() \
>     .hover() \
>     .screenshot("btn_hover_state") \
>     .wait_clickable() \
>     .click()
> ```

---

## 🌐 API Testing (Endpoints Object Model - EOM)

Siguiendo la misma filosofía que el POM para UI, el framework implementa el patrón **Endpoints Object Model (EOM)** para pruebas de API robustas, escalables y con aserciones fluidas.

### 1. Arquitectura EOM
*   **`BaseEndpoint`**: Centraliza las acciones HTTP (`get`, `post`, `put`, `delete`).
*   **`BaseAPITest`**: Gestiona sesiones de `requests`, autenticación y configuración de ambiente.
*   **`APIResponse`**: Wrapper para respuestas que permite encadenar validaciones (Fluent Assertions).

### 2. Ejemplo de Endpoint Object
Crea tus objetos de endpoint en `applications/api/{app_name}/endpoints/`:

```python
from core.api.common.base_endpoint import BaseEndpoint

class UserEndpoint(BaseEndpoint):
    def __init__(self, session):
        super().__init__(session)
        self.url = f"{self.base_url}/users"

    def get_users(self):
        return self.get.call(self.url)

    def create_user(self, name, job):
        return self.post.call(self.url, json={"name": name, "job": job})
```

### 3. Ejemplo de Test de API
```python
from core.api.common.base_api_test import BaseAPITest
from applications.api.demo.endpoints.user_endpoint import UserEndpoint

class TestUserAPI(BaseAPITest):
    app_name = "demo"
    
    def test_create_user(self):
        # 1. Instanciar el endpoint
        users_api = UserEndpoint(self.session)
        
        # 2. Ejecutar y Validar de forma fluida
        users_api.create_user("Johan", "QA") \
            .assert_status_code(201) \
            .assert_json_path("name", "Johan")
```

### 4. App Client Orchestrator (API)
Al igual que el UI tiene `DemoApp`, la capa API usa un **Client Orchestrator** para encapsular flujos multi-endpoint y exponer acceso con Lazy Loading:

```python
# applications/api/nico_search/client.py
class NicoSearchClient:
    def __init__(self, session, config: dict):
        self._session = session
        self._search = None

    @property
    def search(self) -> SearchEndpoint:
        """Lazy-loaded SearchEndpoint."""
        if self._search is None:
            self._search = SearchEndpoint(self._session, self._config)
        return self._search

    def search_and_get_results(self, payload: dict):
        """Composed flow: POST → obtiene GUID → GET resultados."""
        search_response = self.search.search_policies(payload)
        search_response.assert_status_code(201)
        search_id = search_response.body.strip()
        return search_id, self.search.get_results(search_id)
```

`BaseAPITest` auto-descubre y carga el Client por convención de nombre (`client.py`). En los tests simplemente usas `self.app`:

```python
class TestNicoSearch(BaseAPITest):
    app_name = "nico_search"  # ← auto-carga NicoSearchClient como self.app

    @test_case(id="SEARCH-001")
    def test_complete_search_flow(self):
        data = self.get_test_data("SEARCH-001")
        search_id, results = self.app.search_and_get_results(data["data"]["payload"])
        results.assert_status_code(200)
```

### 5. Ventajas del EOM
- **Logging Automático**: Todas las peticiones y respuestas se registran con iconos visuales en la consola y Allure.
- **Fluent Assertions**: Valida status codes y contenido JSON en una sola línea.
- **Mantenibilidad**: Los cambios en los contratos de API se reflejan en un solo lugar (el Endpoint Object).
- **Client Orchestrator**: Encapsula flujos multi-step, el test no sabe qué endpoints internos se llaman.

---

## 📊 Data-Driven & Allure Integration

### 1. Estructura Estándar del JSON (UI & API)
Todos los archivos JSON del framework — tanto UI como API — siguen la **misma estructura obligatoria**. El nombre del archivo debe coincidir con el `id` del decorador `@test_case`.

#### 🖥️ JSON para Tests de UI (`data/{env}/{TEST-ID}.json`)
```json
{
  "tests": {
    "id": "CT-LOGIN-001",
    "title": "Login con credenciales válidas",
    "description": "Verifica el happy path de login con usuario estándar.",
    "feature": "Authentication",
    "story": "Login",
    "severity": "CRITICAL",
    "tag": ["smoke", "p1"],
    "data": {
      "user": "standard_user",
      "pass": "secret_sauce",
      "expected_url": "/dashboard"
    }
  }
}
```

#### 🌐 JSON para Tests de API (`data/{env}/{TEST-ID}.json`)
Para APIs, el `data` contiene un `payload` que representa el body del request:
```json
{
  "tests": {
    "id": "SEARCH-001",
    "title": "Complete Search Flow (POST + GET Results)",
    "description": "End-to-end: POST para iniciar búsqueda → GET resultados por GUID.",
    "feature": "Policy Search",
    "story": "Search Policies",
    "severity": "CRITICAL",
    "tag": ["smoke", "p1", "e2e"],
    "data": {
      "payload": {
        "firstName": "John",
        "lastName": "Doe",
        "policyState": "TX"
      }
    }
  }
}
```

> [!IMPORTANT]
> **El JSON es la única fuente de verdad.** El `@test_case` lee `title`, `description`, `severity`, `feature`, `story` y `tag` directamente del JSON. **No los repitas en el decorador.**

### 2. Cómo acceder a los datos en el test

#### Tests de UI (`BaseTest`)
```python
@test_case(id="CT-LOGIN-001")
def test_valid_login(self):
    data = self.get_data_for_test()          # retorna tests.data {}
    self.app.login_page.open().login(data.get("user"), data.get("pass"))
```

#### Tests de API (`BaseAPITest`)
```python
@test_case(id="SEARCH-001")
def test_search_flow(self):
    data = self.get_test_data("SEARCH-001")  # retorna tests {} completo
    payload = data["data"]["payload"]        # extrae el payload del request
    self.app.search_and_get_results(payload).assert_status_code(200)
```

---

## 📹 Grabación de Video y Limpieza

El framework incluye un sistema de grabación de pantalla local para documentar ejecuciones y una limpieza automática de artefactos para mantener el espacio de trabajo ordenado.

### 1. Configuración de Video (qa.yaml)
Puedes habilitar o deshabilitar la grabación en `applications/web/demo/config/environments/qa.yaml`:

```yaml
video:
  enable_local: true  # true para grabar, false para desactivar
  fps: 10             # Cuadros por segundo (Recomendado: 10-15)
  monitor_index: 0    # 0 para capturar todos los monitores, 1 para el principal
```

> [!WARNING]
> **Privacidad**: La grabación local captura la **pantalla completa** de tu computadora. Asegúrate de no tener información sensible visible durante los tests.

### 2. Almacenamiento y Visualización
*   **Ruta**: Los videos se guardan en `reports/videos/` con formato `.avi`.
*   **VS Code**: Se recomienda la extensión **"Media Preview"** para ver los videos directamente en el editor.

### 3. Limpieza Automática
El framework está configurado para **borrar automáticamente** la carpeta `reports/` (incluyendo videos pasados) al inicio de cada nueva sesión de pruebas. Esto asegura que solo veas los resultados de la ejecución actual.

---

## 🗄️ Integración de Base de Datos (SQLAlchemy)

El framework soporta conexiones a múltiples motores de base de datos (PostgreSQL, SQL Server, MySQL, SQLite) mediante **SQLAlchemy**.

### 1. Configuración (qa.yaml)
Define la URL de conexión en tu archivo de ambiente:

```yaml
database:
  url: "postgresql://user:pass@localhost:5432/dbname"
  # O para SQLite local: "sqlite:///resources/data/test.db"
```

### 2. Estructura de Capas
*   **`core/utils/db_client.py`**: El motor genérico. Maneja el pool de conexiones y sesiones.
*   **`applications/web/demo/app/db_manager.py`**: La capa de negocio. Aquí es donde debes escribir tus queries SQL específicas (SELECT, INSERT, UPDATE, DELETE).

### 3. Uso en los Tests
Accede a la base de datos a través del orquestador:

```python
def test_validar_registro_db(self):
    # Usar una query predefinida en DBManager
    user = self.app.db.get_user_by_username("test_user")
    assert user["email"] == "test@example.com"
    
    # O ejecutar una query directa (solo para mantenimiento/limpieza)
    self.app.db.client.execute_query("DELETE FROM logs WHERE user_id = :id", {"id": 123})
```

---

## 🚀 Funcionalidades "God Tier" Avanzadas

El framework incluye una suite de funcionalidades avanzadas diseñadas para automatización de nivel empresarial.

### 1. Pruebas de Regresión Visual
Realiza comparaciones pixel-perfect de la interfaz de usuario contra imágenes base (baselines).
- **Uso**: `self.app.login_page.assert_visual_match("id_unico_del_test")`
- **Resultado**: Los "diffs" (diferencias) se guardan en `reports/visual/diffs/` si la prueba falla.

### 2. Pruebas de Accesibilidad (A11y)
Escaneos automáticos de cumplimiento WCAG potenciados por **Axe-Core**.
- **Uso**: `self.app.login_page.assert_no_accessibility_violations(impact_level="critical")`
- **Resultado**: Reportes detallados de violaciones en `reports/accessibility/`.

### 3. Monitoreo de Rendimiento del Navegador
El framework permite capturar métricas de rendimiento directamente desde el motor del navegador, lo que permite detectar degradaciones en el tiempo de respuesta que las pruebas funcionales tradicionales suelen pasar por alto.

#### 📊 Métricas Capturadas (Navigation Timing API)
El sistema extrae los siguientes indicadores clave (en milisegundos):

*   **DNS Lookup (`dns_lookup_time`)**: Tiempo que tarda el navegador en resolver el nombre del dominio. Un valor alto puede indicar problemas con el servidor DNS o configuraciones de red.
*   **Connection Time (`connection_time`)**: Tiempo para establecer la conexión TCP y el handshake de SSL/TLS.
*   **Response Time / TTFB (`response_time`)**: Tiempo desde que se envía la petición hasta que se recibe el primer byte del servidor. Crucial para medir la velocidad del backend.
*   **DOM Interactive (`dom_interactive_time`)**: Punto en el que el navegador ha terminado de parsear el HTML y el usuario ya puede empezar a ver elementos en pantalla.
*   **DOM Content Loaded (`dom_content_loaded_time`)**: Tiempo en el que el DOM está listo y los scripts iniciales se han ejecutado.
*   **Total Page Load (`page_load_time`)**: Tiempo total hasta que el evento `load` se dispara (todas las imágenes, scripts y recursos externos han terminado de cargar).

#### 🛠️ Cómo Utilizarlo
Puedes capturar estas métricas en cualquier punto de tu prueba, preferiblemente después de una navegación o acción que cargue contenido nuevo:

```python
def test_performance_dashboard(self):
    self.app.login_page.open().login()
    
    # Captura métricas de la página actual
    metrics = self.app.dashboard_page.capture_performance_metrics()
    
    # Ejemplo de aserción de rendimiento (SLA)
    assert metrics["page_load_time"] < 3000, "La página tarda más de 3 segundos en cargar"
```

#### 📂 Reportes de Performance
Cada vez que llamas a `capture_performance_metrics()`, el sistema genera un reporte JSON detallado en:
`reports/performance/{PageName}_performance.json`

Este archivo contiene tanto las métricas calculadas como el objeto `raw_timing` completo para un análisis forense profundo si fuera necesario.

> [!TIP]
> **Integración CI/CD**: Estos archivos JSON pueden ser recolectados por herramientas de visualización de datos para crear dashboards de tendencia de rendimiento a lo largo del tiempo.

### 4. Auto-healing (Auto-recuperación de Locadores)
El framework incluye un sistema de **resiliencia inteligente** que evita que las pruebas fallen ante cambios menores en el DOM (como IDs dinámicos o ligeros cambios en la estructura HTML).

#### 💡 ¿Cómo funciona?
Cuando una acción (click, escribir, etc.) falla porque el elemento no aparece en el tiempo esperado (`TimeoutException`), el framework no se detiene de inmediato. En su lugar, activa el protocolo de **Auto-healing**:

1.  **Detección de Fallo**: El driver lanza un `TimeoutException`.
2.  **Activación de Estrategias**: Se ejecutan algoritmos de búsqueda alternativa basados en el locador original.
3.  **Fuzzy Matching**:
    *   **Estrategia A (Atributos Parciales)**: Si usaste un `ID` o `Name`, busca elementos cuyo atributo *contenga* parte de ese valor (ej: busca `login` si el original era `login-button`).
    *   **Estrategia B (Recuperación por Texto)**: Si el locador original buscaba un texto específico (`//button[text()='Login']`), el sistema intenta encontrar cualquier elemento que *contenga* ese texto en el resto de la página.
4.  **Recuperación**: Si encuentra un candidato único, realiza la acción sobre él y lanza una advertencia en los logs. Si falla, relanza el error original.

#### 🛠️ Ejemplo Real
*   **Locador programado**: `(By.ID, "login-button")`
*   **Cambio en la App**: El equipo de Front-end cambia el ID a `login-button-v2`.
*   **Resultado**: El test **NO falla**. El framework detecta que `login-button` ya no existe, busca elementos que contengan "login" y recupera el nuevo botón automáticamente.

#### 📝 Interpretación de Logs
Cuando el Auto-healing entra en acción, verás estos mensajes en tu consola o reporte:
```bash
2026-03-09 10:24:17 [WARNING] BaseAction - [AUTO-HEALING] Primary locator ('id', 'login') failed. Attempting recovery...
2026-03-09 10:24:18 [WARNING] BaseAction - [AUTO-HEALING] Successfully recovered element using fuzzy matching!
```

> [!IMPORTANT]
> El Auto-healing está diseñado para **mantener tus pruebas vivas** durante cambios inesperados, pero no sustituye el mantenimiento del código. Si ves muchos avisos de auto-recuperación, es una señal de que debes actualizar tus locadores.

### 5. Notificaciones Proactivas
El framework no solo ejecuta pruebas, sino que comunica los resultados automáticamente al finalizar la sesión, facilitando la visibilidad del estado del proyecto para todo el equipo.

#### 🔗 Integración con el Ciclo de Vida (Pytest Hooks)
El sistema utiliza el hook `pytest_sessionfinish` en el archivo `conftest.py` raíz. Esto garantiza que, sin importar cuántos tests ejecutes, al final recibirás un único resumen consolidado.

#### 🛠️ Configuración (Slack / MS Teams)
La integración por defecto utiliza Webhooks. Solo necesitas añadir la URL en tu archivo de configuración:

```yaml
notifications:
  webhook_url: "https://hooks.slack.com/services/T000/B000/XXXX"
```

#### 🚀 Cómo Integrar otros Sistemas (Extensibilidad)
Si necesitas enviar notificaciones por **Email, Telegram, Jira o WhatsApp**, el sistema es fácilmente extensible. Sigue estos pasos:

1.  **Modifica `core/utils/notifier.py`**: Añade un nuevo método para tu plataforma.
    ```python
    def send_telegram(self, message):
        # Lógica para enviar vía API de Telegram
        pass
    ```
2.  **Actualiza el Hook en `conftest.py`**: Llama a tu nuevo método al finalizar la sesión.
    ```python
    def pytest_sessionfinish(session, exitstatus):
        # ... lógica de estadísticas ...
        notifier.send_telegram("Resumen de ejecución...")
    ```

#### 📊 Ejemplo de Notificación (Payload)
El resumen enviado contiene:
*   **Estado General**: ✅ PASSED o ❌ FAILED (basado en si hubo algún fallo).
*   **Contadores**: Total de pruebas, pasadas, fallidas y saltadas.
*   **Enlace al Reporte**: (Opcional) Si el framework está integrado con un servidor de reportes (ej. Jenkins/Allure), se puede incluir el link directo.

> [!NOTE]
> Las notificaciones solo se envían si la propiedad `webhook_url` está presente en el archivo de configuración. Esto evita spam durante el desarrollo local si no se desea.

### 6. Test Runner GUI (Web Interface)
El framework incluye una **Interfaz Gráfica de Usuario (GUI)** personalizada basada en web, diseñada para ofrecer una experiencia similar a Cypress o Playwright directamente en tu navegador, sin necesidad de dependencias pesadas.

#### 🌟 Características Principales
*   **Visualización de Árbol de Pruebas**: Explora todos tus casos de prueba (`pytest`) organizados de forma jerárquica con sus IDs y descripciones extraídas directamente de los decoradores `@test_case`.
*   **Ejecución y Logs en Tiempo Real**: Lanza casos individuales o "Test Plans" y observa la consola de ejecución en vivo (SSE) con formato de colores (éxitos en verde, errores en rojo, y separadores claros).
*   **Test Plans (Planes de Prueba)**: Selecciona múltiples casos de prueba, combina configuraciones (Navegador, Ambiente, Headless) y guárdalos como un Plan de Prueba reutilizable. Edita o elimina planes fácilmente desde la barra lateral.
*   **Media Gallery Integrada**: Visualiza todos los videos y capturas de pantalla generados por las pruebas que fallaron directamente desde la UI. La galería clasifica los videos mostrando el Nombre de la Prueba, ID y duración (usando métricas reales de OpenCV).
*   **Gestión de Reportes Allure**: Genera y visualiza tu reporte oficial Allure HTML con un solo clic desde la barra superior.
*   **Copiar Logs al Portapapeles**: Extrae fácilmente la salida de tu consola de pruebas para compartirla con tu equipo o adjuntarla a tickets de bugs.

#### 🚀 Cómo Iniciarlo
El Test Runner es una aplicación Flask ligera que sirve el dashboard y se comunica con el framework:
```bash
# Inicia el servidor local
$env:PYTHONPATH = "."; python tools/test_runner/app.py
```
Abre tu navegador en `http://localhost:5000` y comienza a orquestar tus pruebas visualmente.

## 🚀 Ejecución y CI/CD

### 1. Comandos Básicos (PowerShell)
```powershell
# Ejecutar todos los tests
$env:PYTHONPATH = "."; pytest

# Ejecutar con reporte Allure
pytest --alluredir=reports
```

### 2. Configuración Dinámica (Variables de Entorno)
Puedes controlar el comportamiento del framework sin cambiar el código usando variables de entorno:

| Variable | Opciones | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| `ENV` | `qa`, `dev`, `uat`, `prod` | Ambiente de ejecución (YAML). | `$env:ENV="dev"` |
| `BROWSER` | `chrome`, `firefox`, `edge` | Navegador a utilizar. | `$env:BROWSER="firefox"` |
| `HEADLESS` | `true`, `false` | Ejecutar sin interfaz gráfica. | `$env:HEADLESS="true"` |

#### Ejemplos de Combinaciones:
```powershell
# Ejecutar en QA con Firefox en modo Headless
$env:ENV="qa"; $env:BROWSER="firefox"; $env:HEADLESS="true"; pytest

# Ejecutar en DEV con Chrome (Vista real)
$env:ENV="dev"; $env:BROWSER="chrome"; $env:HEADLESS="false"; pytest
```

### 3. Configuraciones Locales con Decoradores
Para facilitar la ejecución desde el IDE sin configurar variables de entorno, puedes usar el decorador de la aplicación (ej: `@demo`).

```python
from applications.web.demo.utils.decorators import demo

@demo  # Define: Browser="edge", Env="qa" por defecto
class TestLogin(BaseTest):
    ...
```

**Prioridad de Resolución:**
1.  **Variables de Entorno** (Terminal): `$env:BROWSER="chrome"` (Máxima prioridad)
2.  **Decorador de Clase**: `@demo` fija el default local.
3.  **Config YAML / Base**: Valores globales del framework.

## 📊 Reportes de Ejecución (Allure)

El framework utiliza **Allure Reports** para generar informes visuales de alta calidad que incluyen pasos de ejecución, capturas de pantalla, severidad y metadatos vinculados a archivos JSON.

### 1. Generación Automática
Cada vez que ejecutas tus pruebas con `pytest`, los resultados crudos se guardan automáticamente en la carpeta `/reports`. 

> [!TIP]
> El framework está configurado para limpiar automáticamente los resultados de ejecuciones anteriores antes de cada nueva corrida (`--clean-alluredir`).

### 2. Visualización del Reporte
Para levantar el servidor visual y ver tus resultados en el navegador, tienes dos opciones:

#### Opción A: Script Rápido (Recomendado)
Ejecuta el archivo batch creado para Windows desde tu terminal:
```powershell
.\serve-report.bat
```

#### Opción B: Usando NPX (Node.js)
Si no deseas usar el script anterior:
```bash
npx allure-commandline serve reports
```

### 3. Evidencia Visual (Screenshots)
El framework permite capturar evidencia en formato PNG y adjuntarla automáticamente al reporte de Allure.

#### 📸 Captura de Pantalla Completa (Full Page)
Por defecto, el método `screenshot` captura **todo el alto de la página** (útil para auditorías de formularios largos o dashboards).

```python
# Captura toda la página (Comportamiento por defecto)
self.app.screenshot("Evidencia Final")

# Captura solo lo que es visible en el viewport
self.app.screenshot("Error Visible", full_page=False)
```

---

## 🧭 Ciclo de Vida: Aislamiento vs. Persistencia

El framework permite elegir entre dos modos de ejecución según las necesidades de tus pruebas:

### 1. Modo Aislamiento (Predeterminado)
Por defecto, **cada test abre y cierra un navegador nuevo**. Es el modo más seguro porque garantiza que cada prueba comience desde cero, sin "basura" o estados residuales de ejecuciones anteriores.

*   **Ideal para:** Pruebas independientes, validaciones rápidas, regresiones críticas.
*   **Comportamiento:** Browser -> Test 1 -> Cerrar -> Browser -> Test 2 -> Cerrar.

### 2. Modo Persistente (Sesión Compartida)
Permite mantener **el mismo navegador abierto** durante todos los métodos dentro de una misma clase de prueba. Esto es ideal para flujos largos donde quieres loguearte una vez y realizar múltiples validaciones secuenciales sin perder tiempo reiniciando la sesión.

*   **Ideal para:** Dashboards complejos, flujos de procesos (ej: Crear factura -> Ver reporte -> Borrar factura).
*   **Comportamiento:** Browser -> Test 1 -> Test 2 -> Test 3 -> Cerrar (al final de la clase).

#### 🛠️ Cómo activarlo
Simplemente añade el atributo `persistent_session = True` en tu clase de prueba:

```python
@go_hotel
class TestDashboard(BaseTest):
    persistent_session = True  # <--- Activa la sesión compartida para esta clase

    @test_case(id="HOTEL-003")
    def test_login_flow(self):
        self.app.login_page.wait_for_page_load().login()

    @test_case(id="HOTEL-004")
    def test_verify_menu(self):
        # El browser sigue abierto y la sesión de login activa
        self.app.dashboard_page.click_cola_cocina()
```

> [!IMPORTANT]
> En **Modo Persistente**, si un método falla y deja el sistema en un estado bloqueado (ej: un modal abierto que cubre la pantalla), es muy probable que los métodos posteriores también fallen. Úsalo con sabiduría.

---


---

## 💻 Integración con Visual Studio Code

El proyecto está optimizado para trabajar con VS Code. Sigue estos pasos para una configuración perfecta:

### 1. Extensiones Necesarias
Instala las siguientes extensiones desde el Marketplace:
*   **Python (Microsoft)**: Soporte de lenguaje, depuración y testing.
*   **Pylance**: IntelliSense rápido y tipado.
*   **Allure Support**: (Opcional) Para visualizar reportes Allure.

### 2. Configuración Inicial
1.  **Seleccionar Intérprete**: Presiona `Ctrl+Shift+P`, escribe `Python: Select Interpreter` y elige tu entorno virtual (`.venv`).
2.  **Activar Testing**: El archivo `.vscode/settings.json` ya activa `pytest` automáticamente. Si no ves los tests, reinicia VS Code o haz clic en "Refresh" en la pestaña de Testing.

### 3. Cómo Ejecutar (Testing Sidebar)
1.  Haz clic en el icono del **Matraz (Testing)** en la barra lateral izquierda.
2.  Navega por el árbol de carpetas hasta `applications/web/demo/tests`.
3.  **Ejecutar**: Clic en el botón **Play** junto al nombre del test o carpeta.
4.  **Depurar**: Clic derecho en el test y selecciona **Debug Test**.

### 4. Depuración Avanzada (F5 / Launch Profiles)
Para ejecutar con configuraciones específicas (Ambiente, Browser, Headless), usa la pestaña **Run and Debug** (`Ctrl+Shift+D`):
*   **Debug: Current Test**: Usa Chrome en modo UI sobre el archivo que tienes abierto.
*   **Run: QA - Chrome (Headless)**: Ejecución rápida sin abrir navegador.
*   **Run: QA - Edge (UI)**: Ejecución sobre Edge para validación visual.

> [!NOTE]
> Todos estos perfiles inyectan automáticamente el `PYTHONPATH` necesario para que no haya errores de importación al depurar.

### 5. Paralelismo Nativo (pytest-xdist)
El framework aprovecha todos los núcleos de tu procesador para ejecutar pruebas simultáneamente, reduciendo drásticamente el tiempo total de ejecución.

#### ⚙️ Cómo Funciona
Utilizamos el plugin `pytest-xdist`. Por defecto, el framework estaba configurado para usar `-n auto` (detectar todos los cores), pero para mantener la compatibilidad con el entorno de Visual Studio Code (que se rompe con xdist activo por defecto), la ejecución paralela se lanza **bajo demanda**.

#### 🚀 Ejecución en Paralelo
Para lanzar tus pruebas utilizando múltiples hilos de ejecución, pasa el flag `-n` seguido del número de workers (hilos) o `auto`:

```powershell
# Ejecutar usando todos los núcleos disponibles de tu CPU
pytest applications/web/demo/tests -n auto

# Ejecutar usando exactamente 3 hilos simultáneos
pytest applications/web/demo/tests -n 3
```

> [!WARNING]
> **Precaución con los Datos**: Cuando ejecutas en paralelo, los tests no se ejecutan secuencialmente. Asegúrate de que tus pruebas sean totalmente **aisladas e independientes** (no compartan el mismo usuario o modifiquen el mismo registro en la misma milésima de segundo) para evitar colisiones en la base de datos o el sistema.

---

### 6. Pipeline GitHub Actions (CI/CD)
El proyecto incluye un flujo de trabajo preconfigurado para Integración Continua (CI) usando GitHub Actions. Esto asegura que tu código se prueba automáticamente cada vez que haces un cambio.

#### 📁 Archivo de Configuración
La definición del pipeline se encuentra en `.github/workflows/python-app.yml` (o un nombre similar).

#### 🛠️ Características del Pipeline
1.  **Ejecución Automática**: Se dispara en cada `push` o Pull Request hacia la rama `main`.
2.  **Entorno Controlado**: Instala Python, las dependencias (`requirements.txt`) y configura el entorno.
3.  **Headless Mode**: Ejecuta los tests en modo Headless (`$env:HEADLESS="true"` o su equivalente en Linux) ya que los servidores de GitHub no tienen interfaz gráfica.
4.  **Generación de Allure Report**: Al finalizar los tests, el pipeline compila los resultados crudos (`alluredir`) en un reporte web interactivo.
5.  **GitHub Pages / Artefactos**: Sube el reporte compilado como un artefacto descargable o lo despliega directamente en GitHub Pages para que todo el equipo pueda verlo con un solo clic.

#### 🚀 Ejecución Local vs CI
Recuerda que en el servidor CI, las rutas y los permisos pueden variar respecto a tu máquina local. Para depurar fallos en el pipeline:
```bash
# Simula la ejecución del CI en tu máquina
$env:ENV="qa"; $env:HEADLESS="true"; pytest applications/web/demo/tests --alluredir=reports
```

---
*Diseñado por Johan Rosabal para una automatización de excelencia.*
