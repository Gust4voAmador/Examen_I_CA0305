# -*- coding: utf-8 -*-
"""
Created on Sat May  4 18:28:50 2024

@author: AMADOR
"""
import pandas as pd
import numpy as np
class Nulos:
    #contructor
    def __init__(self, df_pandas):
        if not isinstance(df_pandas, pd.DataFrame):
            raise ValueError("El objeto ingresado debe ser un DataFrame de pandas")
           
        #atributos
        self._df = df_pandas
    
    @property
    def df(self):
        return self._df
    
    @df.setter
    def df(self, new_df):
        self._df = new_df
        
    def eliminar_nulos(self, col):
        '''
        Elimina filas con valores nulos en la columna especificada y devuelve un nuevo DataFrame.
    
        Parameters
        ----------
        col (str): Nombre de la columna en la que se buscarán valores nulos.
        
        Returns
        ------    
        df_aux (pandas.DataFrame): Nuevo DataFrame con las filas que no contienen valores nulos en la columna especificada.
        '''
        
        #lista para guardar el numero de fila que tiene nulo
        list_null = []
        
        #contador para identificar la fila del null
        contador = 0
        
        # Recorrer la columna seleccionada
        for value in self.df[col]:
            
            #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.isnull.html
            if pd.isnull(value) == True:
                list_null.append(contador)
                
            contador += 1    
                
        #eliminar las filas con nulos del df
        #https://www.freecodecamp.org/espanol/news/eliminar-la-lista-de-filas-del-dataframe-de-pandas/
        
        df_aux = self.df.drop(list_null)
        df_aux = df_aux.reset_index(drop=True)
        
        # Utilizar el método setter para asignar el nuevo DataFrame al atributo df
        #self.df = df_aux
        
        return df_aux
        
        
    def imputacion_estadistica(self, col):
        '''
        Imputa los valores nulos en una columna especificada con la media de 
        los valores no nulos en esa columna.
    
        Parameters
        ----------
        col (str): Nombre de la columna en la que se imputarán los valores nulos.
        
        Returns
        ------    
        df_modificado (pandas.DataFrame): Nuevo DataFrame con los valores nulos
        en la columna especificada imputados con la media de los valores no nulos.
        
        '''        
        # Verificar si la columna es de tipo int o float
        if not (pd.api.types.is_numeric_dtype(self.df[col]) or pd.api.types.is_integer_dtype(self.df[col])):
            raise ValueError("La columna indicada debe ser de tipo numérica (int o float)")
        
        #obtener la media de la estadística
        media = self.df[col].mean()
        
        #Crear copia 
        df_modificado = self.df.copy()
        
        #https://interactivechaos.com/es/manual/tutorial-de-pandas/el-metodo-fillna
        #sustituir los valores nulos por la media
        df_modificado[col] = self.df[col].fillna(media)
        
        # Utilizar el método setter para asignar el nuevo DataFrame al atributo df
        #self.df = df_modificado
        
        return df_modificado

    
    def imputacion_por_grupo(self, cols_agrupar, col):
        '''
        Imputa los valores nulos en una columna con la media agrupada por otras
        columnas especificadas.
    
        Parameters
        ----------
        cols_agrupar (list of str):Lista de nombres de columnas por las cuales 
        agrupar los datos.
        
        col (str): Nombre de la columna en la que se imputarán los valores nulos.
        
        Returns
        ------    
        df_modificado (pandas.DataFrame): Nuevo DataFrame con los valores nulos
        en la columna especificada imputados con la media agrupada por las 
        columnas especificadas.
        
        ''' 
        # Verificar si la columna es de tipo numérico (int o float)
        if not (pd.api.types.is_numeric_dtype(self.df[col]) or pd.api.types.is_integer_dtype(self.df[col])):
            raise ValueError("La columna indicada debe ser de tipo numérica (int o float)")
            
        # Agrupar por las columnas de agrupación 
        #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html
        agrupaciones = self.df.groupby(cols_agrupar)[col]
        
        #obtner la media para cada fila segun su agrupación
        #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.transform.html
        #https://www.youtube.com/watch?v=JPey7neLDzo
        media_agrupada = agrupaciones.transform('mean')
        
        
        # Sustituir los valores nulos por la media agrupada
        #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html
        df_modificado = self.df.copy()  # Copiar del df original
        df_modificado[col] = df_modificado[col].fillna(media_agrupada)
    
        # Utilizar el método setter para asignar el nuevo DataFrame al atributo df
        #self.df = df_modificado
    
        return df_modificado

    


    def imputacion_banda_movil(self, col, banda):
        '''
        Imputa los valores nulos en una columna utilizando el promedio móvil 
        con una banda especificada.
    
        Parameters
        ----------
        col (str): Nombre de la columna en la que se imputarán los valores nulos.
        
        banda (int): Tamaño de la banda para el cálculo del promedio móvil.
        
        Returns
        ------    
        df_aux (pandas.DataFrame): Nuevo DataFrame con los valores nulos
        en la columna especificada imputados utilizando el promedio móvil.
        
        '''        
        
        if not (pd.api.types.is_numeric_dtype(self.df[col]) or pd.api.types.is_integer_dtype(self.df[col])):
            raise ValueError("La columna indicada debe ser de tipo numérica (int o float)") 
        
        if banda < 0:
            raise ValueError("Valor de banda móvil inválido") 
        
        lista_col = self.df[col].tolist()
        df_aux = self.df.copy()  # Hacer una copia del DataFrame original
        
        for i in range(len(lista_col)):
            if np.isnan(lista_col[i]):
                valores = []
                # Calcular el promedio móvil
                # Calcular hacia la izquierda
                izq = i
                while izq >= 0 and len(valores) < banda:
                    if not np.isnan(lista_col[izq]):
                        valores.append(lista_col[izq])
                    izq -= 1
                
                # Calcular hacia la derecha
                der = i + 1
                if len(valores) == 0:
                    while der < len(lista_col) and len(valores) <banda:
                        if not np.isnan(lista_col[der]):
                            valores.append(lista_col[der])
                        der += 1
                else:
                    while der < len(lista_col) and len(valores) <2*banda:
                        if not np.isnan(lista_col[der]):
                            valores.append(lista_col[der])
                        der += 1
                
                if valores:
                    
                    promedio = sum(valores) / len(valores)
                    # Asignar el promedio calculado a la fila y columna correspondientes
                    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.index.html
                    df_aux.loc[df_aux.index[i], col] = promedio
        
        return df_aux    
    
    
