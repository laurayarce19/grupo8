# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 17:43:52 2022

@author: Andrea
"""

import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64
from streamlit_option_menu import option_menu
from  PIL import Image




st.set_page_config(layout= 'wide')

#@st.cache(persist=True) # Código para que quede almacenada la información en el cache

#IMPORTAMOS LAS BASES DE DATOS 
consolidado=pd.read_csv('consolidadohurto.csv',sep=";",low_memory=False)
moto=pd.read_csv('hurto_moto1.csv',sep=";",low_memory=False)
carro=pd.read_csv('hurto_carro.csv',sep=";",low_memory=False)
residencia=pd.read_csv('hurto_residencia.csv',sep=";", low_memory=False)

moto=moto.replace({'Sin dato': np.nan})#ORGANIZAMOS LOS NULOS 
moto['fecha_hecho']= pd.to_datetime(moto['fecha_hecho'])#ORGANIZAMOS EL FORMATO DE LA FECHA 
moto.drop(['ocupacion','estado_civil','sede_receptora','medio_transporte','conducta_especial','unidad_medida', 'permiso','nivel_academico', 'actividad_delictiva','parentesco', 'actividad_delictiva','codigo_barrio', 'grupo_actor', 'discapacidad', 'grupo_especial', 'fecha_ingestion,,','caracterizacion', 'articulo_penal', 'testigo', 'categoria_penal'], axis = 1, inplace = True)
#FUNCION PARA ORGANIZAR LAS EDADES 
def funcion3(x):
 if x < 18:
  valor = np.nan 
 else:
  valor = x
 return valor
moto['edad'] = moto['edad'].apply(funcion3)#CORREGIMOS LAS EDADES CON LA FUNCION DE EDAD 
moto['arma_medio']=moto['arma_medio'].replace({'No': 'Ninguna'})
moto['modalidad']=moto['modalidad'].replace({'Tóxico o agente químico':'Escopolamina',})
moto['modalidad']=moto['modalidad'].replace({'Escopolamina':'Otros',
       'No aplica':'Otros', 'Abuso de confianza':'Otros', 'Llave maestra':'Otros',
       'Miedo o terror':'Otros', 'Suplantación':'Otros', 'Desvalijar o descuartizar':'Otros',
       'Enfrentamiento con la fuerza pública':'Otros', 'Taquillazo':'Otros', 'Vehículo':'Otros'})
moto.drop(58829,inplace=True)#ELIMINAMOS DATOS EXTRAÑOS 
moto.drop(17372,inplace=True)#ELIMINAMOS DATOS EXTRAÑOS
moto['año_hecho'] = moto['fecha_hecho'].dt.year #CREAMOS UNA COLUMNA CON LOS AÑOS
moto['dia_hecho'] = moto['fecha_hecho'].dt.strftime('%A')#CREAMOS UNA COLUMNA CON LOS DIAS DE LA SEMANA
sexoM=['Hombre', 'Mujer']
moto['sexo']=moto['sexo'].apply(lambda x: np.random.choice(sexoM)if pd.isnull(x) else x)#APLICAMOS FUNCION PARA LOS NULOS 
moto['arma_medio']=moto['arma_medio'].replace({np.nan: 'Ninguna','objeto contundente':'arma cortopunzante'})#REEMPLAZAMOS LOS NULOS 
moto['modalidad']=moto['modalidad'].replace({np.nan:'No aplica'})#ORGANIZAMOS LOS NULOS 
colores_m=['Negro', 'Blanco', 'Gris', 'Azul', 'Rojo', 'Verde', 'Naranja',
   'Amarillo', 'Plata', 'Oro', 'Rosado', 'Café', 'Morado', 'Bronce',
   'Beige'] #CREAMOS UNA LISTA DE COLORES DE MOTOS 
moto['color']=moto['color'].apply(lambda x: np.random.choice(colores_m)if pd.isnull(x) else x)#APLICAMOSEN LA FUNCION LA LISTA DE COLORES 
moto['nombre_barrio'] = moto['nombre_barrio'].fillna(moto['codigo_comuna'])#ORGANIZAMOS LOS NULOS 
moto['nombre_barrio']=moto['nombre_barrio'].replace({'codigo_comuna':'nombre_barrio'})
moto['lugar'] = moto['lugar'].fillna(method="ffill")#ELIMINAMOS LOS NULOS 


#ORGANIZAMOS EL DATAFRAME
carro=carro.replace({'Sin dato': np.nan})
carro['fecha_hecho']= pd.to_datetime(carro['fecha_hecho'])
carro.drop(['ocupacion', 'medio_transporte','sede_receptora','conducta_especial','estado_civil','unidad_medida', 'permiso','actividad_delictiva', 'parentesco', 'nivel_academico','testigo','actividad_delictiva','codigo_barrio','grupo_actor', 'discapacidad', 'grupo_especial','fecha_ingestion,,', 'caracterizacion', 'articulo_penal', 'testigo', 'categoria_penal'], axis = 1, inplace = True)
carro['arma_medio']=carro['arma_medio'].replace({'No': 'Ninguna'})
carro['modalidad']=carro['modalidad'].replace({'Descuido':'Otros', 'Suplantación':'Otros',
       'Escopolamina':'Otros', 'Clásica':'Otros', 'No aplica':'Otros', 'Llave maestra':'Otros',
       'Tóxico o agente químico':'Otros', 'Paquete chileno':'Otros', 'Reten ilegal':'Otros',
       'Enfrentamiento con la fuerza pública':'Otros', 'Miedo o terror':'Otros'})
carro['modalidad']=carro['modalidad'].replace({np.nan:'No aplica'})
colores=['Negro', 'Verde', 'Rojo', 'Blanco', 'Plata', 'Gris', 'Beige', #creamos un 
       'Azul', 'Oro', 'Café', 'Amarillo', 'Naranja', 'Morado', 
       'Bronce', 'Rosado']
carro['color']=carro['color'].apply(lambda x: np.random.choice(colores)if pd.isnull(x) else x)
categorias=['Automóvil', 'Vehículo panel', 'Camionetas', 'Buses',
       'Transporte de carga pesada', 'Vehículos de 2 o 4 ruedas',
       'Tecnología', 'Maquinaria pesada', 'Vehículo emergencias']
carro['categoria_bien']=carro['categoria_bien'].apply(lambda x: np.random.choice(categorias)if pd.isnull(x) else x)
carro['categoria_bien']=carro['categoria_bien'].replace({'Transporte de carga pesada':'Otros vehiculos', 'Vehículos de 2 o 4 ruedas':'Otros vehiculos',
'Tecnología':'Otros vehiculos', 'Maquinaria pesada':'Otros vehiculos', 'Vehículo emergencias':'Otros vehiculos'})
sexo=['Hombre', 'Mujer']#CREAMOS UNA LISTA DE SEXOS 
carro['sexo']=carro['sexo'].apply(lambda x: np.random.choice(sexo)if pd.isnull(x) else x)#APLICAMOS LA LISTA DE SEXOS 
carro['nombre_barrio'] = carro['nombre_barrio'].fillna(carro['codigo_comuna'])
carro['nombre_barrio']=carro['nombre_barrio'].replace({'codigo_comuna':'nombre_barrio'})
carro['lugar'] = carro['lugar'].fillna(method="ffill")
carro['bien']=carro['bien'].replace({'Tracto camión':'Tractomula', 'Buseta':'Microbus','Campero':'Camioneta','Cargadores':'Tractomula','Trailer':'Tractomula','Motoniveladora':'Retroexcavadora'})
carro['año_hecho'] = carro['fecha_hecho'].dt.year
carro['dia_hecho'] = carro['fecha_hecho'].dt.strftime('%A')
#FUNCION PARA ORGANIZAR LAS EDADES 
def funcion2(x):
     if x < 18:
      valor = np.nan
     else:
      valor = x
     return valor
carro['edad'] = carro['edad'].apply(funcion2)#APLICAMOS LA FUNCION DE LAS EDADES


#ORGANIZAMOS EL DATA FRAME 
residencia=residencia.replace({'Sin dato': np.nan})
residencia['fecha_hecho']= pd.to_datetime(residencia['fecha_hecho'])
residencia.drop(['grupo_actor','sede_receptora','conducta_especial','medio_transporte', 'estado_civil','actividad_delictiva','parentesco','ocupacion', 'codigo_barrio','discapacidad','fecha_ingestion','grupo_especial', 'nivel_academico', 'testigo','caracterizacion','categoria_penal','articulo_penal','permiso', 'unidad_medida','modelo', 'color'], axis = 1, inplace= True)
residencia['arma_medio']=residencia['arma_medio'].replace({'No': 'Ninguna'})
residencia['modalidad']=residencia['modalidad'].replace({'Rompimiento cerraduta':'Ventosa','Rompimiento de pared':'Ventosa','Rompimiento de ventana':'Ventosa',})
residencia['modalidad']=residencia['modalidad'].replace({np.nan:'No aplica'})
residencia['modalidad']=residencia['modalidad'].replace({'Tóxico o agente químico':'Escopolamina'})
residencia['categoria_bien']=residencia['categoria_bien'].replace({'Muebles':'Accesorios del hogar','Elementos para guardar o almacenar':'Maquinaria y equipo','Herramientas':'Maquinaria y equipo','Equipamiento servicios públicos':'Maquinaria y equipo','Autoparte y elementos de la mecánica automotriz':'Maquinaria y equipo','Transporte aire':'Maquinaria y equipo','Elementos para la publicidad':'Maquinaria y equipo','Elementos para la iluminación':'Maquinaria y equipo','Maquinaria pesada':'Maquinaria y equipo',
                                                               'Prendas de vestir y accesorios':'Accesorios del hogar','Munición':'Accesorios militares', 'Arma de fuego':'Accesorios militares','Contundentes':'Accesorios militares','Arma blanca':'Accesorios militares','Software':'Tecnología','Vehículos de 2 o 4 ruedas':'Automóvil','Camionetas':'Automóvil',
                                                             'Librería':'Arte','Música':'Arte','Medicamento':'Artículos médicos','Elementos escolares':'Otros elementos','Elementos para actividades al aire libre':'Otros elementos','Documentos':'Otros elementos','Artículos de fumador':'Otros elementos','Materiales y elementos para la construcción':'Maquinaria y equipo','Combustible':'Químicos','Sin dato mercancías':'mercancias'})
sexo=['Hombre', 'Mujer']#CREAMOS UNA LISTA DE SEXOS 
residencia['sexo']=residencia['sexo'].apply(lambda x: np.random.choice(sexo)if pd.isnull(x) else x)#APLICAMOS LA LISTA DE SEXOS 
residencia['nombre_barrio'] = residencia['nombre_barrio'].fillna(residencia['codigo_comuna'])
residencia['nombre_barrio']=residencia['nombre_barrio'].replace({'codigo_comuna':'nombre_barrio'})
residencia['lugar'] = carro['lugar'].fillna(method="ffill")
residencia['bien']=residencia['bien'].replace({'Póliza de seguro':'documentos','Permiso porte de arma':'documentos','Visa':'documentos','Documentos falsos':'documentos','Escrito':'documentos','Pasaporte':'documentos','Soat':'documentos', 'Revisión técnico mecánica':'documentos','Licencia':'documentos', 'Sin dato documentos':'documentos','Elementos escolares':'documentos','Tarjeta de identidad':'documentos','Cédula':'documentos','Cdt':'documentos','Manual':'documentos','Escritura':'documentos','Libreta militar':'documentos','Promesa de compraventa':'documentos','Letra de cambio':'documentos','Portadocumentos':'documentos','Documentación electoral':'documentos','Sin dato títulos valor':'documentos','Acciones':'documentos'})
residencia['bien']=residencia['bien'].replace({'Dijes':'joyeria','Sin dato joyas':'joyeria','Piedra preciosa':'joyeria','Joyería':'joyeria','Joyero':'joyeria'})
residencia['bien']=residencia['bien'].replace({'Frutas y verduras':'alimentos','Artículos alimenticios':'alimentos','Salsa':'alimentos','Carne':'alimentos','Calcio':'alimentos','Bebidas':'alimentos', 'Leche':'alimentos','Aceite':'alimentos','Carbohidratos y dulces':'alimentos','Carbonato':'alimentos','Aceite de cocina':'alimentos', 'Alimentos enlatados y embutidos':'alimentos', 'Huevos':'alimentos','Conservas':'alimentos'})
residencia['bien']=residencia['bien'].replace({'Horno':'electrodomesticos','Electrodomésticos cocina y limpieza hogar':'electrodomesticos','Forro para electrodoméstico':'electrodomesticos','Elementos de la cocina':'electrodomesticos','Batidora':'electrodomesticos','Sin dato electrodomésticos':'electrodomesticos','Olla':'electrodomesticos', 'Aspiradora':'electrodomesticos','Cuchillo':'electrodomesticos','Articulos electrónica':'electrodomesticos','Ventilador':'electrodomesticos'})
residencia['bien']=residencia['bien'].replace({ 'Divisiones':'herramientas y materiales','Campana':'herramientas y materiales','Bomba eléctrica':'herramientas y materiales','Cerámicas':'herramientas y materiales','Pulidora':'herramientas y materiales','Caja fuerte':'herramientas y materiales','Cable':'herramientas y materiales','Cobre':'herramientas y materiales','Sin dato herramientas':'herramientas y materiales','Arnés':'herramientas y materiales','Elementos construcción hogar':'herramientas y materiales','Reja':'herramientas y materiales','Roble':'herramientas y materiales','Tapas':'herramientas y materiales', 'Medidor':'herramientas y materiales', 'Taladro':'herramientas y materiales','Instrumento óptico':'herramientas y materiales','Contador':'herramientas y materiales','Máquina industrial':'herramientas y materiales','Alambre':'herramientas y materiales', 'Máquina':'herramientas y materiales', 'Atornillador':'herramientas y materiales', 'Tubería':'herramientas y materiales','Repuestos para maquinaria y equipo':'herramientas y materiales','Martillo':'herramientas y materiales', 'Alicate':'herramientas y materiales','Cortadora':'herramientas y materiales', 'Discos para pulidora':'herramientas y materiales','Mangueras':'herramientas y materiales', 'Material de construcción':'herramientas y materiales', 'Sin dato materiales':'herramientas y materiales', 'Motobombas':'herramientas y materiales', 'Torres de energía':'herramientas y materiales','Extintor':'herramientas y materiales', 'Tejas':'herramientas y materiales', 'Productos químicos':'herramientas y materiales', 'Madera':'herramientas y materiales','Cemento':'herramientas y materiales','Interruptor':'herramientas y materiales', 'Línea telefónica':'herramientas y materiales', 'Caladora compacta':'herramientas y materiales','Proveedores':'herramientas y materiales', 'Acero inoxidable':'herramientas y materiales', 'Carreta':'herramientas y materiales','Pintura':'herramientas y materiales', 'Lámina':'herramientas y materiales','Sellos':'herramientas y materiales',
   'Volantes':'herramientas y materiales', 'Serrucho':'herramientas y materiales', 'Antenas':'herramientas y materiales', 'Bombilla recargable':'herramientas y materiales','Puntilla':'herramientas y materiales','Varilla':'herramientas y materiales','Sin dato maquinaria y equipo':'herramientas y materiales','Pala':'herramientas y materiales', 'Toma':'herramientas y materiales', 'Vibrocompactador':'herramientas y materiales','Poste de energía':'herramientas y materiales','Carpa':'herramientas y materiales','Transformador':'herramientas y materiales',  'Bombas':'herramientas y materiales', 'Herrajes':'herramientas y materiales', 'Zorro':'herramientas y materiales', 'Hierro':'herramientas y materiales',
   'Balanza':'herramientas y materiales', 'Prendas ponal':'herramientas y materiales','Pvc':'herramientas y materiales','Regulador de gas':'herramientas y materiales','Placa':'herramientas y materiales', 'Pegante':'herramientas y materiales', 'Pasacintas':'herramientas y materiales','Válvulas':'herramientas y materiales', 'Datáfono':'herramientas y materiales', 'Cilíndros de gas':'herramientas y materiales', 'Cartucho':'herramientas y materiales', 'Vitrina':'herramientas y materiales', 'Báscula':'herramientas y materiales', 'Aluminio':'herramientas y materiales'})
residencia['bien']=residencia['bien'].replace({'Zapatos':'prendas de vestir' ,'Maletín':'prendas de vestir', 'Ropa exterior':'prendas de vestir','Guantes':'prendas de vestir','Cinturón':'prendas de vestir','Ropa interior':'prendas de vestir','Sin dato prendas de vestir':'prendas de vestir','Prendas cia. Vigilancia':'prendas de vestir' ,'Accesorios prendas de vestir':'prendas de vestir'  })
residencia['bien']=residencia['bien'].replace({ 'Accesorios armas':'armas','Pistola':'armas','Calibre munición':'armas','Carabina':'armas','Contundentes':'armas','Revólver':'armas', 'Sin dato armas':'armas','Arma blanca':'armas','Pistola neumática':'armas','Morral militar':'armas','Sin dato munición':'armas','Bota militar':'armas', 'Escopeta':'armas'  })
residencia['bien']=residencia['bien'].replace({'Escalera':'elementos del hogar', 'Bicicleta':'elementos del hogar','Casa':'elementos del hogar', 'Palma':'elementos del hogar','Decoración del hogar':'elementos del hogar', 'Muebles del hogar':'elementos del hogar','Sin dato mobiliario del hogar':'elementos del hogar','Instrumento musical':'elementos del hogar', 'Patineta':'elementos del hogar','Interior':'elementos del hogar','Carátula':'elementos del hogar', 'Apartamento':'elementos del hogar','Artículos y ropa de cama':'elementos del hogar', 'Toalla':'elementos del hogar', 'Espejo':'elementos del hogar', 'Elementos deportivos':'elementos del hogar', 'Encomiendas':'elementos del hogar','Caja desbloqueo celulares':'elementos del hogar', 'Juegos y muñecos':'elementos del hogar', 'Barra':'elementos del hogar', 'Libros':'elementos del hogar', 'Silla':'elementos del hogar','Llaveros':'elementos del hogar', 'Mesa':'elementos del hogar', 'Gas':'elementos del hogar', 'Cd':'elementos del hogar', 'Obra musical':'elementos del hogar','Esculturas':'elementos del hogar', 'Papel':'elementos del hogar', 'Envase':'elementos del hogar', 'Archivador':'elementos del hogar', 'Megáfono':'elementos del hogar','Micrófono':'elementos del hogar', 'Binoculares':'elementos del hogar', 'Tapa contador agua':'elementos del hogar','Fotografías':'elementos del hogar','Sin dato mercancías':'elementos del hogar', 'Beeper':'elementos del hogar', 'Sin dato obras de arte':'elementos del hogar','Teatro':'elementos del hogar', 'Balón de fútbol':'elementos del hogar','Coche para bebe':'elementos del hogar', 'Minidiscos':'elementos del hogar','Llave':'elementos del hogar', 'Acid-mantle':'elementos del hogar','Botas de caucho':'elementos del hogar', 'Zapatero':'elementos del hogar','Hamaca':'elementos del hogar','Planta':'elementos del hogar', 'Mobiliario del hogar':'elementos del hogar','Sin dato inmuebles':'elementos del hogar'})
residencia['bien']=residencia['bien'].replace({'Plancha de cabello':'Accesorios de peluquería', 'Plancha':'Accesorios de peluquería', 'Secador':'Accesorios de peluquería', 'Masajeador':'Accesorios de peluquería'})
residencia['bien']=residencia['bien'].replace({'Autopartes':'vehiculos','Casco moto':'vehiculos', 'Tanque':'vehiculos', 'Automóvil':'vehiculos', 'Helicóptero':'vehiculos', 'Gps':'vehiculos','Moto':'vehiculos', 'Camioneta':'vehiculos', 'Aeroplano':'vehiculos','Motor':'vehiculos','Avión':'vehiculos' })
residencia['bien']=residencia['bien'].replace({'Perfumería':'Artículos de aseo personal','Loción':'Artículos de aseo personal'})
residencia['bien']=residencia['bien'].replace({'Ave de jaula o pequeña':'Animales domésticos','Otros animales':'Animales domésticos'})
residencia['bien']=residencia['bien'].replace({'Aparato médico':'Insumo médico','Medicamentos':'Insumo médico', 'Artículo de laboratorio':'Insumo médico'})
residencia['bien']=residencia['bien'].replace({'Diario digital':'equipos tecnologicos','Equipos varios':'Electrodoméstico video y audio y accesorios','Grabadora':'equipos tecnologicos','Radio':'equipos tecnologicos','Celular':'equipos tecnologicos','Computador':'equipos tecnologicos','Tablet':'equipos tecnologicos','Accesorios celular':'equipos tecnologicos','Sin dato tecnología':'equipos tecnologicos','Amplificador de sonido':'equipos tecnologicos','Elementos computador':'equipos tecnologicos','Módem':'equipos tecnologicos','Ipod':'equipos tecnologicos','Vcd':'equipos tecnologicos','Lector':'equipos tecnologicos','Lámpara de alumbrado':'equipos tecnologicos','Dvd':'equipos tecnologicos','Monitor':'equipos tecnologicos','Decodificadores/tarjetas decodificadoras':'equipos tecnologicos','Paquete de software':'equipos tecnologicos','Tarjeta para computador':'equipos tecnologicos','Tarjeta de comunicación':'equipos tecnologicos','Teléfono satelital':'equipos tecnologicos','Ups':'equipos tecnologicos','Agenda digital':'equipos tecnologicos','Conmutador':'equipos tecnologicos','Proyector':'equipos tecnologicos','Artículo para video':'equipos tecnologicos', 'Consola':'equipos tecnologicos','Panel solar':'equipos tencologicos','Cámara':'equipos tecnologicos','Cargadores':'equipos tecnologicos','Quemador cd':'equipos tecnologicos','Sin dato articulos electrónica':'equipos tecnologicos','Electrodoméstico video y audio y accesorios':'equipos tecnologicos','equipos tencologicos':'equipos tecnologicos','equipos tecnologico':'equipos tecnologicos'})
residencia['bien']=residencia['bien'].replace({ 'Peso':'dinero','Euro':'dinero', 'Dólar':'dinero','Tarjeta bancaria':'dinero','Sin dato dinero':'dinero','Cheques':'dinero','Libra esterlina inglesa':'dinero','Plata':'dinero','Oro':'dinero','Moneda falsa':'dinero','Billetera':'dinero','Lingotes de oro':'dinero'})
residencia['bien']=residencia['bien'].replace({'Cerveza':'licores','Whiskey':'licores','Champaña':'licores', 'Tequila':'licores','Cogñac':'licores', 'Vodka':'licores','Brandy':'licores', 'Ron':'licores','Aguardiente':'licores','Vino':'licores','Botellas':'licores','Tabaco':'licores', 'Sin dato licor':'licores','Cigarrillo':'licores'})
bien=['equipos tecnologicos', 'elementos del hogar', 'prendas de vestir',
   'electrodomesticos', 'No responde', 'licores', 'dinero', 'armas',
   'Accesorios de peluquería', 'documentos',
   'herramientas y materiales', 'joyeria', 'alimentos', 'vehiculos',
   'Artículos de aseo personal', 'Animales domésticos',
   'Insumo médico']
residencia['bien']=residencia['bien'].apply(lambda x: np.random.choice(bien)if pd.isnull(x) else x)

categoria=['Electrodomésticos', 'Accesorios del hogar', 'Otros elementos',
   'Maquinaria y equipo', 'Tecnología', 'No responde', 'Licor',
   'Dinero', 'Accesorios militares', 'Automóvil', 'Alimento',
   'Inmuebles', 'Flora', 'Materia prima', 'Arte', 'Fauna', 'Químicos',
   'Artículos médicos', 'mercancias']
residencia['categoria_bien']=residencia['categoria_bien'].apply(lambda x: np.random.choice(categoria)if pd.isnull(x) else x)
residencia['grupo_bien'] = residencia['grupo_bien'].fillna(residencia['categoria_bien'])
residencia['grupo_bien']=residencia['grupo_bien'].replace({'Arte':'Mercancía'})
residencia['grupo_bien']=residencia['grupo_bien'].replace({'Accesorios militares':'Equipamiento'})
residencia['año_hecho'] = residencia['fecha_hecho'].dt.year
residencia['dia_hecho'] = residencia['fecha_hecho'].dt.strftime('%A')
#FUNCION PARA ORGANIZAR LAS EDADES 
def funcion4(x):
 if x < 18:
  valor = np.nan
 else:
  valor = x
 return valor
residencia['edad'] = residencia['edad'].apply(funcion4)#APLICAMOS LA FUNCION DE LAS EDADES 






with st.sidebar:
    st.info('''Realizado por: Andrea Molina y Cesar Avila''')
    
    menu=option_menu('Tipos de hurto', ["Problematica","Hurto de carro🚗", "Hurto de moto🏍️","Hurto a residencia🏡","Conclusiones✅️"],
                     icons=['cat','cat','cat','cat','cat'],
                     styles={
                         "container": {"padding": "0!important", "background-color": "#B9ECFD"},
                         "icon": {"color": "#EAC4F5", "font-size": "25px"}, 
                         "nav-link": {"font-size": "23px", "text-align": "left", "margin":"0px", "--hover-color": "#9ED9FD"},
                         "nav-link-selected": {"background-color": "#8CD4FA"},
                          
                        }
                     )

#OPCION PROBLEMATICA EN EL MENU 

if menu== "Problematica":
    
    
    #AGREGAMOS EL TITULO 
    st.markdown("<h1 style ='text-align: center; color:#337AFF;'>Analisis de hurtos de residencia,carro y moto en la ciudad de Medellin👤💰🔫 </h1>", unsafe_allow_html =True)
    from PIL import Image
    
    delito=Image.open('Imagen1.jpg')
    st.image(delito, width=800)
    
    st.info('Colombia es uno de los paises con los indices de criminalidad mas altos del mundo.Medellin es una de las ciudades donde mas hurtos se dan dia a dia,esta es una problematica social que afecta el ')
    

    

    #Agrupamos 
    con=consolidado.groupby(['Conducta'])[['Cantidad_casos']].count().reset_index().rename(columns={'Conducta':'Conducta delictiva'})
    con=con.sort_values('Cantidad_casos', ascending=False)
    fig= px.bar(con, x='Conducta delictiva', y='Cantidad_casos', title= '<b>Conducta delictiva<b>',width=550, height= 470)
    fig.update_layout(
    xaxis_title='Conducta',
    yaxis_title='Cantidad',
    template= 'simple_white', #color del fondo 
    title_x=0.5,)
    st.plotly_chart(fig)
    
    
    st.markdown('Como se puede observar en las conductas delictivas que mas se presentan en la ciudad encontramos el hurto de carro,moto y residencias por tal motivo seran las que se analizaran a profundidad ')
    st.markdown('Es importante analizar este tipo de problemáticas ya que el hurto organizado presenta una dificultad para el crecimiento del país en el sector automovilístico, ya que estas organizaciones criminales y su mercado ilegal tiene un grannegocio en las partes robadas de los automotores, y el hurto de las residenciasrepercute directamente en la calidad de vida de las personas.')
    st.markdown('Analizar esta temática con mucha atención y en la medida de lo posible intentar reducirlo a partir de iniciativas gubernamentales y privadas, utilizando como una de las herramientas la tecnología disponible')
    st.markdown('En este análisis nos enfocaremos en analizar cómo se encuentra la ciudad en este aspecto criminalístico, identificando cuales son los variables representativas de los diferentes tipos de hurto y qué características presentan lo cual es importante para poder determinar un posible patrón en el funcionamiento de las bandas criminales y así reforzar las medidas de seguridad en las áreas más vulneradas o que son más propensas a ser víctimas de estas actividades')
    st.markdown('Siendo este nuestro tema de interes para realizar un analisis de estos hurtos: sus modalidades,victimas,armas, entre otros para conocer de esta manera mas profunda los hurtos en la ciudad.')

    c1,c2,c3 = st.columns((1,1,1)) 
    imgcarro=Image.open('imagen2.jpg')
    c1.image(imgcarro,width= 200)

    imgmoto=Image.open('imagen3.jpg')
    c2.image(imgmoto,width= 200)

    imgresi=Image.open('imagen4.jpg')
    c3.image(imgresi,width= 250)




#AGREGAMOS LA PARTE DE HURTO A CARROS


elif menu == "Hurto de carro🚗":
    #AGREGAMOS TITULO
    st.markdown("<h1 style ='text-align: center; color:#337AFF;'>Analisis de hurtos de carro en la ciudad de Medellin👤💰🔫 </h1>", unsafe_allow_html =True)

    
#REALIZAMOS GRAFICOS  cantidad de casos por año 
    st.markdown("<h3 style ='text-align: center; color:black;'>Hurtos de carro por año</h1>", unsafe_allow_html =True)
    st.info('Se puede observar en general que en los ultimos años ha disminuido los hurtos a carros, en el año 2003 los hurtos alcanzaban casi los 7000 por año, una cifra alarmante ya que generalmente el robo de autos es para la comercialización de autopartes y cometer otros crímenes por lo que se tomaron medidas por parte de la policia para reducir estos hurtos lo que ha logrado que haya una disminucion en estos hurtos hasta alcanzar una cantidad de hurtos denunciados, en el 2021 de aproximadamente 800. Aunque se debe tener presente que estos son solo los hurtos denunciados a la policia por lo que hay una gran cantidad de hurtos que no son reportados los cuales podrian aumentar estas cifras.')
    c4,c5 = st.columns((1,1))
    C1=carro.groupby(['año_hecho'])[['cantidad']].sum().reset_index()
    fig= px.bar(C1, x='año_hecho', y='cantidad',title='Cantidad de hurtos de carro por año', width=370, height= 370)
    fig.update_layout(
    xaxis_title='Año',
    yaxis_title='Cantidad de hurtos',
    template= 'simple_white', 
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.7))
    c4.plotly_chart(fig)
    
    
    
    
    # Crecimiento de la cantidad de hurtos de carro 
    dm2 =C1=carro.groupby(['fecha_hecho'])[['cantidad']].sum().reset_index()
    dm2.iloc[:,1:]= dm2.iloc[:,1:].cumsum()
    fig1= px.line(dm2, x='fecha_hecho', y ='cantidad', title = '<b>Crecimiento de la cantidad de hurtos de carro<b>', width=400, height= 400,
              color_discrete_sequence=px.colors.qualitative.G10)
    fig1.update_layout(
      template = 'simple_white',
      title_x = 0.5,
      legend_title = 'Hurtos A:',
      xaxis_title = '<b>Fecha<b>',
      yaxis_title = '<b>Cantidad de hurtos<b>',)
    c5.plotly_chart(fig1)   

    
    
    
    
    #GRAFICO CANTIDAD DE HURTO POR DIAS
    st.markdown("<h3 style ='text-align: center; color:black;'>Cantidad de hurtos de carro por dia</h1>", unsafe_allow_html =True)
    c6,c7 = st.columns((1,1))
    C2=carro.groupby(['dia_hecho'])[['cantidad']].count().reset_index()
    C2['orden']=C2['dia_hecho'].replace({'Monday': 1 , 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4 , 'Friday':5, 'Saturday': 6, 'Sunday':7})
    C2= C2.sort_values('orden')
    fig= px.bar(C2, x='dia_hecho', y='cantidad',color_discrete_sequence=px.colors.qualitative.Dark2, width=400, height= 400)
    fig.update_layout(
    xaxis_title='Dia',
    yaxis_title='Cantidad de hurtos',
    template= 'simple_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.7))
    c7.plotly_chart(fig)
    c6.markdown('                           ')
    c6.info('Como podemos observar todos los dias en la semana se presentan gran cantidad de hurtos de vehiculos, en general no se encuentra un patron en los dias de la semana con respecto al hurto, pero se resalta que el dia donde mas se presentan los hurtos es el Miercoles.')
    
    
    
    
    
    
    #GRAFICAMOS LA PARTICIPACION DE LAS ARMAS USADAS PARA EL HURTO 
    st.markdown("<h3 style ='text-align: center; color:black;'>Analisis del tipo de arma usada para el hurto</h1>", unsafe_allow_html =True)
    c8,c9, = st.columns((1,1)) 
    C3=carro.groupby(['arma_medio'])[['cantidad']].count().reset_index()
    fig=px.pie(C3, values='cantidad', names= 'arma_medio', title='<b>Armas usadas en los hurtos a carros<b>', width=400, height= 400)
    fig.update_layout(
    template= 'simple_white', 
    legend_title='Tipo de Arma', 
    title_x=0.5,) 
    c8.plotly_chart(fig)
    c9.info('Aca encontramos los porcentajes de participacion de las armas usadas para realizar los hurtos, como podemos observar las armas de fuego son las mas usadas para este tipo de hurto, lo que es preocupante ya que el uso y porte de armas es ilegal en Colombia por el el decreto 1873 del 30 de diciembre de 2021 que restringe el porte de armas en todo el territorio nacional y compete a las fuerzas del estado cómo únicas autorizadas para portar, expedir y generar los permisos respectivos.')
    
    
    
    
    

    
    #GRAFICO CANTIDAD DE HURTO POR CATEGORIA VEHICULO
    st.markdown("<h3 style ='text-align: center; color:black;'>categorias de los vehiculos hurtados</h1>", unsafe_allow_html =True)
    C9=carro.groupby(['categoria_bien'])[['cantidad']].count().reset_index()
    cantidad=carro['cantidad'].count() 
    fig=px.pie(C9, values='cantidad', names='categoria_bien',hole=.5,title='%ede hurtos por categoria')
    fig.update_layout(
    template= 'simple_white', 
    legend_title='Categorias', 
    title_x=0.5, #ubicacion del titulo,
    annotations = [dict(text = str(cantidad), x=0.5, y = 0.5, font_size = 40, showarrow = False )])
    st.plotly_chart(fig)
    st.info('Aca podemos observar que mas del 70% de los vehiculos que se hurtan son automovil, esto se explica ya que según la información de la Secretaría de Movilidad de Medellín, el parque automotor que circula en el Valle de Aburrá, sumando carros y motos, es de 1.464.328. Este valor se desagrega en 589.463 vehiculos estos representan el 40% del parque automotor.')

 


    #GRAFICO DE LA CANTIDAD DE HURTOS POR MODALIDAD 
    st.markdown("<h3 style ='text-align: center; color:black;'>Cantidad de hurtos por modalidad de hurto</h1>", unsafe_allow_html =True)
    c47,c48 = st.columns((1,1))
    C8=carro.groupby(['modalidad'])[['cantidad']].count().sort_values('cantidad',ascending=False).reset_index()
    fig= px.bar(C8, x='modalidad', y='cantidad', width=450, height= 400,color_discrete_sequence=px.colors.qualitative.Light24)
    fig.update_layout(
    xaxis_title='modalidad',
    yaxis_title='Cantidad de hurtos',
    template= 'simple_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.7))
    c48.plotly_chart(fig)
    c47.info('Se puede observar que la modalidad de hurto de carro mas usada es el asalto o atraco esta modalidad de hurto se caracteriza por el uso de la fuerza, la violencia o la intimidación, algunas veces a mano armada y el halado esto quiere decir que el hurto se da cuando sustraen el vehículo del lugar donde se encuentra estacionado.')
    


    #GRAFICAMOS LOS COLORES DE LOS CARROS HURTADOS
    st.markdown("<h3 style ='text-align: center; color:black;'>Analisis del color de carro hurtado</h1>", unsafe_allow_html =True)
    c10,c11, = st.columns((1,1))
    C4=carro.groupby(['color'])[['cantidad']].count().reset_index()
    fig= px.bar(C4, x='color', y='cantidad', title= '<b>Cantidad de carros huertados segun el color<b>',width=400, height= 400,color_discrete_sequence=px.colors.qualitative.Alphabet)
    fig.update_layout(
    xaxis_title='color',
    yaxis_title='Cantidad de hurtos',
    template= 'simple_white', #color del fondo 
    title_x=0.5,)
    c10.plotly_chart(fig)
    c11.info('Analizando el color de los autos encontramos que en su mayoria los autos hurtados son el GRIS y el BlANCO, esto podria explicarse en el comercio autopartes, la mayoria de los autos que son hurtados en la ciudad entran al comercio de las autopartes y  es que según datos extractados del Registro Único Nacional de Transporte (Runt), en la región hay dos tonos de grises que se llevan las preferencias del público: Gris Estrella y Gris Comet. Ambos colores producidos por Renault. El primero registró 2.986 pedidos y el segundo 2.250 en 2018. El tercer lugar lo ocupa el Blanco Galaxia, de Chevrolet, con 2.023 unidades vendidas, seguido por el Plata, de diversas marcas, con 1817 unidades, y el Gris, con 1.791 facturaciones. Por el contrario, tonos como el Azul Dandy, el Bronce Mica, el Verde Amazonia, el Naranja Metálico, el caoba y el Marrón Magnético no son tan populares, pues solo se registró un ejemplar de cada carrocería en estos tonos.')
    
    
    
    #GRAFICAMOS SI LA CANTIDAD DE HURTOS TIENE RELACION CON LA EDAD 
    st.markdown("<h3 style ='text-align: center; color:black;'>Edad VS Cantidad de hurtos de carro</h1>", unsafe_allow_html =True)
    C5=carro.groupby(['edad'])[['cantidad']].sum().reset_index()
    fig = px.scatter(C5, x = 'edad', y ='cantidad', title = '<b>Edad vs Cantidad de hurtos<b>',width=950, height= 550)
    fig.update_layout(
    xaxis_title = '<b>Edad<b>',
    yaxis_title = '<b>Cantidad de hurtos<b>',
    template = 'simple_white',
    title_x = 0.5,)
    st.plotly_chart(fig)
    st.info('Se realiza un analisis de la edad con respecto a la cantidad de hurtos para saber si hay una correlacion estre estas variables y determinar si la edad es un factor relevante en los hurtos, se encuentra que es un factor relevante, ya que a medida de aumenta la edad dismunuyen los hurtos. Esto se podria explicar en que son las personas de edades entre los 18 y 50 años son los que tienen tendecia a usar automoviles, cabe resaltar que la edad donde mas se presentan los hurtos de automoviles es 35 años')
    
    
    
    
    
    #GRAFICO CANTIDAD DE HURTO POR SEXO
    st.markdown("<h3 style ='text-align: center; color:black;'>Cantidad de hurtos por sexo</h1>", unsafe_allow_html =True)
    c40,c41 = st.columns((1,1))
    C7=carro.groupby(['sexo'])[['cantidad']].count().reset_index()
    cantidad=carro['cantidad'].count() 
    fig=px.pie(C7, values='cantidad', names='sexo',hole=.5,title='%ede hurtos por sexo')
    fig.update_layout(
    template= 'simple_white', 
    legend_title='sexo', 
    title_x=0.5, #ubicacion del titulo,
    annotations = [dict(text = str(cantidad), x=0.5, y = 0.5, font_size = 40, showarrow = False )])
    st.plotly_chart(fig)
    st.info('Se analiza el sexo de las personas victimas de hurto y se encuentra que la mayoria de hurtos se da a los hombres, esto podria explicarse ya que segun informacion del RUT de las más de 12 millones de personas en Colombia que tienen su licencia de conducción activa, el  3.176.564 son mujeres (26%) y 8.838.899 son hombres (74%).')
    
    
elif menu == "Hurto de moto🏍️" :
    #AGREGAMOS TITULO
    st.markdown("<h1 style ='text-align: center; color:#337AFF;'>Analisis de hurtos de moto en la ciudad de Medellin👤💰🔫 </h1>", unsafe_allow_html =True)

    
    
    #REALIZAMOS GRAFICOS  cantidad de casos por anio 
    st.markdown("<h3 style ='text-align: center; color:black;'>Cantidad de hurtos de moto por año En la ciudad de Medellin </h1>", unsafe_allow_html =True)
    st.info('El parque automotor de motos en Antioquia en los últimos 10 años a aumentando en un 54% segun el informe de indicadores objetivos sobre cómo vamos en movilidad.En el crecimiento de la cantidad de hurtos a motos podemos observar que en los últimos años se ha comportado de una manera similar a partir del año 2010, en el que el hurto a motos no ha tenido un patron que se pueda establecer.Cabe resaltar que estos hurtos son solo los reportados a la policia por lo que muchos de los hurtos se quedan sin reportar por lo que estas cifras podrian aumentar.')
    c14,c15 = st.columns((1,1))
    M1=moto.groupby(['año_hecho'])[['cantidad']].sum().reset_index()
    fig= px.bar(M1, x='año_hecho', y='cantidad', width=400, height= 400)
    fig.update_layout(
    xaxis_title='Año',
        yaxis_title='Cantidad de hurtos',
        template= 'simple_white', 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.7))   
    c14.plotly_chart(fig)
    
    
    
    
    # Crecimiento de la cantidad de hurtos a moto
    # definir base
    dm2 =M1=moto.groupby(['fecha_hecho'])[['cantidad']].sum().reset_index()
    dm2.iloc[:,1:]= dm2.iloc[:,1:].cumsum()

    fig1= px.line(dm2, x='fecha_hecho', y ='cantidad', title = '<b>Crecimiento de la cantidad de hurtos a moto<b>', width=400, height= 400,
              color_discrete_sequence=px.colors.qualitative.G10)
    fig1.update_layout(
      template = 'simple_white',
      title_x = 0.5,
      legend_title = 'Hurtos A:',
      xaxis_title = '<b>Fecha<b>',
      yaxis_title = '<b>Cantidad de hurtos<b>',)
    c15.plotly_chart(fig1)   
        
    
    
    
    #GRAFICO CANTIDAD DE HURTO POR DIAS    
    st.markdown("<h3 style ='text-align: center; color:black;'>Cantidad de hurtos de motos por dia de la semana</h1>", unsafe_allow_html =True)
    c16,c17 = st.columns((1,1))
    M2=moto.groupby(['dia_hecho'])[['cantidad']].count().reset_index()
    M2['orden']=M2['dia_hecho'].replace({'Monday': 1 , 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4 , 'Friday':5, 'Saturday': 6, 'Sunday':7})
    M2= M2.sort_values('orden')    
    fig= px.bar(M2, x='dia_hecho', y='cantidad', width=400, height= 400,color_discrete_sequence=px.colors.qualitative.Dark2)
    fig.update_layout(
    xaxis_title='Dia',
    yaxis_title='Cantidad de hurtos',
    template= 'simple_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
     yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0.7))
    c17.plotly_chart(fig)
    c16.info('Se puede apreciar que los hurtos de moto tienen mayor incidencia en la semana donde el dia de la semana que mas se dan estos hurtos es el Miercoles esto se debe a que la mayoria de las personas usan la moto como medio de transporte a sus trabajos por lo que la cantidad de motos que se movilizan en las calles en semana es mayor que los fines de semana ya que el dia que menos se dan hurtos de motos son los Sabados.')
        
    
    
    
    
    
    
    
    #GRAFICAMOS LA PARTICIPACION DE LAS ARMAS USADAS PARA EL HURTO 
    st.markdown("<h3 style ='text-align: center; color:black;'>Tipo de arma usada para el hurto de Motos </h1>", unsafe_allow_html =True)
    c18,c19, = st.columns((1,1))   
    M3=moto.groupby(['arma_medio'])[['cantidad']].count().reset_index()
    fig=px.pie(M3, values='cantidad', names= 'arma_medio', title='<b>% de participacion de las armas en los hurtos a motos<b>', width=400, height= 400)
    fig.update_layout(
    template= 'simple_white', 
    legend_title='Tipo de Arma', 
    title_x=0.5,)    
    c18.plotly_chart(fig)     
    c19.info('Se puede observar la participacion de las armas usadas para realizar los hurtos a las motos, donde se encuentra que la llave maestra y el arma de fuego son las que tienen mas del 50% de participacion en  estos. ')
        
     
        
     #GRAFICO DE LA CANTIDAD DE HURTOS POR MODALIDAD 
    st.markdown("<h3 style ='text-align: center; color:black;'>Cantidad de hurtos de motos por modalidad de hurto</h1>", unsafe_allow_html =True)
    c45,c46 = st.columns((1,1))
    M7=moto.groupby(['modalidad'])[['cantidad']].count().sort_values('cantidad',ascending=False).reset_index()
    fig= px.bar(M7, x='modalidad', y='cantidad', width=400, height= 370,color_discrete_sequence=px.colors.qualitative.Light24)
    fig.update_layout(
     xaxis_title='modalidad',
     yaxis_title='Cantidad de hurtos',
     template= 'simple_white',
     paper_bgcolor='rgba(0,0,0,0)',
     plot_bgcolor='rgba(0,0,0,0)',
     legend=dict(
             yanchor="bottom",
             y=1.02,
             xanchor="left",
             x=0.7))
    c46.plotly_chart(fig)
    c45.info('Se puede observar que las modalidades de hurtos que mas se presentan son el halado, esto quiere decir que el hurto se da cuando sustraen el la moto del lugar donde se encuentra estacionada y el atraco, en esta modalidad de hurto se caracteriza por el uso de la fuerza, la violencia o la intimidación, algunas veces a mano armada .')
        
        
        
    #GRAFICAMOS LOS COLORES DE LAS MOTOS HURTADAS 
    st.markdown("<h3 style ='text-align: center; color:black;'>Color de las motos hurtadas</h1>", unsafe_allow_html =True)
    c20,c21, = st.columns((1,1))
    M4=moto.groupby(['color'])[['cantidad']].count().reset_index()
    fig= px.bar(M4, x='color', y='cantidad', title= '<b>Cantidad de motos huertados segun el color<b>',width=400, height= 400,color_discrete_sequence=px.colors.qualitative.Alphabet)
    fig.update_layout(
    xaxis_title='color',
    yaxis_title='Cantidad de hurtos',
    template= 'simple_white',
    title_x=0.5,)
    c21.plotly_chart(fig) 
    c20.markdown('')
    c20.info('Analizando el color de las motos encontramos que en su mayoria las motos hurtadas son color NEGRO, esto podria explicarse en el comercio autopartes, la mayoria de las motos  que son hurtadas en la ciudad entran al comercio de las autopartes y este color es uno de los mas comunes en las motos por lo que se encuentra un gran comercio ilegal en ellos.')
 
        
        
        
    #GRAFICAMOS SI LA CANTIDAD DE HURTOS TIENE RELACION CON LA EDAD 
    st.markdown("<h3 style ='text-align: center; color:black;'>Edad VS Cantidad de hurtos de moto</h1>", unsafe_allow_html =True)
    M5=moto.groupby(['edad'])[['cantidad']].sum().reset_index()
    fig = px.scatter(M5, x = 'edad', y ='cantidad', title = '<b>Edad vs Cantidad de hurtos de moto<b>',width=950, height= 550)
    fig.update_layout(
    xaxis_title = '<b>Edad<b>',
    yaxis_title = '<b>Cantidad de hurtos<b>',
    template = 'simple_white',
    title_x = 0.5,) 
    st.plotly_chart(fig)  
    st.info('Se realiza un analisis de la edad con respecto a la cantidad de hurtos para saber si hay una correlacion estre estas variables y determinar si la edad es un factor relevante en los hurtos, se encuentra que es un factor relevante, aunque observamos que  a medida de aumenta la edad dismunuyen los hurtos. Esto se podria explicar en que son las personas de edades entre los 18 y 40 años son los que tienen tendecia a usar motos, cabe resaltar que la edad de las victimas que mas sufren de estos hurtos son los 25 años.')
    
    
    
    
    
    #GRAFICO CANTIDAD DE HURTO POR SEXO
    st.markdown("<h3 style ='text-align: center; color:black;'>Cantidad de hurtos de moto por sexo</h1>", unsafe_allow_html =True)
    c38,c39 = st.columns((1,1))
    M6=moto.groupby(['sexo'])[['cantidad']].count().reset_index()
    cantidad=carro['cantidad'].count() 
    fig=px.pie(M6, values='cantidad', names='sexo',hole=.5,title='% de hurtos por sexo')
    fig.update_layout(
    template= 'simple_white', 
    legend_title='Sexo', 
    title_x=0.5, 
    annotations = [dict(text = str(cantidad), x=0.5, y = 0.5, font_size = 40, showarrow = False )])
    st.plotly_chart(fig)
    st.info('Se analiza el sexo de las personas victimas de hurto y se encuentra que la mayoria de hurtos se da a los hombres, esto podria explicarse ya que segun informacion del RUT de las más de 12 millones de personas en Colombia que tienen su licencia de conducción activa, el 31,8% son mujeres y el 68,2% son hombres.')
    
    
    
    
    
  
    
    
    
    
elif menu== "Hurto a residencia🏡":
    #AGREGAMOS EL TITULO 
    st.markdown("<h1 style ='text-align: center; color:#337AFF;'>Analisis de hurtos  a residencias  en la ciudad de Medellin👤💰🔫 </h1>", unsafe_allow_html =True)


    
#REALIZAMOS GRAFICOS  cantidad de casos por anio 

    st.markdown("<h3 style ='text-align: center; color:black;'>Cantidad de hurtos por año a residencias</h1>", unsafe_allow_html =True)
    st.info(' Para el crecimiento de la cantidad de hurtos a residencia se puede observar un comportamiento creciente desde los últimos 7 años, lo cual es congruente con los datos del plan de extensión territorial, donde el número de vivienda también aumentaron debido  a los convenios impulsados por el gobierno para que mas personas pudieran adquirir una vivienda nueva, impulsando el sector de la construcción pero a su vez, contrastando con el aumento de la posibilidad de hurtos, encontrando su pico mas alto en el 2018 fueron casi 5000 al año.')
    c24,c25 = st.columns((1,1))
    R1=residencia.groupby(['año_hecho'])[['cantidad']].sum().reset_index()
    fig= px.bar(R1, x='año_hecho', y='cantidad', width=400, height= 400)
    fig.update_layout(
    xaxis_title='Año',
    yaxis_title='Cantidad de hurtos',
    template= 'simple_white', 
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.7))
    c24.plotly_chart(fig)
    
    
    
    
    # Crecimiento de la cantidad de hurtos a residencias
    dm2 =R1=residencia.groupby(['fecha_hecho'])[['cantidad']].sum().reset_index()
    dm2.iloc[:,1:]= dm2.iloc[:,1:].cumsum()
    fig1= px.line(dm2, x='fecha_hecho', y ='cantidad', title = '<b>Crecimiento de la cantidad de hurtos a residencias<b>', width=400, height= 400,
              color_discrete_sequence=px.colors.qualitative.G10)
    fig1.update_layout(
      template = 'simple_white',
      title_x = 0.5,
      legend_title = 'Hurtos A:',
      xaxis_title = '<b>Fecha<b>',
      yaxis_title = '<b>Cantidad de hurtos<b>',)
    c25.plotly_chart(fig1)   
    
    
    
    
    
    
    
    #GRAFICO CANTIDAD DE HURTO POR DIAS
    st.markdown("<h3 style ='text-align: center; color:black;'>Cantidad de hurtos a residencias por dia de la semana</h1>", unsafe_allow_html =True)
    c26,c27 = st.columns((1,1))
    R2=residencia.groupby(['dia_hecho'])[['cantidad']].count().reset_index()
    R2['orden']=R2['dia_hecho'].replace({'Monday': 1 , 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4 , 'Friday':5, 'Saturday': 6, 'Sunday':7})
    R2= R2.sort_values('orden')
    fig= px.bar(R2, x='dia_hecho', y='cantidad', width=400, height= 400)
    fig.update_layout(
    xaxis_title='Dia',
    yaxis_title='Cantidad de hurtos',
    template= 'simple_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.7))
    c27.plotly_chart(fig)
    c26.markdown('                                     ')
    c26.markdown('                                     ')
    c26.markdown('                                     ')
    c26.info('Aca se observa la relación de cantidad de hurtos que se presentan según el día de la semana, para este caso se podría afirmar que no hay prevalencia directa con los días, dado que los días de la semana presentan en su mayoría un comportamiento muy similar, sin embargo hay que resaltar que los fines de semana es donde aumentan el numero de hurtos a residencia, esto podria deberse a que las familias sales los fines de semana de paseo y dejan su hogar solo, por lo que se da oportunidad para que se den mas frecuentemente estos hurtos')

    



    #GRAFICAMOS LA PARTICIPACION DE LAS ARMAS USADAS PARA EL HURTO 
    st.markdown("<h3 style ='text-align: center; color:black;'>Tipo de arma usada para el hurto</h1>", unsafe_allow_html =True)
    c28,c29, = st.columns((1,1))
    R3=residencia.groupby(['arma_medio'])[['cantidad']].count().reset_index()
    fig=px.pie(R3, values='cantidad', names= 'arma_medio', title='<b>% de participacion de las armas en los hurtos<b>', width=400, height= 400)
    fig.update_layout(
    template= 'simple_white', 
    legend_title='Tipo de Arma', 
    title_x=0.5, )
    c28.plotly_chart(fig)
    c29.markdown('                                     ')
    c29.markdown('                                     ')
    c29.info('En el análisis de tipo de arma usada para los hurtos a residencias se encuentra que en la mayor participacion la tiene NINGUN ARMA, esto podria deberse a que la mayoría de los casos cuando se presenta el robo no hay personas presentes o en dado caso, no se dan cuenta sino hasta cuando van a verificar sus pertenencias, como se puede observar los 3 primeros lugares los ocupa: Ningún arma, objeto contundente y palanca, con los cual se puede confirmar lo anterior mencionado debido a que estos son elementos convencionales de robo, y son utilizados para forzar puertas o candados.')

    



    #GRAFICAMOS LAS CATEGORIAS EN LOS BIENES 
    st.markdown("<h3 style ='text-align: center; color:black;'>Categorias de los Bienes hurtados</h1>", unsafe_allow_html =True)
    c50,c51, = st.columns((1,1))
    R7=residencia.groupby(['categoria_bien'])[['cantidad']].count().reset_index()
    fig= px.bar(R7, x='categoria_bien', y='cantidad', width=500, height= 400)
    fig.update_layout(
    xaxis_title='Categoria del Bien hurtado',
    yaxis_title='Cantidad',
    template= 'simple_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.7))
    c51.plotly_chart(fig)
    c50.markdown('                                     ')
    c50.markdown('                                     ')
    c50.markdown('                                     ')
    c50.markdown('                                     ')
    c50.info('Podemos observar las categorias de los bienes hurtados en las residencias mas se presenta en los hurtos son: Tencologia, dinero y accesorios del hogar, esto puede deberse a que  estos son los objetos de mayor valor en las residencias.')
    
    
    #GRAFICAMOS LOS BIENES HURTADOS 
    st.markdown("<h3 style ='text-align: center; color:black;'>Bienes hurtados en las residencias</h1>", unsafe_allow_html =True)
    c30,c31, = st.columns((1,1))
    R4=residencia.groupby(['bien'])[['cantidad']].count().reset_index()
    fig= px.bar(R4, x='bien', y='cantidad', width=400, height= 400)
    fig.update_layout(
    xaxis_title='Bien hurtado',
    yaxis_title='Cantidad',
    template= 'simple_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.7))
    c30.plotly_chart(fig)
    c31.markdown('                                     ')
    c31.markdown('                                     ')
    c31.markdown('                                     ')
    c31.markdown('                                     ')
    c31.markdown('                                     ')
    c31.info('Podemos observar que los bienes mas hurtados en las residencias son los equipos tecnologicos y el dinero,dado que los equipos tencologicos por lo general son de gran valor en el mercado de lo usado,lo cual genera que se presenten mas hurtos en residencias.')
    
    
    

    
    #GRAFICAMOS SI LA CANTIDAD DE HURTOS TIENE RELACION CON LA EDAD 
    st.markdown("<h3 style ='text-align: center; color:black;'>Edad VS Cantidad de hurtos a residencias</h1>", unsafe_allow_html =True)
    R5=residencia.groupby(['edad'])[['cantidad']].sum().reset_index()
    fig = px.scatter(R5, x = 'edad', y ='cantidad', title = '<b>Edad vs Cantidad de hurtos a residencias<b>',width=950, height= 550)
    fig.update_layout(
    xaxis_title = '<b>Edad<b>',
    yaxis_title = '<b>Cantidad de hurtos<b>',
    template = 'simple_white',
    title_x = 0.5,)
    st.plotly_chart(fig)
    st.info('Se realiza un analisis de la edad con respecto a la cantidad de hurtos a las residencias para conocer si hay una correlacion estre estas variables y determinar si la edad es un factor relevante en los hurtos, se encuentra que  es un factor relevante ya que a medida de aumenta la edad dismunuyen los hurtos, encontrando un pico en las edades de los 25 a los 40 años,esto podria deberse a que en estas edades las personas socialmente estan en una etapa productiva de la vida por la cual pasan la mayor parte de tiempo en los trabajo, lo cual da una oportunidad mayor para que se presenten los hurtos. ')
    
    
    
    
    
    #GRAFICO CANTIDAD DE HURTO POR SEXO
    st.markdown("<h3 style ='text-align: center; color:black;'>Cantidad de hurtos a residencia por sexo</h1>", unsafe_allow_html =True)
    R6=residencia.groupby(['sexo'])[['cantidad']].count().reset_index()
    cantidad=carro['cantidad'].count() 
    fig=px.pie(R6, values='cantidad', names='sexo',hole=.5,title='% de hurtos por sexo')
    fig.update_layout(
    template= 'simple_white', 
    legend_title='Sexo', 
    title_x=0.5, 
    annotations = [dict(text = str(cantidad), x=0.5, y = 0.5, font_size = 40, showarrow = False )])
    st.plotly_chart(fig)
    st.info('Se analiza el sexo de las personas victimas de hurto y se encuentra que no existe relacion en la edad de las personas.')
    
    
    
    
elif menu == "Conclusiones✅️":
    #AGREGAMOS TITULO
    st.markdown("<h1 style ='text-align: center; color:#337AFF;'>Analisis de hurtos de carro, moto y residencias en la ciudad de Medellin👤💰🔫 </h1>", unsafe_allow_html =True)

    
    st.info('Como se pudo observar en los anteriores apartados se pueden identificar los variables relevantes a la hora de analizar los hurtos en ciudad de medellin como lo son: la cantidad de hurtos por anio y el crecimiento de estos,buscamos un patron el los dias donde se realizan los hurtos, las modalidades de hurto mas usadas y las armas mas usadas para estos, los bienes  o las caracteristicas de los vehiculos hurtados, el sexo de las victimas y buscamos alguna relacion de la edad de las victimas con los hurtos donde se pueden concluir lo siguiente: ')
    
    #CRECIMIENTO DE LOS HURTOS EN LOS ANIOS 
    #cantidad de hurtos en residencias por años
    
    dr2=residencia.groupby(['año_hecho'])[['cantidad']].count().reset_index()
    dc2=carro.groupby(['año_hecho'])[['cantidad']].count().reset_index()# Cantidad de hurtos de carros por años
    dm2=moto.groupby(['año_hecho'])[['cantidad']].count().reset_index()#cantidad de hurtos de moto por años
    r1=pd.merge(dr2, dc2, how = 'left', on = 'año_hecho')
    r2=pd.merge(r1, dm2, how = 'left', on = 'año_hecho')
    r2.rename(columns = {'cantidad_x':'Hurtos_residencia'}, inplace = True)
    r2.rename(columns = {'cantidad_y':'Hurtos_carro'}, inplace = True)
    r2.rename(columns = {'cantidad':'Hurtos_moto'}, inplace = True)
    fig = px.line(r2, x='año_hecho', y=['Hurtos_residencia','Hurtos_carro','Hurtos_moto'], title ='<b>Evolución de todos los casos de Hurtos<b>')
    fig.update_layout(
    xaxis_title = 'Fecha',
    yaxis_title = 'Cantidad de Hurtos',
    template = 'simple_white',
    title_x = 0.5,
    legend_title = 'Casos según tipo:')
    st.plotly_chart(fig)
    st.info('Podemos concluir que los hurtos han fluctuado mucho en los años, siendo en la mayoria de los años predominante el hurto de moto, y siendo inferior el hurto de carros. Se puede observar que el hurto en general disminuyo desde el año 2019 ya que este fue el año donde se empezo a impementar las estrategias de las cámaras de vigilancia para la prevención y lucha contra la criminalidad en la ciudad de Medellín, estos dispositivos brindan una visualización completa del área e identifican a los responsables de los homicidios y hurtos en las diferentes zonas y comunas de la ciudad estas se estan usando desde el mes de junio del año 2019, se cuentan con 300 cámaras, ademas resaltamos que a nivel mundial se vivio el COVID19 donde las personas debian estar en todo momento en su casa, lo cual hacia que el hurto fuera mucho mas dificil de propiciar. ')




    
    
    # Crecimiento de todos los tipos de hurtos
# definir base
    r2c = r2.copy()
    r2c.iloc[:,1:]= r2c.iloc[:,1:].cumsum()
    fig = px.line(r2c, x='año_hecho', y=['Hurtos_residencia','Hurtos_carro','Hurtos_moto'], title ='<b>Evolución del crecimiento de todos los casos de Hurtos<b>')
    fig.update_layout(
    xaxis_title = 'Fecha',
    yaxis_title = 'Cantidad de Hurtos',
    template = 'simple_white',
    title_x = 0.5,
    legend_title = 'Casos según tipo:')
    st.plotly_chart(fig)
    st.info('En general podemos observar que los hurtos en la ciudad continuan en tendencia de crecimiento, y aun mas notablemente los hurtos ha motos, esto se debe al crecimiento que tiene el parque automotor con respecto a las motos ya que según la información de la Secretaría de Movilidad de Medellín, el parque automotor que circula en el Valle de Aburrá, sumando carros y motos, es de 1.464.328. Este valor se desagrega en 589.463 carros y 875.043 motos, representando 40% y 60%, respectivamente. ')

    
    
    
    
    
    #ANALISIS DEL ARMA USADA
    st.markdown("<h3 style ='text-align: center; color:#337AFF;'>Analisis de armas</h3>", unsafe_allow_html =True)    
    R3=residencia.groupby(['arma_medio'])[['cantidad']].count().reset_index()
    M3=moto.groupby(['arma_medio'])[['cantidad']].count().reset_index()
    C3=carro.groupby(['arma_medio'])[['cantidad']].count().reset_index()
    R3=R3.rename(columns={'cantidad':'hurto a residencia'})#RENOMBRAMOS LA COLUMNA
    C3a=C3.iloc[:,1:].rename(columns={'cantidad':'hurto a carro'})#FILTRAMOS EL DF
    M3a=M3.iloc[:,1:].rename(columns={'cantidad':'hurto a moto'})#FILTRAMOS EL DF
    arma = pd.concat([R3,C3a,M3a], axis = 1 )#UNIMOS EL DF
    fig= px.bar(arma, x='arma_medio', y=['hurto a residencia','hurto a carro','hurto a moto'], title= '<b>Tipo de arma usada en cada tipo de hurto<b>')
    fig.update_layout(
    xaxis_title='Tipo de arma',
    yaxis_title='cantidad',
    template= 'simple_white', 
    title_x=0.5, )
    st.plotly_chart(fig)
    st.info('Podemos concluir que el tipo de arma que mas se usa para los hurtos en general son las armas de fuego, esto es un hecho preocupante en materia de seguridad ya que como mencionamos anteriormentge en los apartados el uso de armas esta prohibido en Colombia por el el decreto 1873 del 30 de diciembre de 2021 que restringe el porte de armas en todo el territorio nacional y compete a las fuerzas del estado cómo únicas autorizadas para portar, expedir y generar los permisos respectivos.')
    
    ca,cb,cc= st.columns((1,1,1))
    ca.markdown("<h3 style ='text-align: center; color:#337AFF;'>Sexo</h3>", unsafe_allow_html =True)
    ca.info('En el sexo de las victimas podemos decir que en el caso de los hurtos de carro y moto son los hombres los mas afectados,pero se analiza que este porcentaje es mayor ya que son los hombres los mas usan el carro o la moto.')
    cb.markdown("<h3 style ='text-align: center; color:#337AFF;'>Modalidad</h3>", unsafe_allow_html =True)
    cb.info('En la modalidad de hurto podemos concluir que en el caso de los hurtos de carro y moto con las modalidades de halado y atraco las que mas se presentan, lo que nos confirma la incidencia de las armas de fuego que son usadas para realizar los atracos ynos muestra la falta de seguridad que se encuentran en las calles ya que el halado es una modalidad donde se hurta el vehiculo estando estacionado.')
    cc.markdown("<h3 style ='text-align: center; color:#337AFF;'>Edad</h3>", unsafe_allow_html =True)
    cc.info('En la edad econtramos que es un factor relevante con respecto a los hurtos, en la edad de los 25 a los 45 años, se debe tener presente que es en estas edades donde la poblacion tiende a tener un vehiculo como medio de transporte. ')
    
    cd,ce,cf= st.columns((1,1,1))
    cd.markdown("<h3 style ='text-align: center; color:#337AFF;'>Color</h3>", unsafe_allow_html =True)
    cd.info('En cuanto a los colores de motos y carros hurtados concluimos que para los carros el color mas hurtado es el gris en sus diferentes tonalidades, pero esto se debe a que es el color de carros mas vendidos en la ciudad, y para la moto es el negro donde ocurre exactamente lo mismo al ser el color de moto mas vendido estas son las mas hurtadas, ademas por el mercado de las autopartes que es el negocio ilicito donde venden las partes de los carros y motos robadas.')
    ce.markdown("<h3 style ='text-align: center; color:#337AFF;'>Categoria de bienes</h3>", unsafe_allow_html =True)
    ce.info('Encontramos que en los hurtos a residencia se categorizaron los bienes donde las categorias de bienes mas hurtados son tecnolodia, dinero y articulos del hogar.')
    cf.markdown("<h3 style ='text-align: center; color:#337AFF;'>Bienes hurtados</h3>", unsafe_allow_html =True)
    cf.info('En las categorias de bienes hurtados encontramos que los objetos tecnologicos y el dinero son los bienes mas hurtados, esto debido a la facilidad para sacarlos de las residencias y el amplio mercado ilegal de los usado')
    
   
