# 🖼️ Editor de Imagens - Streamlit
<img width="1920" height="1191" alt="Image" src="https://github-production-user-asset-6210df.s3.amazonaws.com/121620900/475809888-3d990876-537b-487e-99cb-c1bf8ea444b0.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250807%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250807T233931Z&X-Amz-Expires=300&X-Amz-Signature=6a0ef98d6c93d582c7854d26b8efb3a1d98be6d79f4df0c8bef4190ddc29ef75&X-Amz-SignedHeaders=host" />

Um editor de imagens interativo desenvolvido em Python com Streamlit, que permite aplicar transformações geométricas, ajustes de intensidade e filtros em imagens de forma intuitiva através de uma interface web.

## 📋 Sobre o Projeto

Este projeto é uma aplicação web que oferece funcionalidades básicas de edição de imagens, permitindo aos usuários:

- **Carregar imagens** via upload de arquivos ou captura pela webcam
- **Aplicar transformações geométricas** como rotação, escala e cisalhamento
- **Ajustar intensidade** com controles de brilho, contraste, transformação logarítmica e correção gama
- **Aplicar filtros** como negativo
- **Visualizar em tempo real** as modificações aplicadas
- **Baixar a imagem editada** no formato JPEG

## 🎯 Para que Serve

- **Educação**: Ferramenta didática para aprender processamento de imagens
- **Prototipagem**: Teste rápido de efeitos e transformações em imagens
- **Uso pessoal**: Editor simples para ajustes básicos em fotos
- **Demonstração**: Showcase de técnicas de visão computacional

## 🚀 Como Usar

### Pré-requisitos

```bash
pip install streamlit opencv-python pillow numpy
```

### Executando a Aplicação

1. Clone ou baixe o projeto
2. Navegue até o diretório do projeto
3. Execute o comando:

```bash
streamlit run atividade-II.py
```

4. Acesse a aplicação no navegador (geralmente em `http://localhost:8501`)

### Interface da Aplicação

#### 1. **Upload da Imagem**
- **Upload de arquivo**: Clique em "Faça upload da imagem" e selecione uma imagem (JPG, JPEG, PNG)
- **Webcam**: Marque a opção "Usar webcam" e capture uma foto

#### 2. **Transformações Geométricas** (Sidebar)
- **Rotação**: Gire a imagem de -180° a +180°
- **Escala**: Redimensione de 10% a 300% do tamanho original
- **Cisalhamento X/Y**: Aplique deformação nos eixos X e Y

#### 3. **Ajustes de Intensidade** (Sidebar)
- **Brilho**: Ajuste de -100 a +100
- **Contraste**: Variação de 10% a 300%
- **Transformação Logarítmica**: Melhora detalhes em regiões escuras
- **Correção Gama**: Ajuste não-linear de 0.1 a 5.0

#### 4. **Filtros** (Sidebar)
- **Negativo**: Inverte as cores da imagem

#### 5. **Visualização e Download**
- Compare a imagem original (esquerda) com a editada (direita)
- Baixe o resultado final clicando em "Baixar imagem editada"

## 🛠️ Tecnologias Utilizadas

### **Linguagem de Programação**
- **Python 3.x**: Linguagem principal do projeto

### **Bibliotecas e Frameworks**

#### **Interface e Deployment**
- **[Streamlit](https://streamlit.io/)**: Framework para criação da interface web interativa
  - Componentes utilizados: `st.slider`, `st.checkbox`, `st.file_uploader`, `st.camera_input`, `st.download_button`

#### **Processamento de Imagens**
- **[OpenCV (cv2)](https://opencv.org/)**: Biblioteca principal para processamento de imagens
- **[PIL/Pillow](https://pillow.readthedocs.io/)**: Manipulação de imagens e conversões de formato
- **[NumPy](https://numpy.org/)**: Operações matemáticas em arrays e matrizes

#### **Utilitários**
- **BytesIO**: Manipulação de dados binários para download

## 🔬 Métodos e Técnicas Implementadas

### **1. Transformações Geométricas**

#### **Rotação e Escala**
```python
M_rot = cv2.getRotationMatrix2D((cols/2, rows/2), angle, scale)
img_transformed = cv2.warpAffine(img_cv2, M_rot, (cols, rows))
```
- **Técnica**: Matriz de transformação afim 2D
- **Método**: `cv2.getRotationMatrix2D()` e `cv2.warpAffine()`

#### **Cisalhamento (Shearing)**
```python
shear_matrix = np.float32([
    [1, shear_x / 100, 0],
    [shear_y / 100, 1, 0]
])
```
- **Técnica**: Transformação afim customizada
- **Aplicação**: Deformação controlada nos eixos X e Y

### **2. Ajustes de Intensidade**

#### **Brilho e Contraste**
```python
img_transformed = cv2.convertScaleAbs(img_transformed, alpha=contrast/100, beta=brightness)
```
- **Fórmula**: `new_pixel = alpha × old_pixel + beta`
- **Método**: `cv2.convertScaleAbs()`

#### **Transformação Logarítmica**
```python
img_transformed = np.uint8(255 * (np.log1p(img_transformed) / np.log1p(255)))
```
- **Técnica**: Mapeamento logarítmico para realce de detalhes
- **Aplicação**: Melhora visibilidade em regiões escuras

#### **Correção Gama**
```python
img_transformed = np.clip(255 * ((img_transformed / 255) ** (1.0 / gamma)), 0, 255)
```
- **Técnica**: Correção não-linear de intensidade
- **Fórmula**: `output = input^(1/γ)`

### **3. Operações de Filtros**

#### **Negativo**
```python
img_transformed = cv2.bitwise_not(img_transformed)
```
- **Técnica**: Inversão bitwise
- **Resultado**: Inversão completa das intensidades

### **4. Conversões de Formato**

#### **Conversão PIL ↔ OpenCV**
```python
def pil_to_cv2(img):
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def cv2_to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
```
- **Técnica**: Conversão de espaços de cor RGB ↔ BGR
- **Necessidade**: Compatibilidade entre bibliotecas

## 📁 Estrutura do Projeto

```
projeto/
├── atividade-II.py          # Arquivo principal da aplicação
├── README.md                # Este arquivo de documentação
└── requirements.txt         # Dependências do projeto (opcional)
```

### Exemplo de `requirements.txt`:
```
streamlit>=1.28.0
opencv-python>=4.8.0
Pillow>=10.0.0
numpy>=1.24.0
```

## 🎓 Conceitos de Visão Computacional Aplicados

- **Transformações Geométricas**: Rotação, escala, cisalhamento
- **Mapeamento de Intensidade**: Transformações lineares e não-lineares
- **Espaços de Cor**: Conversões entre RGB e BGR
- **Processamento de Pixel**: Operações ponto a ponto
- **Álgebra Linear**: Matrizes de transformação afim

## 🔧 Possíveis Melhorias Futuras

- [ ] Adicionar mais filtros (blur, sharpen, edge detection)
- [ ] Implementar histograma da imagem
- [ ] Suporte a mais formatos de arquivo
- [ ] Operações morfológicas
- [ ] Detecção de bordas
- [ ] Filtros de ruído
- [ ] Ajuste de saturação e matiz
- [ ] Recorte interativo da imagem

## 📄 Licença

Este projeto é desenvolvido para fins educacionais e pode ser usado livremente para aprendizado e demonstração de técnicas de processamento de imagens.