import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import locale

# Configurar el formato de moneda para mostrar pesos mexicanos
try:
    locale.setlocale(locale.LC_ALL, 'es_MX.UTF-8')  # Para sistemas Unix/Linux
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Spanish_Mexico')  # Para Windows
    except:
        locale.setlocale(locale.LC_ALL, '')  # Fallback a la configuración por defecto

class SistemaContable:
    def __init__(self):
        # Inicializar el diario, mayor, y estados financieros
        self.diario = []
        self.mayor = {}
        self.fecha_actual = datetime.now().strftime("%d/%m/%Y")
        
        # Inicializar cuentas con saldos iniciales
        self.cuentas = {
            "Caja": 30000,
            "Bancos": 100000,
            "Mercancía": 10000,
            "IVA acreditable": 0,
            "IVA por acreditar": 0,
            "Edificios": 1500000,
            "Terrenos": 2800000,
            "Equipo de computo": 20000,
            "Muebles y enseres": 100000,
            "Mobiliaria y equipo": 20000,
            "Equipo de reparto": 400000,
            "Proveedores": 0,
            "IVA trasladado": 0,
            "IVA por trasladar": 0,
            "Anticipo de clientes": 0,
            "Papelería y útiles": 0,
            "Rentas pagadas por anticipado": 0,
            "Capital social": 4980000
        }
        
        # Realizar asiento de apertura
        self.asiento_apertura()
    
    def registrar_asiento(self, descripcion, cargos, abonos):
        """Registra un asiento en el diario y actualiza el mayor"""
        asiento = {
            "fecha": self.fecha_actual,
            "descripcion": descripcion,
            "cargos": cargos,
            "abonos": abonos
        }
        self.diario.append(asiento)
        
        # Actualizar el mayor
        for cuenta, monto in cargos.items():
            if cuenta not in self.mayor:
                self.mayor[cuenta] = {"cargos": [], "abonos": []}
            self.mayor[cuenta]["cargos"].append({"fecha": self.fecha_actual, "descripcion": descripcion, "monto": monto})
            self.cuentas[cuenta] += monto
            
        for cuenta, monto in abonos.items():
            if cuenta not in self.mayor:
                self.mayor[cuenta] = {"cargos": [], "abonos": []}
            self.mayor[cuenta]["abonos"].append({"fecha": self.fecha_actual, "descripcion": descripcion, "monto": monto})
            self.cuentas[cuenta] -= monto
    
    def asiento_apertura(self):
        """Registra el asiento de apertura"""
        cargos = {
            "Caja": 30000,
            "Bancos": 100000,
            "Mercancía": 10000,
            "Edificios": 1500000,
            "Terrenos": 2800000,
            "Equipo de computo": 20000,
            "Muebles y enseres": 100000,
            "Mobiliaria y equipo": 20000,
            "Equipo de reparto": 400000
        }
        
        abonos = {
            "Capital social": 4980000
        }
        
        self.registrar_asiento("Asiento de apertura", cargos, abonos)
        return "1. Asiento de apertura registrado con éxito."
    
    def compra_efectivo(self, monto_sin_iva, cuenta_origen="Bancos"):
        """Registra una compra en efectivo"""
        iva = monto_sin_iva * 0.16
        total = monto_sin_iva + iva
        
        cargos = {
            "Mercancía": monto_sin_iva,
            "IVA acreditable": iva  # Cambiado a IVA acreditable
        }
        
        abonos = {
            cuenta_origen: total
        }
        
        self.registrar_asiento(f"Compra de mercancía en efectivo (pagado con {cuenta_origen})", cargos, abonos)
        return f"2. Compra en efectivo por ${monto_sin_iva:.2f} + IVA ${iva:.2f} = ${total:.2f} registrada con éxito.\nPagado desde: {cuenta_origen}"
    
    def compra_credito(self, monto_sin_iva):
        """Registra una compra a crédito"""
        iva = monto_sin_iva * 0.16
        total = monto_sin_iva + iva
        
        cargos = {
            "Mercancía": monto_sin_iva,
            "IVA por acreditar": iva  # Usamos IVA por acreditar para compras a crédito
        }
        
        abonos = {
            "Proveedores": total
        }
        
        self.registrar_asiento("Compra de mercancía a crédito", cargos, abonos)
        return f"3. Compra a crédito por ${monto_sin_iva:.2f} + IVA ${iva:.2f} = ${total:.2f} registrada con éxito."
    
    def compra_combinada(self, monto_sin_iva, porcentaje_efectivo, cuenta_origen="Bancos"):
        """Registra una compra combinada (parte en efectivo, parte a crédito)"""
        iva = monto_sin_iva * 0.16
        total = monto_sin_iva + iva
        
        monto_efectivo = total * (porcentaje_efectivo / 100)
        monto_credito = total - monto_efectivo
        
        # Calculamos la proporción del IVA para cada parte
        iva_efectivo = iva * (porcentaje_efectivo / 100)
        iva_credito = iva - iva_efectivo
        
        # Calculamos la proporción del monto sin IVA para cada parte
        monto_sin_iva_efectivo = monto_sin_iva * (porcentaje_efectivo / 100)
        monto_sin_iva_credito = monto_sin_iva - monto_sin_iva_efectivo
        
        cargos = {
            "Mercancía": monto_sin_iva,
            "IVA acreditable": iva_efectivo,  # IVA acreditable para la parte en efectivo
            "IVA por acreditar": iva_credito  # IVA por acreditar para la parte a crédito
        }
        
        abonos = {
            cuenta_origen: monto_efectivo,
            "Proveedores": monto_credito
        }
        
        self.registrar_asiento(f"Compra de mercancía combinada (parte pagada con {cuenta_origen})", cargos, abonos)
        return (f"4. Compra combinada por ${monto_sin_iva:.2f} + IVA ${iva:.2f} = ${total:.2f}\n"
                f"   Pago en efectivo desde {cuenta_origen}: ${monto_efectivo:.2f} ({porcentaje_efectivo}%)\n"
                f"   Pago a crédito: ${monto_credito:.2f} ({100-porcentaje_efectivo}%)")
    
    def anticipo_cliente(self, monto_sin_iva, cuenta_destino="Bancos"):
        """Registra un anticipo de cliente con IVA"""
        iva = monto_sin_iva * 0.16
        total = monto_sin_iva + iva
        
        cargos = {
            cuenta_destino: total
        }
        
        abonos = {
            "Anticipo de clientes": monto_sin_iva,
            "IVA trasladado": iva  # Usamos IVA trasladado para los anticipos
        }
        
        self.registrar_asiento(f"Anticipo recibido de cliente (depositado en {cuenta_destino})", cargos, abonos)
        return f"5. Anticipo de cliente por ${monto_sin_iva:.2f} + IVA ${iva:.2f} = ${total:.2f} registrado con éxito.\nDepositado en: {cuenta_destino}"
    
    def compra_papeleria(self, monto_sin_iva, cuenta_origen="Bancos"):
        """Registra una compra de papelería"""
        iva = monto_sin_iva * 0.16
        total = monto_sin_iva + iva
        
        cargos = {
            "Papelería y útiles": monto_sin_iva,
            "IVA acreditable": iva  # Cambiado a IVA acreditable
        }
        
        abonos = {
            cuenta_origen: total
        }
        
        self.registrar_asiento(f"Compra de papelería (pagado con {cuenta_origen})", cargos, abonos)
        return f"6. Compra de papelería por ${monto_sin_iva:.2f} + IVA ${iva:.2f} = ${total:.2f} registrada con éxito.\nPagado desde: {cuenta_origen}"
    
    def pago_rentas_anticipadas(self, monto_sin_iva, meses, cuenta_origen="Bancos"):
        """Registra el pago de rentas anticipadas"""
        iva = monto_sin_iva * 0.16
        total = monto_sin_iva + iva
        
        cargos = {
            "Rentas pagadas por anticipado": monto_sin_iva,
            "IVA acreditable": iva  # Cambiado a IVA acreditable
        }
        
        abonos = {
            cuenta_origen: total
        }
        
        self.registrar_asiento(f"Pago de rentas anticipadas por {meses} meses (pagado con {cuenta_origen})", cargos, abonos)
        return f"7. Pago de rentas anticipadas por {meses} meses: ${monto_sin_iva:.2f} + IVA ${iva:.2f} = ${total:.2f} registrado con éxito.\nPagado desde: {cuenta_origen}"
    
    def generar_diario(self):
        """Genera el texto del libro diario"""
        resultado = "=== LIBRO DIARIO ===\n"
        for i, asiento in enumerate(self.diario, 1):
            resultado += f"\nAsiento {i} - {asiento['fecha']} - {asiento['descripcion']}\n"
            resultado += "CARGOS:\n"
            for cuenta, monto in asiento['cargos'].items():
                resultado += f"  {cuenta}: ${monto:,.2f}\n"
            resultado += "ABONOS:\n"
            for cuenta, monto in asiento['abonos'].items():
                resultado += f"  {cuenta}: ${monto:,.2f}\n"
        return resultado
    
    def generar_mayor(self):
        """Genera el texto de los esquemas de mayor"""
        resultado = "=== ESQUEMAS DE MAYOR ===\n"
        for cuenta, movimientos in self.mayor.items():
            resultado += f"\nCuenta: {cuenta}\n"
            resultado += "CARGOS:\n"
            total_cargos = 0
            for cargo in movimientos["cargos"]:
                resultado += f"  {cargo['fecha']} - {cargo['descripcion']}: ${cargo['monto']:,.2f}\n"
                total_cargos += cargo['monto']
            
            resultado += "ABONOS:\n"
            total_abonos = 0
            for abono in movimientos["abonos"]:
                resultado += f"  {abono['fecha']} - {abono['descripcion']}: ${abono['monto']:,.2f}\n"
                total_abonos += abono['monto']
            
            saldo = total_cargos - total_abonos
            resultado += f"Saldo: ${saldo:,.2f}\n"
        return resultado
    
    def generar_balanza_comprobacion(self):
        """Genera el texto de la balanza de comprobación"""
        resultado = "=== BALANZA DE COMPROBACIÓN ===\n"
        resultado += f"Fecha: {self.fecha_actual}\n"
        resultado += f"{'Cuenta':<30} {'Debe':>15} {'Haber':>15}\n"
        resultado += "-" * 60 + "\n"
        
        total_debe = 0
        total_haber = 0
        
        # Ordenamos las cuentas para una mejor presentación
        cuentas_ordenadas = sorted(self.cuentas.keys())
        
        for cuenta in cuentas_ordenadas:
            saldo = self.cuentas[cuenta]
            
            # Las cuentas de activo y gasto normalmente tienen saldo deudor (positivo)
            # Las cuentas de pasivo, capital e ingreso normalmente tienen saldo acreedor (negativo)
            if cuenta in ["Proveedores", "IVA trasladado", "IVA por trasladar", "Anticipo de clientes", "Capital social"]:
                # Para estas cuentas, el saldo normal es acreedor (negativo)
                if saldo < 0:
                    debe = 0
                    haber = abs(saldo)
                else:
                    debe = saldo
                    haber = 0
            else:
                # Para el resto de cuentas, el saldo normal es deudor (positivo)
                if saldo > 0:
                    debe = saldo
                    haber = 0
                else:
                    debe = 0
                    haber = abs(saldo)
            
            if debe > 0 or haber > 0:
                resultado += f"{cuenta:<30} {debe:>15,.2f} {haber:>15,.2f}\n"
                total_debe += debe
                total_haber += haber
        
        resultado += "-" * 60 + "\n"
        resultado += f"{'TOTAL':<30} {total_debe:>15,.2f} {total_haber:>15,.2f}\n"
        
        # Verificar si la balanza está cuadrada
        if total_debe == total_haber:
            resultado += "\nLa balanza de comprobación está cuadrada."
        else:
            resultado += f"\nLa balanza de comprobación NO está cuadrada. Diferencia: ${abs(total_debe - total_haber):,.2f}"
        
        return resultado
    
    def generar_balance_general(self):
        """Genera el texto del balance general"""
        resultado = "=== BALANCE GENERAL ===\n"
        resultado += f"Fecha: {self.fecha_actual}\n"
        
        # Activos
        resultado += "\nACTIVO\n"
        resultado += "\nCIRCULANTE\n"
        activo_circulante = 0
        for cuenta in ["Caja", "Bancos", "Mercancía", "IVA acreditable", "IVA por acreditar", "Papelería y útiles", "Rentas pagadas por anticipado"]:
            if self.cuentas[cuenta] > 0:
                resultado += f"{cuenta:<30} ${self.cuentas[cuenta]:>15,.2f}\n"
                activo_circulante += self.cuentas[cuenta]
        resultado += f"{'Total Activo Circulante':<30} ${activo_circulante:>15,.2f}\n"
        
        resultado += "\nNO CIRCULANTE\n"
        activo_no_circulante = 0
        for cuenta in ["Edificios", "Terrenos", "Equipo de computo", "Muebles y enseres", "Mobiliaria y equipo", "Equipo de reparto"]:
            if self.cuentas[cuenta] > 0:
                resultado += f"{cuenta:<30} ${self.cuentas[cuenta]:>15,.2f}\n"
                activo_no_circulante += self.cuentas[cuenta]
        resultado += f"{'Total Activo No Circulante':<30} ${activo_no_circulante:>15,.2f}\n"
        
        total_activo = activo_circulante + activo_no_circulante
        resultado += f"\n{'TOTAL ACTIVO':<30} ${total_activo:>15,.2f}\n"
        
        # Pasivos
        resultado += "\nPASIVO\n"
        resultado += "\nCORTO PLAZO\n"
        pasivo_corto_plazo = 0
        for cuenta in ["Proveedores", "IVA trasladado", "IVA por trasladar", "Anticipo de clientes"]:
            if self.cuentas[cuenta] < 0:  # Los pasivos tienen saldo acreedor (negativo)
                valor_absoluto = abs(self.cuentas[cuenta])
                resultado += f"{cuenta:<30} ${valor_absoluto:>15,.2f}\n"
                pasivo_corto_plazo += valor_absoluto
        resultado += f"{'Total Pasivo Corto Plazo':<30} ${pasivo_corto_plazo:>15,.2f}\n"
        
        total_pasivo = pasivo_corto_plazo
        resultado += f"\n{'TOTAL PASIVO':<30} ${total_pasivo:>15,.2f}\n"
        
        # Capital
        resultado += "\nCAPITAL CONTABLE\n"
        capital_contable = abs(self.cuentas["Capital social"])
        resultado += f"{'Capital social':<30} ${capital_contable:>15,.2f}\n"
        resultado += f"{'Total Capital Contable':<30} ${capital_contable:>15,.2f}\n"
        
        resultado += f"\n{'TOTAL PASIVO + CAPITAL':<30} ${(total_pasivo + capital_contable):>15,.2f}\n"
        
        # Verificar si el balance está cuadrado
        if total_activo == (total_pasivo + capital_contable):
            resultado += "\nEl balance general está cuadrado."
        else:
            resultado += f"\nEl balance general NO está cuadrado. Diferencia: ${abs(total_activo - (total_pasivo + capital_contable)):,.2f}"
        
        return resultado


class AplicacionContable:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Contable")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Crear el sistema contable
        self.sistema = SistemaContable()
        
        # Crear el cuaderno de pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear las pestañas
        self.tab_transacciones = ttk.Frame(self.notebook)
        self.tab_diario = ttk.Frame(self.notebook)
        self.tab_mayor = ttk.Frame(self.notebook)
        self.tab_balanza = ttk.Frame(self.notebook)
        self.tab_balance = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_transacciones, text="Transacciones")
        self.notebook.add(self.tab_diario, text="Libro Diario")
        self.notebook.add(self.tab_mayor, text="Esquemas de Mayor")
        self.notebook.add(self.tab_balanza, text="Balanza de Comprobación")
        self.notebook.add(self.tab_balance, text="Balance General")
        
        # Configurar la pestaña de transacciones
        self.configurar_tab_transacciones()
        
        # Configurar las pestañas de reportes
        self.configurar_tab_reportes(self.tab_diario, self.actualizar_diario)
        self.configurar_tab_reportes(self.tab_mayor, self.actualizar_mayor)
        self.configurar_tab_reportes(self.tab_balanza, self.actualizar_balanza)
        self.configurar_tab_reportes(self.tab_balance, self.actualizar_balance)
        
        # Actualizar todos los reportes
        self.actualizar_todos_reportes()
        
        # Mostrar mensaje de bienvenida
        messagebox.showinfo("Sistema Contable", "Sistema inicializado con saldos iniciales.\nSe ha registrado el asiento de apertura.")
    
    def configurar_tab_transacciones(self):
        """Configura la pestaña de transacciones"""
        # Frame principal
        main_frame = ttk.Frame(self.tab_transacciones)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para seleccionar tipo de transacción
        tipo_frame = ttk.LabelFrame(main_frame, text="Tipo de Transacción")
        tipo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.tipo_transaccion = tk.StringVar(value="compra_efectivo")
        
        # Opciones de transacciones
        opciones = [
            ("Compra en Efectivo", "compra_efectivo"),
            ("Compra a Crédito", "compra_credito"),
            ("Compra Combinada", "compra_combinada"),
            ("Anticipo de Cliente", "anticipo_cliente"),
            ("Compra de Papelería", "compra_papeleria"),
            ("Rentas Pagadas por Anticipado", "rentas_anticipadas")
        ]
        
        # Crear los radio buttons
        for i, (texto, valor) in enumerate(opciones):
            rb = ttk.Radiobutton(tipo_frame, text=texto, value=valor, variable=self.tipo_transaccion)
            rb.grid(row=i//3, column=i%3, sticky=tk.W, padx=10, pady=5)
            rb.bind("<ButtonRelease-1>", lambda event: self.root.after(100, self.cambiar_formulario))
        
        # Frame para los formularios
        self.form_frame = ttk.LabelFrame(main_frame, text="Datos de la Transacción")
        self.form_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para los resultados
        self.resultado_frame = ttk.LabelFrame(main_frame, text="Resultado")
        self.resultado_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.resultado_text = scrolledtext.ScrolledText(self.resultado_frame, wrap=tk.WORD, height=5)
        self.resultado_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Inicializar el formulario
        self.formulario_actual = None
        self.cambiar_formulario()
    
    def configurar_tab_reportes(self, tab, actualizar_func):
        """Configura una pestaña de reportes"""
        # Frame principal
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botón de actualizar
        btn_actualizar = ttk.Button(main_frame, text="Actualizar", command=actualizar_func)
        btn_actualizar.pack(anchor=tk.NE, padx=5, pady=5)
        
        # Área de texto
        text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Guardar referencia al área de texto
        tab.text_area = text_area
    
    def cambiar_formulario(self):
        """Cambia el formulario según el tipo de transacción seleccionado"""
        # Limpiar el formulario actual
        if self.formulario_actual:
            self.formulario_actual.destroy()
        
        # Crear un nuevo frame para el formulario
        self.formulario_actual = ttk.Frame(self.form_frame)
        self.formulario_actual.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tipo = self.tipo_transaccion.get()
        
        # Función para crear el selector de cuenta de origen
        def crear_selector_cuenta(row, default="Bancos"):
            ttk.Label(self.formulario_actual, text="Cuenta de Origen:").grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
            cuenta_var = tk.StringVar(value=default)
            cuenta_combo = ttk.Combobox(self.formulario_actual, textvariable=cuenta_var, state="readonly")
            cuenta_combo['values'] = ("Caja", "Bancos")
            cuenta_combo.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            return cuenta_var
        
        # Función para crear el selector de cuenta de destino (para anticipos)
        def crear_selector_cuenta_destino(row, default="Bancos"):
            ttk.Label(self.formulario_actual, text="Cuenta de Destino:").grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
            cuenta_var = tk.StringVar(value=default)
            cuenta_combo = ttk.Combobox(self.formulario_actual, textvariable=cuenta_var, state="readonly")
            cuenta_combo['values'] = ("Caja", "Bancos")
            cuenta_combo.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W)
            return cuenta_var
        
        if tipo == "compra_efectivo":
            ttk.Label(self.formulario_actual, text="Monto (sin IVA):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            self.monto_entry = ttk.Entry(self.formulario_actual)
            self.monto_entry.grid(row=0, column=1, padx=5, pady=5)
            
            self.cuenta_origen_var = crear_selector_cuenta(1)
            
            btn_registrar = ttk.Button(self.formulario_actual, text="Registrar Compra", 
                                      command=self.registrar_compra_efectivo)
            btn_registrar.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
            
        elif tipo == "compra_credito":
            ttk.Label(self.formulario_actual, text="Monto (sin IVA):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            self.monto_entry = ttk.Entry(self.formulario_actual)
            self.monto_entry.grid(row=0, column=1, padx=5, pady=5)
            
            btn_registrar = ttk.Button(self.formulario_actual, text="Registrar Compra", 
                                      command=self.registrar_compra_credito)
            btn_registrar.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
            
        elif tipo == "compra_combinada":
            ttk.Label(self.formulario_actual, text="Monto (sin IVA):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            self.monto_entry = ttk.Entry(self.formulario_actual)
            self.monto_entry.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.formulario_actual, text="% en Efectivo:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
            self.porcentaje_entry = ttk.Entry(self.formulario_actual)
            self.porcentaje_entry.grid(row=1, column=1, padx=5, pady=5)
            self.porcentaje_entry.insert(0, "50")
            
            self.cuenta_origen_var = crear_selector_cuenta(2)
            
            btn_registrar = ttk.Button(self.formulario_actual, text="Registrar Compra", 
                                      command=self.registrar_compra_combinada)
            btn_registrar.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
            
        elif tipo == "anticipo_cliente":
            ttk.Label(self.formulario_actual, text="Monto (sin IVA):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            self.monto_entry = ttk.Entry(self.formulario_actual)
            self.monto_entry.grid(row=0, column=1, padx=5, pady=5)
            
            self.cuenta_destino_var = crear_selector_cuenta_destino(1)
            
            btn_registrar = ttk.Button(self.formulario_actual, text="Registrar Anticipo", 
                                      command=self.registrar_anticipo_cliente)
            btn_registrar.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
            
        elif tipo == "compra_papeleria":
            ttk.Label(self.formulario_actual, text="Monto (sin IVA):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            self.monto_entry = ttk.Entry(self.formulario_actual)
            self.monto_entry.grid(row=0, column=1, padx=5, pady=5)
            
            self.cuenta_origen_var = crear_selector_cuenta(1)
            
            btn_registrar = ttk.Button(self.formulario_actual, text="Registrar Compra", 
                                      command=self.registrar_compra_papeleria)
            btn_registrar.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
            
        elif tipo == "rentas_anticipadas":
            ttk.Label(self.formulario_actual, text="Monto Mensual (sin IVA):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            self.monto_entry = ttk.Entry(self.formulario_actual)
            self.monto_entry.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.formulario_actual, text="Número de Meses:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
            self.meses_entry = ttk.Entry(self.formulario_actual)
            self.meses_entry.grid(row=1, column=1, padx=5, pady=5)
            self.meses_entry.insert(0, "3")
            
            self.cuenta_origen_var = crear_selector_cuenta(2)
            
            btn_registrar = ttk.Button(self.formulario_actual, text="Registrar Pago", 
                                      command=self.registrar_rentas_anticipadas)
            btn_registrar.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
    
    def registrar_compra_efectivo(self):
        """Registra una compra en efectivo"""
        try:
            monto = float(self.monto_entry.get())
            cuenta_origen = self.cuenta_origen_var.get()
            resultado = self.sistema.compra_efectivo(monto, cuenta_origen)
            self.mostrar_resultado(resultado)
            self.actualizar_todos_reportes()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un monto válido.")
    
    def registrar_compra_credito(self):
        """Registra una compra a crédito"""
        try:
            monto = float(self.monto_entry.get())
            resultado = self.sistema.compra_credito(monto)
            self.mostrar_resultado(resultado)
            self.actualizar_todos_reportes()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un monto válido.")
    
    def registrar_compra_combinada(self):
        """Registra una compra combinada"""
        try:
            monto = float(self.monto_entry.get())
            porcentaje = float(self.porcentaje_entry.get())
            cuenta_origen = self.cuenta_origen_var.get()
            
            if porcentaje < 0 or porcentaje > 100:
                messagebox.showerror("Error", "El porcentaje debe estar entre 0 y 100.")
                return
                
            resultado = self.sistema.compra_combinada(monto, porcentaje, cuenta_origen)
            self.mostrar_resultado(resultado)
            self.actualizar_todos_reportes()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")
    
    def registrar_anticipo_cliente(self):
        """Registra un anticipo de cliente"""
        try:
            monto = float(self.monto_entry.get())
            cuenta_destino = self.cuenta_destino_var.get()
            resultado = self.sistema.anticipo_cliente(monto, cuenta_destino)
            self.mostrar_resultado(resultado)
            self.actualizar_todos_reportes()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un monto válido.")
    
    def registrar_compra_papeleria(self):
        """Registra una compra de papelería"""
        try:
            monto = float(self.monto_entry.get())
            cuenta_origen = self.cuenta_origen_var.get()
            resultado = self.sistema.compra_papeleria(monto, cuenta_origen)
            self.mostrar_resultado(resultado)
            self.actualizar_todos_reportes()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un monto válido.")
    
    def registrar_rentas_anticipadas(self):
        """Registra el pago de rentas anticipadas"""
        try:
            monto = float(self.monto_entry.get())
            meses = int(self.meses_entry.get())
            cuenta_origen = self.cuenta_origen_var.get()
            
            if meses <= 0:
                messagebox.showerror("Error", "El número de meses debe ser mayor a 0.")
                return
                
            resultado = self.sistema.pago_rentas_anticipadas(monto, meses, cuenta_origen)
            self.mostrar_resultado(resultado)
            self.actualizar_todos_reportes()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")
    
    def mostrar_resultado(self, texto):
        """Muestra el resultado de una operación"""
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, texto)
    
    def actualizar_diario(self):
        """Actualiza el libro diario"""
        self.tab_diario.text_area.delete(1.0, tk.END)
        self.tab_diario.text_area.insert(tk.END, self.sistema.generar_diario())
    
    def actualizar_mayor(self):
        """Actualiza los esquemas de mayor"""
        self.tab_mayor.text_area.delete(1.0, tk.END)
        self.tab_mayor.text_area.insert(tk.END, self.sistema.generar_mayor())
    
    def actualizar_balanza(self):
        """Actualiza la balanza de comprobación"""
        self.tab_balanza.text_area.delete(1.0, tk.END)
        self.tab_balanza.text_area.insert(tk.END, self.sistema.generar_balanza_comprobacion())
    
    def actualizar_balance(self):
        """Actualiza el balance general"""
        self.tab_balance.text_area.delete(1.0, tk.END)
        self.tab_balance.text_area.insert(tk.END, self.sistema.generar_balance_general())
    
    def actualizar_todos_reportes(self):
        """Actualiza todos los reportes"""
        self.actualizar_diario()
        self.actualizar_mayor()
        self.actualizar_balanza()
        self.actualizar_balance()


# Función principal para ejecutar el programa
def main():
    root = tk.Tk()
    app = AplicacionContable(root)
    root.mainloop()

if __name__ == "__main__":
    main()