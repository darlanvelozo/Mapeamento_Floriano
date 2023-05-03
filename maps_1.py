from numpy import sin, cos, arccos, pi, round
import pandas as pd

# funções matematicas para calcular distancia a partir da longitude e latitude
#=========================================================================================================#  
def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians

def getDistanceBetweenPointsNew(latitude1, longitude1, latitude2, longitude2, unit = 'kilometers'):
    
    theta = longitude1 - longitude2
    
    distance = 60 * 1.1515 * rad2deg(
        arccos(
            (sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) + 
            (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))
        )
    )
    if unit == 'miles':
        return round(distance, 2)
    if unit == 'kilometers':
        return round(distance * 1.609344, 2)
#=========================================================================================================#  

# estrutura de dados em forma de lista [id, nome, latitude, longitude, id_pontos_alcancaveis]
map = [
[1, 'Rua A', -6.770560 ,-43.030300, [2, 18, 20, 30, 31]],
[2,'Rua B', -6.771646,-43.030823, [1,27,18,3]], 
[3, 'Rua c',-6.772433,-43.031271, [2,27,4,26]],
[4, 'Rua D',-6.772504,-43.032432, [3, 25,5]],
[5, 'Rua E',-6.772613,-43.033654, [4,6]],
[6, 'Rua F',-6.771913,-43.033756, [5, 25, 7]],
[7, 'Rua G',-6.770864,-43.033821, [6,24,8]],
[8, 'Rua H',-6.769748, -43.033955, [7, 9]],
[9, 'Rua I',-6.769673,-43.032743, [8,10,24,22]],
[10, 'Rua J',-6.769017, -43.032827, [9,23,11]],
[11, 'Rua K',-6.768593, -43.03288, [10,12]],
[12, 'Rua L',-6.768406,-43.031707, [11,23,14]],
[13, 'Rua M',-6.768537,-43.028397, [16,29,17]],
[14, 'Rua N',-6.768264,-43.030615, [12,21,15]],
[15, 'Rua O',-6.768123,-43.029477, [14,29,16]],
[16, 'Rua P',-6.768000,-43.028457,[15,13]],
[17, 'Rua Q',-6.769424,-43.028337, [13,19]],
[18, 'Rua R',-6.771630, -43.030080, [1,2,26,28]],
[19, 'Rua S',-6.769440,-43.029341, [17,29,30,20]],
[20, 'Rua T',-6.770467,-43.029202, [28,19,1]],
[21, 'Rua U',-6.768737,-43.030518, [14,30,23,29]],
[22, 'Rua V',-6.769558,-43.031551, [23,30,31,9]],
[23, 'Rua W',-6.768871,-43.031612, [12,10,21,22]],
[24, 'Rua X',-6.770748,-43.032673, [9,31,25,7]],
[25, 'Rua Y',-6.771800,-43.032540, [24,6,4,27]],
[26, 'Rua Z',-6.772280, -43.029990, [18,3]],
[27, 'Rua ZA',-6.771696,-43.031362, [2,3,25,31]],
[28, 'Rua ZB',-6.771364, -43.029082, [20,18]],
[29, 'Rua ZC',-6.768643,-43.029405, [15,21,19,13]],
[30, 'Rua ZD',-6.769519,-43.030435, [21,19,22,1]],
[31,'Rua ZE', -6.7707038, -43.0314517, [1,27,24,22]]
]

#nova lista com as distancias para cada ponto
n_map = []

# localiza o item da estrutura de dados pelo ID
def loc_id(lista, id):
    for i in range(len(lista)):
        if id == lista[i][0]:
            return lista[i]

# estrutura de repetição que gera uma lista a partir da lista principal map, agora adicionando as distancias
for i in range(len(map)):
    dist=[]
    for j in range(len(map[i][4])):
        id = map[i][4][j]
        dist.append([loc_id(map, id)[1],getDistanceBetweenPointsNew(map[i][2], map[i][3], loc_id(map,map[i][4][j])[2], loc_id(map,map[i][4][j])[3])*1000])
        
     
    
    n_map.append([map[i][0],map[i][1],map[i][2],map[i][3],map[i][4], dist])
    
# função para calcular distancia entre 2 pontos a partir do id
def distancia_AB(id1, id2):
    
    a = loc_id(map, id1)
    b = loc_id(map, id2)
    distancia_AB = getDistanceBetweenPointsNew(a[2], a[3], b[2], b[3])
        

    return distancia_AB*1000
    
# função que retorna o ponto mais proximo em linha reta em relação ao destino final
def proximidade(id1, id2):
    
    percuso = []
     
    a = loc_id(map, id1)
    b = loc_id(map, id2)
   
    for i in range(len(a[4])):
       percuso.append([distancia_AB(a[4][i], b[0]), a[4][i]])
       
       
    
       
    return [min(percuso)]

# função que retorna os pontos percorridos em relação ao destino
def melhor_caminho(a, b):
    
    
    pontos = []
    pontos.insert(0, [0, a])
    while True:
        p_final = loc_id(n_map, b)
        if b in loc_id(n_map, a)[4] and a in p_final[4]:
            
            break
        else:
            pontos.append(proximidade(a, b)[0])
            a = proximidade(a, b)[0][1]
    pontos.append([0,b])    
    return pontos

# função que calcula a distancia percorrida e retorna o trajeto em forma de lista. ex: [500.0, [id1, id2, id3]]
def percurso_distancia(lista_melhor_caminho):
    distancia_percorrida = 0
    lista = lista_melhor_caminho
    pontos_percorridos = []
    
    for i in range(len(lista)-1):
        a = loc_id(n_map, lista[i][1])
        b = loc_id(n_map, lista[i+1][1])
        pontos_percorridos.append(a[0])
        distancia_percorrida += distancia_AB(a[0], b[0])
        if i == len(lista)-2:
            pontos_percorridos.append(b[0])

    return [distancia_percorrida, pontos_percorridos]

# id dos pontos que o usuario deseja partir(a) e o ponto de chegada(b)
a = int(input("id A: "))
b = int(input("id B: "))

print(percurso_distancia(melhor_caminho(a, b)))

#visualização em tabela pelo pandas
df = pd.DataFrame(n_map,columns=['id', 'nome', 'latitude', 'longitude', 'pontos_alcancaveis', 'distancia'])
df.to_csv("table.csv")


