#!/usr/bin/env python
# coding: utf-8

# ### Importação

# In[1]:


import numpy as np
import cv2


# ### Mapeamento de Vagas x,y,w,h

# In[2]:


vaga1 = [1, 89, 108, 213]
vaga2 = [115, 87, 152, 211]
vaga3 = [289, 89, 138, 212]
vaga4 = [439, 87, 135, 212]
vaga5 = [591, 90, 132, 206]
vaga6 = [738, 93, 139, 204]
vaga7 = [881, 93, 138, 201]
vaga8 = [1027, 94, 147, 202]


# In[3]:


vagas = [vaga1, vaga2, vaga3, vaga4, vaga5, vaga6, vaga7, vaga8]


# In[4]:


print(vagas)


# ### Incluindo video teste

# In[5]:


video_teste = cv2.VideoCapture('video.mp4')


# In[6]:


while True:
    check,img = video_teste.read()
    
    #Aplicação de morfologias
    # Transformando img em escala de cinza
    imgCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Aplicação do método Threshold adaptive para binariar imagem e desconsiderar ruídos
    # Inversão de cores pixels
    imgTh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,25,16)   
    # Suaviza os pixels
    imgBlur = cv2.medianBlur(imgTh, 5)
    # Processo de dilatção os pixels
    kernel = np.ones((3, 3), np.int8)
    imgDil = cv2.dilate(imgBlur, kernel)
    
    vagas_livres = 0

    for x, y, w, h in vagas:
        # parametros para contagem dos pixel
        recorte = imgDil[y:y + h, x: x + w]
        #função de contagem pixel não pretos
        qtdPxBranco = cv2.countNonZero(recorte)
        cv2.putText(img, str(qtdPxBranco), (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),1)
       
        # verificação de ocupação de vaga de acordo com a quatidade de pixels
        if qtdPxBranco > 3000:
            #identificação da vaga ocupada
            cv2.rectangle(img,(x,y),(x + w, y + h), (0, 0, 255), 3)
        else:
            #identificação da vaga livre
            cv2.rectangle(img,(x,y),(x + w, y + h), (0, 255, 0), 3)
            vagas_livres +=1
            
    cv2.rectangle(img,(90, 0), (415, 60), (255, 0, 0), -1)
    cv2.putText(img, f'LIVRE: {vagas_livres}/8', (95, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 5)
            

    cv2.imshow('video',img)
    cv2.imshow('video TH',imgDil)
    
    cv2.waitKey(75)


# In[ ]:




